<template>
  <div class="login">
    <el-row type="flex" justify="center" align="middle" style="height: 100vh;">
      <el-col :span="8">
        <el-card class="login-card">
          <h2>YOLO Drone System</h2>
          <el-tabs v-model="activeTab">
            <el-tab-pane label="Login" name="login">
              <el-form :model="loginForm" label-width="80px">
                <el-form-item label="Username">
                  <el-input v-model="loginForm.username" placeholder="Enter username"></el-input>
                </el-form-item>
                <el-form-item label="Password">
                  <el-input v-model="loginForm.password" type="password" placeholder="Enter password"></el-input>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="handleLogin" style="width: 100%;">Login</el-button>
                </el-form-item>
              </el-form>
            </el-tab-pane>
            
            <el-tab-pane label="Register" name="register">
              <el-form :model="registerForm" label-width="80px">
                <el-form-item label="Username">
                  <el-input v-model="registerForm.username" placeholder="Enter username"></el-input>
                </el-form-item>
                <el-form-item label="Password">
                  <el-input v-model="registerForm.password" type="password" placeholder="Enter password"></el-input>
                </el-form-item>
                <el-form-item label="Role">
                  <el-select v-model="registerForm.userRole" placeholder="Select role" style="width: 100%;">
                    <el-option label="User" value="user"></el-option>
                    <el-option label="Drone" value="drone"></el-option>
                  </el-select>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="handleRegister" style="width: 100%;">Register</el-button>
                </el-form-item>
              </el-form>
            </el-tab-pane>
          </el-tabs>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { droneApi } from '../api'

export default {
  name: 'Login',
  data() {
    return {
      activeTab: 'login',
      loginForm: {
        username: '',
        password: ''
      },
      registerForm: {
        username: '',
        password: '',
        userRole: 'user'
      }
    }
  },
  methods: {
    async handleLogin() {
      if (!this.loginForm.username || !this.loginForm.password) {
        this.$message.warning('Please enter username and password')
        return
      }
      
      localStorage.setItem('currentUser', this.loginForm.username)
      this.$message.success('Login successful')
      this.$router.push('/')
    },
    
    async handleRegister() {
      if (!this.registerForm.username || !this.registerForm.password) {
        this.$message.warning('Please fill in all fields')
        return
      }
      
      try {
        const userId = 'user' + Date.now()
        const response = await droneApi.createUser({
          username: this.registerForm.username,
          userId: userId,
          userRole: this.registerForm.userRole
        })
        
        if (response.data.code === 200) {
          this.$message.success('Registration successful')
          this.activeTab = 'login'
        } else {
          this.$message.error('Registration failed')
        }
      } catch (error) {
        this.$message.error('Registration error: ' + error.message)
      }
    }
  }
}
</script>

<style scoped>
.login {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
}

.login-card {
  text-align: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.login-card h2 {
  margin: 0 0 20px 0;
  color: #409EFF;
}
</style>
