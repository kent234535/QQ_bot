import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 15000,
})

// ── Settings ──
export const getSettings = () => api.get('/settings')
export const updateSettings = (data: Record<string, unknown>) => api.put('/settings', data)

// ── Providers ──
export const listProviders = () => api.get('/providers')
export const createProvider = (data: Record<string, unknown>) => api.post('/providers', data)
export const updateProvider = (id: string, data: Record<string, unknown>) => api.put(`/providers/${id}`, data)
export const deleteProvider = (id: string) => api.delete(`/providers/${id}`)
export const testProviderModel = (id: string, data?: Record<string, unknown>) =>
  api.post(`/providers/${id}/test`, data || null, { timeout: 20000 })

// ── Personas ──
export const listPersonas = () => api.get('/personas')
export const createPersona = (data: Record<string, unknown>) => api.post('/personas', data)
export const updatePersona = (id: string, data: Record<string, unknown>) => api.put(`/personas/${id}`, data)
export const deletePersona = (id: string) => api.delete(`/personas/${id}`)

// ── NapCat ──
export const getNapCatStatus = () => api.get('/napcat/status')
export const connectNapCat = () => api.post('/napcat/connect', null, { timeout: 90000 })
export const disconnectNapCat = () => api.post('/napcat/disconnect', null, { timeout: 30000 })
export const setNapCatApp = (exe: string) => api.post('/napcat/set-app', { exe })
export const getNapCatQRCode = () => api.get('/napcat/qrcode')
