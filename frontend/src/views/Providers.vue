<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { listProviders, createProvider, updateProviderModelKey, deleteProvider } from '@/api/client'

const providers = ref<any[]>([])
const showForm = ref(false)
const form = ref({
  id: '',
  name: '',
  type: 'openai_compat',
  base_url: '',
  api_key: '',
  model: '',
  enabled: true,
})
const editingId = ref('')
const editForm = ref({
  model: '',
  api_key: '',
})
const savingEdit = ref(false)

async function load() {
  const { data } = await listProviders()
  providers.value = data
}

function resetForm() {
  form.value = { id: '', name: '', type: 'openai_compat', base_url: '', api_key: '', model: '', enabled: true }
}

async function save() {
  if (!form.value.id || !form.value.name) return
  await createProvider(form.value)
  showForm.value = false
  resetForm()
  await load()
}

async function remove(id: string) {
  if (!confirm('确认删除该提供商？')) return
  await deleteProvider(id)
  await load()
}

function startEdit(provider: any) {
  editingId.value = provider.id
  editForm.value = {
    model: provider.model || '',
    api_key: '',
  }
}

function cancelEdit() {
  editingId.value = ''
  editForm.value = { model: '', api_key: '' }
}

async function saveModelAndKey(id: string) {
  savingEdit.value = true
  try {
    await updateProviderModelKey(id, {
      model: editForm.value.model,
      api_key: editForm.value.api_key,
    })
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
      <h1>AI 提供商</h1>
      <button class="btn btn-primary" @click="showForm = !showForm">
        {{ showForm ? '取消' : '+ 添加提供商' }}
      </button>
    </div>

    <div v-if="showForm" class="card">
      <div class="form-group">
        <label>ID（唯一标识）</label>
        <input v-model="form.id" placeholder="如 deepseek" />
      </div>
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
        <input v-model="form.model" placeholder="deepseek-chat" />
      </div>
      <button class="btn btn-success" @click="save">保存</button>
    </div>

    <div v-for="p in providers" :key="p.id" class="card">
      <div class="flex-between">
        <div>
          <strong>{{ p.name }}</strong>
          <span class="badge" :class="p.enabled ? 'badge-green' : 'badge-red'" style="margin-left: 8px;">
            {{ p.enabled ? '启用' : '禁用' }}
          </span>
          <span class="badge badge-gray" style="margin-left: 4px;">{{ p.type }}</span>
        </div>
        <div style="display: flex; gap: 8px;">
          <button class="btn btn-primary btn-sm" @click="startEdit(p)">编辑模型/API Key</button>
          <button class="btn btn-danger btn-sm" @click="remove(p.id)">删除</button>
        </div>
      </div>
      <div style="margin-top: 8px; font-size: 0.85em; color: #666;">
        模型: {{ p.model || '未设置' }} &nbsp;|&nbsp;
        API Key: {{ p.api_key || '未设置' }}
      </div>
      <div v-if="editingId === p.id" style="margin-top: 12px; border-top: 1px dashed #ddd; padding-top: 10px;">
        <div class="form-group">
          <label>模型</label>
          <input v-model="editForm.model" placeholder="如 deepseek-chat" />
        </div>
        <div class="form-group">
          <label>API Key（留空表示不修改）</label>
          <input v-model="editForm.api_key" type="password" placeholder="输入新 key" />
        </div>
        <div style="display: flex; gap: 8px;">
          <button class="btn btn-success btn-sm" :disabled="savingEdit" @click="saveModelAndKey(p.id)">保存修改</button>
          <button class="btn btn-primary btn-sm" :disabled="savingEdit" @click="cancelEdit">取消</button>
        </div>
      </div>
    </div>

    <div v-if="!providers.length" class="card" style="color: #888; text-align: center;">
      暂无提供商，点击上方按钮添加
    </div>
  </div>
</template>
