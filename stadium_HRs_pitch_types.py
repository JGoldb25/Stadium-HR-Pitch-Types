#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install pybaseball pandas


# In[36]:


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
home_run_data = fetch_home_run_data("2024-04-01", "2024-09-30") 

# If data was returned, print the first 5 rows of the data table
if home_run_data is not None:
    print("Sample of Home Run Data:")
    print(home_run_data.head())

    # Save to CSV for further analysis
    output_path = r"C:\Users\JoshuaGoldberg\OneDrive - happify.com\Desktop\stadium_analysis\stadium_pitch_type_homers_2024.csv"
    home_run_data.to_csv(output_path, index=False)

    print(f"Home run data saved to '{output_path}'")


# In[46]:


# Print basic statistics
if home_run_data is not None:
    print("Sample of Home Run Data:")
    print(home_run_data.head())

    print(f"\nTotal number of home run records: {len(home_run_data)}")

    # Number of home runs by stadium
    home_runs_by_stadium = home_run_data.groupby('Stadium').size()
    print("\nNumber of home runs by stadium:")
    print(home_runs_by_stadium)

    # Number of home runs by pitch type in each stadium
    home_runs_by_pitch_type = home_run_data.groupby(['Stadium', 'Pitch Type']).size().reset_index(name='Home Runs')
    print("\nNumber of home runs by pitch type in each stadium:")
    print(home_runs_by_pitch_type)

    # Save to CSV for further analysis
    output_path = r"C:\Users\JoshuaGoldberg\OneDrive - happify.com\Desktop\stadium_analysis\mlb_home_runs_april_2024.csv"
    home_run_data.to_csv(output_path, index=False)

    print(f"Home run data saved to '{output_path}'")


# In[62]:


import matplotlib.pyplot as plt
import seaborn as sns

# List of the specific pitch types you want to plot
selected_pitch_types = [
    '4-Seam Fastball', 'Changeup', 'Cutter', 'Knuckle Curve',
    'Sinker', 'Slider', 'Split-Finger', 'Sweeper'
]

# Iterate over each selected pitch type
for pitch_type in selected_pitch_types:
    # Filter data for the current pitch type
    pitch_data = home_run_data[home_run_data['Pitch Type'] == pitch_type]

    # Group the data by stadium and count the number of home runs
    home_runs_by_stadium = pitch_data.groupby('Stadium').size().reset_index(name='Home Runs')

    # Sort by the number of home runs, in descending order
    home_runs_by_stadium_sorted = home_runs_by_stadium.sort_values(by='Home Runs', ascending=False)

    # Create and display the chart for this pitch type
    plt.figure(figsize=(12, 6))  # Adjust the figure size for the chart

    # Plotting the bar chart with sorted data
    sns.barplot(data=home_runs_by_stadium_sorted, x='Stadium', y='Home Runs', palette="Set2", linewidth=2)

    # Add titles and labels
    plt.title(f'Home Runs by Stadium for {pitch_type} Pitch', fontsize=16)
    plt.xlabel('Stadium', fontsize=12)
    plt.ylabel('Number of Home Runs', fontsize=12)
    plt.xticks(rotation=45, ha='right')  # Rotate stadium names for readability

    # Display the plot
    plt.tight_layout()
    plt.show()


# In[69]:


import pandas as pd

# Initialize an empty list to store the ranking data
ranking_data = []

# Iterate over each selected pitch type to calculate rankings
for pitch_type in selected_pitch_types:
    # Filter the data for the current pitch type
    pitch_data = home_run_data[home_run_data['Pitch Type'] == pitch_type]

    # Group by stadium and count the home runs
    home_runs_by_stadium = pitch_data.groupby('Stadium').size().reset_index(name='Home Runs')

    # Rank the stadiums based on home runs (1 is the highest rank)
    home_runs_by_stadium['Rank'] = home_runs_by_stadium['Home Runs'].rank(ascending=False, method='min')

    # Round the ranks to 0 decimal places (integers)
    home_runs_by_stadium['Rank'] = home_runs_by_stadium['Rank'].round(0).astype(int)

    # Select only the rank column and add to the ranking data
    ranking_data.append(home_runs_by_stadium[['Stadium', 'Rank']].set_index('Stadium'))

# Merge all the individual pitch type ranking data into a single DataFrame
rank_summary = ranking_data[0]
for i in range(1, len(ranking_data)):
    rank_summary = rank_summary.merge(ranking_data[i], left_index=True, right_index=True, how='outer')

# Rename the columns to reflect the pitch types
rank_summary.columns = selected_pitch_types

# Calculate the total number of home runs for each stadium
total_home_runs_by_stadium = home_run_data.groupby('Stadium').size().reset_index(name='Total Home Runs')

# Merge the total home runs with the rank summary
rank_summary = rank_summary.merge(total_home_runs_by_stadium.set_index('Stadium'), left_index=True, right_index=True, how='left')

# Fill NaN values with 0 (for pitch types with no home runs in a stadium)
rank_summary[selected_pitch_types] = rank_summary[selected_pitch_types].fillna(0)

# Round all rank columns to integers to ensure no decimals
rank_summary[selected_pitch_types] = rank_summary[selected_pitch_types].round(0).astype(int)

# Add a new column for the total home runs by stadium and rank it
rank_summary['Total Home Runs Rank'] = rank_summary['Total Home Runs'].rank(ascending=False, method='min')

# Sort the table by the total home runs in descending order
rank_summary = rank_summary.sort_values(by='Total Home Runs Rank', ascending=True)

# Define the folder path
folder_path = r'C:\Users\JoshuaGoldberg\OneDrive - happify.com\Desktop\stadium_analysis'

# Save the table to a CSV file
file_path = f'{folder_path}\\stadium_home_run_rank_summary.csv'
rank_summary.to_csv(file_path)

print(f"Summary table saved to {file_path}")


# In[ ]:




