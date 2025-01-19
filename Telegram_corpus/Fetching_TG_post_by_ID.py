from telethon.sync import TelegramClient
import pandas as pd
from datetime import datetime, timezone
import time

# Telegram API credentials
api_id = 'add_yours'
api_hash = 'add_yours'
phone = 'add_yours'
username = 'add_yours'

# Load channel and post IDs from CSV file
channel_data = pd.read_csv('corpus_full.csv') # provided in this repository
#channel_data = channel_data[:100] # uncomment this if you want to test this with a smaller portion first

# Initialize lists to store fetched data
ch_id, m_id, dates, messages = [], [], [], []

# Fetch messages based on channel ID and post ID
with TelegramClient(username, api_id, api_hash) as client:
    for index, row in channel_data.iterrows():
        try:
            channel_id = int(row['Channel ID'])
            post_id = int(row['Post ID'])

            message = client.get_messages(entity=channel_id, ids=post_id)

            if message and message.text:
                ch_id.append(channel_id)
                m_id.append(post_id)
                dates.append(message.date)
                messages.append(message.text)

                print(f"Fetched post {post_id} from channel {channel_id}")
            else:
                print(f"Post {post_id} from channel {channel_id} not found or empty.")

        except Exception as e:
            print(f"Error fetching post {post_id} from channel {channel_id}: {e}")
            continue  # Skip to the next post if an error occurs

# Save the results to a CSV file
data = pd.DataFrame(
    zip(ch_id, m_id, dates, messages),
    columns=['Channel ID', 'Post ID', 'Date', 'Post']
)

data.to_csv('Fetched_Posts.csv', index=False)

print(f"Successfully fetched {len(data)} posts.") # may want to comment this line out when fetching large volume
