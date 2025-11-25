# Scripts Directory

This folder contains all Python scripts used throughout the project.  
Scripts are grouped by their function within the data pipeline.

---

## 1. Preprocessing Scripts (preprocessing/)

Scripts that clean, standardize, and enrich raw rally-level data.  

Specifically, these scripts:
- Combine individual raw match CSVs into a single dataset
- Compute rotation-level metrics for each team
- Compute serve type probabilities per team and rotation
- Prepare datasets for simulation and analysis

Outputs are written to `data/processed/` and serve as inputs to the simulation and analysis scripts.

---

## 2. Simulation Scripts (simulation/)

Implements the Markov-chain based simulation model.

These scripts:
- Generate rally-by-rally simulated matches
- Compute rotation-level probabilities
- Produce set-level summaries automatically (simulated set summaries are generated within the simulation pipeline)
- Handle serve type sequences per rotation

Outputs are written to `data/processed/simulated_matches/` and feed into the comparison analyses.

---

## 3. Analysis Scripts (analysis/)

Contains scripts that compute both **real-only metrics** and **simulated vs real comparisons**.  
Divided into:

### • analysis/real/
Scripts that analyze **only** real match data:
- Serving efficiency (ace/in/error)
- Pass quality
- Side-out efficiency

### • analysis/comparison/
Scripts that analyze **simulated**, **real**, and **combined metrics**, including:
- Rotation efficiency (real, simulated, and combined)
- Serve type distribution comparisons
- Simulated serving vs real receiving

Outputs may include CSVs, plots, or both depending on the metric.

---

## Notes

- Each script writes outputs directly to the corresponding folder in `analysis/`.
- Not all scripts generate the same output format; some produce only visualizations, others only tables.
- The folder structure reflects the analytic workflow rather than enforcing uniform output formats.
