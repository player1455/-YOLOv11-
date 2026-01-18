<template>
  <div class="home">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card class="welcome-card">
          <h2>Welcome to YOLO Drone Obstacle Avoidance System</h2>
          <p>This system provides real-time obstacle detection and avoidance for autonomous drones using YOLOv11.</p>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>Flying Drones Status</span>
              <el-button type="primary" @click="refreshDrones">Refresh</el-button>
            </div>
          </template>
          <el-table :data="drones" style="width: 100%" v-loading="loading">
            <el-table-column prop="userId" label="Drone ID" width="180"></el-table-column>
            <el-table-column prop="status" label="Status" width="120">
              <template #default="scope">
                <el-tag :type="scope.row.status === 0 ? 'success' : 'warning'">
                  {{ scope.row.status === 0 ? 'Automatic' : 'Manual' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="fromAddress" label="From" width="180"></el-table-column>
            <el-table-column prop="toAddress" label="To" width="180"></el-table-column>
            <el-table-column prop="completedTaskCount" label="Completed Tasks" width="150"></el-table-column>
            <el-table-column label="Actions">
              <template #default="scope">
                <el-button size="small" @click="viewDrone(scope.row.userId)">View</el-button>
                <el-button size="small" type="primary" @click="goToFlying(scope.row.userId)">Monitor</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="8">
        <el-card class="stat-card">
          <el-statistic title="Total Drones" :value="drones.length"></el-statistic>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="stat-card">
          <el-statistic title="Active Drones" :value="activeDrones"></el-statistic>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="stat-card">
          <el-statistic title="Total Tasks Completed" :value="totalTasks"></el-statistic>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { droneApi } from '../api'

export default {
  name: 'Home',
  data() {
    return {
      drones: [],
      loading: false
    }
  },
  computed: {
    activeDrones() {
      return this.drones.filter(d => d.status === 0).length
    },
    totalTasks() {
      return this.drones.reduce((sum, d) => sum + (d.completedTaskCount || 0), 0)
    }
  },
  mounted() {
    this.loadDrones()
  },
  methods: {
    async loadDrones() {
      this.loading = true
      try {
        const response = await droneApi.getAllDroneInfo({})
        if (response.data.code === 200) {
          this.drones = response.data.data
        }
      } catch (error) {
        this.$message.error('Failed to load drones')
      } finally {
        this.loading = false
      }
    },
    refreshDrones() {
      this.loadDrones()
    },
    viewDrone(userId) {
      this.$router.push({ name: 'ControlDrone', query: { userId } })
    },
    goToFlying(userId) {
      this.$router.push({ name: 'Flying', query: { userId } })
    }
  }
}
</script>

<style scoped>
.home {
  padding: 20px;
}

.welcome-card {
  text-align: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.welcome-card h2 {
  margin: 0 0 10px 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-card {
  text-align: center;
}
</style>
