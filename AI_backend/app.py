from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from config import Config
from models import db, bcrypt, User, StudentProfile, OfficerProfile, QuestionBank
from flask_cors import CORS
from flask_migrate import Migrate
import os
from werkzeug.utils import secure_filename
import sys

# 导入 CORS 支持模块，用于跨域资源共享（Cross-Origin Resource Sharing）：
# 如果你的前端和后端不在同一个域下（比如前端在 localhost:3000，后端在 localhost:5000），你就需要开启 CORS，否则浏览器会拦截请求。

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# 配置文件上传
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 确保上传目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

# 添加face_recognition目录到系统路径
# sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'face_recognition'))
# from start_server import VideoServerManager

# server_manager = VideoServerManager()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()  # 从客户端请求中提取JSON数据，并赋值给data变量
    if User.query.filter_by(username=data['username']).first():  #查询数据库中是否已存在相同用户名的用户
        return jsonify({'message':'Username exists'}), 400
    
    identity = data.get('identity')
    if identity not in ['student', 'officer', None]:
        return jsonify({'message':'Invalid identity value'}), 400
    
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(username=data['username'], password=hashed_password, identity=identity)
    db.session.add(user)  # 将新建的用户对象添加到数据库会话(Session)中，但还没有提交
    db.session.flush()  # Ensure user.id is available

    if not identity:
        return jsonify({'message': 'Identity is required'}), 400

    if identity == 'student':
        score = data.get('score')
        if score is not None:
            try:
                score = float(score)
            except (ValueError, TypeError):
                return jsonify({'message': 'Invalid score value'}), 400
        student_profile = StudentProfile(user_id = user.id, score=score)
        db.session.add(student_profile)
    
    elif identity =='officer':
        major = data.get('major')
        if major and len(major)>100:
            return jsonify({'message': 'Major too long'}), 400
        officer_profile = OfficerProfile(user_id = user.id, major=major)
        db.session.add(officer_profile)

    db.session.commit()  # 提交数据库事务，真正把用户保存到数据库中
    return jsonify({'message':'User created'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({
            'token': access_token,
            'identity': user.identity
        }), 200
    return jsonify({'message':'Invalid credentials'}), 401

@app.route('/users',methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    print(users)  # 调试：确认用户列表非空
    result = []
    for u in users:
        user_data = {'id':u.id, 'username':u.username, 'identity':u.identity, 'score': None, 'major': None}
        print(f"User: {u.username}, Identity: {u.identity}, StudentProfile: {u.student_profile}, OfficerProfile: {u.officer_profile}")  # 调试
        if u.identity == 'student' and u.student_profile:
            user_data['score'] = u.student_profile.score
        elif u.identity == 'officer' and u.officer_profile:
            user_data['major'] = u.officer_profile.major
        result.append(user_data)
    return jsonify(result), 200


@app.route('/user/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    # current_user_id = get_jwt_identity()
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    # 只有管理员可以删除和查看用户信息
    if user.identity != 'officer':
        return jsonify({'message': 'Unauthorized'}), 403
    
    # 显式删除相关的 StudentProfile 或 OfficerProfile
    if user.student_profile:
        db.session.delete(user.student_profile)
    if user.officer_profile:
        db.session.delete(user.officer_profile)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message':'User deleted'}), 200

@app.route('/upload-photo', methods=['POST'])
@jwt_required()
def upload_photo():
    if 'photo' not in request.files:
        return jsonify({'message': '没有文件'}), 400
    
    file = request.files['photo']
    if file.filename == '':
        return jsonify({'message': '没有选择文件'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # 使用用户ID作为文件名前缀
        user_id = get_jwt_identity()
        filename = f"{user_id}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return jsonify({'message': '文件上传成功', 'filename': filename}), 200
    
    return jsonify({'message': '不支持的文件类型'}), 400

# 题库管理相关API
@app.route('/questions', methods=['POST'])
@jwt_required()
def create_question():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    # 检查用户是否为officer
    if not user or user.identity != 'officer':
        return jsonify({'message': '只有官员可以创建题目'}), 403
    
    data = request.get_json()
    if not all(key in data for key in ['content', 'topic']):
        return jsonify({'message': '缺少必要字段'}), 400
    
    question = QuestionBank(
        content=data['content'],
        topic=data['topic'],
        officer_id=current_user_id
    )
    
    db.session.add(question)
    db.session.commit()
    
    return jsonify({
        'message': '题目创建成功',
        'question': {
            'id': question.id,
            'content': question.content,
            'topic': question.topic,
            'created_at': question.created_at.isoformat()
        }
    }), 201

@app.route('/questions', methods=['GET'])
@jwt_required()
def get_questions():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    # 检查用户是否为officer
    if not user or user.identity != 'officer':
        return jsonify({'message': '只有官员可以查看题目'}), 403
    
    questions = QuestionBank.query.all()
    return jsonify([{
        'id': q.id,
        'content': q.content,
        'topic': q.topic,
        'created_at': q.created_at.isoformat(),
        'updated_at': q.updated_at.isoformat(),
        'officer_id': q.officer_id
    } for q in questions]), 200

@app.route('/questions/<int:question_id>', methods=['DELETE'])
@jwt_required()
def delete_question(question_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    # 检查用户是否为officer
    if not user or user.identity != 'officer':
        return jsonify({'message': '只有官员可以删除题目'}), 403
    
    question = QuestionBank.query.get(question_id)
    if not question:
        return jsonify({'message': '题目不存在'}), 404
    
    # 检查是否是创建该题目的officer
    if question.officer_id != current_user_id:
        return jsonify({'message': '只能删除自己创建的题目'}), 403
    
    db.session.delete(question)
    db.session.commit()
    
    return jsonify({'message': '题目删除成功'}), 200

@app.route('/questions/<int:question_id>', methods=['PUT'])
@jwt_required()
def update_question(question_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    # 检查用户是否为officer
    if not user or user.identity != 'officer':
        return jsonify({'message': '只有官员可以更新题目'}), 403
    
    question = QuestionBank.query.get(question_id)
    if not question:
        return jsonify({'message': '题目不存在'}), 404
    
    # 检查是否是创建该题目的officer
    if question.officer_id != current_user_id:
        return jsonify({'message': '只能更新自己创建的题目'}), 403
    
    data = request.get_json()
    if not all(key in data for key in ['content', 'topic']):
        return jsonify({'message': '缺少必要字段'}), 400
    
    question.content = data['content']
    question.topic = data['topic']
    db.session.commit()
    
    return jsonify({
        'message': '题目更新成功',
        'question': {
            'id': question.id,
            'content': question.content,
            'topic': question.topic,
            'created_at': question.created_at.isoformat(),
            'updated_at': question.updated_at.isoformat()
        }
    }), 200


if __name__=='__main__':
    with app.app_context():  # 数据库操作需要在这个上下文中进行
        db.create_all()  # 创建数据库中的所有表
    app.run(debug=True, port=5000)