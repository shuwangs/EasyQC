import os, shutil

def run_all_r_scripts(input_file, normalization, output_dir):

    '''
    Simulate the analysis results by uploading the files to the mock_assets directory.'''

    pca_type = os.path.join(output_dir, 'pca_sample_type.png')
    pca_order = os.path.join(output_dir, 'pca_injection_order.png')
    is_cov = os.path.join(output_dir, 'internal_standards_rsd.csv')

    shutil.copy('./mock_assets/data_pca_sample_type.png', pca_type)
    shutil.copy('./mock_assets/data_pca_injection_order.png', pca_order)
    shutil.copy('./mock_assets/batch_pooled_qc_rsd_internal_standards.csv', is_cov)

    return {
        pca_order: './results/pca_injection_order.png',
        pca_type: './results/pca_sample_type.png',
        is_cov: './results/internal_standards_rsd.csv',
    }