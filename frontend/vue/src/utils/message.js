import { ElMessage } from 'element-plus'

export function showSuccess(message) {
  ElMessage.success({
    message,
    duration: 3000,
    showClose: true
  })
}

export function showError(message) {
  ElMessage.error({
    message,
    duration: 5000,
    showClose: true
  })
}

export function showWarning(message) {
  ElMessage.warning({
    message,
    duration: 3000,
    showClose: true
  })
}

export function showInfo(message) {
  ElMessage.info({
    message,
    duration: 3000,
    showClose: true
  })
}

export function showLoading(message = '加载中...') {
  return ElMessage.loading({
    message,
    duration: 0
  })
}
