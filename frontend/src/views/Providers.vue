<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { listProviders, createProvider, updateProvider, deleteProvider, listAvailableModels, getSettings, updateSettings } from '@/api/client'

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

// 添加表单：可用模型
const availableModels = ref<string[]>([])
const modelsLoading = ref(false)
const modelsError = ref('')

// 编辑表单
const editingId = ref('')
const editForm = ref({
  name: '',
  type: 'openai_compat',
  base_url: '',
  api_key: '',
  model: '',
})
const savingEdit = ref(false)
const editModels = ref<string[]>([])
const editModelsLoading = ref(false)
const editModelsError = ref('')

async function load() {
  const [p, s] = await Promise.all([listProviders(), getSettings()])
  providers.value = p.data
  activeProviderId.value = s.data.active_provider_id || ''
}

function resetForm() {
  form.value = { name: '', type: 'openai_compat', base_url: '', api_key: '', model: '', enabled: true }
  availableModels.value = []
  modelsError.value = ''
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

async function fetchModels() {
  modelsError.value = ''
  availableModels.value = []
  if (!form.value.base_url || !form.value.api_key) {
    modelsError.value = '请先填写 Base URL 和 API Key'
    return
  }
  modelsLoading.value = true
  try {
    const { data } = await listAvailableModels({
      type: form.value.type,
      base_url: form.value.base_url,
      api_key: form.value.api_key,
    })
    availableModels.value = data.models || []
    if (!availableModels.value.length) modelsError.value = '未找到可用模型'
  } catch (e: any) {
    modelsError.value = e.response?.data?.detail || '获取模型列表失败'
  }
  modelsLoading.value = false
}

function selectModel(model: string) {
  form.value.model = model
  availableModels.value = []
}

function startEdit(p: any) {
  editingId.value = p.id
  editForm.value = {
    name: p.name,
    type: p.type,
    base_url: p.base_url || '',
    api_key: '',
    model: p.model || '',
  }
  editModels.value = []
  editModelsError.value = ''
}

function cancelEdit() {
  editingId.value = ''
  editModels.value = []
  editModelsError.value = ''
}

async function fetchEditModels(p: any) {
  editModelsError.value = ''
  editModels.value = []
  const baseUrl = editForm.value.base_url || p.base_url
  const apiKey = editForm.value.api_key
  if (!baseUrl) {
    editModelsError.value = '请先填写 Base URL'
    return
  }
  // 编辑时 api_key 留空表示不修改，需要用已有的 key 来查询
  // 但已有 key 是掩码的，所以必须填新 key 才能查询
  if (!apiKey) {
    editModelsError.value = '请先填写 API Key 以查询模型列表'
    return
  }
  editModelsLoading.value = true
  try {
    const { data } = await listAvailableModels({
      type: editForm.value.type,
      base_url: baseUrl,
      api_key: apiKey,
    })
    editModels.value = data.models || []
    if (!editModels.value.length) editModelsError.value = '未找到可用模型'
  } catch (e: any) {
    editModelsError.value = e.response?.data?.detail || '获取模型列表失败'
  }
  editModelsLoading.value = false
}

function selectEditModel(model: string) {
  editForm.value.model = model
  editModels.value = []
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

    <div v-if="showForm" class="card">
      <div class="form-group">
        <label>名称</label>
        <input v-model="form.name" placeholder="如 DeepSeek" />
      </div>
      <div class="form-group">
        <label>类型</label>
        <select v-model="form.type">
          <option value="openai_compat">OpenAI 兼容</option>
          <option value="claude">Anthropic Claude</option>
        </select>
      </div>
      <div class="form-group">
        <label>Base URL</label>
        <input v-model="form.base_url" placeholder="https://api.deepseek.com/v1" />
      </div>
      <div class="form-group">
        <label>API Key</label>
        <input v-model="form.api_key" type="password" placeholder="sk-..." />
      </div>
      <div class="form-group">
        <label>模型</label>
        <div style="display: flex; gap: 8px;">
          <input v-model="form.model" placeholder="点击右侧按钮选择或手动输入" style="flex: 1;" />
          <button class="btn btn-primary btn-sm" :disabled="modelsLoading" @click="fetchModels">
            {{ modelsLoading ? '加载中...' : '显示可用模型' }}
          </button>
        </div>
        <div v-if="modelsError" style="color: #e63946; font-size: 0.85em; margin-top: 4px;">{{ modelsError }}</div>
        <div v-if="availableModels.length" style="margin-top: 8px; max-height: 200px; overflow-y: auto; border: 1px solid #ddd; border-radius: 6px;">
          <div
            v-for="m in availableModels" :key="m"
            style="padding: 6px 12px; cursor: pointer; font-size: 0.9em; border-bottom: 1px solid #f0f0f0;"
            :style="form.model === m ? 'background: #d4edda; font-weight: 600;' : ''"
            @click="selectModel(m)"
          >{{ m }}</div>
        </div>
      </div>
      <button class="btn btn-success" @click="save">保存</button>
    </div>

    <div v-for="p in providers" :key="p.id" class="card" :style="activeProviderId === p.id ? 'border: 2px solid #a8e6cf;' : ''">
      <div class="flex-between">
        <div>
          <strong>{{ p.name }}</strong>
          <span v-if="activeProviderId === p.id" class="badge badge-green" style="margin-left: 8px;">当前启用</span>
          <span class="badge badge-gray" style="margin-left: 4px;">{{ p.type }}</span>
        </div>
        <div style="display: flex; gap: 8px;">
          <button v-if="activeProviderId !== p.id" class="btn btn-success btn-sm" @click="activate(p.id)">启用</button>
          <button class="btn btn-primary btn-sm" @click="startEdit(p)">编辑</button>
          <button class="btn btn-danger btn-sm" @click="remove(p.id)">删除</button>
        </div>
      </div>
      <div style="margin-top: 8px; font-size: 0.85em; color: #666;">
        模型: {{ p.model || '未设置' }} &nbsp;|&nbsp;
        API Key: {{ p.api_key || '未设置' }}
      </div>

      <div v-if="editingId === p.id" style="margin-top: 12px; border-top: 1px dashed #ddd; padding-top: 10px;">
        <div class="form-group">
          <label>名称</label>
          <input v-model="editForm.name" />
        </div>
        <div class="form-group">
          <label>类型</label>
          <select v-model="editForm.type">
            <option value="openai_compat">OpenAI 兼容</option>
            <option value="claude">Anthropic Claude</option>
          </select>
        </div>
        <div class="form-group">
          <label>Base URL</label>
          <input v-model="editForm.base_url" />
        </div>
        <div class="form-group">
          <label>API Key（留空表示不修改）</label>
          <input v-model="editForm.api_key" type="password" placeholder="输入新 key" />
        </div>
        <div class="form-group">
          <label>模型</label>
          <div style="display: flex; gap: 8px;">
            <input v-model="editForm.model" placeholder="手动输入或点击右侧选择" style="flex: 1;" />
            <button class="btn btn-primary btn-sm" :disabled="editModelsLoading" @click="fetchEditModels(p)">
              {{ editModelsLoading ? '加载中...' : '显示可用模型' }}
            </button>
          </div>
          <div v-if="editModelsError" style="color: #e63946; font-size: 0.85em; margin-top: 4px;">{{ editModelsError }}</div>
          <div v-if="editModels.length" style="margin-top: 8px; max-height: 200px; overflow-y: auto; border: 1px solid #ddd; border-radius: 6px;">
            <div
              v-for="m in editModels" :key="m"
              style="padding: 6px 12px; cursor: pointer; font-size: 0.9em; border-bottom: 1px solid #f0f0f0;"
              :style="editForm.model === m ? 'background: #d4edda; font-weight: 600;' : ''"
              @click="selectEditModel(m)"
            >{{ m }}</div>
          </div>
        </div>
        <div style="display: flex; gap: 8px;">
          <button class="btn btn-success btn-sm" :disabled="savingEdit" @click="saveEditForm(p.id)">保存修改</button>
          <button class="btn btn-primary btn-sm" :disabled="savingEdit" @click="cancelEdit">取消</button>
        </div>
      </div>
    </div>

    <div v-if="!providers.length" class="card" style="color: #888; text-align: center;">
      暂无模型，点击上方按钮添加
    </div>
  </div>
</template>
