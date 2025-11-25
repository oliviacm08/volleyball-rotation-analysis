import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# -----------------------------
# Raw match data for pass quality
# -----------------------------
raw_file = '/content/drive/MyDrive/Volleyball_Analytics/data/processed/step5/combined_cleaned_rallies.csv'
raw_df = pd.read_csv(raw_file)

# -----------------------------
# Standardize column names
# -----------------------------
if 'rotation_number' in raw_df.columns:
    raw_df.rename(columns={'rotation_number': 'rotation'}, inplace=True)

# -----------------------------
# Create output folders
# -----------------------------
output_folder_drive = '/content/drive/MyDrive/Volleyball_Analytics/project_analysis'
os.makedirs(output_folder_drive, exist_ok=True)

output_folder_local = './project_analysis'
os.makedirs(output_folder_local, exist_ok=True)

# -----------------------------
# Pass Quality per Rotation
# -----------------------------
pass_rot = raw_df.groupby('rotation')['pass_quality'].mean().reset_index()

# Convert rotation to integer for proper sorting
pass_rot['rotation'] = pass_rot['rotation'].str.replace('R', '').astype(int)
pass_rot = pass_rot.sort_values('rotation')

# Plot
plt.figure(figsize=(8,5))
sns.barplot(x='rotation', y='pass_quality', data=pass_rot, palette='Greens_d')
plt.ylabel('Average Pass Quality')
plt.xlabel('Rotation')
plt.title('Pass Quality per Rotation')
plt.ylim(0, raw_df['pass_quality'].max()+0.5)

# Save plots
plot_drive_path = os.path.join(output_folder_drive, 'pass_quality_per_rotation.png')
plot_local_path = os.path.join(output_folder_local, 'pass_quality_per_rotation.png')
plt.savefig(plot_drive_path, dpi=300, bbox_inches='tight')
plt.savefig(plot_local_path, dpi=300, bbox_inches='tight')
plt.show()

# Save aggregated table
table_drive_path = os.path.join(output_folder_drive, 'pass_quality_per_rotation.csv')
table_local_path = os.path.join(output_folder_local, 'pass_quality_per_rotation.csv')
pass_rot.to_csv(table_drive_path, index=False)
pass_rot.to_csv(table_local_path, index=False)

print(f"Pass Quality per Rotation plot saved to Drive: {plot_drive_path}")
print(f"Pass Quality per Rotation plot saved locally: {plot_local_path}")
print(f"Aggregated table saved to Drive: {table_drive_path}")
print(f"Aggregated table saved locally: {table_local_path}")
