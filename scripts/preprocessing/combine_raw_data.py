import pandas as pd
import os
import shutil


local_step5_path = "/content/Volleyball_Analytics/data/verification/step5"
os.makedirs(local_step5_path, exist_ok=True)


drive_step5_path = "/content/drive/MyDrive/Volleyball_Analytics/data/verification/step5"
os.makedirs(drive_step5_path, exist_ok=True)


raw_path = "/content/Volleyball_Analytics/data/raw"
csv_files = [f for f in os.listdir(raw_path) if f.endswith('.csv')]

df_list = []

for idx, file in enumerate(csv_files, start=1):
    temp_df = pd.read_csv(os.path.join(raw_path, file))

    temp_df['match_id'] = idx
    temp_df['match_name'] = file.replace('.csv','')
    df_list.append(temp_df)

all_rallies_df = pd.concat(df_list, ignore_index=True)
all_rallies_df = all_rallies_df.sort_values(by=['match_id','set_number','rally_number']).reset_index(drop=True)


local_csv_path = os.path.join(local_step5_path, "all_rallies_combined.csv")
all_rallies_df.to_csv(local_csv_path, index=False)
drive_csv_path = os.path.join(drive_step5_path, "all_rallies_combined.csv")
all_rallies_df.to_csv(drive_csv_path, index=False)


