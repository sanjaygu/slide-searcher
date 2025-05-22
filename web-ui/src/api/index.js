import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
});

export const searchSlides = async (query, filters = {}) => {
  const response = await api.get('/api/search', {
    params: { query, ...filters },
  });
  return response.data;
};

export const uploadSlides = async (files) => {
  const formData = new FormData();
  files.forEach((file) => {
    formData.append('files', file);
  });

  const response = await api.post('/api/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const getSlideMetadata = async (slideId) => {
  const response = await api.get(`/api/slides/${slideId}`);
  return response.data;
};

export default api; 