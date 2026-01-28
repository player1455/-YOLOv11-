import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000
})

api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/'
    }
    return Promise.reject(error)
  }
)

const flaskApi = axios.create({
  baseURL: import.meta.env.DEV ? 'http://localhost:5001' : '/flask',
  timeout: 10000
})

export const authApi = {
  login(data) {
    return api.post('/login', data)
  },
  register(data) {
    return api.post('/register', data)
  }
}

export const droneApi = {
  getDroneInfo(data) {
    return api.post('/droneInfo', data)
  },
  getAllDroneInfo(data) {
    return api.post('/alldroneInfo', data)
  },
  uploadImage(data) {
    return api.post('/upload', data)
  },
  createDrone(data) {
    return api.post('/createDrone', data)
  },
  updateDrone(data) {
    return api.put('/updateDrone', data)
  },
  getLatestPrediction(data) {
    return api.post('/getLatestPrediction', data)
  }
}

export const userApi = {
  getAllUsers(data) {
    return api.post('/userInfo', data)
  },
  createUser(data) {
    return api.post('/createUser', data)
  },
  updateUser(data) {
    return api.put('/updateUser', data)
  },
  deleteUser(data) {
    return api.delete('/deleteUser', { data })
  }
}

export const yoloApi = {
  predict(data) {
    return flaskApi.post('/predict', data)
  },
  getLatestImage(userId) {
    return flaskApi.get(`/latest_image/${userId}`, { responseType: 'blob' })
  },
  getImageHistory(params) {
    return flaskApi.get('/get_image_history', { params })
  },
  deleteImage(data) {
    return flaskApi.post('/delete_image', data)
  }
}

export default api
