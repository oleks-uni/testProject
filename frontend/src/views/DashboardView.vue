<template>
  <div class="dashboard-container">
    <header class="dashboard-header">
      <h1>My Tasks</h1>
      <button @click="handleLogout" class="logout-btn">Logout</button>
    </header>

    <main class="dashboard-content">
      <div class="actions-bar">
        <button @click="openCreateModal" class="create-btn">+ Create Task</button>
      </div>

      <div v-if="loading" class="loading">Loading tasks...</div>

      <div v-else-if="tasks.length === 0" class="empty-state">
        <p>You don't have any tasks yet.</p>
        <button @click="openCreateModal" class="create-btn">Create your first task</button>
      </div>

      <div v-else class="tasks-list">
        <div
          v-for="task in tasks"
          :key="task.id"
          class="task-card"
          :class="{ completed: task.is_completed }"
        >
          <div class="task-header">
            <h3>{{ task.title }}</h3>
            <div class="task-actions">
              <button @click="toggleComplete(task)" class="action-btn" :class="task.is_completed ? 'progress-btn' : 'complete-btn'">
                {{ task.is_completed ? 'Set in progress' : 'Complete' }}
              </button>
              <button @click="openEditModal(task)" class="action-btn edit-btn">Edit</button>
              <button @click="deleteTask(task.id)" class="action-btn delete-btn">Delete</button>
            </div>
          </div>
          <p class="task-description">{{ task.description || 'No description' }}</p>
          <div class="task-footer">
            <span class="task-date">Created: {{ formatDate(task.created_at) }}</span>
            <span v-if="task.is_completed" class="completed-badge">Completed</span>
          </div>
        </div>
      </div>
    </main>

    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal">
        <h2>{{ isEditing ? 'Edit Task' : 'Create Task' }}</h2>
        <form @submit.prevent="saveTask">
          <div class="form-group">
            <label for="title">Title</label>
            <input
              id="title"
              v-model="taskForm.title"
              type="text"
              placeholder="Task title"
              required
            />
          </div>
          <div class="form-group">
            <label for="description">Description</label>
            <textarea
              id="description"
              v-model="taskForm.description"
              placeholder="Task description"
              rows="3"
            ></textarea>
          </div>
          <div v-if="error" class="error-message">{{ error }}</div>
          <div class="modal-actions">
            <button type="button" @click="closeModal" class="cancel-btn">Cancel</button>
            <button type="submit" :disabled="saving" class="save-btn">
              {{ saving ? 'Saving...' : 'Save' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { taskService } from '@/services/tasks'

const router = useRouter()
const authStore = useAuthStore()

const tasks = ref([])
const loading = ref(true)
const saving = ref(false)
const error = ref(null)
const showModal = ref(false)
const isEditing = ref(false)
const editingTaskId = ref(null)

const taskForm = ref({
  title: '',
  description: ''
})

const fetchTasks = async () => {
  loading.value = true
  try {
    const response = await taskService.getAllTasks()
    tasks.value = response.data
  } catch (err) {
    error.value = 'Failed to load tasks'
    console.error(err)
  } finally {
    loading.value = false
  }
}

const openCreateModal = () => {
  isEditing.value = false
  editingTaskId.value = null
  taskForm.value = { title: '', description: '' }
  error.value = null
  showModal.value = true
}

const openEditModal = (task) => {
  isEditing.value = true
  editingTaskId.value = task.id
  taskForm.value = {
    title: task.title,
    description: task.description || ''
  }
  error.value = null
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  error.value = null
}

const saveTask = async () => {
  saving.value = true
  error.value = null

  try {
    if (isEditing.value) {
      await taskService.updateTask(editingTaskId.value, taskForm.value)
    } else {
      await taskService.createTask(taskForm.value)
    }
    await fetchTasks()
    closeModal()
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to save task'
  } finally {
    saving.value = false
  }
}

const toggleComplete = async (task) => {
  try {
    await taskService.patchTask(task.id, { is_completed: !task.is_completed })
    await fetchTasks()
  } catch (err) {
    console.error('Failed to update task:', err)
  }
}

const deleteTask = async (id) => {
  if (!confirm('Are you sure you want to delete this task?')) return

  try {
    await taskService.deleteTask(id)
    await fetchTasks()
  } catch (err) {
    console.error('Failed to delete task:', err)
  }
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString()
}

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}

onMounted(() => {
  fetchTasks()
})
</script>

<style scoped>
.dashboard-container {
  background: #f5f5f5;
  min-height: 100vh;
  width: 100vw;
  position: fixed;
  top: 0;
  left: 0;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 40px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.dashboard-header h1 {
  margin: 0;
  font-size: 24px;
}

.logout-btn {
  padding: 10px 20px;
  background: white;
  color: #667eea;
  border: none;
  border-radius: 5px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.logout-btn:hover {
  background: #f0f0f0;
  transform: translateY(-1px);
}

.dashboard-content {
  padding: 40px;
  max-width: 800px;
  margin: 0 auto;
}

.actions-bar {
  margin-bottom: 20px;
}

.create-btn {
  padding: 12px 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  transition: opacity 0.3s;
}

.create-btn:hover {
  opacity: 0.9;
}

.loading {
  text-align: center;
  padding: 40px;
  color: #666;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.empty-state p {
  color: #666;
  margin-bottom: 20px;
  font-size: 18px;
}

.tasks-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.task-card {
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.task-card:hover {
  transform: translateY(-2px);
}

.task-card.completed {
  opacity: 0.7;
  background: #f9f9f9;
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.task-header h3 {
  margin: 0;
  color: #333;
}

.task-card.completed .task-header h3 {
  text-decoration: line-through;
  color: #888;
}

.task-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
  transition: opacity 0.3s;
}

.action-btn:hover {
  opacity: 0.8;
}

.complete-btn {
  background: #27ae60;
  color: white;
}

.progress-btn {
  background: #f39c12;
  color: white;
}

.edit-btn {
  background: #3498db;
  color: white;
}

.delete-btn {
  background: #e74c3c;
  color: white;
}

.task-description {
  color: #666;
  margin: 10px 0;
  line-height: 1.5;
}

.task-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

.task-date {
  font-size: 12px;
  color: #999;
}

.completed-badge {
  background: #27ae60;
  color: white;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background: white;
  padding: 30px;
  border-radius: 10px;
  width: 100%;
  max-width: 450px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
}

.modal h2 {
  margin: 0 0 20px 0;
  color: #333;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  color: #555;
  font-weight: 500;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 14px;
  font-family: inherit;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #667eea;
}

.error-message {
  color: #e74c3c;
  margin-bottom: 15px;
  text-align: center;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.cancel-btn {
  padding: 10px 20px;
  background: #95a5a6;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: opacity 0.3s;
}

.cancel-btn:hover {
  opacity: 0.9;
}

.save-btn {
  padding: 10px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: opacity 0.3s;
}

.save-btn:hover:not(:disabled) {
  opacity: 0.9;
}

.save-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
