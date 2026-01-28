import { defineStore } from 'pinia'
import { ref } from 'vue'
import { droneApi, yoloApi } from '../../api'

export const useDroneStore = defineStore('drone', () => {
  const currentDrone = ref(null)
  const boxes = ref([])
  const currentImage = ref(null)
  const isStreaming = ref(false)
  const streamInterval = ref(null)
  const imageDelay = ref(0)

  async function getDroneInfo(userId) {
    try {
      const response = await droneApi.getDroneInfo({ userId })
      if (response.data.code === 200) {
        currentDrone.value = response.data.data
      }
    } catch (error) {
      console.error('Failed to get drone info:', error)
      throw error
    }
  }

  async function uploadImage(data) {
    try {
      const response = await droneApi.uploadImage(data)
      if (response.data.code === 200) {
        boxes.value = response.data.data.boxes || []
        currentImage.value = 'data:image/jpeg;base64,' + response.data.data.image
      }
      return response.data
    } catch (error) {
      console.error('Failed to upload image:', error)
      throw error
    }
  }

  function startStream(userId, callback, interval = 50) {
    if (isStreaming.value) return
    
    isStreaming.value = true
    const startTime = Date.now()
    
    streamInterval.value = setInterval(async () => {
      try {
        const response = await yoloApi.getLatestImage(userId)
        if (response.status === 200) {
          const blob = response.data
          const imageUrl = URL.createObjectURL(blob)
          currentImage.value = imageUrl
          imageDelay.value = Date.now() - startTime
          
          if (callback) callback(imageUrl)
        }
      } catch (error) {
        console.error('Stream error:', error)
      }
    }, interval)
  }

  function stopStream() {
    if (streamInterval.value) {
      clearInterval(streamInterval.value)
      streamInterval.value = null
    }
    isStreaming.value = false
    currentImage.value = null
  }

  function reset() {
    currentDrone.value = null
    boxes.value = []
    currentImage.value = null
    stopStream()
  }

  return {
    currentDrone,
    boxes,
    currentImage,
    isStreaming,
    imageDelay,
    getDroneInfo,
    uploadImage,
    startStream,
    stopStream,
    reset
  }
})
