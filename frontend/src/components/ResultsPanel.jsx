import React from 'react';

const ResultsPanel = ({ result }) => {
  if (!result) return null;

  return (
    <div className="results-panel">
      <img
        src={result.results['./results/internal_standards_rsd.csv']?.replace('.csv', '.png')}
        alt="dotplot"
        className="image-wide"
      />
      <div className="pca-row">
        <img src={result.results['./results/pca_sample_type.png']} alt="PCA Type" />
        <img src={result.results['./results/pca_injection_order.png']} alt="PCA Injection" />
      </div>
    </div>
  );
};

export default ResultsPanel;
