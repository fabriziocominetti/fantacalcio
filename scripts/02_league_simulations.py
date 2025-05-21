import pandas as pd
import numpy as np
from tqdm import tqdm
import os
import tkinter as tk
from tkinter import filedialog

# Step 1: Load match results CSV
def load_match_data(file_path):
    data = pd.read_csv(file_path)

    teams = pd.unique(data[['home_team', 'away_team']].values.ravel())
    teams.sort()
    team_map = {name: idx + 1 for idx, name in enumerate(teams)}
    team_reverse_map = {v: k for k, v in team_map.items()}

    home_scores = data[['matchday', 'home_team', 'home_score']].copy()
    home_scores['round_team'] = home_scores['matchday'].astype(str) + '_' + home_scores['home_team']
    home_scores = home_scores.rename(columns={'home_score': 'score'})[['round_team', 'score']]

    away_scores = data[['matchday', 'away_team', 'away_score']].copy()
    away_scores['round_team'] = away_scores['matchday'].astype(str) + '_' + away_scores['away_team']
    away_scores = away_scores.rename(columns={'away_score': 'score'})[['round_team', 'score']]

    scores_data = pd.concat([home_scores, away_scores], axis=0).reset_index(drop=True)

    return data, teams, team_map, team_reverse_map, scores_data

# Step 2: Score-to-goals conversion
def score_to_goals_dynamic(score, min_score=66, step=6):
    if pd.isna(score):
        return 0
    if score < min_score:
        return 0
    return int((score - min_score) // step) + 1

# Step 3: Generate one random league schedule
def generate_random_schedule(teams, num_matchdays):
    matchdays = []
    for round_number in range(1, num_matchdays + 1):
        shuffled = np.random.permutation(teams)
        pairings = [(round_number, shuffled[i], shuffled[i + 1]) for i in range(0, len(shuffled), 2)]
        matchdays.extend(pairings)
    return pd.DataFrame(matchdays, columns=['round', 'team1_name', 'team2_name'])

# Step 4: Simulation loop
def simulate_random_leagues(num_simulations, teams, scores_data, step_size):
    results = []
    num_matchdays = scores_data['round_team'].str.extract(r'^(\d+)_')[0].astype(int).max()

    for _ in tqdm(range(num_simulations)):
        schedule = generate_random_schedule(teams, num_matchdays)

        schedule['round_team1'] = schedule['round'].astype(str) + '_' + schedule['team1_name']
        schedule['round_team2'] = schedule['round'].astype(str) + '_' + schedule['team2_name']

        merged = schedule.merge(scores_data, left_on='round_team1', right_on='round_team', how='left')
        merged = merged.rename(columns={'score': 'score1'})
        merged = merged.merge(scores_data, left_on='round_team2', right_on='round_team', how='left')
        merged = merged.rename(columns={'score': 'score2'})
        merged = merged.drop(columns=['round_team_x', 'round_team_y'])

        merged['goal1'] = merged['score1'].apply(lambda x: score_to_goals_dynamic(x, step=step_size))
        merged['goal2'] = merged['score2'].apply(lambda x: score_to_goals_dynamic(x, step=step_size))

        merged['points1'] = (merged['goal1'] > merged['goal2']) * 3 + (merged['goal1'] == merged['goal2']) * 1
        merged['points2'] = (merged['goal2'] > merged['goal1']) * 3 + (merged['goal1'] == merged['goal2']) * 1

        t1 = merged.groupby('team1_name').agg({'score1': 'sum', 'points1': 'sum'}).reset_index()
        t2 = merged.groupby('team2_name').agg({'score2': 'sum', 'points2': 'sum'}).reset_index()

        final = pd.merge(t1, t2, left_on='team1_name', right_on='team2_name', how='outer')
        final['team'] = final['team1_name'].combine_first(final['team2_name'])
        final['score'] = final['score1'].fillna(0) + final['score2'].fillna(0)
        final['points'] = final['points1'].fillna(0) + final['points2'].fillna(0)

        final = final[['team', 'score', 'points']].sort_values(by='points', ascending=False).reset_index(drop=True)
        final['rank'] = final.index + 1

        results.append(final)

    return pd.concat(results, ignore_index=True)

# Main script
def main():
    import sys

    # File dialog
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select the processed calendar CSV", 
        filetypes=[("CSV Files", "*.csv")]
    )

    if not file_path:
        print("No file selected. Exiting.")
        return

    try:
        step_size = float(input("Enter score-to-goal step size (default is 6): ") or 6.0)
    except ValueError:
        print("Invalid input. Using default value of 6.")
        step_size = 6.0

    print("Loading data...")
    data, teams, team_map, team_reverse_map, scores_data = load_match_data(file_path)

    print("Running simulations...")
    plot_data = simulate_random_leagues(
        num_simulations=10000,
        teams=teams,
        scores_data=scores_data,
        step_size=step_size
    )

    league_name = os.path.basename(file_path).split("processed_calendario_")[1].split(".csv")[0]
    output_filename = f"output/simulation_results_{league_name}.csv"
    os.makedirs("output", exist_ok=True)
    plot_data.to_csv(output_filename, index=False)

    print(f"Done. Results saved to: {output_filename}")

if __name__ == "__main__":
    main()
