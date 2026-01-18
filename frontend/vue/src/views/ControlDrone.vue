<template>
  <div class="control-drone">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>Drone Control Panel</span>
              <el-button @click="$router.push('/')">Back</el-button>
            </div>
          </template>
          
          <el-form :model="controlForm" label-width="120px">
            <el-form-item label="Drone ID">
              <el-select v-model="controlForm.userId" placeholder="Select drone" @change="loadDroneInfo">
                <el-option
                  v-for="drone in drones"
                  :key="drone.userId"
                  :label="drone.userId"
                  :value="drone.userId"
                ></el-option>
              </el-select>
            </el-form-item>
            
            <el-form-item label="Status">
              <el-radio-group v-model="controlForm.status">
                <el-radio :label="0">Automatic</el-radio>
                <el-radio :label="1">Manual</el-radio>
              </el-radio-group>
            </el-form-item>
            
            <el-form-item label="From Address">
              <el-input v-model="controlForm.fromAddress" placeholder="Enter departure location"></el-input>
            </el-form-item>
            
            <el-form-item label="To Address">
              <el-input v-model="controlForm.toAddress" placeholder="Enter destination"></el-input>
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" @click="updateDrone">Update Drone</el-button>
              <el-button @click="resetForm">Reset</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="24">
        <el-card>
          <template #header>
            <span>Control Log</span>
          </template>
          <el-timeline>
            <el-timeline-item
              v-for="(log, index) in controlLogs"
              :key="index"
              :timestamp="log.timestamp"
            >
              {{ log.action }}
            </el-timeline-item>
          </el-timeline>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { droneApi } from '../api'

export default {
  name: 'ControlDrone',
  data() {
    return {
      drones: [],
      controlForm: {
        userId: this.$route.query.userId || '',
        status: 0,
        fromAddress: '',
        toAddress: ''
      },
      controlLogs: []
    }
  },
  mounted() {
    this.loadDrones()
    if (this.controlForm.userId) {
      this.loadDroneInfo()
    }
  },
  methods: {
    async loadDrones() {
      try {
        const response = await droneApi.getAllDroneInfo({})
        if (response.data.code === 200) {
          this.drones = response.data.data
        }
      } catch (error) {
        this.$message.error('Failed to load drones')
      }
    },
    
    async loadDroneInfo() {
      try {
        const response = await droneApi.getDroneInfo({ userId: this.controlForm.userId })
        if (response.data.code === 200) {
          const data = response.data.data
          this.controlForm.status = data.condition
          this.controlForm.fromAddress = data.fromAddress
          this.controlForm.toAddress = data.toAddress
        }
      } catch (error) {
        this.$message.error('Failed to load drone info')
      }
    },
    
    async updateDrone() {
      if (!this.controlForm.userId) {
        this.$message.warning('Please select a drone')
        return
      }
      
      try {
        await droneApi.updateUser({
          userId: this.controlForm.userId,
          userRole: 'drone'
        })
        
        this.addControlLog(`Updated drone ${this.controlForm.userId}: status=${this.controlForm.status}, from=${this.controlForm.fromAddress}, to=${this.controlForm.toAddress}`)
        this.$message.success('Drone updated successfully')
      } catch (error) {
        this.$message.error('Failed to update drone')
      }
    },
    
    addControlLog(action) {
      this.controlLogs.unshift({
        action: action,
        timestamp: new Date().toLocaleString()
      })
      
      if (this.controlLogs.length > 10) {
        this.controlLogs.pop()
      }
    },
    
    resetForm() {
      this.controlForm = {
        userId: '',
        status: 0,
        fromAddress: '',
        toAddress: ''
      }
    }
  }
}
</script>

<style scoped>
.control-drone {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
