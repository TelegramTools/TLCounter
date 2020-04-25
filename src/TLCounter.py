#!/usr/bin/python3
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.errors import FloodWaitError
from telethon.utils import get_peer_id, get_input_peer, get_display_name
from telethon.tl.types import Chat, User, Channel
from datetime import datetime
from time import sleep
from sys import exit
from getpass import getpass
from os import remove, path
import logging
import progressbar
import sqlite3

version = "2.0"
TotalDialogs = 0
UserCount = 0
ChannelCount = 0
SupCount = 0
ConvertedGroupsIDs = []
NewGroupsIDs = []
NumChannel = 0
NumUser = 0
NumChat = 0
NumSuper = 0
UserId = None
api_id = YOUR_API_ID_HERE
api_hash = 'YOUR API HASH HERE'
TLdevice_model = 'Desktop device'
TLsystem_version = 'Console'
TLapp_version = '- TLCounter ' + version
TLlang_code = 'en'
TLsystem_lang_code = 'en'
client = TelegramClient('UserSession', api_id, api_hash, device_model=TLdevice_model, system_version=TLsystem_version, app_version=TLapp_version, lang_code=TLlang_code, system_lang_code=TLsystem_lang_code)

def sprint(string, *args, **kwargs):
    """Safe Print (handle UnicodeEncodeErrors on some terminals)"""
    try:
        print(string, *args, **kwargs)
    except UnicodeEncodeError:
        string = string.encode('utf-8', errors='ignore')\
                       .decode('ascii', errors='ignore')
        print(string, *args, **kwargs)

def DBConnection(first, close):
    conn = sqlite3.connect("TLCounter-UserData.db")
    CreateTables(conn)
    if first is True:
        print("Created database successfully!")
    if close is True:
        conn.close()
        return
    else:
        return conn

def CreateTables(db):
    global version
    try:
        cursor = db.cursor()
        cursor.execute('''
        CREATE TABLE Version(AppName TEXT, AppVersion TEXT, CreationDate TEXT, LastUpdated TEXT)''')
        db.commit()
        date = str(datetime.today())
        reg = ("TLCounter", version, date, None)
        db.execute("INSERT INTO Version VALUES(?,?,?,?)", reg)
        db.commit()
    except:
        pass

def GatherHistory(*args, **kwargs):
    try:
        return client.get_messages(*args, **kwargs, limit=0).total
    except FloodWaitError as e:
        print("We have reached a flood limitation. Waiting for " + str(datetime.timedelta(seconds=e.seconds)))
        sleep(e.seconds)
        GatherHistory(*args, **kwargs)
    except Exception as e:
        logging.exception("TLCOUNTER EXCEPTION IN GatherHistory: " + str(e))
        logging.exception("ENTITY: " + str(*args, **kwargs))
        print("Something went wrong in Telegram's side. This is the full exception:\n\n" + str(e))
        input("Press ENTER to try again the request and continue counting the messages...")
        GatherHistory(*args, **kwargs)
    return

def SendRequest(*args, **kwargs):
    try:
        return client(*args, **kwargs)
    except FloodWaitError as e:
        print("We have reached a flood limitation. Waiting for " + str(datetime.timedelta(seconds=e.seconds)))
        sleep(e.seconds)
        SendRequest(*args, **kwargs)
    except Exception as e:
        logging.exception("TLCOUNTER EXCEPTION IN SendRequest: " + str(e))
        logging.exception("ENTITY: " + str(*args, **kwargs))
        print("Something went wrong in Telegram's side. This is the full exception:\n\n" + str(e))
        input("Press ENTER to try again the request and continue counting the messages...")
        SendRequest(*args, **kwargs)
    return

def StartCount(dialogs):
    global TotalDialogs, UserCount, ChannelCount, UserId, ConvertedGroupsIDs, NewGroupsIDs, NumChannel, NumUser, NumChat, \
        NumSuper, SupCount, version
    CachedSupergroups = []
    FirstRun = None
    database = DBConnection(False, False)
    db1 = database.cursor()
    db1.execute('SELECT * FROM Version')
    for row in db1:
        if row[3] is None:
            FirstRun = True
        else:
            FirstRun = False
    if FirstRun is True:
        cursor = database.cursor()
        cursor.execute('''CREATE TABLE GroupsInfo(SuperGroupID INTEGER PRIMARY KEY, OldGroupID INTEGER)''')
        date = str(datetime.today())
        reg5 = (date,)
        database.execute("UPDATE Version SET LastUpdated=?", reg5)
        database.commit()
    else:
        date = str(datetime.today())
        reg5 = (date, version)
        database.execute("UPDATE Version SET LastUpdated=?, AppVersion=?", reg5)
        database.commit()
        db3 = database.cursor()
        db3.execute('SELECT * FROM GroupsInfo')
        for row in db3:
            CachedSupergroups.append(row[0])
    print("\nChecking and processing each chat's data before counting...")
    UserId = client.get_me().id
    for dialog in dialogs:
        client.get_input_entity(dialog)
        if isinstance(dialog.entity, Chat):
            NumChat = NumChat + 1
        if isinstance(dialog.entity, User):
            NumUser = NumUser + 1
        if isinstance(dialog.entity, Channel):
            if dialog.entity.megagroup == True:
                NumSuper = NumSuper + 1
            else:
                NumChannel = NumChannel + 1

    completed = 0
    bar = progressbar.ProgressBar(max_value=NumSuper, widget=None, poll_interval=1)
    bar.update(completed)
    for dialog in dialogs:
        if isinstance(dialog.entity, Channel):
            if dialog.entity.megagroup == True:
                ID1 = get_peer_id(get_input_peer(dialog, allow_self=False))
                strid = str(ID1).replace("-100", "")
                ID = int(strid)
                if ID not in CachedSupergroups:
                    gotChatFull = SendRequest(GetFullChannelRequest(client.get_input_entity(ID1)))
                    reg = (gotChatFull.full_chat.id, gotChatFull.full_chat.migrated_from_chat_id)
                    database.execute("INSERT INTO GroupsInfo VALUES(?,?)", reg)                    
                completed = completed + 1
                bar.update(completed)
    try:
        database.commit()
    except:
        pass
    LookIds = []
    for dialog in dialogs:
        ID = None
        try:
            ID = get_peer_id(get_input_peer(dialog, allow_self=False))
        except:
            ID = UserId
        if isinstance(dialog.entity, Channel):
            strid = str(ID).replace("-100", "")
            ID = int(strid)
        elif isinstance(dialog.entity, Chat):
            strid = str(ID).replace("-", "")
            ID = int(strid)
        LookIds.append(ID)
    for dialog in dialogs:
        if isinstance(dialog.entity, Channel):
            if dialog.entity.megagroup == True:
                ID1 = get_peer_id(get_input_peer(dialog, allow_self=False))
                strid = str(ID1).replace("-100", "")
                ID = int(strid)
                db3 = database.cursor()
                db3.execute('SELECT * FROM GroupsInfo WHERE SuperGroupID={id}'.\
                    format(id=ID))
                for row in db3:
                    if row[1] is not None:
                        NewGroupsIDs.append(row[0])
                        ConvertedGroupsIDs.append(row[1])
    bar.finish()
    DBConnection(False, True)
    print("\nAll is ready. Counting your chats: ")
    print()
    for dialog in dialogs:
        ID = None
        try:
            ID = get_peer_id(get_input_peer(dialog, allow_self=False))
        except:
            ID = UserId
        if isinstance(dialog.entity, Channel):
            strid = str(ID).replace("-100", "")
            ID = int(strid)
        elif isinstance(dialog.entity, Chat):
            strid = str(ID).replace("-", "")
            ID = int(strid)
        if get_display_name(dialog.entity) == "":
            name = "Deleted Account"
        elif ID == UserId:
            name = "***--Chat with yourself (Saved Messages)--***"
        else:
            name = get_display_name(dialog.entity)
        if ID not in ConvertedGroupsIDs:
            count = GatherHistory(client.get_input_entity(dialog))
            if isinstance(dialog.entity, Channel):
                sprint(' {}: {}'.format(name, count) + " *")
                if dialog.entity.megagroup == True:
                    SupCount = SupCount + count
                else:
                    ChannelCount = ChannelCount + count
            elif isinstance(dialog.entity, (Chat, User)):
                sprint(' {}: {}'.format(name, count))
                UserCount = UserCount + count
        if ID in NewGroupsIDs:
            if (ID not in LookIds) and (ID in ConvertedGroupsIDs):
                logging.warning("NOT PRESENT ID IN DIALOGS: " + str(ID))
                continue
            else:
                index = NewGroupsIDs.index(ID)
                #DEBUG: logging.warning("ID: " + str(int("-" + str(ConvertedGroupsIDs[index]))))
                OldChatCount = GatherHistory(client.get_input_entity(int("-" + str(ConvertedGroupsIDs[index]))))
                print("· !--> You also have ", OldChatCount, " messages before '" + name + "' was converted into a supergroup.")
                UserCount = UserCount + OldChatCount

##ENTRY POINT OF THE CODE
try:
    remove("TLCounter-log.log")
except:
    pass
logging.basicConfig(filename="TLCounter-log.log", level=logging.DEBUG, format='%(asctime)s %(message)s')
logging.warning("THIS IS CORRECTLY BEING LOGGED!")
print("Welcome to Telegram Chat Counter! This app made by ferferga will count the total number of messages in your account.\n")
print("\n")
if not client.is_connected():
    while True:
        print("Connecting to Telegram...")
        client.connect()
        if not client.is_connected():
            getpass("A connection to Telegram couldn't be established. Press ENTER to try again: ")
        else:
            break
    if not client.is_user_authorized():
        client.start(force_sms=False)
        while True:
            if not client.is_user_authorized():
                getpass("The phone, or the code you typed is invalid, because you couldn't log in.\nPress ENTER to try again: ")
            if client.is_user_authorized():
                print("\nSuccessfully logged in!")
                break
        try:
            remove("TLCounter-UserData.db")
        except:
            pass
        DBConnection(True, False)
    else:
        if path.isfile("TLCounter-UserData.db"):
            DBConnection(False, False)
        else:
            DBConnection(True, False)
    
me = client.get_me()
if me.username is None:
    print ('You are logged in as ' + me.first_name + ' (+' + me.phone + ')')
else:
    print ('You are logged in as ' + me.first_name + ' (' + me.username + '). Your phone is +' + me.phone)

print("Getting your chat list...")
dialogs = client.get_dialogs(limit=None)
print('You have', dialogs.total, 'chats. Processing...')
print()
StartCount(dialogs)
TotalDialogs = UserCount + ChannelCount + SupCount
ConvertedCount = len(NewGroupsIDs)
NumChat = NumChat - ConvertedCount
print("\n\n")
print("-----------------------------------------------------")
print("| TOTAL COUNTS                                       |")
print("· Normal groups and chats:", UserCount)
print("· Channels:", ChannelCount)
print("· Supergroups:", SupCount)
print("· TOTAL MESSAGES:", TotalDialogs)
print()
print("-----------------------------------------------------")
print("| OTHER INTERESTING DETAILS                          |")
print("· Number of Channels:", NumChannel)
if ConvertedCount != 0:
    print("· Number of Supergroups:", NumSuper, "(", ConvertedCount, "of those groups have been converted from normal groups to supergroups)")
else:
    print("· Number of Supergroups:", NumSuper)
print("· Number of Normal groups:", NumChat)
print("· Number of conversations with individual users:", NumUser)
print("\n\nCOUNTED COMPLETED! OPTIONS:")
while True:
    print("\nDo you want to log out of TLCounter? If you want to count your messages frequently, you might want to keep your session logged in.")
    print("> Available commands: ")
    print("  !1: Log out")
    print("  !Q: Close the program without logging out.")
    print()
    answer = str(input("Enter a command: "))
    answer = answer.replace(" ", "")
    answer = answer.upper()
    if not (answer == '!Q' or answer == '!1'):
        while True:
            print()
            answer = input("The command you entered was not valid. Please, enter a valid one: ")
            answer.replace(" ", "")
            answer.upper()
            if (answer == "!Q") or (answer == "!1"):
                break
    if (answer == "!Q"):
        client.disconnect()
        exit(0)
    if (answer == "!1"):
        print("Logging you out of Telegram...")
        client.log_out()
        getpass("Done! Press ENTER to close TLCounter!: ")
        exit(0)
