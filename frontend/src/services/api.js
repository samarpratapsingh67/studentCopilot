import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000',
  headers: {
    'Content-Type': 'application/json',
  },
});

const normalizePrediction = (payload) => {
  const probability =
    typeof payload?.probability === 'number'
      ? payload.probability
      : payload?.churned === 1
      ? 0.82
      : 0.18;

  let segment = 'Low';
  if (probability > 0.7) {
    segment = 'High';
  } else if (probability > 0.3) {
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

export default api;
