import pandas as pd
import os

raw_path = '/content/drive/MyDrive/Volleyball_Analytics/data/processed/step5/combined_cleaned_rallies.csv'
output_drive = '/content/drive/MyDrive/Volleyball_Analytics/project_analysis'
output_local = '/content/drive/MyDrive/Volleyball_Analytics/project_analysis'

os.makedirs(output_drive, exist_ok=True)
os.makedirs(output_local, exist_ok=True)


df_raw = pd.read_csv(raw_path)

if 'rotation_number' in df_raw.columns:
    rot_col = 'rotation_number'
elif 'rotation' in df_raw.columns:
    rot_col = 'rotation'
else:
    raise KeyError("No rotation column found in raw data")

df_raw['rotation_number'] = df_raw[rot_col].apply(lambda x: int(str(x).replace('R','')) if pd.notna(x) else None)
df_raw = df_raw.dropna(subset=['rotation_number'])

df_raw['win_serving'] = (df_raw['rally_winner'] == df_raw['serving_team']).astype(int)

real_eff = (
    df_raw.groupby('rotation_number')['win_serving']
    .mean()
    .reset_index()
    .rename(columns={'win_serving':'Efficiency_real'})
)

csv_drive = os.path.join(output_drive, 'rotation_efficiency_real.csv')
csv_local = os.path.join(output_local, 'rotation_efficiency_real.csv')

real_eff.to_csv(csv_drive, index=False)
real_eff.to_csv(csv_local, index=False)

print("Real Rotation Efficiency CSV saved to:")
print(csv_drive)
print(csv_local)