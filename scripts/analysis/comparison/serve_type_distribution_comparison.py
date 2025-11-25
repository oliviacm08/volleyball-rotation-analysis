import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


raw_path = '/content/drive/MyDrive/Volleyball_Analytics/data/processed/step5/combined_cleaned_rallies.csv'
sim_path = '/content/drive/MyDrive/Volleyball_Analytics/data/processed/simulations/all_simulated_rallies.csv'

output_drive = '/content/drive/MyDrive/Volleyball_Analytics/project_analysis'
output_local = './project_analysis'
plots_drive = os.path.join(output_drive, 'plots')
plots_local = os.path.join(output_local, 'plots')

os.makedirs(output_drive, exist_ok=True)
os.makedirs(output_local, exist_ok=True)
os.makedirs(plots_drive, exist_ok=True)
os.makedirs(plots_local, exist_ok=True)

df_real = pd.read_csv(raw_path)
df_sim = pd.read_csv(sim_path)

def normalize_rotation_col(df):
    if 'rotation_number' in df.columns:
        col = 'rotation_number'
    elif 'rotation' in df.columns:
        col = 'rotation'
    else:
        raise KeyError("No rotation column found (expected 'rotation_number' or 'rotation').")

    def to_R(x):
        if pd.isna(x): 
            return np.nan
        s = str(x)
        s = s.strip()
        
        if s.upper().startswith('R'):
            return s.upper()
        
        try:
            i = int(float(s))
            return f'R{i}'
        except:
            
            return s.upper()
    df['rotation_number'] = df[col].apply(to_R)

    df = df[ df['rotation_number'].notna() ].copy()
    return df

df_real = normalize_rotation_col(df_real)
df_sim  = normalize_rotation_col(df_sim)


df_real = df_real[df_real['serve_type'].notna()].copy()
df_sim  = df_sim[df_sim['serve_type'].notna()].copy()


df_real['serve_type'] = df_real['serve_type'].astype(str).str.strip().str.upper()
df_sim['serve_type']  = df_sim['serve_type'].astype(str).str.strip().str.upper()


real_group = (
    df_real
    .groupby(['serving_team','rotation_number','serve_type'])
    .size()
    .unstack(fill_value=0)
)

real_dist = real_group.div(real_group.sum(axis=1), axis=0)

for col in ['FLOAT','HYBRID','JUMP']:
    if col not in real_dist.columns:
        real_dist[col] = 0
real_dist = real_dist[['FLOAT','HYBRID','JUMP']]
real_dist.columns = ['FLOAT_real','HYBRID_real','JUMP_real']


sim_group = (
    df_sim
    .groupby(['serving_team','rotation_number','serve_type'])
    .size()
    .unstack(fill_value=0)
)

sim_dist = sim_group.div(sim_group.sum(axis=1), axis=0)
for col in ['FLOAT','HYBRID','JUMP']:
    if col not in sim_dist.columns:
        sim_dist[col] = 0
sim_dist = sim_dist[['FLOAT','HYBRID','JUMP']]
sim_dist.columns = ['FLOAT_sim','HYBRID_sim','JUMP_sim']


merged = real_dist.join(sim_dist, how='outer').fillna(0).reset_index()


merged['max_abs_diff'] = merged.apply(
    lambda r: max(
        abs(r['FLOAT_real'] - r['FLOAT_sim']),
        abs(r['HYBRID_real'] - r['HYBRID_sim']),
        abs(r['JUMP_real'] - r['JUMP_sim'])
    ), axis=1
)

csv_drive = os.path.join(output_drive, 'serve_type_distribution_per_rotation_per_team.csv')
csv_local = os.path.join(output_local, 'serve_type_distribution_per_rotation_per_team.csv')
merged.to_csv(csv_drive, index=False)
merged.to_csv(csv_local, index=False)

print('Saved CSV to:', csv_drive, 'and', csv_local)

# -----------------------------
# Plot per team (save to Drive and local)
# -----------------------------
for team in merged['serving_team'].unique():
    df_team = merged[ merged['serving_team'] == team ].copy()
    
    df_team['rot_index'] = df_team['rotation_number'].str.replace('R','').astype(int)
    df_team = df_team.sort_values('rot_index')

    x = np.arange(len(df_team))
    width = 0.12

    fig, ax = plt.subplots(figsize=(14,6))

    # Real
    ax.bar(x - 2*width, df_team['FLOAT_real'], width, label='FLOAT (real)')
    ax.bar(x - width,    df_team['HYBRID_real'], width, label='HYBRID (real)')
    ax.bar(x,            df_team['JUMP_real'], width, label='JUMP (real)')

    # Sim
    ax.bar(x + width,    df_team['FLOAT_sim'], width, label='FLOAT (sim)')
    ax.bar(x + 2*width,  df_team['HYBRID_sim'], width, label='HYBRID (sim)')
    ax.bar(x + 3*width,  df_team['JUMP_sim'], width, label='JUMP (sim)')

    ax.set_xticks(x)
    ax.set_xticklabels(df_team['rotation_number'])
    ax.set_xlabel('Rotation')
    ax.set_ylabel('Proportion')
    ax.set_title(f'Serve Type Distribution per Rotation — {team}')
    ax.legend(ncols=2)
    plt.tight_layout()

    
    fname = f'serve_type_distribution_per_rotation_per_team_{team}.png'
    plt.savefig(os.path.join(plots_drive, fname), dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(plots_local, fname), dpi=300, bbox_inches='tight')
    plt.close(fig)
    print('Saved plot for', team)

print('Done.')