import axios from 'axios';

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://43.205.216.10:5000';

const api = axios.create({
  baseURL: apiBaseUrl,
  headers: {
    'Content-Type': 'application/json',
  },
});

const normalizePrediction = (payload) => {
  const probability = typeof payload?.probability === 'number' ? payload.probability : null;

  let segment = 'Low';
  if (probability !== null && probability > 0.7) {
    segment = 'High';
  } else if (probability !== null && probability > 0.3) {
    segment = 'Medium';
  }

  return {
    ...payload,
    probability,
    segment,
  };
};

export const predictCustomer = async (data) => {
  const response = await api.post('/predictAPI', data);
  return normalizePrediction(response.data);
};

export const fetchModelComparison = async () => {
  const response = await api.get('/modelComparisonAPI');
  return response.data;
};

export const fetchDashboardStats = async () => {
  const response = await api.get('/dashboardStatsAPI');
  return response.data;
};

export const triggerRetrain = async () => {
  const response = await api.post('/retrainAPI');
  return response.data;
};

export default api;
