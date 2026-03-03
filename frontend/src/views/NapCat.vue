<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { getNapCatStatus, startNapCat, stopNapCat, getNapCatQRCode } from '@/api/client'

const status = ref<any>(null)
const qrcode = ref<any>(null)
const loading = ref(false)
const msg = ref('')
let pollTimer: ReturnType<typeof setInterval> | null = null

async function fetchStatus() {
  try {
    const { data } = await getNapCatStatus()
    status.value = data
  } catch {
    status.value = null
  }
}

async function doStart() {
  loading.value = true
  msg.value = '正在启动消息代理服务（关闭旧 QQ → 切换模式 → 启动），请稍候...'
  try {
    const { data } = await startNapCat()
    msg.value = data.message || (data.ok ? '启动成功' : '启动失败')
    await fetchStatus()
  } catch {
    msg.value = '启动请求失败'
  }
  loading.value = false
}

async function doStop() {
  loading.value = true
  try {
    const { data } = await stopNapCat()
    msg.value = data.message || '已停止'
    qrcode.value = null
    await fetchStatus()
  } catch {
    msg.value = '停止请求失败'
  }
  loading.value = false
}

async function fetchQRCode() {
  try {
    const { data } = await getNapCatQRCode()
    qrcode.value = data
  } catch {
    qrcode.value = { ok: false, message: '获取二维码失败' }
  }
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

    <div class="card">
      <div class="flex-between">
        <div>
          <strong>连接状态</strong>
          <span v-if="status" class="badge" :class="status.qq_login === true ? 'badge-green' : status.webui_reachable ? 'badge-green' : status.qq_running ? 'badge-gray' : 'badge-red'" style="margin-left: 8px;">
            {{ status.qq_login === true ? 'QQ 已登录' : status.webui_reachable ? '等待登录 QQ' : status.qq_running ? 'QQ 已启动，WebUI 未就绪' : '未启动' }}
          </span>
        </div>
        <button class="btn btn-primary btn-sm" @click="fetchStatus">刷新</button>
      </div>

      <div v-if="status" style="margin-top: 8px; font-size: 0.85em; color: #666;">
        <div>NapCat 模式:
          <span :style="{ color: status.napcat_mode ? '#2a9d8f' : '#e63946', fontWeight: 600 }">
            {{ status.napcat_mode ? '已启用' : '未启用' }}
          </span>
        </div>
        <div>WebUI:
          <span :style="{ color: status.webui_reachable ? '#2a9d8f' : '#e63946' }">
            {{ status.webui_reachable ? '已连接' : '未连接' }}
          </span>
        </div>
        <div>QQ 登录:
          <span :style="{ color: status.qq_login === true ? '#2a9d8f' : '#e63946', fontWeight: 600 }">
            {{ status.qq_login === true ? '已登录' : '未登录' }}
          </span>
        </div>
        <div v-if="status.login_error">登录提示: {{ status.login_error }}</div>
      </div>
    </div>

    <div class="card">
      <strong>操作</strong>
      <div style="margin-top: 8px; font-size: 0.85em; color: #888;">
        第一步：启动 QQ 消息代理 → 第二步：登录 QQ（扫码）
      </div>
      <div class="flex gap-8 mt-10">
        <button class="btn btn-success" @click="doStart" :disabled="loading">启动 QQ 消息代理</button>
        <button class="btn btn-primary" @click="fetchQRCode" :disabled="loading || !status || !status.webui_reachable">登录 QQ</button>
        <button class="btn btn-danger" @click="doStop" :disabled="loading">停止</button>
      </div>
      <div v-if="msg" style="margin-top: 10px; color: #555;">{{ msg }}</div>
    </div>

    <div v-if="qrcode" class="card">
      <strong>登录二维码</strong>
      <div v-if="qrcode.is_login" style="margin-top: 8px; color: #2a9d8f; font-weight: 600;">
        QQ 已登录，无需二维码
      </div>
      <div v-else>
        <div v-if="qrcode.message && !qrcode.qrcode_image_api" style="margin-top: 8px;" :style="{ color: qrcode.ok === false ? '#e63946' : '#555' }">
          {{ qrcode.message }}
        </div>
        <div v-if="qrcode.qrcode_image_api" style="margin-top: 10px;">
          <img
            :src="qrcode.qrcode_image_api"
            alt="QQ 登录二维码"
            style="width: 220px; height: 220px; border: 1px solid #ddd; border-radius: 8px; background: #fff;"
          />
          <div style="margin-top: 8px; color: #666; font-size: 0.85em;">
            请使用手机 QQ 扫码登录，登录后状态会自动刷新
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
