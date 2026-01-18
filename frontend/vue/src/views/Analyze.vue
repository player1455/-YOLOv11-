<template>
  <div class="analyze">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>System Analytics</span>
              <el-button @click="$router.push('/')">Back</el-button>
            </div>
          </template>
          
          <el-row :gutter="20">
            <el-col :span="6">
              <el-card class="stat-card">
                <el-statistic title="Total Users" :value="stats.totalUsers"></el-statistic>
              </el-card>
            </el-col>
            <el-col :span="6">
              <el-card class="stat-card">
                <el-statistic title="Total Drones" :value="stats.totalDrones"></el-statistic>
              </el-card>
            </el-col>
            <el-col :span="6">
              <el-card class="stat-card">
                <el-statistic title="Active Drones" :value="stats.activeDrones"></el-statistic>
              </el-card>
            </el-col>
            <el-col :span="6">
              <el-card class="stat-card">
                <el-statistic title="Total Tasks" :value="stats.totalTasks"></el-statistic>
              </el-card>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>Users by Role</span>
          </template>
          <div class="chart-container">
            <div v-for="(count, role) in userRoles" :key="role" class="role-bar">
              <div class="role-label">{{ role }}</div>
              <el-progress :percentage="getPercentage(count, stats.totalUsers)" :color="getRoleColor(role)"></el-progress>
              <div class="role-count">{{ count }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>Drone Distribution</span>
          </template>
          <div class="chart-container">
            <div class="distribution-item">
              <span class="label">Automatic Mode:</span>
              <span class="value">{{ stats.activeDrones }}</span>
            </div>
            <div class="distribution-item">
              <span class="label">Manual Mode:</span>
              <span class="value">{{ stats.manualDrones }}</span>
            </div>
            <el-progress :percentage="getPercentage(stats.activeDrones, stats.totalDrones)" status="success" style="margin-top: 10px;"></el-progress>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="24">
        <el-card>
          <template #header>
            <span>Task Completion by Drone</span>
          </template>
          <el-table :data="drones" style="width: 100%">
            <el-table-column prop="userId" label="Drone ID" width="180"></el-table-column>
            <el-table-column prop="status" label="Mode" width="120">
              <template #default="scope">
                <el-tag :type="scope.row.status === 0 ? 'success' : 'warning'">
                  {{ scope.row.status === 0 ? 'Automatic' : 'Manual' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="fromAddress" label="From" width="180"></el-table-column>
            <el-table-column prop="toAddress" label="To" width="180"></el-table-column>
            <el-table-column prop="completedTaskCount" label="Tasks Completed">
              <template #default="scope">
                <el-progress :percentage="getPercentage(scope.row.completedTaskCount, maxTasks)" :stroke-width="20"></el-progress>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="24">
        <el-card>
          <template #header>
            <span>Daily Task Completion</span>
          </template>
          <div class="daily-stats">
            <div v-for="(day, index) in dailyStats" :key="index" class="day-item">
              <div class="day-label">{{ day.date }}</div>
              <el-progress :percentage="day.percentage" :color="getDayColor(index)"></el-progress>
              <div class="day-count">{{ day.count }} tasks</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { droneApi } from '../api'

export default {
  name: 'Analyze',
  data() {
    return {
      users: [],
      drones: [],
      stats: {
        totalUsers: 0,
        totalDrones: 0,
        activeDrones: 0,
        manualDrones: 0,
        totalTasks: 0
      },
      userRoles: {
        'admin': 0,
        'drone': 0,
        'user': 0
      },
      dailyStats: [
        { date: 'Monday', count: 45, percentage: 75 },
        { date: 'Tuesday', count: 52, percentage: 87 },
        { date: 'Wednesday', count: 38, percentage: 63 },
        { date: 'Thursday', count: 60, percentage: 100 },
        { date: 'Friday', count: 48, percentage: 80 },
        { date: 'Saturday', count: 30, percentage: 50 },
        { date: 'Sunday', count: 25, percentage: 42 }
      ]
    }
  },
  computed: {
    maxTasks() {
      return Math.max(...this.drones.map(d => d.completedTaskCount || 0), 1)
    }
  },
  mounted() {
    this.loadData()
  },
  methods: {
    async loadData() {
      try {
        const [usersRes, dronesRes] = await Promise.all([
          droneApi.getUserInfo({}),
          droneApi.getAllDroneInfo({})
        ])
        
        if (usersRes.data.code === 200) {
          this.users = usersRes.data.data
          this.calculateUserStats()
        }
        
        if (dronesRes.data.code === 200) {
          this.drones = dronesRes.data.data
          this.calculateDroneStats()
        }
      } catch (error) {
        this.$message.error('Failed to load data')
      }
    },
    
    calculateUserStats() {
      this.stats.totalUsers = this.users.length
      this.users.forEach(user => {
        if (this.userRoles[user.userRole] !== undefined) {
          this.userRoles[user.userRole]++
        }
      })
    },
    
    calculateDroneStats() {
      this.stats.totalDrones = this.drones.length
      this.stats.activeDrones = this.drones.filter(d => d.status === 0).length
      this.stats.manualDrones = this.drones.filter(d => d.status === 1).length
      this.stats.totalTasks = this.drones.reduce((sum, d) => sum + (d.completedTaskCount || 0), 0)
    },
    
    getPercentage(value, total) {
      if (total === 0) return 0
      return Math.round((value / total) * 100)
    },
    
    getRoleColor(role) {
      const colors = {
        'admin': '#F56C6C',
        'drone': '#E6A23C',
        'user': '#67C23A'
      }
      return colors[role] || '#409EFF'
    },
    
    getDayColor(index) {
      const colors = ['#409EFF', '#67C23A', '#E6A23C', '#F56C6C', '#909399', '#C0C4CC', '#D3D4D6']
      return colors[index % colors.length]
    }
  }
}
</script>

<style scoped>
.analyze {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-card {
  text-align: center;
  margin-bottom: 20px;
}

.chart-container {
  padding: 20px;
}

.role-bar {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.role-label {
  width: 100px;
  font-weight: bold;
}

.role-count {
  width: 50px;
  text-align: right;
  margin-left: 10px;
}

.distribution-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  font-size: 16px;
}

.distribution-item .label {
  font-weight: bold;
}

.distribution-item .value {
  color: #409EFF;
  font-weight: bold;
}

.daily-stats {
  padding: 20px;
}

.day-item {
  margin-bottom: 20px;
}

.day-label {
  margin-bottom: 5px;
  font-weight: bold;
}

.day-count {
  margin-top: 5px;
  text-align: right;
  color: #909399;
}
</style>
