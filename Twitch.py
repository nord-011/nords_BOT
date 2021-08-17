import random
import socket
import ssl
import time
import requests
from ssl import SSLContext
from Weather import get_temp

import toml

MODS = 'nord_011', 'tomsomnium1', 'paauulli'
eg_test = 'nord_011', 'okayegbot'
BOT_up = 1

start_time = time.time()

def send(irc: ssl.SSLSocket, message: str):
    irc.send(bytes(f'{message}\r\n', 'UTF-8'))

def send_chat(irc: ssl.SSLSocket, message: str, channel: str):
    send(irc, f'PRIVMSG {channel} :{message}')

def send_pong(irc: ssl.SSLSocket):
    send(irc, 'PONG :tmi.twitch.tv')

def handle_chat(irc: ssl.SSLSocket, raw_message: str):
   try:
    components = raw_message.split()

    user, host = components[0].split('!')[1].split('@')
    channel = components[2]
    message = ' '.join(components[3:])[1:]
    message2 = ' '.join(components[3:])[6:]
    message_no_command = ' '.join(components[4:])
    message_no_command_no_space = ''.join(components[4:])
    plus_message = '+'.join(components[4:])
    underscore_search = '_'.join(components[4:])
    minus_search = '-'.join(components[4:])
    massping_message = ' '.join(components[4:])
    message_components = message.split()

    def massping(text):
        resp = requests.get(f"https://tmi.twitch.tv/group/user/{channel[1:]}/chatters").json()
        chatters = resp["chatters"]["moderators"] + resp["chatters"]["vips"] + resp["chatters"]["viewers"]

        for i in chatters:
            send_chat(irc, f"@{i} {text}", channel)

    if message == '~stop':
        if user == 'nord_011':
            send_chat(irc, f'/me FeelsDankMan 🔧  MrDestructoid BOT is now in maintenance', channel)
            global BOT_up
            BOT_up = BOT_up - 1
        else:
            send_chat(irc, f'NOIDONTTHINKSO', channel)
    if message == '~start':
            if user == 'nord_011':
                send_chat(irc, f'/me \ FeelsDankMan / WEEEEEEEEEE BOT ONLINE', channel)
                BOT_up = BOT_up + 1
            else:
                send_chat(irc, f'NOIDONTTHINKSO', channel)
    if BOT_up < 0:
        BOT_up = 0
    if BOT_up >1:
        BOT_up =1

    if message.lower().__contains__('hurensohn') or message.lower().__contains__('huso') or message.lower().__contains__('hs'):
        send_chat(irc, f'/timeout {user} 15s', channel)
        random_number = random.randint(1, 10)
        if random_number == 1:
            send_chat(irc, f'/me : T D: X I C @{user}', channel)

    if message.__contains__('🖕'):
        send_chat(irc, f'/me : T D: X I C @{user}', channel)


    if message.__contains__('nord') and channel != '#nord_011':
        send_chat(irc, f'DinkDonk "{user}: "{message}" in channel {channel}"', '#nords_bot')

    if message.lower().startswith('~join'):
        write = open('channels.txt', 'a')
        write.write(f'{(message_components[1]).lower()} \n')
        connect_to_channel1 = f'#{message_components[1]}'
        connect_to_channel = connect_to_channel1[0:]
        send(irc, f'JOIN #{message_components[1].lower()}')
        send_chat(irc, f'hackerCD joined channel', channel)
        send_chat(irc, f'hackerCD connected to channel {message_components[1]}', '#nords_bot')
        send_chat(irc, f'hackerCD connected', connect_to_channel)
        write.close()

    if message.__contains__('A Raid Event at Level') and user == 'huwobot':
        file = open('raidusers.txt')
        for users in file:
            print(users)
            send_chat(irc, f'dankClappers  RAID DETECTED!!! {users}', channel)
        file.close()
    if message.lower().startswith('~notifyme raid'):
        file = open('raidusers.txt', 'r')
        read = file.read()
        if f'@{user},' in read:
            send_chat(irc, f"/me FeelsDankMan @{user} you are already registered! If you don't want to be notified anymore, just type '~removeme raid' 4Head", channel)
            file.close()
        else:
            write = open('raidusers.txt', 'a')
            write.write(f'@{user}, ')
            send_chat(irc, f'/me :) 👍 @{user} I will now notify you as soon as a raid appears', channel)
            file.close()
    if message.lower().startswith('~removeme raid'):
        file = open('raidusers.txt', 'r')
        read = file.read()
        if user in read:
            newfile = read.replace(f'@{user}, ', '')
            file2 = open('raidusers.txt', 'w')
            file2.write(newfile)
            send_chat(irc, f'/me :( removed you from the list', channel)
            file2.close()
        else:
            send_chat(irc, f'/me FeelsDankMan you are not registered', channel)
        file.close()


    if message.lower() == '~ping':
        if BOT_up == 1:
            random_number = random.randint(1, 51)
            emoji_list = '🇩🇪', '🇺🇬', '🌈', '🌽', '🌻', '🌭', '🍔', '🐢', '🐶', '🍌', '🍎', '🍒', '🍐', '🥭', '🐱'
            random_emoji = random.choice(emoji_list)
            if random_number < 48:
                now = time.time()
                send_chat(irc, f'PONG! FeelsDankMan WineTime running for: {round((now - start_time) / 60)}{random_emoji}', channel)
            if random_number == 49:
                send_chat(irc, f'PING! FeelsDankMan', channel)
            if random_number == 50:
                send_chat(irc, f'PING￼ THIS￼ docCBT', channel)
            if random_number == 51:
                send_chat(irc, f'/me monkaS bot dead', channel)
        else:
            send_chat(irc, f'FeelsDankMan 🔧 MrDestructoid', channel)
    if message.lower() == '~pong':
        try:
            send_chat(irc, f'PING! FeelsDankMan TeaTime', channel)
            send_chat(irc, f'/me : {user} said "{message}"', '#nords_bot')
        except:
            pass

    if message.startswith('!clear'):
        send_chat(irc, f'◯⸻⸻⸻⸻⸻⸻◯ NaM ◯⸻⸻⸻⸻⸻⸻◯ NaM ◯⸻⸻⸻⸻⸻⸻◯ NaM \
                ◯⸻⸻⸻⸻⸻⸻◯ NaM ◯⸻⸻⸻⸻⸻⸻◯ NaM ◯⸻⸻⸻⸻⸻⸻◯ NaM ◯⸻⸻⸻⸻⸻⸻◯ NaM \
                ◯⸻⸻⸻⸻⸻⸻◯ NaM ◯⸻⸻⸻⸻⸻⸻◯ NaM ◯⸻⸻⸻⸻⸻⸻◯ NaM ◯⸻⸻⸻⸻⸻⸻◯ NaM \
                ◯⸻⸻⸻⸻⸻⸻◯ NaM ◯⸻⸻⸻⸻⸻⸻◯ NaM ◯⸻⸻⸻⸻⸻⸻◯ NaM ◯⸻⸻⸻⸻⸻⸻◯ NaM \
                ◯⸻⸻⸻⸻⸻⸻◯ NaM ◯⸻⸻⸻⸻⸻⸻◯ NaM ◯⸻⸻⸻⸻⸻⸻◯ NaM \◯⸻⸻⸻⸻⸻⸻◯ NaM \
                ◯⸻⸻⸻⸻⸻⸻◯ NaM ◯⸻⸻⸻⸻⸻⸻◯ NaM ◯⸻⸻⸻⸻⸻⸻◯ NaM ◯⸻⸻⸻⸻⸻⸻◯ NaM ', channel)
        time.sleep(0.1)
        send_chat(irc, f'/clear', channel)
        send_chat(irc, f'/me : {user} said "{message}"', '#nords_bot')

    if message == 'FeelsDankMan' and user == 'nord_011':
        send_chat(irc, f'FeelsDankMan', channel)

    if message == 'monkaS':
        propability = random.randint(1, 10)
        if propability == 5:
            send_chat(irc, f'monk ass BillyApprove', channel)
        else:
            pass

    if message.lower() == '~status':
        if user in MODS:
            send_chat(irc, f'{BOT_up}', channel)
        else:
            time.sleep(0.1)

    if message == 'ppAutismo' and user == 'testisttest':
        send_chat(irc, F'ppAutismo', channel)

    if message.__contains__('is now eating:') and user == 'supibot':
        send_chat(irc, f'guhu @{message_components[0]} OpieOP', channel)

    if message == 'asd' and user == 'nord_011':
        random_number = random.randint(1, 5)
        if random_number == 5:
            send_chat(irc, f'/me : FeelsDankMan The autism spectrum encompasses a range of neurodevelopmental conditions,\
            including autism and Asperger syndrome, generally known as autism spectrum disorders (ASD).', channel)
        else:
            pass

    if message.startswith('FeelsDankMan crayonTime') and user == 'nord_011':
        send_chat(irc, f'FeelsDankMan crayonTime', channel)

    if message.startswith('moin') and BOT_up == 1 and user == 'nord_011':
        send_chat(irc, f'FeelsDankMan 👋', channel)
        send_chat(irc, f'/me : {user} said "{message}"', '#nords_bot')

    if message.startswith('WH OMEGA') and BOT_up == 1:
        send_chat(irc, f'WH :D', channel)
        send_chat(irc, f'/me : {user} said "{message}"', '#nords_bot')

    if message.startswith('W H OMEGA') and BOT_up == 1:
        send_chat(irc, f'W H :D', channel)
        send_chat(irc, f'/me : {user} said "{message}"', '#nords_bot')

    if message.startswith('gumo') and BOT_up == 1:
        send_chat(irc, f'FeelsDankMan 👋', channel)
        send_chat(irc, f'/me : {user} said "{message}"', '#nords_bot')

    if message.lower().startswith('~massping'):
        channel_no_hashtag1 = channel.split('#')
        channel_no_hashtag = str(channel_no_hashtag1[1])
        if user == f'{channel_no_hashtag}' or user in MODS:
            try:
                massping(massping_message)
            except:
                return
        else:
            send_chat(irc, f'NOIDONTTHINKSO', channel)
            send_chat(irc, f'/me : {user} said "{message}"', '#nords_bot')
            pass

    if message == '?' and user == 'nord_011':
        send_chat(irc, f'❓ ⠀ ⠀ ⠀ ⠀ ⠀ ❓ ⠀ ⠀ ⠀  ⠀ ⠀ ❓⠀ ⠀ ⠀  ⠀ ⠀ ⠀ ❓ ⠀ ⠀  ⠀ ❓ ⠀ ⠀ ⠀  ⠀ ⠀⠀⠀ ❓ ⠀ ⠀⠀ ⠀ ❓ ⠀ ⠀ ⠀ ⠀ ⠀ \
         ❓ ⠀ ⠀ ⠀❓⠀⠀ FeelsDankMan ...⠀⠀ ❓ ⠀ ⠀ ⠀ ⠀ ❓ ⠀⠀⠀⠀⠀ ❓ ⠀ ⠀ ⠀ ❓ ❓ ⠀ ⠀ ⠀ ❓ 󠀀 󠀀 ', channel)

    if message.startswith('Moin') and BOT_up == 1 and user == 'nord_011':
        send_chat(irc, f'FeelsDankMan 👋', channel)
        send_chat(irc, f'/me : {user} said "{message}"', '#nords_bot')

    if message.startswith('~v'):
        send_chat(irc, f'/timeout @{user} 1s', channel)
        send_chat(irc, f'/me : {user} said "{message}"', '#nords_bot')
    if message.startswith('~vanish'):
        send_chat(irc, f'/timeout @{user} 1s', channel)
        send_chat(irc, f'/me : {user} said "{message}"', '#nords_bot')

    if message.startswith('~') and BOT_up == 1:
        message_components = message.split()
        command = message_components[0][1:]
        print(f'{message}')
        main_channel = '#nords_bot'
        send_chat(irc, f'/me : {user} said "{message}" in channel: "{channel}"', main_channel)

        const_answers = {
            'danking': '/me : FeelsDankMan 🤏 we do a little danking',
            'squid': 'Squid1 FeelsDankMan Squid4',
            'eguero': 'Eguero https://youtu.be/U1fhiP2fjYc?t=132',
            'forsenbased':
                'https://www.reddit.com/r/funny/comments/d4c2n/cake_pan_trade/c0xjhnm/?context=3 \
                MegaLUL BAY ZED',
            'powerup': 'PowerUpL FeelsDankMan PowerUpR',
            'shrug': '¯\_ FeelsDankMan _/¯',
            'id': 'just click your name in chatterino 4Head',
            'tomsomnium1': 'PepeLaugh https://i.imgur.com/RTrJYt5.png',
            'tomsomnium2': 'cmonBruh https://i.nuuls.com/tcW0F.png',
            'pauli': 'https://twitter.com/Nord_011/status/1426592189237313539 FeelsOkayMan',
            'paauulli': 'https://twitter.com/Nord_011/status/1426592189237313539 FeelsOkayMan',
            'help': 'List of all the commands FeelsDankMan 👉 https://github.com/nord-011/nords_BOT',
            'commands': 'List of all the commands FeelsDankMan 👉 https://github.com/nord-011/nords_BOT',
            'bttv': 'bttvNice https://betterttv.com/emotes/shared/search?query={message_components[1]}',
            'ffz': 'FrankerZ https://www.frankerfacez.com/emoticons/?q={message_components[1]}',
            'logs': 'hackerCD https://logs.ivr.fi/?channel={message_components[2]}&username={message_components[1]}',
            'following': '👤 https://twitchfollowing.com/?{message_components[1]}',
            'google': 'hackerCD https://www.google.com/search?q={plus_message}',
            'chatstats': 'hackerCD https://stats.streamelements.com/c/{message_components[1]}',
            'yt': 'hackerCD https://www.youtube.com/results?search_query={plus_message}',
            'twitch': 'imGlitch https://www.twitch.tv/search?term={message_components[1]}',
            'twitchuser': 'imGlitch https://www.twitch.tv/{message_components[1]}',
            'subreddit': 'hackerCD https://www.reddit.com/r/{message_components[1]}/',
            'reddituser': 'hackerCD https://www.reddit.com/u/{message_components[1]}/',
            'reddit': 'hackerCD https://www.reddit.com/search/?q={plus_message}',
            'wiki': 'hackerCD https://en.wikipedia.org/wiki/{underscore_search}',
            'urban': 'hackerCD https://www.urbandictionary.com/define.php?term={plus_message}',
            'duden': 'DatSheffy https://www.duden.de/rechtschreibung/{plus_message}',
            'tts': 'https://www.elunduscore.com/',
            'info': 'https://emotes.raccatta.cc/twitch/{message_components[1]}',
            'user': 'https://emotes.raccatta.cc/twitch/{message_components[1]}',
            'lyrics': 'https://genius.com/{minus_search}-lyrics',
            'emote': 'https://e.wrnv.xyz/{message_components[1]}',
            'age': '/me : nord is {random.randint(1, 100)} years old forsenScoots',
            'madmonq': 'Wow I sure feel energized after taking some MADMONQ ® PogChamp (remove this part of the \
                message when you send this, thanks :) )',
            'selloutsen': 'Wow I sure feel energized after taking some MADMONQ ® PogChamp (remove this part of the \
                message when you send this, thanks :) )'
        }

        if command.lower() in const_answers:
            ans = const_answers[command.lower()]
            send_chat(irc, eval(f"f'{ans}'"), channel)
            return

        if command.lower() == 'moing' and user == 'nord_011':
            send_chat(irc, f'/me : FeelsDankMan 👋', channel)

        if command.lower() == 'say':
            if user == 'nord_011' or user == 'nords_bot':
                if message.startswith('~say channel:'):
                    send_other_chat_var = ' '.join(components[6:])
                    send_chat(irc, f'{send_other_chat_var}', f'#{message_components[2]}')
                else:
                    send_chat(irc, f'{message2}', channel)
            else:
                send_chat(irc, f'NOIDONTTHINKSO', channel)

        if command.lower() == 'send' and user == 'nord_011':
            send_chat(irc, f'{" ".join(message_components[2:])}', f'#{message_components[1]}')

        if command.lower() == 'yil':
            if message.lower() == '~yil':
                send_chat(irc, f'/me dankAngry you have no yil if you keep using the command without a target', channel)
            elif user == message_no_command:
                random_number = random.randint(1, 11)
                if random_number < 10:
                    send_chat(irc, f'/me : you have {random_number} yil forsenBlunder', channel)
                if random_number == 11:
                    random_number2 = random.randint(10000, 90000)
                    send_chat(irc, f'/me : you have {random_number2} yil PogChamp', channel)
            else:
                random_number = random.randint(1, 11)
                if random_number < 10:
                    send_chat(irc, f'/me : {message_no_command} has {random_number} yil forsenBlunder', channel)
                if random_number == 11:
                    random_number2 = random.randint(10000, 90000)
                    send_chat(irc, f'/me : {message_no_command} has {random_number2} yil PogChamp', channel)

        if command.lower() == 'peepo':
            send_chat(irc, f'/me peepoHappy 💊 {user}, {user}, look! the guy with the white van gave me candy!!!', channel)
            time.sleep(5)
            send_chat(irc, f'/me peepoSad {user} my tummy hurts and everything is blurry...', channel)


        if command.lower() == 'pyramid':
            channel_no_hashtag1 = channel.split('#')
            channel_no_hashtag = str(channel_no_hashtag1[1])
            if user == f'{channel_no_hashtag}' or user in MODS:
                pyramid_message1 = " ".join(message_components[2:])
                pyramid_message = f'{pyramid_message1} '
                length = int(message_components[1])
                message_lengh = pyramid_message*length
                if len(message_lengh) > 500:
                    send_chat(irc, f'/me : monkaS max length is 500 characters you madman', channel)
                else:
                    repetitions = 1
                    while repetitions < length:
                        sent_message = pyramid_message * repetitions
                        send_chat(irc, f'{sent_message}', channel)
                        repetitions = repetitions+1
                    else:
                        while repetitions >= 1:
                            sent_message = pyramid_message * repetitions
                            send_chat(irc, f'{sent_message}', channel)
                            repetitions = repetitions-1
            else:
                send_chat(irc, f'NOIDONTTHINKSO', channel)


        if command.lower() == 'weather':
            try:
                capitalized_string = message_components[1].capitalize()
                if message == '~weather':
                    send_chat(irc, f'/me : please provide a city :Z', channel)
                else:
                    send_chat(irc, f'{get_temp(capitalized_string)}', channel)
            except:
                return

        if command.lower() == 'ktoc' or command.lower() == 'kelvin' or command.lower() == 'kelvintocelsius':
            string = message_no_command_no_space.lower()
            if message.lower() == 'ktoc' or message.lower() == 'kelvin' or message.lower() == 'kelvintocelsius':
                send_chat(irc, f'/me : please provide a temp. :Z', channel)
            else:
                try:
                    k_message = string.split('k')
                    calc = float(k_message[0]) - float(273.15)
                    result = round(calc, 2)
                    send_chat(irc, f'{result}°C', channel)
                except:
                    send_chat(irc, f"/me : If there were letters in your temp, i'd be concerned monkaS", channel)
                    return

        if command == 'clear' and user in MODS:
            send_chat(irc, f'◯⸻⸻⸻⸻⸻⸻◯ NaM ◯⸻⸻⸻⸻⸻⸻◯ NaM ◯⸻⸻⸻⸻⸻⸻◯ NaM \
                ◯⸻⸻⸻⸻⸻⸻◯ NaM ◯⸻⸻⸻⸻⸻⸻◯ NaM ◯⸻⸻⸻⸻⸻⸻◯ NaM ◯⸻⸻⸻⸻⸻⸻◯ NaM \
                ◯⸻⸻⸻⸻⸻⸻◯ NaM ◯⸻⸻⸻⸻⸻⸻◯ NaM ◯⸻⸻⸻⸻⸻⸻◯ NaM ◯⸻⸻⸻⸻⸻⸻◯ NaM \
                ◯⸻⸻⸻⸻⸻⸻◯ NaM ◯⸻⸻⸻⸻⸻⸻◯ NaM ◯⸻⸻⸻⸻⸻⸻◯ NaM ◯⸻⸻⸻⸻⸻⸻◯ NaM \
                ◯⸻⸻⸻⸻⸻⸻◯ NaM ◯⸻⸻⸻⸻⸻⸻◯ NaM ◯⸻⸻⸻⸻⸻⸻◯ NaM \◯⸻⸻⸻⸻⸻⸻◯ NaM \
                ◯⸻⸻⸻⸻⸻⸻◯ NaM ◯⸻⸻⸻⸻⸻⸻◯ NaM ◯⸻⸻⸻⸻⸻⸻◯ NaM ◯⸻⸻⸻⸻⸻⸻◯ NaM ', channel)
            time.sleep(0.1)
            send_chat(irc, f'/clear', channel)

        if command.lower() == 'suggest':
            message = ' '.join(components[4:])
            write = open('suggestions.txt', 'a')
            write.write(f'{user}: {message} \n')
            write.close()


        if command.lower() == 'spam':
            channel_no_hashtag1 = channel.split('#')
            channel_no_hashtag = str(channel_no_hashtag1[1])
            if user == f'{channel_no_hashtag}' or user in MODS:
                try:
                    counter = 0
                    message = ' '.join(components[5:])
                    if user == 'nord_011':
                        while counter < int(message_components[1]):
                            send_chat(irc, f'￼ {message}', channel)
                            time.sleep(0.01)
                            counter += 1
                        else:
                            send_chat(irc, f'/me : Befehl ausgeführt, Meister. Erbitte weitere befehle FeelsDankMan 7', channel)
                    elif int(message_components[1]) > 20:
                        time.sleep(1)
                        send_chat(irc, f'/me : maximum is 20 you madman monkaS', channel)
                    else:
                        while counter < int(message_components[1]):
                            send_chat(irc, f'￼ {message}', channel)
                            time.sleep(0.01)
                            counter += 1
                        else:
                            time.sleep(1)
                            send_chat(irc, f'@{user} done ApuApproved', channel)
                except:
                    send_chat(irc, f'/me : please provide a number between 1 and 20 :Z', channel)
            else:
                send_chat(irc, f'NOIDONTTHINKSO', channel)
                pass

        if command.lower() == 'color':
            if user in MODS:
                if message.lower() == '~color random':
                    random_number = random.randint(1, 15)
                    if random_number == 1:
                        send_chat(irc, f'/color Green', channel)
                        send_chat(irc, f'/me FeelsDankMan 👍 color changed', channel)
                    if random_number == 2:
                        send_chat(irc, f'/color Red', channel)
                        send_chat(irc, f'/me FeelsDankMan 👍 color changed', channel)
                    if random_number == 3:
                        send_chat(irc, f'/color Blue', channel)
                        send_chat(irc, f'/me FeelsDankMan 👍 color changed', channel)
                    if random_number == 4:
                        send_chat(irc, f'/color Firebrick', channel)
                        send_chat(irc, f'/me FeelsDankMan 👍 color changed', channel)
                    if random_number == 5:
                        send_chat(irc, f'/color Coral', channel)
                        send_chat(irc, f'/me FeelsDankMan 👍 color changed', channel)
                    if random_number == 6:
                        send_chat(irc, f'/color YellowGreen', channel)
                        send_chat(irc, f'/me FeelsDankMan 👍 color changed', channel)
                    if random_number == 7:
                        send_chat(irc, f'/color OrangeRed', channel)
                        send_chat(irc, f'/me FeelsDankMan 👍 color changed', channel)
                    if random_number == 8:
                        send_chat(irc, f'/color SeaGreen', channel)
                        send_chat(irc, f'/me FeelsDankMan 👍 color changed', channel)
                    if random_number == 9:
                        send_chat(irc, f'/color GoldenRod', channel)
                        send_chat(irc, f'/me FeelsDankMan 👍 color changed', channel)
                    if random_number == 10:
                        send_chat(irc, f'/color Chocolate', channel)
                        send_chat(irc, f'/me FeelsDankMan 👍 color changed', channel)
                    if random_number == 11:
                        send_chat(irc, f'/color CadetBlue', channel)
                        send_chat(irc, f'/me FeelsDankMan 👍 color changed', channel)
                    if random_number == 12:
                        send_chat(irc, f'/color DodgerBlue', channel)
                        send_chat(irc, f'/me FeelsDankMan 👍 color changed', channel)
                    if random_number == 13:
                        send_chat(irc, f'/color HotPink', channel)
                        send_chat(irc, f'/me FeelsDankMan 👍 color changed', channel)
                    if random_number == 14:
                        send_chat(irc, f'/color BlueViolet', channel)
                        send_chat(irc, f'/me FeelsDankMan 👍 color changed', channel)
                    if random_number == 15:
                        send_chat(irc, f'/color SpringGreen', channel)
                        send_chat(irc, f'/me FeelsDankMan 👍 color changed', channel)

                if message.lower() == '~color default':
                    send_chat(irc, f'/color Green', channel)
                    send_chat(irc, f'/me FeelsDankMan 👍 color changed', channel)
                if message.lower() == '~color red':
                    send_chat(irc, f'/color Red', channel)
                    send_chat(irc, f'/me FeelsDankMan 👍 color changed', channel)
                if message.lower() == '~color blue':
                    send_chat(irc, f'/color Blue', channel)
                    send_chat(irc, f'/me FeelsDankMan 👍 color changed', channel)
                if message.lower() == '~color light red':
                    send_chat(irc, f'/color Firebrick', channel)
                    send_chat(irc, f'/me FeelsDankMan 👍 color changed', channel)
                if message.lower() == '~color coral':
                    send_chat(irc, f'/color Coral', channel)
                    send_chat(irc, f'/me FeelsDankMan 👍 color changed', channel)
                if message.lower() == '~color light green':
                    send_chat(irc, f'/color YellowGreen', channel)
                    send_chat(irc, f'/me FeelsDankMan 👍 color changed', channel)
                if message.lower() == '~color orange':
                    send_chat(irc, f'/color OrangeRed', channel)
                    send_chat(irc, f'/me FeelsDankMan 👍 color changed', channel)
                if message.lower() == '~color dark green':
                    send_chat(irc, f'/color SeaGreen', channel)
                    send_chat(irc, f'/me FeelsDankMan 👍 color changed', channel)
                if message.lower() == '~color gold':
                    send_chat(irc, f'/color GoldenRod', channel)
                    send_chat(irc, f'/me FeelsDankMan 👍 color changed', channel)
                if message.lower() == '~color light orange':
                    send_chat(irc, f'/color Chocolate', channel)
                    send_chat(irc, f'/me FeelsDankMan 👍 color changed', channel)
                if message.lower() == '~color petrol':
                    send_chat(irc, f'/color CadetBlue', channel)
                    send_chat(irc, f'/me FeelsDankMan 👍 color changed', channel)
                if message.lower() == '~color light blue':
                    send_chat(irc, f'/color DodgerBlue', channel)
                    send_chat(irc, f'/me FeelsDankMan 👍 color changed', channel)
                if message.lower() == '~color pink':
                    send_chat(irc, f'/color HotPink', channel)
                    send_chat(irc, f'/me FeelsDankMan 👍 color changed', channel)
                if message.lower() == '~color violet':
                    send_chat(irc, f'/color BlueViolet', channel)
                    send_chat(irc, f'/me FeelsDankMan 👍 color changed', channel)
                if message.lower() == '~color green':
                    send_chat(irc, f'/color SpringGreen', channel)
                    send_chat(irc, f'/me FeelsDankMan 👍 color changed', channel)
            else:
                send_chat(irc, f'/me : FeelsDankMan 🖕 nö', channel)

        if command.lower() == 'time':
            random_number = random.randint(1, 100)
            if random_number < 97:
                send_chat(irc, f'/me : FeelsDankMan 🕐 {time.strftime("%I:%M:%S %p")}', channel)
            elif random_number == 98:
                send_chat(irc, f'forsenScoots bottom right on your desktop', channel)
            elif random_number == 99 or 100:
                send_chat(irc, f'/me FeelsDankMan uhm...', channel)
                time.sleep(1)
                send_chat(irc, f'FeelsDankMan .oO( https://www.wikihow.life/Read-a-Clock )', channel)
                time.sleep(10)
                send_chat(irc, f'/me FeelsDankMan 🕐 {time.strftime("%M:%I %p")}?', channel)

        if command.lower() == 'coinflip':
            random_number = random.randint(1, 100)
            if random_number < 49:
                send_chat(irc, f'🪙 Tails! (no)', channel)
            if random_number == 50:
                send_chat(irc, f"FeelsDankMan 🪙 I can't really tell...", channel)
            if random_number > 51:
                send_chat(irc, F'🪙 Heads! (yes)', channel)
            if random_number == 49:
                send_chat(irc, f"FeelsDankMan I lost the coin...", channel)

        if command.lower() == 'cf':
            random_number = random.randint(1, 100)
            if random_number < 49:
                send_chat(irc, f'🪙 Tails! (no)', channel)
            if random_number == 50:
                send_chat(irc, f"FeelsDankMan 🪙 I can't really tell...", channel)
            if random_number > 51:
                send_chat(irc, F'🪙 Heads! (yes)', channel)
            if random_number == 49:
                send_chat(irc, f"FeelsDankMan I lost the coin...", channel)

        if command.lower() == 'yell':
            message_uppercase = message[5:].upper()
            send_chat(irc, f'/me : FeelsDankMan 📣 {message_uppercase}', channel)

        if command.lower() == 'abc':
            if user in MODS:
                for character in "abcdefghijklmnopqrstuvwxy":
                    send_chat(irc, f'/me FeelsDankMan {character}...', channel)
                    time.sleep(0.25)
                send_chat(irc, f'/me FeelsDankMan z...', channel)
            else:
                send_chat(irc,f'/me FeelsDankMan abcdefghijklmnopqrstuvwxyz', channel)

        if command.lower() == 'dababy':
            if message.lower() == '~dababy':
                send_chat(irc, f'👉😂👈 ', channel)
            else:
                send_chat(irc, f'👉 {message_components[1]} 👈 LESSS GOOO', channel)

        if command.lower() == 'pingme':
            random_number = random.randint(1, 20)
            if random_number < 19:
                send_chat(irc, f'FeelsDankMan 👉 @{user}', channel)
            if random_number == 20:
                send_chat(irc, f'FeelsDankMan PONG!', channel)
                time.sleep(0.75)
                send_chat(irc, f'FeelsDankMan uhm...', channel)
                time.sleep(0.75)
                send_chat(irc, F'FeelsDankMan 👉 @{user}', channel)
                time.sleep(0.75)
                send_chat(irc, f'FeelsDankMan 👍 fixed', channel)

        if command.lower() == 'pokeme':
            send_chat(irc, F'FeelsDankMan 👉 @{user}', channel)

        if command.lower() == 'Ping':
            random_number = random.randint(1, 50)
            if random_number < 48:
                send_chat(irc, f'PONG! FeelsDankMan WineTime', channel)
            if random_number == 49:
                send_chat(irc, f'PING! FeelsDankMan', channel)
            if random_number == 50:
                send_chat(irc, f'PING￼ THIS￼ docCBT', channel)

        if command.lower() == 'kiss':
            if message == '~kiss':
                send_chat(irc, f'flushE 💋 ', channel)
            else:
                send_chat(irc, f'flushE 💋 {message_components[1]}', channel)

        if command.lower() =='math' and user == 'nord_011':
            string = message_no_command_no_space
            if len(string.split('*')) != 1:
                pass
            elif len(string.split('+')) != 1:
                numbers = string.split('+')
                result = int(numbers[0]) + int(numbers[1])
                send_chat(irc, result, channel)

        if command.lower() == 'poke':
            if message.startswith('~poke @'):
                if message.lower() == '~poke @':
                    send_chat(irc, f'FeelsDankMan 🖕 no user provided', channel)
                else:
                    send_chat(irc, f'FeelsDankMan 👉 {message_components[1]}', channel)
            else:
                if message.lower() == '~poke':
                    send_chat(irc, f'FeelsDankMan 🖕 no user provided', channel)
                else:
                    send_chat(irc, f'FeelsDankMan 👉 @{message_components[1]}', channel)

        if command.lower() == 'hug':
            if message.lower() == '~hug':
                send_chat(irc, f"FeelsBadMan FBCatch {user} wants to hug someone", channel)
            else:
                send_chat(irc, f':) FBCatch :) {message_components[1]}, {user} wants to give you a warm hug',channel)
                time.sleep(50)
                if message == '~accept' and user == {message_components[1]}:
                    send_chat(irc, f'PogChamp 👉 dankHug')

        if command.lower() == 'shutdown':
            if user == 'nord_011' or user == 'pajlada':
                send_chat(irc, f'FeelsDankMan 👍 verstanden, Meister', channel)
                time.sleep(0.1)
                BOT_up = BOT_up-1
            else:
                send_chat(irc, f'ask @nord_011 or @pajlada :tf:', channel)

        if command.lower() == 'fist':
            if message.lower() == '~fist':
                send_chat(irc, f"/me shoves a fist up your arse VaN 🤜(_(_|", channel)
            else:
                first_word_after_command = ''.join(components[4])
                send_chat(irc, f"/me shoves a fist up {first_word_after_command}'s arse VaN 🤜(_(_|", channel)

        if command.lower() == 'würfel':
            random_number = random.randint(1, 7)
            if random_number == 1:
                send_chat(irc, f'/me : PepeLaugh rate mal', channel)
                time.sleep(3)
                send_chat(irc, f'/me : hast ne Eins MaxLOL', channel)
            if random_number == 2:
                send_chat(irc, f'/me : nur ne Zwei FeelsBadMan .oO( EleGiggle )', channel)
            if random_number == 3:
                if channel.__contains__('tomsomnium1'):
                    send_chat(irc, f'/me : ne 3 du Loser LULE', channel)
                if channel.__contains__('davenetlive'):
                    send_chat(irc, f'/me : ne 3 du Loser LULE', channel)
                if channel.__contains__('nord_011'):
                    send_chat(irc, f'/me : ne 3 du Loser LULW', channel)
                if channel.__contains__('paauulli'):
                    send_chat(irc, f'/me : ne 3 du Loser LULW', channel)
            if random_number == 4:
                send_chat(irc, f'/me : ne Vier sogar SeemsGood', channel)
            if random_number == 5:
                send_chat(irc, f'/me : ne Fünf VisLaud', channel)
            if random_number == 6:
                send_chat(irc, f'/me : PepeLaugh rate mal', channel)
                time.sleep(3)
                send_chat(irc, f'/me : hast ne Sechs PagMan ', channel)
            if random_number == 7:
                send_chat(irc, f'/me : eShrug wo soll ich nen Würfel her haben', channel)

   except Exception as Error:
       try:
        print(Error)
        send_chat(irc, f'NotLikeThis you broke it @{user} / Error: {Error}', channel)
        return
       except:
           print(Error)
           pass


if __name__ == '__main__':
    config = toml.load('config.toml')

    bot_username = config['bot_username']
    channel_name = config['channel_name']
    oauth_token = config['oauth_token']

    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context: SSLContext = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    irc = context.wrap_socket(socket)

    irc.connect(('irc.chat.twitch.tv', 6697))

    send(irc, f'PASS oauth:{oauth_token}')
    send(irc, f'NICK {bot_username}')
    send(irc, f'JOIN #{channel_name}')
    send_chat(irc, f'/me \ FeelsDankMan / WEEEEEEEEE BOT ONLINE', '#nords_bot')

    f = open('channels.txt')
    for channel in f:
        print(channel)
        send(irc, f'JOIN #{channel}')

    while True:
        data = irc.recv(1024)
        irc_raw_message = data.decode('utf-8', errors='replace')

        for line in irc_raw_message.splitlines():
            if line.startswith('PING :tmi.twitch.tv'):
                send_pong(irc)
            else:
                try:
                    components = line.split()
                    command = components[1]
                except:
                    components = line.split()
                    command = components

                if command == 'PRIVMSG':
                    handle_chat(irc, line)


