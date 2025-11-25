import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np # Import numpy

# -----------------------------
# Load simulated rallies
# -----------------------------
sim_file = '/content/drive/MyDrive/Volleyball_Analytics/data/processed/simulations/all_simulated_rallies.csv'
sim_df = pd.read_csv(sim_file)


if 'rotation_number' in sim_df.columns:
    sim_df.rename(columns={'rotation_number': 'rotation'}, inplace=True)

output_folder_drive = '/content/drive/MyDrive/Volleyball_Analytics/project_analysis'
output_folder_local = './project_analysis'
os.makedirs(output_folder_drive, exist_ok=True)
os.makedirs(output_folder_local, exist_ok=True)

sns.set(style="whitegrid")

# -----------------------------
# Calculate Rotation Efficiency (Serving Team)
# -----------------------------
sim_df['serve_win'] = (sim_df['result'] == 'win').astype(int)

rotation_eff = sim_df.groupby('rotation')['serve_win'].mean().reset_index()
rotation_eff['rotation'] = rotation_eff['rotation'].str.replace('R','').astype(int)
rotation_eff = rotation_eff.sort_values('rotation')

# -----------------------------
# y-axis
# -----------------------------
plt.figure(figsize=(8,5))
sns.barplot(x='rotation', y='serve_win', data=rotation_eff, palette='Purples_d')
plt.ylabel('Rotation Efficiency (Serving Team)')
plt.xlabel('Rotation')
plt.title('Rotation Efficiency per Rotation (Serving Team)')


y_min = max(0, rotation_eff['serve_win'].min() - 0.02)
y_max = min(1, rotation_eff['serve_win'].max() + 0.02)
plt.ylim(y_min, y_max)
plt.yticks([round(y,3) for y in
            list(np.arange(y_min, y_max+0.001, 0.01))])  # 1% intervals

# -----------------------------
# Save plots 
# -----------------------------
plot_drive_path = os.path.join(output_folder_drive, 'rotation_efficiency_per_rotation.png')
plot_local_path = os.path.join(output_folder_local, 'rotation_efficiency_per_rotation.png')
plt.savefig(plot_drive_path, dpi=300, bbox_inches='tight')
plt.savefig(plot_local_path, dpi=300, bbox_inches='tight')
plt.show()

# Save aggregated table 
table_drive_path = os.path.join(output_folder_drive, 'rotation_efficiency_per_rotation.csv')
table_local_path = os.path.join(output_folder_local, 'rotation_efficiency_per_rotation.csv')
rotation_eff.to_csv(table_drive_path, index=False)
rotation_eff.to_csv(table_local_path, index=False)

print(f"Rotation Efficiency plot saved to Drive: {plot_drive_path}")
print(f"Rotation Efficiency plot saved locally: {plot_local_path}")
print(f"Aggregated table saved to Drive: {table_drive_path}")
print(f"Aggregated tabl