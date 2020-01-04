import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
WEEKDAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city, month, day = '', '', ''
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    while city not in CITY_DATA:
        city = input("Which city would you like to investigate (chicago, new york city, washington) - default chicago? ").lower().rstrip().lstrip()
        if city == '':
            city = 'chicago'
    
    # get user input for month (all, january, february, ... , june)
    while month not in MONTHS and month != 'all':
        month = input("Which month (all, january, february, ... , june) - default all? ").lower().rstrip().lstrip()
        if month == '':
            month = 'all'

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while day not in WEEKDAYS and day != 'all':
        day = input("Which day of the week (all, monday, tuesday, ... sunday) - default all?").lower().rstrip().lstrip()
        if day == '':
            day = 'all'

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel.

    Args:
        df - Pandas DataFrame containing city data 
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    most_common = df.mode()
    # display the most common month
    print('The most common month: {}.'.format(df['month'].mode()[0]))

    # display the most common day of week
    print('The most common day of week: {}.'.format(df['day_of_week'].mode()[0]))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print('The most common hour: {}.'.format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.

    Args:
        df - Pandas DataFrame containing city data
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    # 'Start Station', 'End Station'
    print('The most common start station: {}.'.format(df['Start Station'].mode()[0]))
    
    # display most commonly used end station
    print('The most common end station: {}.'.format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    combinations = df.groupby(['Start Station', 'End Station']).size().to_frame('count').reset_index()
    most_frequent = combinations.iloc[combinations['count'].idxmax()]
    print('The most common trip: {} -> {}.'.format(most_frequent['Start Station'], most_frequent['End Station']))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.

    Args:
        df - Pandas DataFrame containing city data
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time: {}'.format(df['Trip Duration'].sum()))

    # display mean travel time
    print('Mean travel time: {}'.format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users.
    
    Args:
        df - Pandas DataFrame containing city data
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User type counts: \n{}'.format(df.groupby(['User Type']).size().to_frame('count').reset_index().sort_values(ascending=False, by='count')))
         
    # Display counts of gender
    if 'Gender' in df:
        print('User gender count: \n{}'.format(df.groupby(['Gender']).size().to_frame('count').reset_index().sort_values(ascending=False, by='count')))
    else:
        print('User gender data not available')
        
    # Display earliest (min), most recent (max), and most common year of birth (count)
    if 'Birth Year' in df:
        print('\nEarliest year of birth: {:.0f}'.format(df['Birth Year'].min()))
        print('Most recent year of birth: {:.0f}'.format(df['Birth Year'].max()))
        print('Most common year of birth: {:.0f}'.format(df['Birth Year'].mode()[0]))
    else:
        print('User birth year data not available')
       
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
def display_data(df):
    """Displays raw data on user request.

    Args:
        df - Pandas DataFrame containing city data
    """
    show_raw_data = ''
    while show_raw_data != 'yes' and show_raw_data != 'no':
        show_raw_data = input("\ndo you want to see raw data? Enter yes or no: ").lower().rstrip().lstrip()
    if show_raw_data == 'no':
        return
    
    show_data = True
    index_start = 0
    index_end = 5
    while show_data:
        print('Raw data [{}, {}]: \n {}'.format(index_start, index_end, df.iloc[index_start:index_end]))
        show_more_lines = ''
        while show_more_lines != 'yes' and show_more_lines != 'no':
            show_more_lines = input('do you want to see more 5 lines of raw data? Enter yes or no: ').lower().rstrip().lstrip()
        if show_more_lines == 'yes':
            index_start += 5
            index_end += 5
        else:
            break
    

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
