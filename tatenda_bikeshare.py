import time
import pandas as pd

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'}

def get_filters(name):
    """
    Asks the user to specify a city, month, and day to analyze.
    Args:
        name (str): User's name
    Returns:
        tuple: City, month, and day filters
    """
    print(f"\nHello, {name}! Let's explore some US bikeshare data.")

    # Get the city filter
    city = input("Enter the city (Chicago, New York City, Washington): ").lower()
    while city not in CITY_DATA:
        print("Invalid city. Please try again.")
        city = input("Enter the city (Chicago, New York City, Washington): ").lower()

    # Get the month filter
    month = input("Enter the month (January, February, March, ..., all): ").lower()
    while month not in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
        print("Invalid month. Please try again.")
        month = input("Enter the month (January, February, March, ..., all): ").lower()

    # Get the day filter
    day = input("Enter the day of the week (Monday, Tuesday, Wednesday, ..., all): ").lower()
    while day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
        print("Invalid day. Please try again.")
        day = input("Enter the day of the week (Monday, Tuesday, Wednesday, ..., all): ").lower()

    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        city (str): Name of the city
        month (str): Name of the month to filter by, or "all" to apply no month filter
        day (str): Name of the day of the week to filter by, or "all" to apply no day filter
    Returns:
        df (DataFrame): Pandas DataFrame containing the filtered data
    """
    filename = CITY_DATA[city]
    df = pd.read_csv(filename)

    # Removing redudant column Unnamed:0
    df.drop(columns=['Unnamed: 0'], inplace=True)  # Remove the 'Unnamed: 0' column

    # Convert the 'Start Time' column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from the 'Start Time' column
    df['Month'] = df['Start Time'].dt.month_name()
    df['Day of Week'] = df['Start Time'].dt.day_name()

    # Apply month filter if applicable
    if month != 'all':
        df = df[df['Month'] == month.title()]

    # Apply day filter if applicable
    if day != 'all':
        df = df[df['Day of Week'] == day.title()]

    return df

# Define the missing_values_summary function
def missing_values_summary(df):
    missing_values = df.isnull().sum()
    missing_values_percentage = (missing_values / len(df)) * 100
    missing_values_table = pd.concat([missing_values, missing_values_percentage], axis=1)
    missing_values_table = missing_values_table.rename(columns={0: 'Missing Values', 1: 'Percentage (%)'})
    missing_values_table = missing_values_table[missing_values_table['Missing Values'] > 0].sort_values('Missing Values', ascending=False)
    return missing_values_table

def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
    Args:
        df (DataFrame): Pandas DataFrame containing the filtered data
    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Check if 'Month' column exists in the DataFrame
    if 'Month' not in df.columns:
        print("The 'Month' column does not exist in the DataFrame.")
        return

    # Check if 'Start Time' column has values
    if df['Start Time'].empty:
        print("The 'Start Time' column is empty in the DataFrame.")
        return

    # Display the most common month
    common_month = df['Month'].mode()[0]
    print('Most Common Month:', common_month)

    # Check if 'Day of Week' column exists in the DataFrame
    if 'Day of Week' not in df.columns:
        print("The 'Day of Week' column does not exist in the DataFrame.")
        return

    # Check if 'Day of Week' column has values
    if df['Day of Week'].empty:
        print("The 'Day of Week' column is empty in the DataFrame.")
        return

    # Display the most common day of the week
    common_day = df['Day of Week'].mode()[0]
    print('Most Common Day of the Week:', common_day)

    # Extract the hour from the 'Start Time' column
    df['Hour'] = df['Start Time'].dt.hour

    # Display the most common start hour
    common_hour = df['Hour'].mode()[0]
    print('Most Common Start Hour:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
    Args:
        df (DataFrame): Pandas DataFrame containing the filtered data
    """
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Check if 'Start Station' column exists in the DataFrame
    if 'Start Station' not in df.columns:
        print("The 'Start Station' column does not exist in the DataFrame.")
        return

    # Check if 'Start Station' column has values
    if df['Start Station'].empty:
        print("The 'Start Station' column is empty in the DataFrame.")
        return

    # Display the most common start station
    common_start_station = df['Start Station'].mode()[0]
    print('Most Common Start Station:', common_start_station)

    # Check if 'End Station' column exists in the DataFrame
    if 'End Station' not in df.columns:
        print("The 'End Station' column does not exist in the DataFrame.")
        return

    # Check if 'End Station' column has values
    if df['End Station'].empty:
        print("The 'End Station' column is empty in the DataFrame.")
        return
    
def plot_frequency_of_start_end_stations(df):
    """
    Plot the frequency of rides by start and end stations.
    Args:
        df (DataFrame): The bikeshare data
    """
    start_time = time.time()

    # Calculate the counts of each start station
    start_station_counts = df['Start Station'].value_counts().head(10)

    # Calculate the counts of each end station
    end_station_counts = df['End Station'].value_counts().head(10)

    # Create a bar chart for start stations
    plt.figure(figsize=(10, 6))
    start_station_counts.plot(kind='bar')
    plt.title('Top 10 Most Frequent Start Stations')
    plt.xlabel('Start Station')
    plt.ylabel('Number of Rides')
    plt.show()

    # Create a bar chart for end stations
    plt.figure(figsize=(10, 6))
    end_station_counts.plot(kind='bar')
    plt.title('Top 10 Most Frequent End Stations')
    plt.xlabel('End Station')
    plt.ylabel('Number of Rides')
    plt.show()

    print("\nThis took %s seconds." % (time.time() - start_time))

    # Display the most common end station
    common_end_station = df['End Station'].mode()[0]
    print('Most Common End Station:', common_end_station)

    # Combine 'Start Station' and 'End Station' columns to create a trip route column
    df['Trip Route'] = df['Start Station'] + ' to ' + df['End Station']

    # Display the most common trip route
    common_trip_route = df['Trip Route'].mode()[0]
    print('Most Common Trip Route:', common_trip_route)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
    Args:
        df (DataFrame): Pandas DataFrame containing the filtered data
    """
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Check if 'Trip Duration' column exists in the DataFrame
    if 'Trip Duration' not in df.columns:
        print("The 'Trip Duration' column does not exist in the DataFrame.")
        return

    # Check if 'Trip Duration' column has values
    if df['Trip Duration'].empty:
        print("The 'Trip Duration' column is empty in the DataFrame.")
        return

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time:', total_travel_time, 'seconds')

    # Display average travel time
    avg_travel_time = df['Trip Duration'].mean()
    print('Average Travel Time:', avg_travel_time, 'seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

import matplotlib.pyplot as plt

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Statistics...\n')

    # Count user types
    user_types = df['User Type'].value_counts()

    # Display user type counts
    print('User Type Counts:')
    for user_type, count in user_types.items():
        print(f'{user_type}: {count}')
    
def plot_frequency_of_user_type(df):
    """
    Plot the frequency of rides by user type.
    Args:
        df (DataFrame): The bikeshare data
    """
    # Calculate the counts of each user type
    user_type_counts = df['User Type'].value_counts()

    # Plot the bar chart
    user_type_counts.plot(kind='bar')

    # Set the title, x-axis label, and y-axis label
    plt.title('Counts of Rides by User Type')
    plt.xlabel('User Type')
    plt.ylabel('Number of Rides')

    # Display the plot
    plt.show()

    # Check if 'Gender' column exists in the dataframe
    if 'Gender' in df.columns:
        # Count gender types
        gender_counts = df['Gender'].value_counts()

        # Display gender counts
        print('\nGender Counts:')
        for gender, count in gender_counts.items():
            print(f'{gender}: {count}')
    
def plot_frequency_by_gender(df):
    """
    Plot the frequency of rides by gender.
    Args:
        df (DataFrame): The bikeshare data
    """
    if 'Gender' in df.columns:
        # Calculate the counts of each gender
        gender_counts = df['Gender'].value_counts()

        # Plot the bar chart
        gender_counts.plot(kind='bar')

        # Set the title, x-axis label, and y-axis label
        plt.title('Counts of Rides by Gender')
        plt.xlabel('Gender')
        plt.ylabel('Number of Rides')

        # Display the plot
        plt.show()
    else:
        print('Gender information is not available for this dataset.')

    # Check if 'Birth Year' column exists in the dataframe
    if 'Birth Year' in df.columns:
        # Count birth year frequencies and sort them in ascending order
        birth_year_counts = df['Birth Year'].value_counts().sort_index()

        # Display birth year counts
        print('\nBirth Year Counts:')
        for year, count in birth_year_counts.items():
            print(f'{year}: {count}')

        # Display birth year statistics
        print('\nBirth Year Statistics:')
        most_common_year = birth_year_counts.idxmax()
        earliest_year = birth_year_counts.idxmin()
        most_recent_year = birth_year_counts.idxmax()
        print(f'Most Common Birth Year: {most_common_year}')
        print(f'Earliest Birth Year: {earliest_year}')
        print(f'Most Recent Birth Year: {most_recent_year}')

def display_data(df):
    # Initialise variables for pagination
    start_index = 0
    increment = 10

    while True:
        # Prompt the user to see the next set of rows
        show_data = input('Do you want to see the next 10 rows of data? Enter yes or no: ').lower()
        if show_data != 'yes':
            break

        # Calculate the end index and display the data
        end_index = start_index + increment
        print(df.iloc[start_index:end_index])
        start_index = end_index

        # Check if all data has been displayed
        if start_index >= len(df):
            print('End of data.')
            break

def main():
    name = input('Please enter your name: ')
    print(f'\nHello, {name}! Let\'s explore some US bikeshare data!')
    
    while True:
        city, month, day = get_filters(name)

        df = load_data(city, month, day)

        #Main analysis functions
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        #User data display 
        display_data(df)

        # Generate missing values summary
        summary_table = missing_values_summary(df)
        print("\nMissing Values Summary:")
        print(summary_table)

        # Ask the user if they want to see the visualizations
        show_visualizations = input('\nWould you like to see the visualizations? Enter yes or no: ')

        if show_visualizations.lower() == 'yes':
            plot_frequency_by_gender(df)
            plot_frequency_of_user_type(df)
            plot_frequency_of_start_end_stations(df)

        restart = input('\nWould you like to restart? Enter yes or no: ')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
