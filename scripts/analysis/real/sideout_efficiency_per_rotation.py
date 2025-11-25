import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# -----------------------------
# Load raw match data
# -----------------------------
raw_file = '/content/drive/MyDrive/Volleyball_Analytics/data/processed/step5/combined_cleaned_rallies.csv'
df = pd.read_csv(raw_file)

if 'rotation_number' in df.columns:
    df.rename(columns={'rotation_number': 'rotation'}, inplace=True)


# Side-out efficiency = % of rallies won by receiving team on opponent serve
df['side_out_won'] = (df['rally_winner'] == df['receiving_team']).astype(int)

side_out_eff = df.groupby('rotation')['side_out_won'].mean().reset_index()
side_out_eff['rotation'] = side_out_eff['rotation'].str.replace('R','').astype(int)
side_out_eff = side_out_eff.sort_values('rotation')

# -----------------------------
# Plot
# -----------------------------
sns.set(style="whitegrid")
plt.figure(figsize=(8,5))
sns.barplot(x='rotation', y='side_out_won', data=side_out_eff, palette='Blues_d')
plt.ylabel('Side-Out Efficiency')
plt.xlabel('Rotation')
plt.title('Side-Out Efficiency per Rotation')
plt.ylim(0,1)

# -----------------------------
# Save Plot and Table
# -----------------------------
output_folder_drive = '/content/drive/MyDrive/Volleyball_Analytics/project_analysis'
output_folder_local = './project_analysis'
os.makedirs(output_folder_drive, exist_ok=True)
os.makedirs(output_folder_local, exist_ok=True)

plot_drive_path = os.path.join(output_folder_drive, 'side_out_efficiency_per_rotation.png')
plot_local_path = os.path.join(output_folder_local, 'side_out_efficiency_per_rotation.png')
plt.savefig(plot_drive_path, dpi=300, bbox_inches='tight')
plt.savefig(plot_local_path, dpi=300, bbox_inches='tight')
plt.show()

table_drive_path = os.path.join(output_folder_drive, 'side_out_efficiency_per_rotation.csv')
table_local_path = os.path.join(output_folder_local, 'side_out_efficiency_per_rotation.csv')
side_out_eff.to_csv(table_drive_path, index=False)
side_out_eff.to_csv(table_local_path, index=False)

print(f"Plot saved to Drive: {plot_drive_path}")
print(f"Plot saved locally: {plot_local_path}")
print(f"Table saved to Drive: {table_drive_path}")
print(f"Table saved locally: {table_local_path}")