<script setup lang="ts">
import { ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const sidebarOpen = ref(false)

const navItems = [
  { path: '/personas', label: '角色', icon: '🎭' },
  { path: '/providers', label: '模型', icon: '🤖' },
  { path: '/napcat', label: '连接', icon: '🔗' },
  { path: '/settings', label: '设置', icon: '⚙️' },
]
</script>

<template>
  <div class="app">
    <!-- 移动端遮罩 -->
    <div v-if="sidebarOpen" class="sidebar-overlay" @click="sidebarOpen = false"></div>

    <!-- 移动端菜单按钮 -->
    <button class="mobile-menu-btn" @click="sidebarOpen = !sidebarOpen">
      <span></span><span></span><span></span>
    </button>

    <nav class="sidebar" :class="{ open: sidebarOpen }">
      <div class="logo">
        <div class="logo-icon">Q</div>
        <div>
          <h2>QQ Bot</h2>
          <small>控制台</small>
        </div>
      </div>
      <ul>
        <li v-for="item in navItems" :key="item.path">
          <router-link
            :to="item.path"
            :class="{ active: route.path === item.path }"
            @click="sidebarOpen = false"
          >
            <span class="nav-icon">{{ item.icon }}</span>
            <span class="nav-label">{{ item.label }}</span>
            <span v-if="route.path === item.path" class="nav-indicator"></span>
          </router-link>
        </li>
      </ul>
      <div class="sidebar-footer">
        <small>v1.0</small>
      </div>
    </nav>
    <main class="content">
      <router-view />
    </main>
  </div>
</template>

<style>
:root {
  --sidebar-w: 240px;
  --primary: #4361ee;
  --primary-light: #eef1ff;
  --success: #2a9d8f;
  --success-light: #d4edda;
  --danger: #e63946;
  --danger-light: #f8d7da;
  --gray-50: #f8f9fc;
  --gray-100: #f1f3f8;
  --gray-200: #e2e6ef;
  --gray-300: #cdd3e0;
  --gray-400: #9ba3b5;
  --gray-500: #6b7280;
  --gray-700: #374151;
  --gray-800: #1f2937;
  --gray-900: #111827;
  --card-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
  --card-shadow-hover: 0 4px 12px rgba(0,0,0,0.08), 0 2px 4px rgba(0,0,0,0.04);
  --radius: 10px;
  --radius-sm: 6px;
  --transition: 0.2s ease;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
  background: var(--gray-100);
  color: var(--gray-800);
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}

.app {
  display: flex;
  min-height: 100vh;
}

/* ─── Sidebar ─── */
.sidebar {
  width: var(--sidebar-w);
  background: var(--gray-900);
  color: #fff;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  position: sticky;
  top: 0;
  height: 100vh;
  z-index: 100;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 24px 20px 20px;
  border-bottom: 1px solid rgba(255,255,255,0.08);
}

.logo-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: linear-gradient(135deg, var(--primary), #7c3aed);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 1.1em;
}

.logo h2 {
  font-size: 1.2em;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.logo small {
  color: var(--gray-400);
  font-size: 0.75em;
}

.sidebar ul {
  list-style: none;
  padding: 8px 0;
  flex: 1;
}

.sidebar li a {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 20px;
  margin: 2px 8px;
  border-radius: 8px;
  color: var(--gray-400);
  text-decoration: none;
  font-size: 0.92em;
  font-weight: 500;
  transition: all var(--transition);
  position: relative;
}

.sidebar li a:hover {
  background: rgba(255,255,255,0.06);
  color: #fff;
}

.sidebar li a.active {
  background: rgba(67, 97, 238, 0.15);
  color: #fff;
}

.nav-indicator {
  position: absolute;
  left: -8px;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 20px;
  background: var(--primary);
  border-radius: 0 3px 3px 0;
}

.nav-icon { font-size: 1.15em; }
.nav-label { flex: 1; }

.sidebar-footer {
  padding: 16px 20px;
  border-top: 1px solid rgba(255,255,255,0.08);
  color: var(--gray-500);
  font-size: 0.75em;
}

/* ─── Content ─── */
.content {
  flex: 1;
  padding: 32px 40px;
  max-width: 960px;
  min-width: 0;
}

h1 {
  margin-bottom: 20px;
  font-size: 1.5em;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: var(--gray-900);
}

/* ─── Cards ─── */
.card {
  background: #fff;
  border-radius: var(--radius);
  padding: 20px 24px;
  margin-bottom: 14px;
  box-shadow: var(--card-shadow);
  border: 1px solid var(--gray-200);
  transition: box-shadow var(--transition), border-color var(--transition);
}

.card:hover {
  box-shadow: var(--card-shadow-hover);
}

/* ─── Forms ─── */
.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  font-weight: 600;
  margin-bottom: 6px;
  font-size: 0.875em;
  color: var(--gray-700);
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 9px 13px;
  border: 1px solid var(--gray-200);
  border-radius: var(--radius-sm);
  font-size: 0.9em;
  color: var(--gray-800);
  background: var(--gray-50);
  transition: border-color var(--transition), box-shadow var(--transition), background var(--transition);
  outline: none;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.1);
  background: #fff;
}

.form-group input::placeholder,
.form-group textarea::placeholder {
  color: var(--gray-400);
}

.form-group textarea {
  resize: vertical;
  min-height: 80px;
  line-height: 1.5;
}

/* ─── Buttons ─── */
.btn {
  padding: 8px 18px;
  border: none;
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-size: 0.875em;
  font-weight: 500;
  transition: all var(--transition);
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.btn:hover { transform: translateY(-1px); }
.btn:active { transform: translateY(0); }
.btn:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }

.btn-primary {
  background: var(--primary);
  color: #fff;
  box-shadow: 0 1px 2px rgba(67, 97, 238, 0.3);
}
.btn-primary:hover { background: #3651d4; }

.btn-danger {
  background: var(--danger);
  color: #fff;
  box-shadow: 0 1px 2px rgba(230, 57, 70, 0.3);
}
.btn-danger:hover { background: #c5303c; }

.btn-success {
  background: var(--success);
  color: #fff;
  box-shadow: 0 1px 2px rgba(42, 157, 143, 0.3);
}
.btn-success:hover { background: #238b7e; }

.btn-outline {
  background: transparent;
  color: var(--gray-500);
  border: 1px solid var(--gray-300);
}
.btn-outline:hover {
  background: var(--gray-50);
  color: var(--gray-700);
  border-color: var(--gray-400);
}

.btn-sm {
  padding: 5px 12px;
  font-size: 0.8em;
}

/* ─── Badges ─── */
.badge {
  display: inline-flex;
  align-items: center;
  padding: 2px 10px;
  border-radius: 20px;
  font-size: 0.75em;
  font-weight: 600;
  letter-spacing: 0.02em;
}

.badge-green {
  background: var(--success-light);
  color: #155724;
}

.badge-red {
  background: var(--danger-light);
  color: #721c24;
}

.badge-gray {
  background: var(--gray-100);
  color: var(--gray-500);
  border: 1px solid var(--gray-200);
}

/* ─── Utilities ─── */
.flex { display: flex; }
.flex-between { display: flex; justify-content: space-between; align-items: center; }
.gap-8 { gap: 8px; }
.mt-10 { margin-top: 10px; }
.mb-10 { margin-bottom: 10px; }

/* ─── Mobile ─── */
.mobile-menu-btn {
  display: none;
  position: fixed;
  top: 16px;
  left: 16px;
  z-index: 200;
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 8px;
  background: var(--gray-900);
  cursor: pointer;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 5px;
}

.mobile-menu-btn span {
  display: block;
  width: 20px;
  height: 2px;
  background: #fff;
  border-radius: 2px;
}

.sidebar-overlay {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.4);
  z-index: 90;
}

@media (max-width: 768px) {
  .mobile-menu-btn { display: flex; }
  .sidebar-overlay { display: block; }

  .sidebar {
    position: fixed;
    left: 0;
    top: 0;
    transform: translateX(-100%);
    transition: transform 0.25s ease;
  }

  .sidebar.open {
    transform: translateX(0);
  }

  .content {
    padding: 24px 16px;
    padding-top: 64px;
  }
}
</style>
