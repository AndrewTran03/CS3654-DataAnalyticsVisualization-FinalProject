import csv, twint, time, pandas, io, sys, warnings
from datetime import datetime, timedelta

class TwitterManager():
    '''
    When initialized, suppress warnings. Don't want to console
    to be spammed by pandas warnings
    '''
    def __init__(self):
        warnings.filterwarnings("ignore")
        return
    '''
    Using ids present in the twitter_human_bots_dataset,
    search twitter for tweets from those IDs and store certain information
    about them in a DataFrame, which is later
    converted into a csv file.
    '''
    def get_data(self):
        fileName = 'twitter_human_bots_dataset.csv'
        whole_table = pandas.DataFrame()
        total_length = len(pandas.read_csv(fileName))
        with open(fileName) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='\n')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                    continue
                data = row[0].split(',')
                id = data[0]
                self.disable_printing()
                '''
                Attempting to get twitter data for an id
                '''
                try:
                    time.sleep(1)
                    table = self.find_tweets_with_id(id)
                except Exception as e:
                    self.enable_printing()
                    print("[" + str(line_count) + " / " + str(total_length) + "]")
                    line_count += 1
                    print("Error getting tweets for " + id + ".  Skipping and continuing")
                    print(e)
                    continue
                self.enable_printing()
                print("[" + str(line_count) + " / " + str(total_length) + "]")
                line_count += 1
                if table.empty:
                    continue
                table['bot_or_human'] = data[1]
                if whole_table.empty:
                    whole_table = table
                else:
                    whole_table = pandas.concat([whole_table, table])
        whole_table.to_csv('twitter_data.csv')
    '''
    Helper function for get_data. This function
    specifically handles getting information from twitter.
    '''
    def find_tweets_with_id(self, id):
        endingTime = self.datetime_to_string(datetime.now())
        #endingTime = self.datetime_to_string(end)
        startingTime = "2021-01-01"
        c = twint.Config()
        #c.Search = id
        c.Since = startingTime
        c.Until = endingTime
        c.Limit = 5
        c.Store_object = True
        c.Lang = 'en'
        c.Pandas = True
        c.User_id = id
        twint.run.Search(c)
        table = twint.storage.panda.Tweets_df
        if table.empty:
            return table
        return table[['id', 'tweet', 'hashtags', 'cashtags', 'user_id', 'nlikes', 'nreplies', 'nretweets']]
    '''
    This simple helper function is for
    convenience of converting the current datetime to
    the correct string for the twint API call.
    '''
    def datetime_to_string(self, date):
        return date.strftime("%Y-%m-%d")
    '''
    Disables printing to the console. This function
    was made in order to supress twints console printing, which
    it does every time it gets data from twitter.

    This gets annoying, so I disable it.
    '''
    def disable_printing(self):
        trap = io.StringIO()
        sys.stdout = trap
        return
    '''
    Re-Enables printing to the console.
    '''
    def enable_printing(self):
        sys.stdout = sys.__stdout__
        return
