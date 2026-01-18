import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000
})

const flaskApi = axios.create({
  baseURL: '/flask',
  timeout: 30000
})

export const droneApi = {
  uploadImage(data) {
    return api.post('/upload', data)
  },
  
  getDroneInfo(data) {
    return api.post('/droneInfo', data)
  },
  
  getAllDroneInfo(data) {
    return api.post('/alldroneInfo', data)
  },
  
  getUserInfo(data) {
    return api.post('/userInfo', data)
  },
  
  deleteUser(data) {
    return api.delete('/deleteUser', { data })
  },
  
  updateUser(data) {
    return api.put('/updateUser', data)
  },
  
  createUser(data) {
    return api.post('/createUser', data)
  },
  
  getLatestPrediction(data) {
    return api.post('/getLatestPrediction', data)
  }
}

export const yoloApi = {
  predict(data) {
    return flaskApi.post('/predict', data)
  },
  
  getImageHistory(params) {
    return flaskApi.get('/get_image_history', { params })
  },
  
  deleteImage(data) {
    return flaskApi.post('/delete_image', data)
  },
  
  getLatestImage(userId) {
    return flaskApi.get(`/latest_image/${userId}`, { responseType: 'blob' })
  }
}

export default api
