# Analysis Directory

This folder contains all analytical outputs derived from both the real match data and the simulation model.  
It is divided into two major subdirectories: **comparison/** and **real/**.

---

## 1. Comparison Analyses (comparison/)

Contains all metrics that involve **simulated data**, **comparisons between simulated and real**, or interactions between the simulated serving model and real receiving structures.

Includes:

- Rotation efficiency derived from real data, simulated data, and the comparison between the two  
- Serve type distribution comparisons, including team-specific visualizations  
- Simulated serving vs real receiving performance comparisons  
- Simulated set-level summaries

These analyses may include:
- comparison tables  
- plots  
- simulated summaries  

(Outputs vary by metric; some analyses produce only CSVs, others produce only visualizations, others both.)

---

## 2. Real-Only Analyses (real/)

Contains analyses based **exclusively on real match data**, without any simulation component.

Includes:

- Serve performance (ace / in / error structure)
- Pass quality distributions and rotation-based patterns
- Side-out efficiency by rotation or set

Rotation efficiency is *not* included here — it is part of the comparison workflow.

---

## Notes

- The structure mirrors the analytical flow of the project:
  - **comparison/** for anything involving simulation  
  - **real/** for metrics derived only from real matches  
- Files inside each folder correspond directly to the output of the scripts in `scripts/analysis/`.  
- Some analyses naturally generate only a CSV, others only plots, depending on what the metric requires.
