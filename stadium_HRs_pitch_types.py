#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install pybaseball pandas


# In[34]:


from pybaseball import statcast
import pandas as pd

# Function to fetch home run data for a specified date range
def fetch_home_run_data(start_date, end_date):
    # Pull Statcast data for the specified date range
    data = statcast(start_date, end_date)  # Positional arguments for dates

    # Filter only home runs
    home_runs = data[data['events'] == 'home_run']

    # Check the columns of the DataFrame to see what's available
    print(f"Columns in dataset: {list(home_runs.columns)}")
    
    # Define a mapping of home teams to stadium names
    stadium_mapping = {
        'AZ': 'Chase Field',
        'ATL': 'Truist Park',
        'BAL': 'Oriole Park at Camden Yards',
        'BOS': 'Fenway Park',
        'CHC': 'Wrigley Field',
        'CIN': 'Great American Ball Park',
        'CLE': 'Progressive Field',
        'COL': 'Coors Field',
        'CWS': 'Guaranteed Rate Field',
        'DET': 'Comerica Park',
        'HOU': 'Minute Maid Park',
        'KC': 'Kauffman Stadium',
        'LAA': 'Angel Stadium',
        'LAD': 'Dodger Stadium',
        'MIA': 'LoanDepot Park',
        'MIL': 'American Family Field',
        'MIN': 'Target Field',
        'NYM': 'Citi Field',
        'NYY': 'Yankee Stadium',
        'OAK': 'Oakland Coliseum',
        'PHI': 'Citizens Bank Park',
        'PIT': 'PNC Park',
        'SD': 'Petco Park',
        'SEA': 'T-Mobile Park',
        'SF': 'Oracle Park',
        'STL': 'Busch Stadium',
        'TB': 'Tropicana Field',
        'TEX': 'Globe Life Field',
        'TOR': 'Rogers Centre',
        'WSH': 'Nationals Park'
    }

    # Add stadium names manually if not already in the dataset
    if 'stadium_name' not in home_runs.columns:
        home_runs['stadium_name'] = home_runs['home_team'].map(stadium_mapping)

    # Check column names and find the correct column for the play description
    if 'des' in home_runs.columns:
        home_run_details = home_runs[[ 
            'game_date',          # Date of the game
            'player_name',        # Batter's name
            'pitch_name',         # Type of pitch
            'home_team',          # Home team (for stadium)
            'away_team',          # Away team
            'des',                # Play description
            'events',             # Ball in play outcomes
            'stadium_name'        # Stadium name
        ]].copy()

        # Rename columns for clarity
        home_run_details.rename(columns={
            'pitch_name': 'Pitch Type',
            'player_name': 'Pitcher Name',  
            'des': 'Play Description',        
            'stadium_name': 'Stadium'
        }, inplace=True)
    else:
        # If the 'des' column doesn't exist, handle the missing column scenario
        print("The column 'des' is missing from the dataset. Available columns are:", list(home_runs.columns))
        return None

    # Function to extract the player's name until the word "hits" or "homers"
    def extract_player_name(description):
        # Split the description by spaces
        words = description.split()
        
        # Find the index of "hits" or "homers", if present
        if "hits" in words:
            end_index = words.index("hits")
        elif "homers" in words:
            end_index = words.index("homers")
        else:
            # If neither "hits" nor "homers" is found, take the whole description
            return ' '.join(words)
        
        # Return the part of the description up to the word before "hits" or "homers"
        return ' '.join(words[:end_index])

    # Add the 'batter' column by applying the function to the 'des' column
    home_run_details['Batter Name'] = home_run_details['Play Description'].apply(extract_player_name)

    # Reorder the columns: Stadium first, then Game Date
    home_run_details = home_run_details[['game_date', 'Play Description', 'events', 'Stadium', 'home_team', 'away_team', 'Pitcher Name', 'Batter Name', 'Pitch Type']]

    return home_run_details

# Fetch data for April 2024
home_run_data = fetch_home_run_data("2024-04-01", "2024-04-10")

# If data was returned, print the first 5 rows of the data table
if home_run_data is not None:
    print("Sample of Home Run Data:")
    print(home_run_data.head())

    # Save to CSV for further analysis
    output_path = r"C:\Users\JoshuaGoldberg\OneDrive - happify.com\Desktop\stadium_analysis\mlb_home_runs_april_2024.csv"
    home_run_data.to_csv(output_path, index=False)

    print(f"Home run data saved to '{output_path}'")


# In[ ]:




