<template>
  <div class="dashboard-container">
    <header class="dashboard-header">
      <h1>Dashboard</h1>
      <button @click="handleLogout" class="logout-btn">Logout</button>
    </header>
    <main class="dashboard-content">
      <p>Welcome to your task manager!</p>
    </main>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.dashboard-container {
  background: white;
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
  color: #333;
}
</style>
