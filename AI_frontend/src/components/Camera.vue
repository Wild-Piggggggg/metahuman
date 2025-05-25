<template>
  <div class="camera-container">
    <div class="camera-box">
      <video ref="video" class="camera-video" autoplay playsinline></video>
      <canvas ref="canvas" class="camera-canvas" style="display: none;"></canvas>
    </div>
    <div class="camera-controls">
      <button @click="startCamera" class="btn" v-if="!isStreaming">开启摄像头</button>
      <button @click="stopCamera" class="btn btn-secondary" v-if="isStreaming">关闭摄像头</button>
      <button @click="takePhoto" class="btn" v-if="isStreaming">拍照</button>
    </div>
    <div v-if="photoTaken" class="photo-preview">
      <div class="preview-header">
        <h3>照片预览</h3>
        <button @click="closePreview" class="btn-close">×</button>
      </div>
      <img :src="photoUrl" alt="拍摄的照片" class="preview-image" />
      <div class="preview-controls">
        <button @click="savePhoto" class="btn">保存照片</button>
        <button @click="closePreview" class="btn btn-secondary">取消</button>
      </div>
    </div>
  </div>
</template>

<script>
import { io } from 'socket.io-client'

export default {
  name: 'Camera',
  data() {
    return {
      isStreaming: false,
      photoTaken: false,
      photoUrl: '',
      stream: null,
      socket: null,
      frameCount: 0
    }
  },
  methods: {
    async startCamera() {
      try {
        this.stream = await navigator.mediaDevices.getUserMedia({
          video: {
            width: { ideal: 1280 },
            height: { ideal: 720 },
            facingMode: 'user'
          },
          audio: false
        })
        
        const video = this.$refs.video
        video.srcObject = this.stream
        this.isStreaming = true

        // 连接WebSocket
        this.socket = io('http://localhost:5001')
        
        // 开始发送视频帧
        this.startFrameCapture()
      } catch (error) {
        console.error('无法访问摄像头:', error)
        alert('无法访问摄像头，请确保已授予权限')
      }
    },
    
    startFrameCapture() {
      const video = this.$refs.video
      const canvas = this.$refs.canvas
      const context = canvas.getContext('2d')
      
      const captureFrame = () => {
        if (!this.isStreaming) return
        
        canvas.width = video.videoWidth
        canvas.height = video.videoHeight
        context.drawImage(video, 0, 0, canvas.width, canvas.height)
        
        // 每30帧发送一次
        if (this.frameCount % 48 === 0) {
          const frameData = canvas.toDataURL('image/jpeg').split(',')[1]
          if (this.socket && this.socket.connected) {
            this.socket.emit('video_frame', { frame: frameData })
          }
        }
        
        this.frameCount++
        requestAnimationFrame(captureFrame)
      }
      
      captureFrame()
    },
    
    stopCamera() {
      if (this.stream) {
        this.stream.getTracks().forEach(track => track.stop())
        this.stream = null
      }
      if (this.socket) {
        this.socket.disconnect()
        this.socket = null
      }
      this.isStreaming = false
      this.photoTaken = false
      this.photoUrl = ''
      this.frameCount = 0
    },
    
    takePhoto() {
      const video = this.$refs.video
      const canvas = this.$refs.canvas
      const context = canvas.getContext('2d')
      
      canvas.width = video.videoWidth
      canvas.height = video.videoHeight
      context.drawImage(video, 0, 0, canvas.width, canvas.height)
      
      this.photoUrl = canvas.toDataURL('image/jpeg')
      this.photoTaken = true
    },
    
    closePreview() {
      this.photoTaken = false
      this.photoUrl = ''
    },
    
    async savePhoto() {
      try {
        const response = await fetch(this.photoUrl)
        const blob = await response.blob()
        
        const formData = new FormData()
        formData.append('photo', blob, 'photo.jpg')
        
        const token = localStorage.getItem('token')
        await fetch('http://localhost:5000/upload-photo', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`
          },
          body: formData
        })
        
        alert('照片保存成功！')
        this.closePreview()
      } catch (error) {
        console.error('保存照片失败:', error)
        alert('保存照片失败，请重试')
      }
    }
  },
  beforeUnmount() {
    this.stopCamera()
  }
}
</script>

<style scoped>
.camera-container {
  width: 100%;
  max-width: 640px;
  margin: 20px auto;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: var(--shadow);
}

.camera-box {
  position: relative;
  width: 100%;
  padding-top: 56.25%; /* 16:9 宽高比 */
  background: #000;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 20px;
}

.camera-video {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.camera-controls {
  display: flex;
  gap: 10px;
  justify-content: center;
  margin-bottom: 20px;
}

.camera-controls .btn {
  width: auto;
  padding: 8px 20px;
}

.photo-preview {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  max-width: 90%;
  width: 500px;
}

.preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.preview-header h3 {
  margin: 0;
  color: #333;
}

.btn-close {
  background: none;
  border: none;
  font-size: 24px;
  color: #666;
  cursor: pointer;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.btn-close:hover {
  background-color: #f0f0f0;
  color: #333;
}

.preview-image {
  width: 100%;
  border-radius: 4px;
  margin-bottom: 15px;
}

.preview-controls {
  display: flex;
  gap: 10px;
  justify-content: center;
}

.preview-controls .btn {
  width: auto;
  padding: 8px 20px;
}

@media (max-width: 480px) {
  .camera-controls {
    flex-direction: column;
  }
  
  .camera-controls .btn {
    width: 100%;
  }
  
  .preview-controls {
    flex-direction: column;
  }
  
  .preview-controls .btn {
    width: 100%;
  }
}
</style> 