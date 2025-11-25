import pandas as pd
import numpy as np
import os

# ------------------------------------------------
# Paths
# ------------------------------------------------
base = "/content/drive/MyDrive/Volleyball_Analytics/data/processed"
step5 = os.path.join(base, "step5")
simulations = os.path.join(base, "simulations")
sim_rallies_path = os.path.join(simulations, "rallies")
sim_summaries_path = os.path.join(simulations, "summaries")

for p in [simulations, sim_rallies_path, sim_summaries_path]:
    os.makedirs(p, exist_ok=True)

# ------------------------------------------------
# Load data
# ------------------------------------------------
rotation_metrics = pd.read_csv(os.path.join(step5, "rotation_metrics.csv"))
rotation_metrics["rotation_number"] = rotation_metrics["rotation_number"].astype(str)

rotation_serve_probs = pd.read_csv(os.path.join(step5, "rotation_serve_probs.csv"))
rotation_serve_probs["rotation_number"] = rotation_serve_probs["rotation_number"].astype(str)

teams = sorted(rotation_metrics["team"].unique())

# ------------------------------------------------
# Simulation function
# ------------------------------------------------
def simulate_set_fixed_serves(team_a, team_b, rotation_metrics, rotation_serve_probs, set_target=15):

    rally_num = 1
    points = {team_a: 0, team_b: 0}
    serving_team = team_a
    rotations_list = ["R1", "R2", "R3", "R4", "R5", "R6"]
    sim_rallies = []

    # Pre-generate serve type sequence per rotation based on proportions
    serve_sequences = {}
    for team in [team_a, team_b]:
        serve_sequences[team] = {}
        for rot in rotations_list:
            subset = rotation_serve_probs[(rotation_serve_probs["serving_team"]==team) &
                                          (rotation_serve_probs["rotation_number"]==rot)]
            # If no data, default uniform
            if subset.empty:
                serve_types = ["JUMP", "FLOAT", "HYBRID"]
                probs = [1/3]*3
            else:
                serve_types = subset["serve_type"].tolist()
                probs = subset["prob"].tolist()

            # Generate a sufficiently long sequence of serve types
            n_rallies = 100  # safe overestimate
            serve_sequence = list(np.random.choice(serve_types, size=n_rallies, p=probs))
            serve_sequences[team][rot] = serve_sequence

    # Initialize rotation index trackers
    rotation_idx = {team_a: 0, team_b: 0}

    while True:
        rotation = rotations_list[rotation_idx[serving_team] % 6]
        # Choose serve type from precomputed sequence
        serve_type_list = serve_sequences[serving_team][rotation]
        serve_type = serve_type_list[rally_num % len(serve_type_list)]

        # Win probability for serving team & rotation
        win_row = rotation_metrics[(rotation_metrics["team"]==serving_team) &
                                   (rotation_metrics["rotation_number"]==rotation)]
        win_prob = win_row["win_prob"].values[0] if not win_row.empty else rotation_metrics["win_prob"].mean()

        rally_result = "win" if np.random.rand() < win_prob else "loss"

        if rally_result == "win":
            points[serving_team] += 1
        else:
            serving_team = team_b if serving_team == team_a else team_a
            # Move to next rotation for new serving team
            rotation_idx[serving_team] += 1
            points[serving_team] += 1

        sim_rallies.append({
            "rally_num": rally_num,
            "serving_team": serving_team,
            "rotation": rotation,
            "serve_type": serve_type,
            "result": rally_result,
            "score_team_a": points[team_a],
            "score_team_b": points[team_b]
        })

        rally_num += 1

        # Set end condition: 15 points & 2-point lead
        if max(points.values()) >= set_target and abs(points[team_a]-points[team_b]) >= 2:
            break

    return pd.DataFrame(sim_rallies), points

# ------------------------------------------------
# Run full simulation
# ------------------------------------------------
all_rallies = []
all_summaries = []

for i, team_a in enumerate(teams):
    for team_b in teams[i+1:]:
        match_id = f"{team_a}_vs_{team_b}"
        for set_num in range(1, 6):  # 5 sets per match
            sim_df, points = simulate_set_fixed_serves(team_a, team_b, rotation_metrics, rotation_serve_probs)

            sim_df["match"] = match_id
            sim_df["set"] = set_num

            all_rallies.append(sim_df)

            all_summaries.append({
                "match": match_id,
                "set": set_num,
                "team_a": team_a,
                "team_b": team_b,
                "team_a_points": points[team_a],
                "team_b_points": points[team_b]
            })

           
            sim_df.to_csv(os.path.join(sim_rallies_path, f"{match_id}_set{set_num}.csv"), index=False)


all_rallies_df = pd.concat(all_rallies, ignore_index=True)
all_summaries_df = pd.DataFrame(all_summaries)

all_rallies_df.to_csv(os.path.join(simulations, "all_simulated_rallies.csv"), index=False)
all_summaries_df.to_csv(os.path.join(simulations, "all_simulated_summaries.csv"), index=False)

print("Simulation complete. Combined CSVs and individual sets saved.")