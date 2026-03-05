<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { getNapCatStatus, connectNapCat, disconnectNapCat, setNapCatApp, getNapCatQRCode } from '@/api/client'

const status = ref<any>(null)
const qrcode = ref<any>(null)
const loading = ref(false)
const msg = ref('')
let pollTimer: ReturnType<typeof setInterval> | null = null

const connected = computed(() => status.value?.connected === true)
const webuiReady = computed(() => status.value?.webui_reachable === true)
const apps = computed(() => status.value?.apps || [])
const activeExe = computed(() => status.value?.active_exe || '')
const napcatInstalled = computed(() => status.value?.napcat_installed !== false)

async function fetchStatus() {
  try {
    const { data } = await getNapCatStatus()
    status.value = data
  } catch {
    // 网络瞬断不清空状态
  }
}

async function doConnect() {
  loading.value = true
  msg.value = '正在连接，请稍候...'
  qrcode.value = null
  try {
    const { data } = await connectNapCat()
    if (data.qrcode_image_api || data.qrcode_url) {
      qrcode.value = data
      msg.value = data.message || '请使用手机 QQ 扫码登录'
    } else if (data.is_login) {
      msg.value = 'QQ 已连接并登录'
    } else {
      msg.value = data.message || (data.ok ? '连接成功' : '连接失败')
    }
    await fetchStatus()
  } catch {
    msg.value = '连接请求失败，请检查网络'
  }
  loading.value = false
}

async function doDisconnect() {
  loading.value = true
  msg.value = '正在断开...'
  qrcode.value = null
  try {
    const { data } = await disconnectNapCat()
    msg.value = data.message || '已断开'
    await fetchStatus()
  } catch {
    msg.value = '断开请求失败'
  }
  loading.value = false
}

async function doRefreshQR() {
  loading.value = true
  try {
    const { data } = await getNapCatQRCode()
    if (data.is_login) {
      qrcode.value = null
      msg.value = 'QQ 已登录'
      await fetchStatus()
    } else {
      qrcode.value = data
      msg.value = data.message || ''
    }
  } catch {
    msg.value = '获取二维码失败'
  }
  loading.value = false
}

async function doSwitchApp(exe: string) {
  if (exe === activeExe.value) return
  loading.value = true
  qrcode.value = null
  msg.value = ''
  try {
    const { data } = await setNapCatApp(exe)
    msg.value = data.message || ''
    await fetchStatus()
  } catch {
    msg.value = '切换失败'
  }
  loading.value = false
}

onMounted(() => {
  fetchStatus()
  pollTimer = setInterval(fetchStatus, 5000)
})

onUnmounted(() => {
  if (pollTimer) clearInterval(pollTimer)
})
</script>

<template>
  <div>
    <h1>连接管理</h1>

    <!-- 状态卡片 -->
    <div class="card">
      <div class="flex-between">
        <div class="status-row">
          <div class="status-dot" :class="connected ? 'dot-green' : 'dot-red'"></div>
          <strong>{{ connected ? '已连接' : '未连接' }}</strong>
        </div>
        <div class="flex gap-8">
          <button v-if="!connected" class="btn btn-success" :disabled="loading || !napcatInstalled" @click="doConnect">
            连接
          </button>
          <button v-if="webuiReady || connected" class="btn btn-danger" :disabled="loading" @click="doDisconnect">
            断开
          </button>
        </div>
      </div>

      <div v-if="!napcatInstalled" class="hint hint-danger">
        未检测到 NapCat，请先安装 NapCat
      </div>

      <!-- QQ 应用选择 -->
      <div v-if="apps.length > 1" class="app-selector">
        <label>QQ 应用</label>
        <div class="app-btns">
          <button v-for="app in apps" :key="app.exe"
            class="btn btn-sm"
            :class="app.exe === activeExe ? 'btn-primary' : 'btn-outline'"
            :disabled="loading"
            :title="app.exe"
            @click="doSwitchApp(app.exe)">
            {{ app.name }}
          </button>
        </div>
      </div>

      <div v-if="msg" class="msg-text">{{ msg }}</div>
    </div>

    <!-- 二维码卡片 -->
    <div v-if="qrcode && !qrcode.is_login" class="card qr-card">
      <div class="flex-between">
        <strong>扫码登录</strong>
        <button class="btn btn-primary btn-sm" :disabled="loading" @click="doRefreshQR">
          刷新二维码
        </button>
      </div>
      <div v-if="qrcode.message && !qrcode.qrcode_image_api" class="hint"
        :class="qrcode.ok === false ? 'hint-danger' : ''">
        {{ qrcode.message }}
      </div>
      <div v-if="qrcode.qrcode_image_api" class="qr-wrapper">
        <img :src="qrcode.qrcode_image_api" alt="QQ 登录二维码" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.status-row {
  display: flex;
  align-items: center;
  gap: 10px;
}
.status-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}
.dot-green {
  background: var(--success);
  box-shadow: 0 0 0 3px rgba(42, 157, 143, 0.2);
}
.dot-red {
  background: var(--danger);
  box-shadow: 0 0 0 3px rgba(230, 57, 70, 0.15);
}
.hint {
  margin-top: 10px;
  font-size: 0.85em;
  color: var(--gray-500);
  padding: 8px 12px;
  border-radius: var(--radius-sm);
  background: var(--gray-50);
}
.hint-danger {
  color: var(--danger);
  background: var(--danger-light);
}
.app-selector {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid var(--gray-200);
}
.app-selector label {
  font-size: 0.8em;
  color: var(--gray-500);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 600;
}
.app-btns {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-top: 8px;
}
.msg-text {
  margin-top: 12px;
  color: var(--gray-500);
  white-space: pre-line;
  font-size: 0.9em;
  line-height: 1.6;
}
.qr-card {
  text-align: center;
}
.qr-wrapper {
  margin-top: 16px;
  display: inline-block;
  padding: 12px;
  background: #fff;
  border: 1px solid var(--gray-200);
  border-radius: var(--radius);
}
.qr-wrapper img {
  width: 200px;
  height: 200px;
  display: block;
  border-radius: var(--radius-sm);
}
</style>
