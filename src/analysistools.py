
import os
import numpy as np
import pandas as pd
#from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.colors import ListedColormap


def get_yearly_paper_counts(df):
    """
    Cleans the dataframe by removing records with missing years and
    aggregates paper counts by year.

    Args:
        df (pd.DataFrame): Input dataframe containing 'year' and 'amount' columns.

    Returns:
        pd.DataFrame: A dataframe with unique years and their corresponding total amounts.
    """
    # Create a copy to avoid modifying the original dataframe
    work_df = df.copy()
    year_with_nan = work_df[work_df["year"].isna()]
    print(f"Papers without a year record: {len(year_with_nan)}")

    # Drop rows where 'year' is missing and ensure 'amount' is numeric
    work_df = work_df.dropna(subset=['year'])
    work_df['amount'] = 1
    work_df['amount'] = pd.to_numeric(work_df['amount'], errors='coerce').fillna(0)

    # Group by 'year' and sum the 'amount'
    # reset_index() converts the grouping index back into a column
    year_count = work_df.groupby('year')['amount'].sum().reset_index()

    # Ensure year is integer (optional, prevents '2020.0')
    year_count['year'] = year_count['year'].astype(int)

    return year_count

def display_paper_yearly(data, year_gap, output_dir):
    """
    Generates and saves a bar chart showing the number of papers published per year.

    Args:
        data (pd.DataFrame): DataFrame containing 'year' and 'amount' columns.
        year_gap (int): The interval frequency for X-axis labels.
        output_dir (str): The folder path where the image will be saved.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Initialize the plot
    plt.figure(figsize=(35, 15))

    x = list(data['year'])
    y = list(data['amount'])
    x_pos = np.arange(len(x))

    # Plot the bar chart
    plt.bar(x_pos, y, width=0.85, color='#95A2C3')
    plt.xlabel("Year", fontsize=32, fontname="Arial")
    plt.ylabel("Paper Count", fontsize=32, fontname="Arial")

    # Set custom X-axis labels based on the year_gap
    tick_idx = np.arange(0, len(x_pos), year_gap)
    tick_labels = [x[i] for i in tick_idx]
    plt.xticks(tick_idx, tick_labels, fontsize=28)

    # Style configuration
    plt.yticks(fontsize=28)
    plt.xlim(-0.5, len(x_pos) - 0.5)
    plt.grid(True, linestyle='--', zorder=0)
    plt.gca().set_axisbelow(True)

    # Define full file path separately to avoid overwriting the directory argument
    file_name = "paper_published_yearly.png"
    full_save_path = os.path.join(output_dir, file_name)
    plt.savefig(full_save_path, dpi=300, bbox_inches='tight')
    print(f"Chart successfully saved to: {full_save_path}")


def count_authors(author_data):
    """
    Counts the number of authors from the provided author string.

    Args:
        author_data (str): A string containing author names (e.g., "John Doe, Jane Smith").

    Returns:
        int: The number of authors found, or 0 if the input is invalid.
    """
    # Check if the input is a valid string; return 0 for NaN or non-string values
    if not isinstance(author_data, str) or author_data.strip() == "":
        return 0

    # Assuming authors are separated by commas or semicolons
    # Adjust the split character based on your specific CSV format
    authors = author_data.split(';')
    return len(authors)


def calc_yearly_avg_authors(data):
    """
    Calculate the average number of authors per paper grouped by publication year
    :param data: Input dataframe containing columns 'year' and 'authors'
    :return: Dataframe with each year and its corresponding average author count
    """
    # Calculate author count for each paper using custom count_authors function
    data['a_amount'] = data['authors'].apply(lambda x: count_authors(x))

    # Print all unique author count values for data inspection
    print("paper with most authors", data['a_amount'].max())

    # Extract only year and author count columns to a new dataframe
    author_df = data.loc[:, ["year", "a_amount"]]

    # Display first 5 rows to preview the filtered data
    # print(author_df.head())

    # Group records by year and compute mean author number, reset index to convert group key to column
    authoravg_df = author_df.groupby(by=["year"]).mean().reset_index()
    authoravg_df['year'] = authoravg_df['year'].astype(int)

    return authoravg_df


def display_authorship_yearly(data, year_gap, output_dir):
    '''
    Plot line chart showing yearly average number of authors and save figure to target directory
    :param data: DataFrame containing columns 'year' and 'a_amount'
    :param year_gap: Interval for x-axis tick labels (unused in current tick logic, reserved for extension)
    :param output_dir: Target folder path to store output PNG image
    :return: None, generates and saves plot file locally
    '''
    # Create figure canvas with specified size and white background
    plt.figure(figsize=(35, 15), facecolor='white')

    # Extract x-axis year values and y-axis average author counts
    x = list(data['year'])
    y = list(data['a_amount'])
    # Generate sequential position indices for plotting
    x_pos = np.arange(len(x))

    # Draw line plot with circle markers, custom color and line size settings
    plt.plot(
        x_pos, y,
        marker='o',
        linestyle='-',
        color='#95A2C3',
        linewidth=3,
        markersize=10
    )

    # Set X/Y axis labels with specified font family and size
    plt.xlabel("Year", fontsize=32, fontname="Arial")
    plt.ylabel("Average Number of Authors", fontsize=32, fontname="Arial")

    # Auto rotate x-axis tick labels to prevent text overlap
    plt.gcf().autofmt_xdate()

    # Customize tick range and label text for X and Y axes
    tick_idx = np.arange(0, len(x_pos), year_gap)
    tick_labels = [x[i] for i in tick_idx]
    plt.xticks(tick_idx, tick_labels, fontsize=28)

    plt.yticks(fontsize=28)

    # Set horizontal axis boundary range
    plt.xlim(-1, 52)
    plt.gcf().autofmt_xdate()

    # Enable dashed background grid and render grid behind plot lines
    plt.grid(True, linestyle='--', zorder=0)
    plt.gca().set_axisbelow(True)

    # Define output file name and combine with target directory path
    file_name = "avg_author_yearly.png"
    full_save_path = os.path.join(output_dir, file_name)

    # Save high-resolution figure, trim extra blank borders
    plt.savefig(full_save_path, dpi=300, bbox_inches='tight')
    print(f"Chart successfully saved to: {full_save_path}")

    # Pop up figure window for preview
    plt.show()

# End of Section 1

# create a data frame with topic number along with its freq and all words
def __get_topic_allwords__(all_topics, t_model):
    '''
    get all ll word representing the topic
    :param all_topics: topics from freq df
    :param t_model: topic model
    :return: df with topic number, freq, all word representing the topic
    '''

    #create 3 empty list
    topic_list = []
    freq_list = []
    words_list = []

    for topic in all_topics:
        #topic_name = "Topic" + str(topic)
        #topic_list.append(topic_name)
        topic_list.append(topic)
        # print(topic_name)
        frq = t_model.get_topic_freq(topic)
        freq_list.append(frq)
        wordset = t_model.get_topic(topic)[:15]
        # print("====Get item from get_topic Results====")
        topic_word = []
        for item in wordset:
            # print()
            # topic_word += '' + str(item[0])
            topic_word.append(item[0])

        words_list.append(topic_word)
    # words_list.append(join(topic_word))
    topics_df = pd.DataFrame(list(zip(topic_list, freq_list, words_list)), columns=['Topic', 'Freq', 'Allwords'])
    return topics_df


