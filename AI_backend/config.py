class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:p20011015@localhost:3306/user_management'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'your-secret-key'
    SECRET_KEY = "your-secret-key"