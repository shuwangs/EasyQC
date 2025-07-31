import aixos from 'axios';

const API_BASE_URL = 'http://localhost:5000';

export const uploadFileToServer = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await aixos.post(`${API_BASE_URL}/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error uploading file:', error);
    throw error;
  }
}