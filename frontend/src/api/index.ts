import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

// Response interceptor
api.interceptors.response.use(
  response => response.data,
  error => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

// ==================== Monitor APIs ====================
export const getOverview = () => api.get('/metrics/overview')
export const getNodes = () => api.get('/metrics/nodes')
export const getPods = (namespace?: string) => api.get('/metrics/pods', { params: { namespace } })
export const getServices = (namespace?: string) => api.get('/metrics/services', { params: { namespace } })
export const getNamespaces = () => api.get('/metrics/namespaces')
export const getDeployments = (namespace?: string) => api.get('/metrics/deployments', { params: { namespace } })

// ==================== Alert APIs ====================
export const getAlertRules = () => api.get('/alerts/rules')
export const createAlertRule = (data: any) => api.post('/alerts/rules', data)
export const updateAlertRule = (id: number, data: any) => api.put(`/alerts/rules/${id}`, data)
export const deleteAlertRule = (id: number) => api.delete(`/alerts/rules/${id}`)

export const getAlerts = (status?: string) => api.get('/alerts', { params: { status } })
export const acknowledgeAlert = (id: number, data: any) => api.post(`/alerts/${id}/acknowledge`, data)

// ==================== Task APIs ====================
export const getTasks = () => api.get('/tasks')
export const createTask = (data: any) => api.post('/tasks', data)
export const updateTask = (id: number, data: any) => api.put(`/tasks/${id}`, data)
export const deleteTask = (id: number) => api.delete(`/tasks/${id}`)
export const runTask = (id: number) => api.post(`/tasks/${id}/run`)
export const getTaskRuns = (id: number) => api.get(`/tasks/${id}/runs`)

// ==================== Knowledge APIs ====================
export const getArticles = (categoryId?: number) => api.get('/knowledge/articles', { params: { category_id: categoryId } })
export const createArticle = (data: any) => api.post('/knowledge/articles', data)
export const getCases = (category?: string) => api.get('/knowledge/cases', { params: { category } })
export const createCase = (data: any) => api.post('/knowledge/cases', data)
export const getCategories = () => api.get('/knowledge/categories')

// ==================== Chat APIs ====================
export const chat = (message: string, sessionId: string = 'web:direct') =>
  api.post('/chat', { message, session_id: sessionId })

export const diagnose = (data: any) => api.post('/diagnose', data)

export default api
