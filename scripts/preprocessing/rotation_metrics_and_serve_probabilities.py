# Rotation metrics and serve probabilities computation
import pandas as pd
import numpy as np
import os
import shutil


# ---------------------------
# Step 1: Paths & Folders
# ---------------------------
local_step5 = "/content/Volleyball_Analytics/data/processed/step5"
drive_step5 = "/content/drive/MyDrive/Volleyball_Analytics/data/processed/step5"
local_scripts = "/content/Volleyball_Analytics/scripts"
drive_scripts = "/content/drive/MyDrive/Volleyball_Analytics/scripts"

os.makedirs(local_step5, exist_ok=True)
os.makedirs(drive_step5, exist_ok=True)
os.makedirs(local_scripts, exist_ok=True)
os.makedirs(drive_scripts, exist_ok=True)

# ---------------------------
# Step 2: Load combined cleaned rallies
# ---------------------------
combined_csv = "/content/Volleyball_Analytics/data/processed/step5/combined_cleaned_rallies.csv"
rallies_df = pd.read_csv(combined_csv)

# ---------------------------
# Step 3: Compute rotation metrics
# ---------------------------
rotation_metrics = []

teams = rallies_df["serving_team"].unique()
for team in teams:
    team_df = rallies_df[rallies_df["serving_team"] == team]
    rotations = sorted(team_df["rotation_number"].unique())
    
    for rot in rotations:
        rot_df = team_df[team_df["rotation_number"] == rot]
        rallies_served = len(rot_df)
        points_won = (rot_df["rally_winner"] == team).sum()
        win_prob = points_won / rallies_served if rallies_served > 0 else 0
        
        # Run lengths
        runs = (rot_df["rally_winner"] != team).cumsum()
        run_lengths = rot_df.groupby(runs).apply(lambda g: (g["rally_winner"] == team).sum())
        avg_run_length = run_lengths.mean() if not run_lengths.empty else 0
        max_run_length = run_lengths.max() if not run_lengths.empty else 0
        
        rotation_metrics.append({
            "team": team,
            "rotation_number": rot,
            "rallies_served": rallies_served,
            "points_won": points_won,
            "win_prob": win_prob,
            "avg_run_length": avg_run_length,
            "max_run_length": max_run_length
        })

rot_metrics_df = pd.DataFrame(rotation_metrics)

# Rankings within each team
rot_metrics_df["rank_points"] = rot_metrics_df.groupby("team")["points_won"].rank(method="min", ascending=False)
rot_metrics_df["rank_win_prob"] = rot_metrics_df.groupby("team")["win_prob"].rank(method="min", ascending=False)

# Save rotation metrics
rotation_metrics_csv = os.path.join(local_step5, "rotation_metrics.csv")
rot_metrics_df.to_csv(rotation_metrics_csv, index=False)
shutil.copy(rotation_metrics_csv, os.path.join(drive_step5, "rotation_metrics.csv"))

# ---------------------------
# Step 4: Compute rotation serve probabilities
# ---------------------------
grouped_counts = rallies_df.groupby(['serving_team', 'rotation_number', 'serve_type']).size().reset_index(name='count')
grouped_counts['prob'] = grouped_counts.groupby(['serving_team', 'rotation_number'])['count'].transform(lambda x: x / x.sum())
serve_probs = grouped_counts[['serving_team', 'rotation_number', 'serve_type', 'prob']]

# Save serve probabilities
serve_probs_csv = os.path.join(local_step5, "rotation_serve_probs.csv")
serve_probs.to_csv(serve_probs_csv, index=False)
shutil.copy(serve_probs_csv, os.path.join(drive_step5, "rotation_serve_probs.csv"))

# ---------------------------
# Step 5: Check serving sequences
# ---------------------------
# Count sequence mismatches
mismatches = (rallies_df['serving_team'] != rallies_df['rally_winner'].shift(1)).sum()
print(f"Serving sequence mismatches (check): {mismatches}")
import pandas as pd
import numpy as np
import os
import shutil

# ---------------------------
# Step 1: Paths & Folders
# ---------------------------
local_step5 = "/content/Volleyball_Analytics/data/processed/step5"
drive_step5 = "/content/drive/MyDrive/Volleyball_Analytics/data/processed/step5"
local_scripts = "/content/Volleyball_Analytics/scripts"
drive_scripts = "/content/drive/MyDrive/Volleyball_Analytics/scripts"

os.makedirs(local_step5, exist_ok=True)
os.makedirs(drive_step5, exist_ok=True)
os.makedirs(local_scripts, exist_ok=True)
os.makedirs(drive_scripts, exist_ok=True)

# ---------------------------
# Step 2: Load combined cleaned rallies
# ---------------------------
combined_csv = "/content/Volleyball_Analytics/data/processed/step5/combined_cleaned_rallies.csv"
rallies_df = pd.read_csv(combined_csv)

# ---------------------------
# Step 3: Compute rotation metrics
# ---------------------------
rotation_metrics = []

teams = rallies_df["serving_team"].unique()
for team in teams:
    team_df = rallies_df[rallies_df["serving_team"] == team]
    rotations = sorted(team_df["rotation_number"].unique())
    
    for rot in rotations:
        rot_df = team_df[team_df["rotation_number"] == rot]
        rallies_served = len(rot_df)
        points_won = (rot_df["rally_winner"] == team).sum()
        win_prob = points_won / rallies_served if rallies_served > 0 else 0
        
        # Run lengths
        runs = (rot_df["rally_winner"] != team).cumsum()
        run_lengths = rot_df.groupby(runs).apply(lambda g: (g["rally_winner"] == team).sum())
        avg_run_length = run_lengths.mean() if not run_lengths.empty else 0
        max_run_length = run_lengths.max() if not run_lengths.empty else 0
        
        rotation_metrics.append({
            "team": team,
            "rotation_number": rot,
            "rallies_served": rallies_served,
            "points_won": points_won,
            "win_prob": win_prob,
            "avg_run_length": avg_run_length,
            "max_run_length": max_run_length
        })

rot_metrics_df = pd.DataFrame(rotation_metrics)

# Rankings within each team
rot_metrics_df["rank_points"] = rot_metrics_df.groupby("team")["points_won"].rank(method="min", ascending=False)
rot_metrics_df["rank_win_prob"] = rot_metrics_df.groupby("team")["win_prob"].rank(method="min", ascending=False)

# Save rotation metrics
rotation_metrics_csv = os.path.join(local_step5, "rotation_metrics.csv")
rot_metrics_df.to_csv(rotation_metrics_csv, index=False)
shutil.copy(rotation_metrics_csv, os.path.join(drive_step5, "rotation_metrics.csv"))

# ---------------------------
# Step 4: Compute rotation serve probabilities
# ---------------------------
grouped_counts = rallies_df.groupby(['serving_team', 'rotation_number', 'serve_type']).size().reset_index(name='count')
grouped_counts['prob'] = grouped_counts.groupby(['serving_team', 'rotation_number'])['count'].transform(lambda x: x / x.sum())
serve_probs = grouped_counts[['serving_team', 'rotation_number', 'serve_type', 'prob']]

# Save serve probabilities
serve_probs_csv = os.path.join(local_step5, "rotation_serve_probs.csv")
serve_probs.to_csv(serve_probs_csv, index=False)
shutil.copy(serve_probs_csv, os.path.join(drive_step5, "rotation_serve_probs.csv"))

# ---------------------------
# Step 5: Check serving sequences
# ---------------------------
# Count sequence mismatches
mismatches = (rallies_df['serving_team'] != rallies_df['rally_winner'].shift(1)).sum()
print(f"Serving sequence mismatches (check): {mismatches}")
import numpy as np
import os
import shutil

# ---------------------------
# Step 1: Paths & Folders
# ---------------------------
local_step5 = "/content/Volleyball_Analytics/data/processed/step5"
drive_step5 = "/content/drive/MyDrive/Volleyball_Analytics/data/processed/step5"
local_scripts = "/content/Volleyball_Analytics/scripts"
drive_scripts = "/content/drive/MyDrive/Volleyball_Analytics/scripts"

os.makedirs(local_step5, exist_ok=True)
os.makedirs(drive_step5, exist_ok=True)
os.makedirs(local_scripts, exist_ok=True)
os.makedirs(drive_scripts, exist_ok=True)

# ---------------------------
# Step 2: Load combined cleaned rallies
# ---------------------------
combined_csv = "/content/Volleyball_Analytics/data/processed/step5/combined_cleaned_rallies.csv"
rallies_df = pd.read_csv(combined_csv)

# ---------------------------
# Step 3: Compute rotation metrics
# ---------------------------
rotation_metrics = []

teams = rallies_df["serving_team"].unique()
for team in teams:
    team_df = rallies_df[rallies_df["serving_team"] == team]
    rotations = sorted(team_df["rotation_number"].unique())
    
    for rot in rotations:
        rot_df = team_df[team_df["rotation_number"] == rot]
        rallies_served = len(rot_df)
        points_won = (rot_df["rally_winner"] == team).sum()
        win_prob = points_won / rallies_served if rallies_served > 0 else 0
        
        # Run lengths
        runs = (rot_df["rally_winner"] != team).cumsum()
        run_lengths = rot_df.groupby(runs).apply(lambda g: (g["rally_winner"] == team).sum())
        avg_run_length = run_lengths.mean() if not run_lengths.empty else 0
        max_run_length = run_lengths.max() if not run_lengths.empty else 0
        
        rotation_metrics.append({
            "team": team,
            "rotation_number": rot,
            "rallies_served": rallies_served,
            "points_won": points_won,
            "win_prob": win_prob,
            "avg_run_length": avg_run_length,
            "max_run_length": max_run_length
        })

rot_metrics_df = pd.DataFrame(rotation_metrics)

# Rankings within each team
rot_metrics_df["rank_points"] = rot_metrics_df.groupby("team")["points_won"].rank(method="min", ascending=False)
rot_metrics_df["rank_win_prob"] = rot_metrics_df.groupby("team")["win_prob"].rank(method="min", ascending=False)

# Save rotation metrics
rotation_metrics_csv = os.path.join(local_step5, "rotation_metrics.csv")
rot_metrics_df.to_csv(rotation_metrics_csv, index=False)
shutil.copy(rotation_metrics_csv, os.path.join(drive_step5, "rotation_metrics.csv"))

# ---------------------------
# Step 4: Compute rotation serve probabilities
# ---------------------------
grouped_counts = rallies_df.groupby(['serving_team', 'rotation_number', 'serve_type']).size().reset_index(name='count')
grouped_counts['prob'] = grouped_counts.groupby(['serving_team', 'rotation_number'])['count'].transform(lambda x: x / x.sum())
serve_probs = grouped_counts[['serving_team', 'rotation_number', 'serve_type', 'prob']]

# Save serve probabilities
serve_probs_csv = os.path.join(local_step5, "rotation_serve_probs.csv")
serve_probs.to_csv(serve_probs_csv, index=False)
shutil.copy(serve_probs_csv, os.path.join(drive_step5, "rotation_serve_probs.csv"))

# ---------------------------
# Step 5: Check serving sequences
# ---------------------------
# Count sequence mismatches
mismatches = (rallies_df['serving_team'] != rallies_df['rally_winner'].shift(1)).sum()
print(f"Serving sequence mismatches (check): {mismatches}")