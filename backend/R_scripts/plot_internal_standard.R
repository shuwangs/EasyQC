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
area  <- readr::read_delim(input_file, delim = "\t", na = c("NA", "N/A"))

# Identify clean column names
if (data_type == "metabolomics") {
    internal_standards <- c("ce_22_6_is", "x4_nitrobenzoic_acid_neg_1_is", "x4_nitrobenzoic_acid_neg_2_is")

} else if (data_type == "lipidomics") {
    internal_standards <- grepl("is", colnames(area |> janitor::clean_names()))
}

name_hash <- tibble(name = colnames(area), clean_name = colnames(area |> janitor::clean_names()))

df <- area |>
  janitor::clean_names() |>
  dplyr::mutate(sample_type = case_when(
    grepl("Blank|blank", sample_id) ~ "Blank",
    grepl("Pooled QC_Batch\\d+", sample_id) ~ str_extract(sample_id, "Pooled QC_Batch\\d+"),
    grepl("NIST|Nist|nist", sample_id) ~ "NIST",
    grepl("Sample", sample_id) ~ "Sample",
    grepl("Ext Buffer|Ext", sample_id) ~ "Ext Buffer",
    grepl("Control Material", sample_id) ~ "Control Material"
  )) |>
  dplyr::relocate(sample_type, .after = sample_id)

outfolder <- file.path(output_dir, "dotplots")
if (!dir.exists(outfolder)) {
  dir.create(outfolder, recursive = TRUE)
}

for (feature in internal_standards) {
    if (!(feature %in% colnames(df))) {
    message(paste("⚠️ Feature not found in data:", feature))
    next
  }

  max_value <- max(df[[feature]], na.rm = TRUE)

  gg_plot <- ggplot(df, aes(x = sample_id, y = !!sym(feature), colour = sample_type)) +
    geom_point(size = 2) +
    labs(title = feature, x = "Sample ID", y = "Intensity") +
    theme_minimal() +
    scale_color_brewer(palette = "Set3")

  outpath <- file.path(outfolder, paste0(feature, ".png"))

  ggsave(outpath, gg_plot, width = 8, height = 4, units = "in")
}

