import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog

def select_csv_file():
    """
    Open a dialog to select a CSV file.
    """
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select the CSV file with the calendar",
        filetypes=[("CSV files", "*.csv")]
    )
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    return file_path, file_name

def load_and_process_calendar(file_path):
    """
    Load and process the league calendar from CSV file.
    """
    data = pd.read_csv(file_path, sep=';', header=None, encoding_errors='ignore', skiprows=3)

    data.drop(5, axis=1, inplace=True)

    half = data.shape[1] // 2
    data_half1 = data.iloc[:, :half]
    data_half2 = data.iloc[:, half:]

    data_half1.columns = ['home_team', 'home_score', 'away_score', 'away_team', 'result']
    data_half2.columns = ['home_team', 'home_score', 'away_score', 'away_team', 'result']

    fanta_df = pd.concat([data_half1, data_half2], ignore_index=True)

    fanta_df['matchday'] = fanta_df['home_team'].str.extract(r'(\d+)\s+Giornata\s+lega')
    fanta_df['matchday'] = fanta_df['matchday'].ffill()
    fanta_df['matchday'] = fanta_df['matchday'].infer_objects(copy=False)

    # Drop rows where 'home_team' contains 'Giornata lega' (these are just matchday headers)
    fanta_df = fanta_df[~fanta_df['home_team'].str.contains('Giornata lega', na=False)]

    fanta_df['matchday'] = fanta_df['matchday'].astype(int)
    fanta_df = fanta_df.sort_values(by='matchday', ascending=True)

    fanta_df = fanta_df.reset_index(drop=True)

    # Drop rows where all of the specified columns are NaN
    columns_to_check = ['home_team', 'home_score', 'away_score', 'away_team', 'result']
    fanta_df = fanta_df.dropna(subset=columns_to_check, how='all')

    fanta_df['home_team'] = fanta_df['home_team'].astype('string')
    fanta_df['away_team'] = fanta_df['away_team'].astype('string')
    fanta_df['home_score'] = fanta_df['home_score'].str.replace(',', '.').astype(float)
    fanta_df['away_score'] = fanta_df['away_score'].str.replace(',', '.').astype(float)

    return fanta_df

def main():
    """
    Main function to run the calendar processing.
    """
    file_path, file_name = select_csv_file()
    if not file_path:
        print("No file selected. Exiting.")
        return

    calendar_df = load_and_process_calendar(file_path)

    if calendar_df.empty:
        print("No valid matches found in the selected file.")
        return

    os.makedirs("output", exist_ok=True)
    calendar_df.to_csv(f"output/processed_{file_name.lower()}.csv", index=False)
    print(f"Calendar processed and saved to output/{file_name}.csv")

if __name__ == "__main__":
    main()
