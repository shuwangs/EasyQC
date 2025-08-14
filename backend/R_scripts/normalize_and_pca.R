# 做你该做的事情，比如输出图或表
library(ggplot2)
library(tidyverse)
library(officer)

args <- commandArgs(trailingOnly = TRUE)
input_file <- args[1]
normalization <- args[2]
data_type <- args[3]
output_dir <- args[4]

# Read and clean input
area  <- readr::read_delim(input_file, delim = "\t", na = c("NA", "N/A")) |>
    janitor::clean_names() |>
    dplyr::mutate(sample_type = case_when(
      grepl("Blank", `sample_id`) ~ "Blank",
      # grepl("Pooled QC", `sample_id`) ~ "Pooled QC",
      grepl("Pooled QC_Batch\\d+", sample_id) ~ str_extract(sample_id, "Pooled QC_Batch\\d+"),
      grepl("NIST|Nist|nist", `sample_id`) ~ "NIST",
      grepl("Sample|sample", `sample_id`) ~ "Sample",
      grepl("Ext Buffer|Ext", `sample_id`) ~ "Ext Buffer",
      grepl("Control Material", sample_id) ~ "Control Material"
    ),
    seq = row_number(sample_id)
    ) |>
    dplyr::relocate(sample_type, seq , .after = sample_id)
    
 
# Filtering the missing values --------------------------------------------
df <- area[5:ncol(area)]
imputed_data <- omicsTools::handle_missing_values(df, 
                threshold = 0.25, 
                imputation_method = "half_min")

imputed_data <- dplyr::bind_cols(area[1:4], imputed_data)
# PCA
pca_res <- stats::prcomp(imputed_data[, -c(1:4)], center = T, scale. = T)
# get eigenvalues
eigs <- pca_res$sdev^2
# get cumulative variance
pc_var <- eigs / sum(eigs)
cumvar <- cumsum(eigs) / sum(eigs)
  
plot_DT <- pca_res$x[, c(1, 2)]
plot_DT <- as.data.frame(plot_DT) 
plot_DT$sample_type <- imputed_data$sample_type
plot_DT$seq <- as.numeric(imputed_data$seq)

 
## change here what you dont want to plot.
plot_DT <- plot_DT|>
   dplyr::filter(!sample_type %in% c("NIST", "Ext Buffer", "Blank") )

data.table::setDT(plot_DT)
  
  # radiation
ggplot2::ggplot(plot_DT, ggplot2::aes(x = PC1, y = PC2, color = sample_type)) +
    ggplot2::geom_point(size = 2, alpha = 0.66) +
    ggplot2::labs(
      title = "Raw Data",
      subtitle = "PCA Scores Plot",
      caption = "",
      x = paste0("PC1 (", formatC(pc_var[1] * 100, digits = 2, format = "f"), "%)"),
      y = paste0("PC2 (", formatC(pc_var[2] * 100, digits = 2, format = "f"), "%)")
    )
ggplot2::ggsave(paste(output_dir, "data_pca_sample_type.png", sep = '/'), device = "png", width = 5, height = 4, dpi = 300, units = "in")
  
  
  ## injection_order
ggplot2::ggplot(plot_DT, ggplot2::aes(x = PC1, y = PC2, color = seq)) +
    ggplot2::geom_point(size = 2, alpha = 0.66) +
    ggplot2::geom_text(ggplot2::aes(label = seq), vjust = -1, size = 2) +  
    ggplot2::labs(
      title = "Raw Data",
      subtitle = "PCA Scores Plot",
      caption = "",
      x = paste0("PC1 (", formatC(pc_var[1] * 100, digits = 2, format = "f"), "%)"),
      y = paste0("PC2 (", formatC(pc_var[2] * 100, digits = 2, format = "f"), "%)")
    )
  
ggplot2::ggsave(paste(outdir, "data_pca_injection_order.png", sep = '/'), device = "png", width = 5, height = 4, dpi = 300, units = "in")
