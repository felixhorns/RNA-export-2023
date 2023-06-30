# Engineering RNA export for measurement and manipulation of living cells

This repository holds code for analysis and plotting related to the development of synthetic RNA export systems and their application for non-destructive measurement of cell dynamics and delivering RNA from cell to cell.

## Citation

If you use this code, please cite this paper.

Horns *et al.*, Engineering RNA export for measurement and manipulation of living cells, *Cell* **186** (2023).

## Configuration

### Environment

The primary environment uses Python 3.7.7 and is specified in `environment.yml`. Use of the Conda package manger is recommended.

One notebook uses an alternative Python environment to support BigFISH. This environment can be installed using `environment_bigfish.yml`.

### Obtaining data

This code is associated with a parent repository that contains preprocessed data.

Most of the analysis can be run using the preprocessed data. Several notebooks require other larger data files, such as images.

The complete set of data is freely available from CaltechDATA. (TODO provide link).

In the Github repository, code and small data files (e.g. qPCR data) are provided. However, larger data files are not included on Github because of storage constraints. The larger data files are freely available from CaltechDATA.

## Contents

| **Figures**          | **Filename**                     | **Comments**             |
| -------------------- | -------------------------------- | ------------------------ |
| 1E, 1H, 1K           | qPCR_simple                      |                          |
| S1K, S1L             | qPCR_VLP_screen                  |                          |
| 2D                   | qPCR_EPN_screen                  |                          |
| S1C                  | qPCR_clarify_filter              |                          |
| S1D                  | qPCR_NoRT                        |                          |
| S1E                  | qPCR_export_rate                 |                          |
| S1F                  | qPCR_tag_number                  |                          |
| S1G, S1H             | qPCR_vary_expression             |                          |
| S1I                  | qPCR_stable_cell_line            |                          |
| 1L, 2F               | qPCR_RNase_protection            |                          |
| S1M, S2E             | qPCR_stability_supernatant       |                          |
| S1N, S2F             | qPCR_stability_blood             |                          |
| S2A                  | qPCR_export_rate_EPN24MCP        |                          |
| S2G, S2H, S2I        | qPCR_cargo_capacity              |                          |
| S2K                  | qPCR_booster                     |                          |
| S2L                  | qPCR_ESCRT_inhibitor             |                          |
| S2M                  | qPCR_PP7_coat_protein            |                          |
| 3A, 3B               | qPCR_K562_Jurkat                 |                          |
| 3C, 3D               | qPCR_mouse_hamster               |                          |
| S3D, S3E             | qPCR_GAPDH                       |                          |
| S1A, S2C             | dynamic_light_scattering         |                          |
| 3B, 3C, 3D, S3A, S3B | transcriptome_export             |                          |
| 3E                   | transcriptome_bias               |                          |
| S3C                  | transcriptome_detection_rate     |                          |
| S4D                  | transcriptome_stress             |                          |
| 4D, 4E               | pop_dyn_accuracy_reproducibility |                          |
| 4F, 4G, 4H, S6C      | pop_dyn_plot_dynamics            |                          |
| 4I, S6B, S6D         | pop_dyn_growth_rates             |                          |
| S6A                  | pop_dyn_rarefaction              |                          |
| S5G, S5H             | pop_dyn_sensitivity              |                          |
| S5A, S5B, S5C        | barcode_diversity                |                          |
| S4B                  | growth_rate                      |                          |
| S2D                  | imaging_EPN24MCP_particles       | Uses bigfish environment |
| 7B, 7C               | imaging_Cre_delivery_coculture   |                          |
| S4C                  | flow_toxicity                    |                          |
| S4F                  | flow_toxicity_stable_cell_line   |                          |
| S5E                  | flow_silencing                   |                          |
| 6C                   | flow_Cre                         |                          |
| 6E                   | flow_two_color                   |                          |
| S7A                  | flow_Cre_mRNA_transfection       |                          |
| S7B                  | flow_GagMCP_Cre                  |                          |
| S7C                  | flow_VSVG_titration              |                          |
| S7D                  | flow_Cre_booster                 |                          |
| S7E, S7F             | flow_mCherry_dynamics            |                          |

## Disclaimer

This project is not maintained. Software is provided as is and requests for support may not be addressed.

## Contact

If you have questions or comments, please contact Felix Horns at rfhorns@gmail.com.
