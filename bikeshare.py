import time
import pandas as pd
import difflib

CITY_FILENAMES = {'chicago': 'chicago.csv',
                  'new york city': 'new_york_city.csv',
                  'washington': 'washington.csv'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Validates the inputs and attempts to find close matches.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print('_'*40)
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('\nGiven below is the list of cities with available data:') 
    print('\n'.join(city.title() for city in CITY_FILENAMES.keys()))
    
    while True:
        city = input('\nEnter the name of the city to be analyzed: ')
            
        if city not in CITY_FILENAMES.keys():
            try:
                city = difflib.get_close_matches(city, CITY_FILENAMES.keys())[0]
                print('Filtering data for {}.'.format(city.title()))
                break
            except:
                print('Invalid input, please try again')
        else:
            break
        

    # get user input for month (all, january, february, ... , june)
    months = ['january','february','march','april','may','june','july','august',\
              'september','october','november','december'] 
    while True:
        month = input('\nEnter the month to be analyzed.\n(Input \'all\' if you' +
                  ' would like to analyze entire data): ').lower()
        if month != 'all' and month not in months:
            try:
                month = difflib.get_close_matches(month, months)[0]
                print('Filtering data for {}.'.format(month.title()))
                break
            except:
                print('Invalid input, please try again')
        else:
            break    

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['monday','tuesday','wednesday','thursday','friday','saturday'\
           ,'sunday']
    while True:
        day = input('\nEnter the day to be analyzed. \n(Input \'all\' if you' +
                  ' would like to analyze entire data): ').lower()
        if day != 'all' and day not in days:
            try:
                day = difflib.get_close_matches(day, days)[0]
                print('Filtering data for {}.'.format(day.title()))
                break
            except:
                print('Invalid input, please try again')
        else:
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
    
    df = pd.read_csv(CITY_FILENAMES[city.lower()])    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    if 'month' not in df.columns:
        df['month'] = df['Start Time'].dt.month
        
    if 'weekday' not in df.columns:
        df['weekday'] = df['Start Time'].dt.weekday
        
    months = ['january','february','march','april','may','june','july','august',\
              'september','october','november','december']        
    
    while month != 'all':
        month_n = months.index(month.lower()) + 1
        if month_n in list(df['month']):
            df = df[df['month'] == month_n]
            break
        else:
            avail_months = list(df['month'].value_counts().index -1)
            avail_months.sort()
            print('\nData unavailable for the entered month')
            print('These are the months available in the data:')
            for i in avail_months:
                print(months[i].title())
            month = input('Enter the month to be analyzed. \n' +
                          'Input \'all\' if you would like' +
                          'to analyze the complete data: ').lower()              
            
    if day != 'all':
        days = ['monday','tuesday','wednesday','thursday','friday','saturday'\
                ,'sunday']
        day_n = days.index(day.lower())
        df = df[df['weekday'] == day_n]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['january','february','march','april','may','june','july','august'\
              'september','october','november','december']
    freq_month = df.groupby('month')['month'].count().idxmax() - 1
    print(months[freq_month].title() + ' had the most bikeshares.')

    # display the most common day of week
    days = ['monday','tuesday','wednesday','thursday','friday','saturday'\
            ,'sunday']
    freq_day = df.groupby('weekday')['weekday'].count().idxmax()
    print(days[freq_day].title() + 's had the most bikeshares.')
    
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    freq_hour = df.groupby('hour')['hour'].count().idxmax()
    print('The most bikeshares happened from {}:00 to {}:59.'\
          .format(freq_hour,freq_hour))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    freq_start = df.groupby('Start Station')['Start Station'].count().idxmax()
    print('\'{}\' is the most commonly used start station.'.format(freq_start))
    
    # display most commonly used end station
    freq_end = df.groupby('End Station')['End Station'].count().idxmax()
    print('\'{}\' is the most commonly used end station.'.format(freq_end))

    # display most frequent combination of start station and end station trip
    freq_journey = df.groupby(['Start Station','End Station'])\
        ['Start Station'].count().idxmax()
    print('\'' + '\' to \''.join(freq_journey) + '\' is the most frequent ' +
          'combination of start station and end station trip.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def convert_seconds(total_seconds):
    """ 
    Takes total seconds as input and returns 
    hours, minutes and seconds
    """    
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int((total_seconds % 3600) % 60)
    return hours, minutes, seconds

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    # convert to hours, minutes and seconds
    h, m, s = convert_seconds(total_travel)
    print('A total travel time of {} hour(s) {} minute(s) and {} second(s)'\
          .format(h, m, s) + ' was recorded.')

    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    h, m, s = convert_seconds(mean_travel)
    print('Each trip had an average travel time of ' + 
          '{} hour(s) {} minute(s) and {} second(s)'.format(h, m, s))
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('There are {} types of users in the database:'.format(len(user_types)))
    for user, value in user_types.items():
        print('{} {}(s).'.format(value, user.lower()))
    
    # Display counts of gender
    print('\nGender:')
    try:
        genders = df['Gender'].value_counts()
        for gender, value in genders.items():
            print('{} users were {}.'.format(value, gender.lower()))
    except:
        print('Gender data unavailable for the selected filters.')
    

    # Display earliest, most recent, and most common year of birth
    print('\nAge:')
    try:
        oldest = int(df['Birth Year'].min())
        youngest = int(df['Birth Year'].max())
        freq_age = int(df['Birth Year'].value_counts().idxmax())
        print('Oldest user was born in {}.'.format(oldest))
        print('Youngest user was born in {}.'.format(youngest))
        print('Most common year of birth was {}.'.format(freq_age))
    except:
        print('Birth year data unavailable for the selected filters.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    '''
    Takes a pandas dataframe as input and prints the raw data.
    Prints 10 rows at a time and asks for prompt to continue printing
    '''
    # set option to print all columns in the print statement
    pd.set_option('display.max_columns', None)
    i = 0
    while True:
        print(df.iloc[i:i+5])
        i += 5
        scroll = input('Scroll down? Enter yes or no: ')
        if scroll.lower() not in ['yes','y']:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        raw_data = input('Would you like to see the raw data? Enter yes or no: ')
        if raw_data.lower() in ['yes','y']:
            display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no: ')
        if restart.lower() not in ['yes','y']:
            break


if __name__ == "__main__":
	main()
