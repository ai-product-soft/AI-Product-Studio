import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const healthCheck = () => api.get('/health')

export const getProjects = () => api.get('/projects')
export const getProject = (id: number) => api.get(`/projects/${id}`)
export const createProject = (data: { name: string; client_idea: string }) => api.post('/projects', data)
export const updateProject = (id: number, data: any) => api.patch(`/projects/${id}`, data)
export const deleteProject = (id: number) => api.delete(`/projects/${id}`)

export const startResearch = (id: number) => api.post(`/projects/${id}/research`)
export const startPlan = (id: number) => api.post(`/projects/${id}/plan`)
export const startGeneration = (id: number) => api.post(`/projects/${id}/generate`)
export const startPromotion = (id: number) => api.post(`/projects/${id}/promote`)
export const startSales = (id: number) => api.post(`/projects/${id}/sales`)

export const getJobs = (projectId: number) => api.get(`/jobs/project/${projectId}`)
export const getJob = (id: number) => api.get(`/jobs/${id}`)

export const getDownloadToken = (projectId: number) => api.get(`/download/token/${projectId}`)

export default api
