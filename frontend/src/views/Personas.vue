<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { listPersonas, createPersona, updatePersona, deletePersona, getSettings, updateSettings } from '@/api/client'

const personas = ref<any[]>([])
const activePersonaId = ref('')
const showForm = ref(false)
const form = ref({ name: '', system_prompt: '' })

const editingId = ref('')
const editForm = ref({ name: '', system_prompt: '' })

async function load() {
  const [pe, s] = await Promise.all([listPersonas(), getSettings()])
  personas.value = pe.data
  activePersonaId.value = s.data.active_persona_id || ''
}

function resetForm() {
  form.value = { name: '', system_prompt: '' }
}

async function save() {
  if (!form.value.name || !form.value.system_prompt) return
  await createPersona(form.value)
  showForm.value = false
  resetForm()
  await load()
}

async function remove(id: string) {
  if (!confirm('确认删除该角色？')) return
  try {
    await deletePersona(id)
  } catch (e: any) {
    alert(e.response?.data?.detail || '删除失败')
  }
  if (activePersonaId.value === id) {
    await updateSettings({ active_persona_id: '' })
  }
  await load()
}

async function activate(id: string) {
  await updateSettings({ active_persona_id: id })
  activePersonaId.value = id
}

function startEdit(p: any) {
  editingId.value = p.id
  editForm.value = { name: p.name, system_prompt: p.system_prompt }
}

function cancelEdit() {
  editingId.value = ''
}

async function saveEdit(id: string) {
  if (!editForm.value.name || !editForm.value.system_prompt) return
  await updatePersona(id, editForm.value)
  editingId.value = ''
  await load()
}

const sortedPersonas = computed(() =>
  [...personas.value].sort((a, b) => (a.id === activePersonaId.value ? -1 : b.id === activePersonaId.value ? 1 : 0))
)

onMounted(load)
</script>

<template>
  <div>
    <div class="flex-between mb-10">
      <h1>角色管理</h1>
      <button class="btn btn-primary" @click="showForm = !showForm">
        {{ showForm ? '取消' : '+ 添加角色' }}
      </button>
    </div>

    <!-- 添加表单 -->
    <div v-if="showForm" class="card form-card">
      <div class="form-group">
        <label>名称</label>
        <input v-model="form.name" placeholder="如 傲娇少女" />
      </div>
      <div class="form-group">
        <label>角色描述</label>
        <textarea v-model="form.system_prompt" placeholder="你是一个..." rows="4"></textarea>
      </div>
      <button class="btn btn-success" @click="save">保存</button>
    </div>

    <!-- 角色卡片列表 -->
    <div v-for="p in sortedPersonas" :key="p.id" class="card persona-card"
      :class="{ 'card-active': activePersonaId === p.id }">
      <div class="flex-between">
        <div class="persona-info">
          <strong>{{ p.name }}</strong>
          <span v-if="activePersonaId === p.id" class="badge badge-green">当前启用</span>
        </div>
        <div class="btn-group">
          <button v-if="activePersonaId !== p.id" class="btn btn-success btn-sm" @click="activate(p.id)">启用</button>
          <button class="btn btn-primary btn-sm" @click="startEdit(p)">编辑</button>
          <button class="btn btn-danger btn-sm" @click="remove(p.id)">删除</button>
        </div>
      </div>

      <!-- 编辑面板 -->
      <div v-if="editingId === p.id" class="edit-panel">
        <div class="form-group">
          <label>名称</label>
          <input v-model="editForm.name" />
        </div>
        <div class="form-group">
          <label>角色描述</label>
          <textarea v-model="editForm.system_prompt" rows="4"></textarea>
        </div>
        <div class="btn-group">
          <button class="btn btn-success btn-sm" @click="saveEdit(p.id)">保存修改</button>
          <button class="btn btn-outline btn-sm" @click="cancelEdit">取消</button>
        </div>
      </div>

      <!-- 预览 -->
      <div v-else class="prompt-preview">{{ p.system_prompt }}</div>
    </div>

    <div v-if="!personas.length" class="card empty-card">
      暂无角色，点击上方按钮添加
    </div>
  </div>
</template>

<style scoped>
.form-card {
  border: 1px dashed var(--primary);
  background: var(--primary-light);
}
.persona-card.card-active {
  border-color: var(--success);
  border-width: 2px;
}
.persona-info {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}
.btn-group {
  display: flex;
  gap: 6px;
}
.edit-panel {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid var(--gray-200);
}
.prompt-preview {
  margin-top: 10px;
  padding: 12px 14px;
  background: var(--gray-50);
  border-radius: var(--radius-sm);
  font-size: 0.85em;
  color: var(--gray-700);
  white-space: pre-wrap;
  line-height: 1.6;
  border: 1px solid var(--gray-200);
}
.empty-card {
  color: var(--gray-400);
  text-align: center;
  padding: 40px;
}
</style>
