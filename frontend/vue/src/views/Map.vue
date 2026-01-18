<template>
  <div class="map-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>Drone GPS Map</span>
          <div class="header-actions">
            <el-input
              v-model="searchDroneId"
              placeholder="Search drone by ID"
              clearable
              style="width: 200px; margin-right: 10px;"
            >
              <template #append>
                <el-button @click="searchAndLocateDrone">
                  <el-icon><search /></el-icon>
                </el-button>
              </template>
            </el-input>
            <el-button @click="refreshDroneLocations">Refresh</el-button>
          </div>
        </div>
      </template>
      
      <div class="map-wrapper">
        <div id="map" ref="mapContainer"></div>
      </div>
      
      <div class="drone-list">
        <el-table :data="drones" style="width: 100%">
          <el-table-column prop="userId" label="Drone ID" width="120"></el-table-column>
          <el-table-column prop="status" label="Status" width="100">
            <template #default="scope">
              <el-tag :type="scope.row.status === 0 ? 'success' : 'warning'">
                {{ scope.row.status === 0 ? 'Automatic' : 'Manual' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="fromAddress" label="From" width="150"></el-table-column>
          <el-table-column prop="toAddress" label="To" width="150"></el-table-column>
          <el-table-column prop="completedTaskCount" label="Tasks Completed" width="150"></el-table-column>
          <el-table-column label="GPS Coordinates" width="200">
            <template #default="scope">
              <span v-if="scope.row.gpsCoordinates">
                {{ scope.row.gpsCoordinates.lat.toFixed(4) }}, {{ scope.row.gpsCoordinates.lng.toFixed(4) }}
              </span>
              <span v-else class="text-gray-500">Not available</span>
            </template>
          </el-table-column>
          <el-table-column label="Action" width="120">
            <template #default="scope">
              <el-button 
                type="primary" 
                size="small" 
                @click="centerMapOnDrone(scope.row)"
              >
                Locate
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>
  </div>
</template>

<script>
import { droneApi } from '../api'
import { Search } from '@element-plus/icons-vue'

export default {
  name: 'Map',
  components: {
    Search
  },
  data() {
    return {
      map: null,
      drones: [],
      markers: {},
      leaflet: null,
      searchDroneId: ''
    }
  },
  mounted() {
    this.initMap()
    this.refreshDroneLocations()
    // 每隔5秒自动刷新一次无人机位置
    setInterval(() => {
      this.refreshDroneLocations()
    }, 5000)
  },
  methods: {
    async initMap() {
      // 动态加载Leaflet库和样式
      await this.loadLeaflet()
      
      // 初始化地图，默认显示南宁
      const nanningCoordinates = [22.8170, 108.3661]
      this.map = L.map('map').setView(nanningCoordinates, 12)
      
      // 添加OpenStreetMap图层
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(this.map)
    },
    
    async loadLeaflet() {
      // 确保只加载一次Leaflet
      if (window.L) {
        this.leaflet = window.L
        return
      }
      
      // 创建style标签并添加Leaflet样式
      const style = document.createElement('link')
      style.rel = 'stylesheet'
      style.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'
      document.head.appendChild(style)
      
      // 创建script标签并添加Leaflet脚本
      const script = document.createElement('script')
      script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'
      document.body.appendChild(script)
      
      // 等待脚本加载完成
      await new Promise(resolve => {
        script.onload = resolve
      })
      
      this.leaflet = window.L
    },
    
    async refreshDroneLocations() {
      try {
        // 获取所有无人机信息
        const response = await droneApi.getAllDroneInfo({ token: 'test-token' })
        
        if (response.data.code === 200) {
          this.drones = response.data.data
          this.updateDroneMarkers()
        }
      } catch (error) {
        console.error('Failed to refresh drone locations:', error)
        this.$message.error('Failed to refresh drone locations')
      }
    },
    
    updateDroneMarkers() {
      if (!this.map) return
      
      // 遍历所有无人机
      this.drones.forEach(drone => {
        // 为没有GPS坐标的无人机设置默认南宁坐标
        // 只在第一次生成，之后保持不变
        if (!drone.gpsCoordinates) {
          // 如果没有GPS坐标，生成基于南宁的随机坐标
          const nanningCoordinates = [22.8170, 108.3661]
          drone.gpsCoordinates = this.generateRandomCoordinates(nanningCoordinates[0], nanningCoordinates[1], 10)
        }
        
        const { lat, lng } = drone.gpsCoordinates
        const droneId = drone.userId
        
        // 如果已经存在标记，保持位置不变
        if (this.markers[droneId]) {
          // 不再更新位置，保持无人机位置稳定
        } else {
          // 否则创建新标记
          const marker = L.marker([lat, lng], {
            icon: this.createDroneIcon(drone.status === 0, droneId),
            title: droneId
          })
          
          // 添加弹出信息
          marker.bindPopup(`
            <div class="drone-popup">
              <h4>Drone: ${droneId}</h4>
              <p>Status: ${drone.status === 0 ? 'Automatic' : 'Manual'}</p>
              <p>From: ${drone.fromAddress}</p>
              <p>To: ${drone.toAddress}</p>
              <p>Tasks Completed: ${drone.completedTaskCount}</p>
              <p>GPS: ${lat.toFixed(4)}, ${lng.toFixed(4)}</p>
            </div>
          `)
          
          marker.addTo(this.map)
          this.markers[droneId] = marker
        }
      })
      
      // 移除不在列表中的标记
      Object.keys(this.markers).forEach(droneId => {
        const exists = this.drones.some(drone => drone.userId === droneId)
        if (!exists) {
          this.map.removeLayer(this.markers[droneId])
          delete this.markers[droneId]
        }
      })
    },
    
    createDroneIcon(isFlying, droneId) {
      // 创建自定义无人机图标，显示无人机名字
      return L.divIcon({
        className: 'drone-icon',
        html: `
          <div class="drone-marker ${isFlying ? 'flying' : 'landed'}">
            <div class="drone-body"></div>
            <div class="drone-wings"></div>
            <div class="drone-label">${droneId}</div>
          </div>
        `,
        iconSize: [30, 45],
        iconAnchor: [15, 30]
      })
    },
    
    generateRandomCoordinates(baseLat, baseLng, radiusKm) {
      // 生成基于基准坐标的随机GPS坐标
      const radiusDeg = radiusKm / 111.32 // 1度约等于111.32公里
      const randomLat = baseLat + (Math.random() - 0.5) * 2 * radiusDeg
      const randomLng = baseLng + (Math.random() - 0.5) * 2 * radiusDeg / Math.cos(baseLat * Math.PI / 180)
      
      return {
        lat: randomLat,
        lng: randomLng
      }
    },
    
    centerMapOnDrone(drone) {
      if (drone.gpsCoordinates) {
        this.map.setView([drone.gpsCoordinates.lat, drone.gpsCoordinates.lng], 15)
        // 打开弹出信息
        if (this.markers[drone.userId]) {
          this.markers[drone.userId].openPopup()
        }
      }
    },
    
    searchAndLocateDrone() {
      if (!this.searchDroneId.trim()) {
        this.$message.warning('Please enter a drone ID')
        return
      }
      
      const drone = this.drones.find(d => d.userId === this.searchDroneId.trim())
      if (drone) {
        this.centerMapOnDrone(drone)
        this.$message.success(`Located drone: ${drone.userId}`)
      } else {
        this.$message.error(`Drone ${this.searchDroneId} not found`)
      }
    }
  }
}
</script>

<style scoped>
.map-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.map-wrapper {
  height: 500px;
  margin-bottom: 20px;
  border-radius: 4px;
  overflow: hidden;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

#map {
  width: 100%;
  height: 100%;
}

.drone-list {
  margin-top: 20px;
}

/* 自定义无人机图标样式 */
:deep(.drone-icon) {
  transform-origin: center;
}

:deep(.drone-marker) {
  position: relative;
  width: 30px;
  height: 45px;
}

:deep(.drone-body) {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 16px;
  height: 16px;
  background-color: #409eff;
  border-radius: 50%;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  top: 25%;
}

:deep(.drone-wings) {
  position: absolute;
  top: 25%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 30px;
  height: 30px;
}

:deep(.drone-wings::before),
:deep(.drone-wings::after) {
  content: '';
  position: absolute;
  width: 8px;
  height: 24px;
  background-color: #67c23a;
  border-radius: 4px;
}

:deep(.drone-wings::before) {
  transform: rotate(45deg);
  top: -8px;
  left: 11px;
}

:deep(.drone-wings::after) {
  transform: rotate(-45deg);
  top: -8px;
  right: 11px;
}

/* 无人机标签样式 */
:deep(.drone-label) {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 2px 6px;
  border-radius: 10px;
  font-size: 10px;
  font-weight: bold;
  white-space: nowrap;
  z-index: 1000;
  pointer-events: none;
}

:deep(.drone-marker.flying) :deep(.drone-body) {
  background-color: #f56c6c;
  animation: pulse 1.5s infinite;
}

:deep(.drone-marker.landed) :deep(.drone-body) {
  background-color: #909399;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(245, 108, 108, 0.4);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(245, 108, 108, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(245, 108, 108, 0);
  }
}

:deep(.drone-popup) {
  min-width: 200px;
}

:deep(.drone-popup h4) {
  margin: 0 0 10px 0;
  color: #409eff;
}

:deep(.drone-popup p) {
  margin: 5px 0;
  font-size: 14px;
}

/* 搜索输入框样式 */
.header-actions {
  display: flex;
  align-items: center;
}

.text-gray-500 {
  color: #909399;
}
</style>