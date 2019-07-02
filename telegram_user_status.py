import sys
from telethon import TelegramClient, sync
import pandas as pd
from datetime import datetime, timedelta


def user_status(api_id, api_hash, group_name):
    """
    This function can be used to get users who was active in last 24 hours
    :param api_id: Your API ID
    :param api_hash: Your API hash
    :param group_name:  group/channel name
    :return: pandas DataFrame
    """
    client = TelegramClient('session_name', api_id, api_hash).start()

    participants = client.get_participants(group_name)

    time_limit = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')

    user_name = []
    user_status = []

    if len(participants):
        for x in participants:
            try:
                if str(x.status).startswith('UserStatusRecen'):
                    user_name.append(x.first_name)
                    user_status.append('recently')
                elif str(x.status).startswith('UserStatusOnline'):
                    user_name.append(x.first_name)
                    user_status.append('online')
                elif x.status.was_online.strftime('%Y-%m-%d %H:%M:%S') >= time_limit:
                    user_name.append(x.first_name)
                    user_status.append(x.status.was_online.strftime('%Y-%m-%d %H:%M:%S'))
                else:
                    pass
            except:
                pass

    df = pd.DataFrame({'User': user_name, 'status': user_status})
    print('Number of active users in last 24 hours is {}.'.format(df.shape[0]))
    print(df.head(5))


def main():
    user_status(int(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]))


if __name__ == '__main__':
    main()
