import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

# -----------------------------
# Comparison data
# -----------------------------
comp_file = '/content/drive/MyDrive/Volleyball_Analytics/project_analysis/rotation_efficiency_comparison.csv'
comp_df_wide = pd.read_csv(comp_file)

comp_df = comp_df_wide.melt(id_vars=['rotation'],
                          value_vars=['Efficiency_sim', 'Efficiency_real'],
                          var_name='Type',
                          value_name='Efficiency')

comp_df['Type'] = comp_df['Type'].map({'Efficiency_sim': 'Simulated (Serving)',
                                       'Efficiency_real': 'Real (Receiving)'})


output_folder_drive = '/content/drive/MyDrive/Volleyball_Analytics/project_analysis'
output_folder_local = './project_analysis'
os.makedirs(output_folder_drive, exist_ok=True)
os.makedirs(output_folder_local, exist_ok=True)

sns.set(style="whitegrid")

# -----------------------------
# Plot side-by-side bars
# -----------------------------
plt.figure(figsize=(12,6))

purple_color = sns.color_palette("Purples_d")[3] 
blue_color = sns.color_palette("Blues_d")[3]   


custom_palette = {
    'Simulated (Serving)': purple_color,
    'Real (Receiving)': blue_color
}

sns.barplot(
    x='rotation',
    y='Efficiency',
    hue='Type',
    data=comp_df,
    palette=custom_palette,
    dodge=True,
    width=0.4
)

plt.xlabel('Rotation')
plt.ylabel('Efficiency')
plt.title('Rotation Efficiency (Simulated Serving vs Real Receiving)')
plt.legend(title='Data Type')



y_min = max(0, comp_df['Efficiency'].min() - 0.02)
y_max = min(1, comp_df['Efficiency'].max() + 0.02)
plt.ylim(y_min, y_max)


plt.yticks(np.linspace(y_min, y_max, 7))

plt.show()


plot_drive_path = os.path.join(output_folder_drive, 'rotation_efficiency_comparison.png')
plot_local_path = os.path.join(output_folder_local, 'rotation_efficiency_comparison.png')
plt.savefig(plot_drive_path, dpi=300, bbox_inches='tight')
plt.savefig(plot_local_path, dpi=300, bbox_inches='tight')

print(f"Comparison plot saved to Drive: {plot_drive_path}")
print(f"Comparison plot saved locally: {plot_local_path}")