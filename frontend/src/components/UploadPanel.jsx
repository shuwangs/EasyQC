import React, { useState } from 'react';
import { uploadFileToServer } from '../api/api';

const normalizationOptions = ['none', 'tic', 'is', 'qc', 'pqn', 'is+qc', 'is+pqn'];

const UploadPanel = ({ setResult, isUploading, setIsUploading }) => {
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const file = e.target.file.files[0];
    const normalization = e.target.normalization.value;

    if (!file) return;

    setError('');
    setResult(null);
    setIsUploading(true);

    try {
      const res = await uploadFileToServer(file, normalization);
      setResult(res);
    } catch (err) {
      setError(err.response?.data?.error || 'Upload failed.');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="upload-panel">
      <form onSubmit={handleSubmit}>
        <label>Please upload your file</label><br />
        <input type="file" name="file" accept=".txt" required /><br /><br />

        <label>Choose Normalization method</label><br />
        <select name="normalization" defaultValue="none">
          {normalizationOptions.map(opt => (
            <option key={opt} value={opt}>{opt}</option>
          ))}
        </select><br /><br />

        <button type="submit" disabled={isUploading}>
          {isUploading ? 'Uploading...' : 'Upload'}
        </button>
      </form>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      <br />
      <div className="cov-link">
        <strong>CoV Table</strong>
      </div>
    </div>
  );
};

export default UploadPanel;
