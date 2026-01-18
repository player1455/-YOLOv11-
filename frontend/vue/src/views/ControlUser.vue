<template>
  <div class="control-user">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>User Management</span>
              <el-button @click="$router.push('/')">Back</el-button>
            </div>
          </template>
          
          <el-table :data="users" style="width: 100%" v-loading="loading">
            <el-table-column prop="userId" label="User ID" width="180"></el-table-column>
            <el-table-column prop="username" label="Username" width="150"></el-table-column>
            <el-table-column prop="userRole" label="Role" width="120">
              <template #default="scope">
                <el-tag :type="getRoleType(scope.row.userRole)">
                  {{ scope.row.userRole }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="creationDate" label="Created Date" width="200">
              <template #default="scope">
                {{ formatDate(scope.row.creationDate) }}
              </template>
            </el-table-column>
            <el-table-column label="Actions" width="200">
              <template #default="scope">
                <el-button size="small" @click="editUser(scope.row)">Edit</el-button>
                <el-button size="small" type="danger" @click="deleteUser(scope.row.userId)">Delete</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
    
    <el-dialog v-model="dialogVisible" title="Edit User" width="30%">
      <el-form :model="editForm" label-width="100px">
        <el-form-item label="User ID">
          <el-input v-model="editForm.userId" disabled></el-input>
        </el-form-item>
        <el-form-item label="Username">
          <el-input v-model="editForm.username"></el-input>
        </el-form-item>
        <el-form-item label="Role">
          <el-select v-model="editForm.userRole" style="width: 100%;">
            <el-option label="User" value="user"></el-option>
            <el-option label="Drone" value="drone"></el-option>
            <el-option label="Admin" value="admin"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="saveUser">Save</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { droneApi } from '../api'

export default {
  name: 'ControlUser',
  data() {
    return {
      users: [],
      loading: false,
      dialogVisible: false,
      editForm: {
        userId: '',
        username: '',
        userRole: 'user'
      }
    }
  },
  mounted() {
    this.loadUsers()
  },
  methods: {
    async loadUsers() {
      this.loading = true
      try {
        const response = await droneApi.getUserInfo({})
        if (response.data.code === 200) {
          this.users = response.data.data
        }
      } catch (error) {
        this.$message.error('Failed to load users')
      } finally {
        this.loading = false
      }
    },
    
    editUser(user) {
      this.editForm = {
        userId: user.userId,
        username: user.username,
        userRole: user.userRole
      }
      this.dialogVisible = true
    },
    
    async saveUser() {
      try {
        await droneApi.updateUser(this.editForm)
        this.$message.success('User updated successfully')
        this.dialogVisible = false
        this.loadUsers()
      } catch (error) {
        this.$message.error('Failed to update user')
      }
    },
    
    async deleteUser(userId) {
      this.$confirm('Are you sure to delete this user?', 'Warning', {
        confirmButtonText: 'OK',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }).then(async () => {
        try {
          await droneApi.deleteUser({ userId })
          this.$message.success('User deleted successfully')
          this.loadUsers()
        } catch (error) {
          this.$message.error('Failed to delete user')
        }
      }).catch(() => {})
    },
    
    getRoleType(role) {
      const types = {
        'admin': 'danger',
        'drone': 'warning',
        'user': 'success'
      }
      return types[role] || 'info'
    },
    
    formatDate(dateStr) {
      if (!dateStr) return '-'
      return new Date(dateStr).toLocaleString()
    }
  }
}
</script>

<style scoped>
.control-user {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
