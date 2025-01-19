from telethon.sync import TelegramClient
import pandas as pd
from datetime import datetime, timezone
import time

start_time_full = time.time()

api_id = 'enter_your_id'
api_hash = "enter_your_hash"
phone = '+enter_your_phone_accosiated_with_telegram_account'
username = "enter_your_telegram_username"

channels_data = pd.read_csv('Links.csv') # file with links to channels is provided in this repo as well
links = channels_data['Link'].tolist()


war_start = datetime(2022, 02, 24, tzinfo=timezone.utc)
#end_date = datetime(2024, 1, 27, tzinfo=timezone.utc)
#channel_stat = pd.read_csv('channel_stat.csv')
c_st = []

ch_id, m_id, dates, messages, views = [], [], [], [], []
counter = 0
with TelegramClient(username, api_id, api_hash) as client:
    for channel in links:
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        start_time = time.time()
        print('Channel # ', counter, 'started at: ', current_time)
        for message in client.iter_messages(channel):
            #if message.date >= war_start and message.date <= end_date and type(message.text) == str and len(message.text) >= 3:
            if message.date >= war_start and type(message.text) == str and len(message.text) >= 3:
                # print('HERE IS A POST: ', message.text)
                ch_id.append(message.peer_id.channel_id)
                m_id.append(message.id)
                dates.append(message.date)
                messages.append(message.text)
                #views.append(message.views)
        counter += 1
                #counter += 1
                #if counter == 5:
                #    break
        ch = channel[13:]
        print('Channel name: ', ch)
        #ch_name = f"{ch}_02-23-2022--12-31-2022_API.csv"
        ch_name = f"{ch}_01-01-2023--01-01-2023_API.csv"
        data = pd.DataFrame(
            #zip(ch_id, m_id, dates, messages, views),
            #columns=['Channel ID', 'Post ID', 'Date', 'Post', 'Views']
            zip(ch_id, m_id, dates, messages),
            columns=['Channel ID', 'Post ID', 'Date', 'Post']
            )
        data.to_csv('./Channels/' + ch_name, index=False)
        c_st.append(len(data))
         #print(data)

        end_time = time.time()
        print('====> Finished processing after: ', round((end_time - start_time)/60, 2), ' minutes with ', len(data), ' posts.')

#ch_stat = pd.DataFrame(channel_stat)
df = pd.DataFrame({'Column1': c_st})
channel_stat = pd.concat([channel_stat, df], ignore_index=True)
channel_stat.to_csv('channel_stat.csv')
end_time_full = time.time()
elapsed_time = end_time_full - start_time_full

print(f"Elapsed time: {round(elapsed_time/60)} minutes")
