<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { listProviders, createProvider, updateProvider, deleteProvider, testProviderModel, getSettings, updateSettings } from '@/api/client'

const providers = ref<any[]>([])
const activeProviderId = ref('')
const showForm = ref(false)
const form = ref({
  name: '',
  type: 'openai_compat',
  base_url: '',
  api_key: '',
  model: '',
  enabled: true,
})

const editingId = ref('')
const editForm = ref({
  name: '',
  type: 'openai_compat',
  base_url: '',
  api_key: '',
  model: '',
})
const savingEdit = ref(false)

const testingId = ref('')
const testResult = ref<{ ok: boolean; msg: string } | null>(null)

async function load() {
  const [p, s] = await Promise.all([listProviders(), getSettings()])
  providers.value = p.data
  activeProviderId.value = s.data.active_provider_id || ''
}

function resetForm() {
  form.value = { name: '', type: 'openai_compat', base_url: '', api_key: '', model: '', enabled: true }
}

async function save() {
  if (!form.value.name) return
  await createProvider(form.value)
  showForm.value = false
  resetForm()
  await load()
}

async function remove(id: string) {
  if (!confirm('确认删除该模型？')) return
  await deleteProvider(id)
  if (activeProviderId.value === id) {
    await updateSettings({ active_provider_id: '' })
  }
  await load()
}

async function activate(id: string) {
  await updateSettings({ active_provider_id: id })
  activeProviderId.value = id
}

async function startEdit(p: any) {
  editingId.value = p.id
  editForm.value = {
    name: p.name,
    type: p.type,
    base_url: p.base_url || '',
    api_key: '',
    model: p.model || '',
  }
  testResult.value = null
  testingId.value = ''
}

function cancelEdit() {
  editingId.value = ''
}

async function saveEditForm(id: string) {
  if (!editForm.value.name) return
  savingEdit.value = true
  try {
    await updateProvider(id, editForm.value)
    cancelEdit()
    await load()
  } finally {
    savingEdit.value = false
  }
}

async function testModel(id: string) {
  testingId.value = id
  testResult.value = null
  try {
    await testProviderModel(id, {
      type: editForm.value.type,
      base_url: editForm.value.base_url,
      api_key: editForm.value.api_key,
      model: editForm.value.model,
    })
    testResult.value = { ok: true, msg: '模型可用' }
  } catch (e: any) {
    testResult.value = { ok: false, msg: e.response?.data?.detail || '检测失败' }
  }
}

const sortedProviders = computed(() =>
  [...providers.value].sort((a, b) => (a.id === activeProviderId.value ? -1 : b.id === activeProviderId.value ? 1 : 0))
)

onMounted(load)
</script>

<template>
  <div>
    <div class="flex-between mb-10">
      <h1>模型</h1>
      <button class="btn btn-primary" @click="showForm = !showForm">
        {{ showForm ? '取消' : '+ 添加模型' }}
      </button>
    </div>

    <!-- 添加表单 -->
    <div v-if="showForm" class="card form-card">
      <div class="form-group">
        <label>名称</label>
        <input v-model="form.name" placeholder="如 DeepSeek" />
      </div>
      <div class="form-row">
        <div class="form-group" style="flex: 1;">
          <label>类型</label>
          <select v-model="form.type">
            <option value="openai_compat">OpenAI 兼容</option>
            <option value="claude">Anthropic Claude</option>
          </select>
        </div>
        <div class="form-group" style="flex: 2;">
          <label>Base URL</label>
          <input v-model="form.base_url" placeholder="https://api.deepseek.com/v1" />
        </div>
      </div>
      <div class="form-row">
        <div class="form-group" style="flex: 1;">
          <label>API Key</label>
          <input v-model="form.api_key" type="password" placeholder="sk-..." />
        </div>
        <div class="form-group" style="flex: 1;">
          <label>模型</label>
          <input v-model="form.model" placeholder="如 deepseek-chat" />
        </div>
      </div>
      <div class="form-hint">请查阅 API 提供方的官方文档查看可用模型名称</div>
      <button class="btn btn-success" @click="save">保存</button>
    </div>

    <!-- 模型卡片列表 -->
    <div v-for="p in sortedProviders" :key="p.id" class="card provider-card"
      :class="{ 'card-active': activeProviderId === p.id }">
      <div class="flex-between">
        <div class="provider-info">
          <strong>{{ p.name }}</strong>
          <span v-if="activeProviderId === p.id" class="badge badge-green">当前启用</span>
          <span class="badge badge-gray">{{ p.type === 'claude' ? 'Claude' : 'OpenAI' }}</span>
        </div>
        <div class="btn-group">
          <button v-if="activeProviderId !== p.id" class="btn btn-success btn-sm" @click="activate(p.id)">启用</button>
          <button class="btn btn-primary btn-sm" @click="startEdit(p)">编辑</button>
          <button class="btn btn-danger btn-sm" @click="remove(p.id)">删除</button>
        </div>
      </div>
      <div class="provider-meta">
        <span>模型: {{ p.model || '未设置' }}</span>
        <span>API Key: {{ p.api_key || '未设置' }}</span>
      </div>

      <!-- 编辑面板 -->
      <div v-if="editingId === p.id" class="edit-panel">
        <div class="form-group">
          <label>名称</label>
          <input v-model="editForm.name" />
        </div>
        <div class="form-row">
          <div class="form-group" style="flex: 1;">
            <label>类型</label>
            <select v-model="editForm.type">
              <option value="openai_compat">OpenAI 兼容</option>
              <option value="claude">Anthropic Claude</option>
            </select>
          </div>
          <div class="form-group" style="flex: 2;">
            <label>Base URL</label>
            <input v-model="editForm.base_url" />
          </div>
        </div>
        <div class="form-group">
          <label>API Key</label>
          <input v-model="editForm.api_key" type="password" placeholder="留空则不修改" />
        </div>
        <div class="form-group">
          <label>模型</label>
          <div class="model-row">
            <input v-model="editForm.model" placeholder="如 deepseek-chat" />
            <button class="btn btn-primary btn-sm" :disabled="testingId === p.id && !testResult" @click="testModel(p.id)">
              {{ testingId === p.id && !testResult ? '检测中...' : '检测可用性' }}
            </button>
          </div>
          <div v-if="testingId === p.id && testResult" class="test-result"
            :class="testResult.ok ? 'test-ok' : 'test-fail'">
            {{ testResult.msg }}
          </div>
        </div>
        <div class="btn-group">
          <button class="btn btn-success btn-sm" :disabled="savingEdit" @click="saveEditForm(p.id)">保存修改</button>
          <button class="btn btn-outline btn-sm" :disabled="savingEdit" @click="cancelEdit">取消</button>
        </div>
      </div>
    </div>

    <div v-if="!providers.length" class="card empty-card">
      暂无模型，点击上方按钮添加
    </div>
  </div>
</template>

<style scoped>
.form-card {
  border: 1px dashed var(--primary);
  background: var(--primary-light);
}
.form-row {
  display: flex;
  gap: 12px;
}
.form-hint {
  font-size: 0.8em;
  color: var(--gray-400);
  margin-bottom: 14px;
}
.provider-card.card-active {
  border-color: var(--success);
  border-width: 2px;
}
.provider-info {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}
.btn-group {
  display: flex;
  gap: 6px;
}
.provider-meta {
  margin-top: 10px;
  font-size: 0.83em;
  color: var(--gray-500);
  display: flex;
  gap: 16px;
}
.edit-panel {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid var(--gray-200);
}
.model-row {
  display: flex;
  gap: 8px;
}
.model-row input { flex: 1; }
.test-result {
  margin-top: 6px;
  font-size: 0.83em;
  font-weight: 600;
}
.test-ok { color: var(--success); }
.test-fail { color: var(--danger); }
.empty-card {
  color: var(--gray-400);
  text-align: center;
  padding: 40px;
}
@media (max-width: 768px) {
  .form-row { flex-direction: column; gap: 0; }
}
</style>
