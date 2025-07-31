import React, { useState } from 'react';
import UploadPanel from '../components/UploadPanel';
import ResultsPanel from '../components/ResultsPanel';
import '../styles/UploadView.css';

const UploadView = () => {
  const [result, setResult] = useState(null);  // 后端返回的图片/表格路径
  const [isUploading, setIsUploading] = useState(false);

  return (
    <div className="upload-grid">
      <UploadPanel
        setResult={setResult}
        isUploading={isUploading}
        setIsUploading={setIsUploading}
      />
      <ResultsPanel result={result} />
    </div>
  );
};

export default UploadView;
