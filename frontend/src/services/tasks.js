import api from './api'

export const taskService = {
  getAllTasks() {
    return api.get('/task/create/')
  },

  getTask(id) {
    return api.get(`/task/tasks/${id}/`)
  },

  createTask(taskData) {
    return api.post('/task/create/', taskData)
  },

  updateTask(id, taskData) {
    return api.patch(`/task/tasks/${id}/`, taskData)
  },

  patchTask(id, taskData) {
    return api.patch(`/task/tasks/${id}/`, taskData)
  },

  deleteTask(id) {
    return api.delete(`/task/tasks/${id}/`)
  }
}
