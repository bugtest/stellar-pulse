import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response.data
  },
  error => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

// ==================== Monitor APIs ====================
export const getOverview = (): Promise<any> => api.get('/metrics/overview')
export const getNodes = (): Promise<any> => api.get('/metrics/nodes')
export const getPods = (namespace?: string): Promise<any> => api.get('/metrics/pods', { params: { namespace } })
export const getServices = (namespace?: string): Promise<any> => api.get('/metrics/services', { params: { namespace } })
export const getNamespaces = (): Promise<any> => api.get('/metrics/namespaces')
export const getDeployments = (namespace?: string): Promise<any> => api.get('/metrics/deployments', { params: { namespace } })

// ==================== Alert APIs ====================
export const getAlertRules = (): Promise<any> => api.get('/alerts/rules')
export const createAlertRule = (data: any): Promise<any> => api.post('/alerts/rules', data)
export const updateAlertRule = (id: number, data: any): Promise<any> => api.put(`/alerts/rules/${id}`, data)
export const deleteAlertRule = (id: number): Promise<any> => api.delete(`/alerts/rules/${id}`)

export const getAlerts = (status?: string): Promise<any> => api.get('/alerts', { params: { status } })
export const acknowledgeAlert = (id: number, data: any): Promise<any> => api.post(`/alerts/${id}/acknowledge`, data)

// ==================== Task APIs ====================
export const getTasks = (): Promise<any> => api.get('/tasks')
export const createTask = (data: any): Promise<any> => api.post('/tasks', data)
export const updateTask = (id: number, data: any): Promise<any> => api.put(`/tasks/${id}`, data)
export const deleteTask = (id: number): Promise<any> => api.delete(`/tasks/${id}`)
export const runTask = (id: number): Promise<any> => api.post(`/tasks/${id}/run`)
export const getTaskRuns = (id: number): Promise<any> => api.get(`/tasks/${id}/runs`)

// ==================== Knowledge APIs ====================
export const getArticles = (categoryId?: number): Promise<any> => api.get('/knowledge/articles', { params: { category_id: categoryId } })
export const createArticle = (data: any): Promise<any> => api.post('/knowledge/articles', data)
export const getCases = (category?: string): Promise<any> => api.get('/knowledge/cases', { params: { category } })
export const createCase = (data: any): Promise<any> => api.post('/knowledge/cases', data)
export const getCategories = (): Promise<any> => api.get('/knowledge/categories')

// ==================== Chat APIs ====================
export const chat = (message: string, sessionId: string = 'web:direct'): Promise<any> =>
  api.post('/chat', { message, session_id: sessionId })

export const diagnose = (data: any): Promise<any> => api.post('/diagnose', data)

export default api
