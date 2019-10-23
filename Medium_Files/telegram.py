########################################################################################################################
# # To get Telegram group/channel information first you need to follow below steps:                                  # #
# #   1. Register to telegram using your mobile number                                                               # #
# #    2. Join the telegram group/channel about which information be to extracted                                    # #
# #      3. Create an app at https://my.telegram.org/apps, and note api_id & api_hash of your telegram               # #
# #  Note: You must have admin privileges to extract telegram channel data                                           # #
########################################################################################################################


from telethon import TelegramClient, sync
import pandas as pd

# ---------------------------------------------------------------------------------------------

api_id = your API ID
api_hash = 'Your API Hash'
phone_number = 'Registered mobile number with country code'
channel_username = 'your channel name'  # Channel name can be found in channel link (https://t.me/CHANNEL_NAME)
# ---------------------------------------------------------------------------------------------


client = TelegramClient('session_name', api_id, api_hash).start()

# You will be asked to enter your mobile number- Enter mobile number with country code
# Enter OTP (For OTP check Telegram inbox)
# ======================================================================================================================
#                                               Getting user details
# ======================================================================================================================
participants = client.get_participants(channel_username)

# This code can be used to extracted upto 10k user's details
# Let's get first name, last name and username
# ---------------------------------------------------------------------------------------------

firstname =[]
lastname = []
username = []
if len(participants):
    for x in participants:
        firstname.append(x.first_name)
        lastname.append(x.last_name)
        username.append(x.username)

# ---------------------------------------------------------------------------------------------
# list to data frame conversion

data ={'first_name' :firstname, 'last_name':lastname, 'user_name':username}

df_user = pd.DataFrame(data)

# ======================================================================================================================
#                                               Getting Chats
# ======================================================================================================================

chats =client.get_messages(channel_username, n) # n = Number of messages to be extracted
message_id = []
message = []
sender = []
reply_to = []
time = []
if len(chats):
    for chat in chats:
        message_id.append(chat.id)
        message.append(chat.message)
        sender.append(chat.from_id)
        reply_to.append(chat.reply_to_msg_id)
        time.append(chat.date)
data ={'message_id':message_id, 'message': message, 'sender_ID':sender, 'reply_to_msg_id':reply_to, 'time':time}
df = pd.DataFrame(data)
messages = df.sort_index(ascending= False)

# ======================================================================================================================
#                                       Searching for messages which contain specific keyword
# ======================================================================================================================
# Get messages and timestamps
messages =[]
time = []
for message in client.iter_messages(channel_username, search='keyword'):
    messages.append(message.message)
    time.append(message.date)
data ={'time':time, 'message':messages}

df = pd.DataFrame(data)

