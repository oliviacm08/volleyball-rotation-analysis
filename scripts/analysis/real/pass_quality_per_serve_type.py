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
#  Pass Quality per Serve Type
# -----------------------------
pass_serve = raw_df.groupby('serve_type')['pass_quality'].mean().reset_index()

# Plot
plt.figure(figsize=(8,5))
sns.barplot(x='serve_type', y='pass_quality', data=pass_serve, palette='Oranges_d')
plt.ylabel('Average Pass Quality')
plt.xlabel('Serve Type')
plt.title('Pass Quality per Serve Type')
plt.ylim(0, raw_df['pass_quality'].max()+0.5)

# Save plots
plot_drive_path = os.path.join(output_folder_drive, 'pass_quality_per_serve_type.png')
plot_local_path = os.path.join(output_folder_local, 'pass_quality_per_serve_type.png')
plt.savefig(plot_drive_path, dpi=300, bbox_inches='tight')
plt.savefig(plot_local_path, dpi=300, bbox_inches='tight')
plt.show()

# Save aggregated table
table_drive_path = os.path.join(output_folder_drive, 'pass_quality_per_serve_type.csv')
table_local_path = os.path.join(output_folder_local, 'pass_quality_per_serve_type.csv')
pass_serve.to_csv(table_drive_path, index=False)
pass_serve.to_csv(table_local_path, index=False)

print(f"Pass Quality per Serve Type plot saved to Drive: {plot_drive_path}")
print(f"Pass Quality per Serve Type plot saved locally: {plot_local_path}")
print(f"Aggregated table saved to Drive: {table_drive_path}")
print(f"Aggregated table saved locally: {table_local_path}")

