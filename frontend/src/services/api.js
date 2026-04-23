import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || '/api';

const api = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      const refresh = localStorage.getItem('refresh_token');
      if (refresh) {
        try {
          const res = await axios.post(`${API_BASE}/token/refresh/`, { refresh });
          localStorage.setItem('access_token', res.data.access);
          error.config.headers.Authorization = `Bearer ${res.data.access}`;
          return api.request(error.config);
        } catch {
          localStorage.clear();
          window.location.href = '/login';
        }
      }
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  login: (credentials) => api.post('/token/', credentials),
  refresh: (refresh) => api.post('/token/refresh/', { refresh }),
};

export const projectsAPI = {
  getClients: (params) => api.get('/projects/clients/', { params }),
  createClient: (data) => api.post('/projects/clients/', data),
  updateClient: (id, data) => api.put(`/projects/clients/${id}/`, data),
  deleteClient: (id) => api.delete(`/projects/clients/${id}/`),

  getProjects: (params) => api.get('/projects/projects/', { params }),
  getProject: (id) => api.get(`/projects/projects/${id}/`),
  createProject: (data) => api.post('/projects/projects/', data),
  updateProject: (id, data) => api.put(`/projects/projects/${id}/`, data),
  deleteProject: (id) => api.delete(`/projects/projects/${id}/`),
  getDashboardStats: () => api.get('/projects/projects/dashboard_stats/'),
  getProjectSummary: (id) => api.get(`/projects/projects/${id}/summary/`),

  getPhases: (params) => api.get('/projects/phases/', { params }),
  createPhase: (data) => api.post('/projects/phases/', data),
  updatePhase: (id, data) => api.put(`/projects/phases/${id}/`, data),
  deletePhase: (id) => api.delete(`/projects/phases/${id}/`),

  getTasks: (params) => api.get('/projects/tasks/', { params }),
  createTask: (data) => api.post('/projects/tasks/', data),
  updateTask: (id, data) => api.put(`/projects/tasks/${id}/`, data),
  deleteTask: (id) => api.delete(`/projects/tasks/${id}/`),

  getMilestones: (params) => api.get('/projects/milestones/', { params }),
  createMilestone: (data) => api.post('/projects/milestones/', data),
  updateMilestone: (id, data) => api.put(`/projects/milestones/${id}/`, data),
};

export const resourcesAPI = {
  getEquipment: (params) => api.get('/resources/equipment/', { params }),
  createEquipment: (data) => api.post('/resources/equipment/', data),
  updateEquipment: (id, data) => api.put(`/resources/equipment/${id}/`, data),
  getAvailableEquipment: () => api.get('/resources/equipment/available/'),
  getMaintenanceDue: () => api.get('/resources/equipment/maintenance_due/'),

  getMaterials: (params) => api.get('/resources/materials/', { params }),
  createMaterial: (data) => api.post('/resources/materials/', data),
  updateMaterial: (id, data) => api.put(`/resources/materials/${id}/`, data),
  getLowStock: () => api.get('/resources/materials/low_stock/'),

  getAllocations: (params) => api.get('/resources/allocations/', { params }),
  createAllocation: (data) => api.post('/resources/allocations/', data),

  getMaintenance: (params) => api.get('/resources/maintenance/', { params }),
  createMaintenance: (data) => api.post('/resources/maintenance/', data),
  updateMaintenance: (id, data) => api.put(`/resources/maintenance/${id}/`, data),
};

export const financeAPI = {
  getBudgets: (params) => api.get('/finance/budgets/', { params }),
  getBudget: (id) => api.get(`/finance/budgets/${id}/`),
  createBudget: (data) => api.post('/finance/budgets/', data),
  updateBudget: (id, data) => api.put(`/finance/budgets/${id}/`, data),

  getBudgetItems: (params) => api.get('/finance/budget-items/', { params }),
  createBudgetItem: (data) => api.post('/finance/budget-items/', data),
  updateBudgetItem: (id, data) => api.put(`/finance/budget-items/${id}/`, data),

  getInvoices: (params) => api.get('/finance/invoices/', { params }),
  getInvoice: (id) => api.get(`/finance/invoices/${id}/`),
  createInvoice: (data) => api.post('/finance/invoices/', data),
  updateInvoice: (id, data) => api.put(`/finance/invoices/${id}/`, data),
  getOverdueInvoices: () => api.get('/finance/invoices/overdue/'),
  getInvoiceSummary: () => api.get('/finance/invoices/summary/'),

  createPayment: (data) => api.post('/finance/payments/', data),

  getExpenses: (params) => api.get('/finance/expenses/', { params }),
  createExpense: (data) => api.post('/finance/expenses/', data),
  updateExpense: (id, data) => api.put(`/finance/expenses/${id}/`, data),
};

export const procurementAPI = {
  getVendors: (params) => api.get('/procurement/vendors/', { params }),
  createVendor: (data) => api.post('/procurement/vendors/', data),
  updateVendor: (id, data) => api.put(`/procurement/vendors/${id}/`, data),

  getPurchaseOrders: (params) => api.get('/procurement/purchase-orders/', { params }),
  getPurchaseOrder: (id) => api.get(`/procurement/purchase-orders/${id}/`),
  createPurchaseOrder: (data) => api.post('/procurement/purchase-orders/', data),
  updatePurchaseOrder: (id, data) => api.put(`/procurement/purchase-orders/${id}/`, data),
  getPendingDelivery: () => api.get('/procurement/purchase-orders/pending_delivery/'),

  getInventoryTransactions: (params) => api.get('/procurement/inventory-transactions/', { params }),
  createInventoryTransaction: (data) => api.post('/procurement/inventory-transactions/', data),
};

export const hrAPI = {
  getDepartments: () => api.get('/hr/departments/'),
  createDepartment: (data) => api.post('/hr/departments/', data),

  getEmployees: (params) => api.get('/hr/employees/', { params }),
  getEmployee: (id) => api.get(`/hr/employees/${id}/`),
  createEmployee: (data) => api.post('/hr/employees/', data),
  updateEmployee: (id, data) => api.put(`/hr/employees/${id}/`, data),
  getEmployeeStats: () => api.get('/hr/employees/stats/'),

  getAttendance: (params) => api.get('/hr/attendance/', { params }),
  createAttendance: (data) => api.post('/hr/attendance/', data),
  getTodayAttendance: () => api.get('/hr/attendance/today/'),

  getLeaveRequests: (params) => api.get('/hr/leave-requests/', { params }),
  createLeaveRequest: (data) => api.post('/hr/leave-requests/', data),
  updateLeaveRequest: (id, data) => api.put(`/hr/leave-requests/${id}/`, data),
  getPendingLeaves: () => api.get('/hr/leave-requests/pending/'),

  getPayrolls: (params) => api.get('/hr/payroll/', { params }),
  createPayroll: (data) => api.post('/hr/payroll/', data),
};

export const documentsAPI = {
  getDocuments: (params) => api.get('/documents/documents/', { params }),
  getDocument: (id) => api.get(`/documents/documents/${id}/`),
  createDocument: (data) => api.post('/documents/documents/', data, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  updateDocument: (id, data) => api.put(`/documents/documents/${id}/`, data),
  getExpiringDocuments: () => api.get('/documents/documents/expiring_soon/'),

  getCategories: () => api.get('/documents/categories/'),
  getDrawingSets: (params) => api.get('/documents/drawing-sets/', { params }),
};

export default api;
