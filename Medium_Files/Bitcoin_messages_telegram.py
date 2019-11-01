from telethon import TelegramClient, sync
import pandas as pd
# ---------------------------------------------------------------------------------------------

api_id = Your Api ID  # integer
api_hash = 'Your api hash'  # string

channel_username = ['Altcoins','AlunaCrypto','Argenpool','BFU_Cryptochat','BTCFork','BTCPrivate','BitMaxioEnglishOfficial',
                    'BitSharesDEX','BitcoinAirXBA','BitcoinBravado','BitcoinChat','BitcoinCore','BitcoinCore ','BitcoinGPU ',
                    'BitcoinTradingUS','Bitex_Global_Ico_Official','CoinDesk','CoinParliament','ColuLocalNetworkChat','ComTrust',
                    'Counterparty','CryptoCharters','CryptoCoinCoach','CryptoMarketWallStreet','CryptoMining','Crypto_World_News',
                    'Cryptogene','DeCenterOrg','Decred','DigiByteCoin','DigixDAO', 'ICOInsiderCommunity','Kucoin_Exchange','Neo_Blockchain',
                    'NxtCommunity','OmniLayer','Peerplays','PikcioChain','Ripple','SolarexICO','TheCoinFather','ZCashco','altcoin','asianwhales',
                    'aworkerio','binanceexchange','bitcoin','bitcoinbing1','bitcoinchannel','bitcoingold','bitcoinitalia','bitcoinitalia ','blockchainedindia',
                    'blockchainlifeofficial','blockchains','blockmason','btccom','bytecoinchat','chronobank','civicplatform','cobinhood','coindesk_news',
                    'coinfarm','coingeckonews', 'coingeckoofficial','coinmarketcap','creativechain','decentch','dentcoin','dfinity','district0x','essentia_one',
                    'icocountdown','icospeaks','icospeaksnews','litecoin','monacoin','monero','mysterium_network','nemred','pascalcoin','pemburu_bitcoin','sirinlabs',
                    'teambitcoindaily','thecoinfarm','thriveico','tokenmarket','tradingcryptocoach','ukcrypto','utoday_en','whatsoncrypto','www_Bitcoin_com']
client = TelegramClient('session_name', api_id, api_hash).start()

messages =[]
time = []
for i in range(len(channel_username)):
    for message in client.iter_messages(channel_username[i], search='bitcoin'):
        messages.append(message.message)
        time.append(message.date)

    for message in client.iter_messages(channel_username[i], search='btc'):
        messages.append(message.message)
        time.append(message.date)
data = {'time': time, 'message': messages}
df = pd.DataFrame(data)
df = df.drop_duplicates().reset_index(drop=True)
df.to_csv('tele_btc_messages.csv', index= False)

