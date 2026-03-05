<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getSettings, updateSettings } from '@/api/client'

const form = ref({
  max_interactions: 20,
  max_tokens: 2000,
  temperature: 0.8,
  timeout: 20,
  cooldown_seconds: 5,
  max_context_messages: 20,
})
const msg = ref('')
const msgOk = ref(true)

async function load() {
  const { data } = await getSettings()
  form.value = {
    max_interactions: data.max_interactions,
    max_tokens: data.max_tokens,
    temperature: data.temperature,
    timeout: data.timeout,
    cooldown_seconds: data.cooldown_seconds,
    max_context_messages: data.max_context_messages,
  }
}

async function save() {
  try {
    await updateSettings(form.value)
    msg.value = '保存成功'
    msgOk.value = true
    setTimeout(() => msg.value = '', 2000)
  } catch {
    msg.value = '保存失败'
    msgOk.value = false
  }
}

onMounted(load)
</script>

<template>
  <div>
    <h1>设置</h1>
    <div class="card">
      <div class="settings-grid">
        <div class="form-group">
          <label>每用户最大交互次数</label>
          <input type="number" v-model.number="form.max_interactions" min="1" />
        </div>
        <div class="form-group">
          <label>单次最大 Token 数</label>
          <input type="number" v-model.number="form.max_tokens" min="100" max="16384" />
        </div>
        <div class="form-group">
          <label>
            生成温度 (0-2)
            <span class="label-hint">温度越大，回答随机性越高</span>
          </label>
          <input type="number" v-model.number="form.temperature" min="0" max="2" step="0.1" />
        </div>
        <div class="form-group">
          <label>API 超时（秒）</label>
          <input type="number" v-model.number="form.timeout" min="10" />
        </div>
        <div class="form-group">
          <label>
            消息冷却时间（秒）
            <span class="label-hint">0 = 不限制</span>
          </label>
          <input type="number" v-model.number="form.cooldown_seconds" min="0" />
        </div>
        <div class="form-group">
          <label>最大上下文消息数</label>
          <input type="number" v-model.number="form.max_context_messages" min="2" />
        </div>
      </div>
      <div class="save-row">
        <button class="btn btn-primary" @click="save">保存设置</button>
        <span v-if="msg" class="save-msg" :class="msgOk ? 'msg-ok' : 'msg-fail'">{{ msg }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.settings-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4px 20px;
}
.label-hint {
  font-weight: 400;
  color: var(--gray-400);
  font-size: 0.88em;
  margin-left: 4px;
}
.save-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding-top: 4px;
}
.save-msg {
  font-weight: 600;
  font-size: 0.9em;
}
.msg-ok { color: var(--success); }
.msg-fail { color: var(--danger); }
@media (max-width: 768px) {
  .settings-grid {
    grid-template-columns: 1fr;
  }
}
</style>
