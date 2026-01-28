<template>
  <div class="flying">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>无人机实时监控 - {{ userId }}</span>
              <div>
                <el-button @click="$router.push('/')">返回首页</el-button>
                <el-button 
                  type="primary" 
                  @click="toggleImageStream" 
                  :loading="imageStreamLoading"
                  :type="isImageStreaming ? 'danger' : 'success'"
                  style="margin-left: 10px;">
                  {{ isImageStreaming ? '停止视频流' : '开始视频流' }}
                </el-button>
                <el-button 
                  type="primary" 
                  @click="toggleRealTimePrediction" 
                  :loading="realTimePredicting"
                  :type="realTimePredicting ? 'danger' : 'success'"
                  style="margin-left: 10px;">
                  {{ realTimePredicting ? '停止实时预测' : '开始实时预测' }}
                </el-button>
              </div>
            </div>
          </template>
          
          <el-row :gutter="20">
            <el-col :span="12">
              <div class="upload-section">
                <el-tabs v-model="activeTab">
                  <el-tab-pane label="上传图片" name="upload">
                    <el-upload
                      class="upload-demo"
                      drag
                      :auto-upload="false"
                      :on-change="handleFileChange"
                      accept="image/*"
                    >
                      <el-icon class="el-icon--upload"><upload-filled /></el-icon>
                      <div class="el-upload__text">
                        将图片拖到此处或 <em>点击上传</em>
                      </div>
                    </el-upload>
                    <el-button type="primary" @click="predict" :loading="predicting" style="margin-top: 10px;">
                      预测障碍物
                    </el-button>
                  </el-tab-pane>
                  <el-tab-pane label="摄像头" name="camera">
                    <div class="camera-section">
                      <video v-if="cameraActive" ref="videoElement" autoplay playsinline width="100%" height="auto"></video>
                      <div v-else class="camera-placeholder">
                        <el-empty description="摄像头未激活"></el-empty>
                      </div>
                      <el-button 
                        type="primary" 
                        @click="toggleCamera" 
                        :disabled="realTimePredicting"
                        style="margin-top: 10px;">
                        {{ cameraActive ? '停止摄像头' : '启动摄像头' }}
                      </el-button>
                      <el-button 
                        type="success" 
                        @click="captureImage" 
                        :disabled="!cameraActive || realTimePredicting" 
                        style="margin-top: 10px; margin-left: 10px;">
                        捕获图片
                      </el-button>
                    </div>
                  </el-tab-pane>
                </el-tabs>
              </div>
            </el-col>
            
            <el-col :span="12">
              <div class="result-section">
                <h3>预测结果</h3>
                <div class="image-container">
                  <img 
                    v-if="currentImage" 
                    :src="currentImage" 
                    alt="预测结果" 
                    class="stream-image"
                  />
                  <div v-else class="placeholder">
                    <el-empty description="暂无图片"></el-empty>
                  </div>
                  <div class="image-info">
                    <span>状态: {{ isImageStreaming ? '视频流播放中' : '就绪' }}</span>
                    <span>延迟: {{ imageDelay }}ms</span>
                  </div>
                </div>
                <div v-if="realTimePredicting" class="real-time-indicator">
                  <el-tag type="warning">实时预测中</el-tag>
                  <div class="fps-info">FPS: {{ fps }}</div>
                </div>
                <div v-if="isImageStreaming" class="image-stream-indicator">
                  <el-tag type="success">视频流模式</el-tag>
                  <div class="play-info">实时显示最新图片</div>
                </div>
              </div>
            </el-col>
          </el-row>
          
          <el-row :gutter="20" style="margin-top: 20px;">
            <el-col :span="24">
              <div v-if="boxes.length > 0">
                <h3>检测到的障碍物 ({{ boxes.length }})</h3>
                <el-table :data="boxes" style="width: 100%">
                  <el-table-column prop="class_name" label="类别" width="150"></el-table-column>
                  <el-table-column prop="confidence" label="置信度" width="120">
                    <template #default="scope">
                      {{ (scope.row.confidence * 100).toFixed(2) }}%
                    </template>
                  </el-table-column>
                  <el-table-column prop="xyxy" label="边界框">
                    <template #default="scope">
                      [{{ scope.row.xyxy.map(x => x.toFixed(0)).join(', ') }}]
                    </template>
                  </el-table-column>
                </el-table>
              </div>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { UploadFilled } from '@element-plus/icons-vue'
import { droneApi, yoloApi } from '../api'

export default {
  name: 'Flying',
  components: {
    UploadFilled
  },
  data() {
    return {
      userId: this.$route.query.userId || 'test_drone',
      selectedFile: null,
      imageData: null,
      predicting: false,
      resultImage: null,
      boxes: [],
      activeTab: 'upload',
      cameraActive: false,
      videoStream: null,
      canvas: null,
      realTimePredicting: false,
      realTimeInterval: null,
      fps: 0,
      frameCount: 0,
      lastFpsUpdate: 0,
      refreshInterval: null,
      isPredicting: false, // 预测状态标志，避免阻塞
      
      // 视频流模式
      currentImage: null, // 当前显示的图片
      isImageStreaming: false, // 是否处于视频流模式
      imageStreamLoading: false, // 视频流加载状态
      imageStreamInterval: null, // 视频流定时器
      lastImageTime: 0, // 上一张图片的时间戳
      imageDelay: 0, // 图片延迟
      lastImageFilename: null, // 上一张图片的文件名
      imageCache: new Map(), // 图片缓存
      imageLoadInterval: 50, // 图片加载间隔（毫秒），降低延迟
      isLoadingImage: false, // 是否正在加载图片
    }
  },
  mounted() {
    // 初始化canvas元素用于图像捕获
    this.canvas = document.createElement('canvas')
    // 如果用户ID是drone001，自动切换到摄像头标签页
    if (this.userId === 'drone001') {
      this.activeTab = 'camera'
    }
    
    // 启动定时刷新，从后端获取最新的预测结果
    this.startRefreshInterval()
  },
  beforeUnmount() {
    // 组件销毁前清理资源
    this.stopRealTimePrediction()
    this.stopRefreshInterval()
    this.stopImageStream()
    if (this.videoStream) {
      this.videoStream.getTracks().forEach(track => track.stop())
    }
  },
  methods: {
    handleFileChange(file) {
      this.selectedFile = file.raw
      const reader = new FileReader()
      reader.onload = (e) => {
        this.imageData = e.target.result
      }
      reader.readAsDataURL(this.selectedFile)
    },
    async toggleCamera() {
      if (this.cameraActive) {
        // 关闭摄像头
        if (this.videoStream) {
          this.videoStream.getTracks().forEach(track => track.stop())
          this.videoStream = null
        }
        this.cameraActive = false
        this.$message.success('摄像头已停止')
      } else {
        // 启动摄像头
        try {
          const videoElement = this.$refs.videoElement
          if (videoElement) {
            this.videoStream = await navigator.mediaDevices.getUserMedia({ video: true })
            videoElement.srcObject = this.videoStream
            this.cameraActive = true
            this.$message.success('摄像头已启动')
          }
        } catch (error) {
          this.$message.error('无法访问摄像头: ' + error.message)
          console.error('摄像头错误:', error)
        }
      }
    },
    captureImage() {
      const videoElement = this.$refs.videoElement
      if (!videoElement || !this.cameraActive) {
        return
      }
      
      // 设置canvas大小与视频一致
      this.canvas.width = videoElement.videoWidth
      this.canvas.height = videoElement.videoHeight
      
      // 绘制视频帧到canvas
      const ctx = this.canvas.getContext('2d')
      ctx.drawImage(videoElement, 0, 0, this.canvas.width, this.canvas.height)
      
      // 将canvas内容转换为data URL
      this.imageData = this.canvas.toDataURL('image/jpeg')
      this.$message.success('图片已捕获')
    },
    async predict() {
      if (!this.imageData) {
        this.$message.warning('请先选择一张图片')
        return
      }
      
      this.predicting = true
      try {
        const response = await droneApi.uploadImage({
          userId: this.userId,
          image: this.imageData,
          token: 'test-token'
        })
        
        if (response.data.code === 200) {
          this.boxes = response.data.data.boxes || []
          this.resultImage = 'data:image/jpeg;base64,' + response.data.data.image
          this.$message.success('预测完成')
        } else {
          this.$message.error('预测失败')
        }
      } catch (error) {
        this.$message.error('预测错误: ' + error.message)
      } finally {
        this.predicting = false
      }
    },
    toggleRealTimePrediction() {
      if (this.realTimePredicting) {
        this.stopRealTimePrediction()
      } else {
        this.startRealTimePrediction()
      }
    },
    async startRealTimePrediction() {
      // 如果摄像头未启动，先启动摄像头
      if (!this.cameraActive) {
        await this.toggleCamera()
        if (!this.cameraActive) {
          this.$message.error('无法启动摄像头，无法开始实时预测')
          return
        }
      }
      
      this.realTimePredicting = true
      this.frameCount = 0
      this.lastFpsUpdate = Date.now()
      this.fps = 0
      this.isPredicting = false // 添加预测状态标志，避免阻塞
      
      // 开始实时预测循环，每100ms（0.1秒）尝试发送一张图片
      this.realTimeInterval = setInterval(() => {
        this.realTimePredict()
      }, 100) // 每100ms尝试一次
      
      this.$message.success('实时预测已启动')
    },
    stopRealTimePrediction() {
      this.realTimePredicting = false
      if (this.realTimeInterval) {
        clearInterval(this.realTimeInterval)
        this.realTimeInterval = null
      }
      this.isPredicting = false
      this.$message.success('实时预测已停止')
    },
    async realTimePredict() {
      // 如果已经在预测中，直接返回，避免阻塞
      if (this.isPredicting || !this.cameraActive || !this.realTimePredicting) {
        return
      }
      
      try {
        this.isPredicting = true
        const videoElement = this.$refs.videoElement
        if (!videoElement) {
          this.isPredicting = false
          return
        }
        
        // 更新FPS计数（异步进行，不阻塞）
        this.frameCount++
        const now = Date.now()
        if (now - this.lastFpsUpdate >= 1000) {
          this.fps = this.frameCount
          this.frameCount = 0
          this.lastFpsUpdate = now
        }
        
        // 快速绘制视频帧到canvas
        this.canvas.width = videoElement.videoWidth
        this.canvas.height = videoElement.videoHeight
        const ctx = this.canvas.getContext('2d')
        ctx.drawImage(videoElement, 0, 0, this.canvas.width, this.canvas.height)
        
        // 将canvas内容转换为data URL
        const imageData = this.canvas.toDataURL('image/jpeg', 0.8) // 降低质量，加快传输
        
        // 获取当前时间戳
        const timestamp = new Date().toISOString()
          .replace(/[^0-9]/g, '')
          .slice(0, -3)
          .replace(/(\d{8})(\d{6})(\d{3})/, '$1_$2_$3')
        
        // 发送到YOLO服务进行预测，包含时间戳
        const response = await droneApi.uploadImage({
          userId: this.userId,
          image: imageData,
          token: 'test-token',
          timestamp: timestamp
        })
        
        if (response.data.code === 200) {
          // 异步更新UI，避免阻塞
          this.$nextTick(() => {
            this.boxes = response.data.data.boxes || []
            this.resultImage = 'data:image/jpeg;base64,' + response.data.data.image
          })
        }
      } catch (error) {
        console.error('实时预测错误:', error)
      } finally {
        // 无论成功失败，都释放预测锁
        this.isPredicting = false
      }
    },
    
    // 启动定时刷新
    startRefreshInterval() {
      if (this.refreshInterval) {
        this.stopRefreshInterval()
      }
      
      this.refreshInterval = setInterval(() => {
        this.refreshPrediction()
      }, 2000) // 每2秒刷新一次
      
      console.log(`定时刷新已启动，每 2000ms 刷新一次`)
    },
    
    // 停止定时刷新
    stopRefreshInterval() {
      if (this.refreshInterval) {
        clearInterval(this.refreshInterval)
        this.refreshInterval = null
        console.log('定时刷新已停止')
      }
    },
    
    // 刷新预测结果
    async refreshPrediction() {
      // 实时预测模式下不进行定时刷新，避免冲突
      if (this.realTimePredicting) {
        return
      }
      
      try {
        // 1. 获取最新的预测数据（包含障碍物信息）
        const response = await droneApi.getLatestPrediction({
          userId: this.userId,
          token: 'test-token'
        })
        
        if (response.data.code === 200) {
          const predictionData = response.data.data.prediction
          if (predictionData) {
            this.boxes = predictionData.boxes || []
          }
        }
        
        // 2. 如果是视频流模式，更新图片
        if (this.isImageStreaming) {
          await this.updateImageStream()
        }
        
      } catch (error) {
        console.error('刷新预测结果失败:', error)
      }
    },
    
    // 切换视频流
    toggleImageStream() {
      if (this.isImageStreaming) {
        this.stopImageStream()
      } else {
        this.startImageStream()
      }
    },
    
    // 开始视频流
    async startImageStream() {
      this.imageStreamLoading = true
      try {
        // 清空之前的数据
        this.currentImage = null
        this.lastImageFilename = null
        
        this.isImageStreaming = true
        
        // 停止定时刷新，避免冲突
        this.stopRefreshInterval()
        
        // 立即更新一次
        await this.updateImageStream()
        
        // 开始定时更新，每100ms更新一次
        this.imageStreamInterval = setInterval(() => {
          this.updateImageStream()
        }, this.imageLoadInterval)
        
        this.$message.success('视频流已启动')
      } catch (error) {
        this.$message.error('启动视频流失败: ' + error.message)
      } finally {
        this.imageStreamLoading = false
      }
    },
    
    // 停止视频流
    stopImageStream() {
      this.isImageStreaming = false
      if (this.imageStreamInterval) {
        clearInterval(this.imageStreamInterval)
        this.imageStreamInterval = null
      }
      
      this.currentImage = null
      this.lastImageFilename = null
      
      // 重新启动定时刷新
      this.startRefreshInterval()
      
      this.$message.success('视频流已停止')
    },
    
    // 更新视频流
    async updateImageStream() {
      if (this.isLoadingImage) {
        return // 已经在加载中，避免重复加载
      }
      
      this.isLoadingImage = true
      try {
        // 直接获取最新图片，减少延迟
        const response = await yoloApi.getLatestImage(this.userId)
        
        if (response.status === 200) {
          // 将Blob转换为Data URL
          const blob = response.data
          const imageUrl = URL.createObjectURL(blob)
          
          // 直接更新显示，不检查是否为新图片
          this.currentImage = imageUrl
          
          // 计算实际延迟（使用响应头或其他方式获取真实延迟）
          const currentTime = Date.now()
          this.imageDelay = currentTime - Date.now() // 简化延迟计算
        }
      } catch (error) {
        console.error('更新视频流失败:', error)
      } finally {
        this.isLoadingImage = false
      }
    },
    
    // 清理旧图片
    async cleanupOldImages(currentImages) {
      if (currentImages.length === 0) {
        return
      }
      
      try {
        // 只保留最新的5张图片
        const imagesToKeep = currentImages.slice(0, 5)
        
        // 获取所有图片
        const allImages = await this.fetchAllImages()
        
        // 删除旧图片
        for (const image of allImages) {
          if (!imagesToKeep.includes(image)) {
            await this.deleteImage(image)
            // 从缓存中移除
            this.imageCache.delete(image)
          }
        }
      } catch (error) {
        console.error('清理旧图片失败:', error)
      }
    },
    
    // 获取所有图片
    async fetchAllImages() {
      try {
        const response = await yoloApi.getImageHistory({
          userId: this.userId,
          token: 'test-token'
        })
        
        if (response.data.code === 200) {
          return response.data.data.images || []
        }
      } catch (error) {
        console.error('获取图片列表失败:', error)
      }
      return []
    },
    
    // 解析图片文件名中的时间戳
    parseImageTime(imageName) {
      // 图片格式: {userId}_{YYYYMMDD_HHMMSS_mmm}.jpg
      const parts = imageName.split('_')
      if (parts.length < 4) return 0
      
      const datePart = parts[1] // YYYYMMDD
      const timePart = parts[2] // HHMMSS
      const msPart = parts[3].replace('.jpg', '') // mmm
      
      // 转换为Date对象
      const year = parseInt(datePart.substring(0, 4))
      const month = parseInt(datePart.substring(4, 6)) - 1 // 月份从0开始
      const day = parseInt(datePart.substring(6, 8))
      const hour = parseInt(timePart.substring(0, 2))
      const minute = parseInt(timePart.substring(2, 4))
      const second = parseInt(timePart.substring(4, 6))
      const ms = parseInt(msPart)
      
      const date = new Date(year, month, day, hour, minute, second, ms)
      return date.getTime()
    },
    
    // 删除图片
    async deleteImage(filename) {
      try {
        const response = await yoloApi.deleteImage({
          userId: this.userId,
          filename: filename,
          token: 'test-token'
        })
        
        if (response.data.code === 200) {
          console.log('图片已删除:', filename)
        }
      } catch (error) {
        console.error('删除图片失败:', error)
      }
    }
  }
}
</script>

<style scoped>
.flying {
  padding: 20px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.upload-section {
  padding: 20px;
  text-align: center;
}
.result-section {
  padding: 20px;
  text-align: center;
  position: relative;
}
.image-container img {
  max-width: 100%;
  max-height: 400px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
.stream-image {
  transition: opacity 0.1s ease-in-out;
  max-width: 100%;
  max-height: 600px;
  width: auto;
  height: auto;
  object-fit: contain;
}
.image-info {
  margin-top: 10px;
  display: flex;
  justify-content: space-between;
  font-size: 14px;
  color: #606266;
}
.placeholder {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.camera-section {
  text-align: center;
}
.camera-section video {
  border: 1px solid #ddd;
  border-radius: 4px;
  max-width: 100%;
  max-height: 300px;
  background-color: #f0f0f0;
}
.camera-placeholder {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f0f0f0;
  border:1px dashed #ddd;
  border-radius: 4px;
}
:deep(.el-tabs__content) {
  margin-top: 10px;
}
.real-time-indicator {
  margin-top: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}
.image-stream-indicator {
  margin-top: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}
.fps-info, .play-info {
  font-size: 14px;
  color: #606266;
  font-weight: bold;
}
/* 实时预测状态下的样式 */
.real-time-active {
  animation: pulse 1.5s infinite;
}
@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(255, 77, 79, 0.4);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(255, 77, 79, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(255, 77, 79, 0);
  }
}
</style>
