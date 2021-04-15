import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# List of cities the user can choose from
cities = ['chicago', 'new york city', 'washington']

# List of months the user can choose from (not case sensitive!)
months = ['january', 'february', 'march', 'april', 'may', 'june','all']

# The days the user can choose from (not case sensitive, using the 3 first characters will not work!)
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday','all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input('Input the name of the city to analyze:').lower()
            if city not in cities:
                print('-'*40)
                print('This city is not available.\nAvailable cities are: Chicago, New York City and Washington.\n')
                print('Please try again!')
                print('-'*40)
                continue

    # get user input for month (all, january, february, ... , june)
            month = input('Input the name of the month to filter by, or "all" to apply no month filter:').lower()
            if month not in months:
                print('-'*40)
                print('This month is not available.\nAvailable months are: January, February, March, April, May and June.\n')
                print('Please try again!')
                print('-'*40)
                continue

    # get user input for day of week (all, monday, tuesday, ... sunday)
            day = input('Input the name of the day of week to filter by, or "all" to apply no day filter:').lower()
            if day not in days:
                print('-'*40)
                print('This day is not available.\nAvailable days are: Monday, Tuesday, Wednesday, Thursday and Friday.\n')
                print('Please try again!')
                print('-'*40)
                continue
            else:
                print('-'*40)
                print('Got valid user info - Thank you!')
                break

        except ValueError:
            print('\n')
            print('This is not a valid input')

        except KeyboardInterrupt:
            print('\n')
            print('Thank you for your time!\nSee you next time.')
            break

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
    df['day_of_week'] = df['Start Time'].dt.day_name()


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
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    print("Most Frequent Month (only applicable if month = 'all'):", months[popular_month - 1].title())

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print("Most common day of week (only applicable if day = 'all'):", popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Frequent Start Hour:', popular_hour)
    print('-'*40)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most frequently used Start Station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most frequently used End Station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    popular_end_start_combination = df.groupby(['Start Station','End Station']).size().nlargest(1)
    print('Most frequent Start and End Station combination:\n', popular_end_start_combination)
    print('-'*40)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time in hours:',round((total_travel_time)/60)/60),2

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Average travel time in minutes:',round((mean_travel_time)/60)),2
    print('-'*40)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Count users by user type:\n',user_types)
    print()

    # Display counts of gender
    try:
        gender_types = df['Gender'].value_counts()
        print('Count users by gender type:\n',gender_types)
        print()
        print('The number of missing user information for gender type:', df.isnull().sum().sum())
        print()
    except KeyError:
        print('No gender data available for the given month and day')

    # Display earliest, most recent, and most common year of birth
    try:
        min_birth_year = int(df['Birth Year'].min())
        print('The earlest year of birth within users:',min_birth_year)
        print()
    except KeyError:
        print('No birth data available for the given month and day')

    try:
        max_birth_year = int(df['Birth Year'].max())
        print('The most recent year of birth within users:',max_birth_year)
        print()
    except KeyError:
        print('No birth data available for the given month and day')

    try:
        mode_birth_year = int(df['Birth Year'].mode())
        print('The most common year of birth within users:',mode_birth_year)
    except KeyError:
        print('No birth data available for the given month and day')

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)


def show_data(df):

    row_count = df.shape[0]

    # iterate from 0 to the number of rows counting by 5
    for i in range(0, row_count, 5):

        # asks for user input
        show = input("Do you want to see raw trip data?.\nAnswer with 'yes' or 'no':")
        if show.lower() != 'yes':
            break

        # print rows from data_frame from i to i + 5 rows
        data = df.iloc[i: i + 5]
        print(data)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
