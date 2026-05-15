const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

// Basic fetch function
export const fetchAPI = async (endpoint: string, options?: RequestInit) => {
  const response = await fetch(`${API_URL}${endpoint}`, options);
  if (!response.ok) throw new Error('Network response was not ok');
  return response.json();
};

// Old API functions (for backward compatibility)
export const healthCheck = async () => fetchAPI('/health');
export const getProjects = async () => fetchAPI('/projects');
export const createProject = async (data: any) => fetchAPI('/projects', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) });
export const getProject = async (id: string) => fetchAPI(`/projects/${id}`);
export const getJobs = async (projectId: string) => fetchAPI(`/projects/${projectId}/jobs`);
export const startResearch = async (projectId: string) => fetchAPI(`/projects/${projectId}/jobs/research`, { method: 'POST' });
export const startPlan = async (projectId: string) => fetchAPI(`/projects/${projectId}/jobs/plan`, { method: 'POST' });
export const startGeneration = async (projectId: string) => fetchAPI(`/projects/${projectId}/jobs/generation`, { method: 'POST' });
export const startPromotion = async (projectId: string) => fetchAPI(`/projects/${projectId}/jobs/promotion`, { method: 'POST' });
export const startSales = async (projectId: string) => fetchAPI(`/projects/${projectId}/jobs/sales`, { method: 'POST' });
export const getDownloadToken = async (jobId: string) => fetchAPI(`/jobs/${jobId}/download`);
