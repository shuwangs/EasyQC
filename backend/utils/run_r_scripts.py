import os, shutil
import subprocess

# def run_all_r_scripts(input_file, normalization, output_dir):

#     '''
#     Simulate the analysis results by uploading the files to the mock_assets directory.'''

#     pca_type = os.path.join(output_dir, 'pca_sample_type.png')
#     pca_order = os.path.join(output_dir, 'pca_injection_order.png')
#     is_cov = os.path.join(output_dir, 'internal_standards_rsd.csv')

#     shutil.copy('./mock_assets/data_pca_sample_type.png', pca_type)
#     shutil.copy('./mock_assets/data_pca_injection_order.png', pca_order)
#     shutil.copy('./mock_assets/batch_pooled_qc_rsd_internal_standards.csv', is_cov)

#     return {
#         pca_order: './results/pca_injection_order.png',
#         pca_type: './results/pca_sample_type.png',
#         is_cov: './results/internal_standards_rsd.csv',
#     }



def call_r_script(script_name, input_file, normalization_method, data_type, output_dir):
    script_path = os.path.join("backend", "R_scripts", script_name)
    result = subprocess.run(
        ["Rscript", script_path, input_file, normalization_method, output_dir],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"{script_name} failed: {result.stderr}")

def run_all_r_scripts(input_file, normalization_method, data_type, output_dir):
    call_r_script("dotplot.R", input_file, normalization_method, data_type, output_dir)
    call_r_script("cov_table.R", input_file, normalization_method, data_type, output_dir)
    call_r_script("pca_plot.R", input_file, normalization_method, data_type, output_dir)

    return {
        "dotplot": "/results/dotplot.png",
        "pca_raw": "/results/pca_raw.png",
        "cov_table": "/results/cov_table.csv"
    }
