import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


real_file = '/content/drive/MyDrive/Volleyball_Analytics/data/processed/step5/combined_cleaned_rallies.csv'
df = pd.read_csv(real_file)

if 'rotation_number' in df.columns:
    df.rename(columns={'rotation_number':'rotation'}, inplace=True)


df['serve_result'] = df['serve_result'].astype(str).str.lower().str.strip()


output_folder_drive = '/content/drive/MyDrive/Volleyball_Analytics/project_analysis'
output_folder_local = './project_analysis'
os.makedirs(output_folder_drive, exist_ok=True)
os.makedirs(output_folder_local, exist_ok=True)

sns.set(style="whitegrid")


metrics = df.groupby('rotation')['serve_result'].value_counts(normalize=True).unstack(fill_value=0)

for col in ['ace', 'error']:
    if col not in metrics.columns:
        metrics[col] = 0

metrics['in_play'] = 1 - metrics.get('ace',0) - metrics.get('error',0)
metrics = metrics[['ace','error','in_play']].reset_index()


metrics_melted = metrics.melt(id_vars='rotation', value_vars=['ace','error','in_play'], 
                              var_name='Serve Outcome', value_name='Percentage')

plt.figure(figsize=(12,6))
sns.barplot(x='rotation', y='Percentage', hue='Serve Outcome', data=metrics_melted, palette=['red','orange','green'])
plt.xlabel('Rotation')
plt.ylabel('Percentage')
plt.title('Serve Performance by Rotation (Real Matches)')
plt.ylim(0,1)
plt.legend(title='Serve Outcome')
plt.show()


plot_drive_path = os.path.join(output_folder_drive, 'serve_performance_by_rotation_real.png')
plot_local_path = os.path.join(output_folder_local, 'serve_performance_by_rotation_real.png')
plt.savefig(plot_drive_path, dpi=300, bbox_inches='tight')
plt.savefig(plot_local_path, dpi=300, bbox_inches='tight')

table_drive_path = os.path.join(output_folder_drive, 'serve_performance_by_rotation_real.csv')
table_local_path = os.path.join(output_folder_local, 'serve_performance_by_rotation_real.csv')
metrics.to_csv(table_drive_path, index=False)
metrics.to_csv(table_local_path, index=False)

print(f"Serve Performance plot saved to Drive: {plot_drive_path}")
print(f"Serve Performance plot saved locally: {plot_local_path}")
print(f"Aggregated table saved to Drive: {table_drive_path}")
print(f"Aggregated table saved locally: {table_local_path}")