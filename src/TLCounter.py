from telethon import *
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.errors import FloodWaitError
import telethon
from telethon.utils import *
from telethon.tl.functions.messages import *
import sys
import datetime

TotalDialogs = 0
UserCount = 0
ChannelCount = 0
ConvertedGroupsIDs = []
NewGroupsIDs = []
NumChannel = 0
NumUser = 0
NumChat = 0
NumSuper = 0
UserId = None
api_id = ##INSERT YOUR APIID HERE
api_hash = ##INSERT YOUR APIHASH HERE
TLdevice_model = 'Desktop device'
TLsystem_version = 'Console'
TLapp_version = '- TLCounter 1.1'
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

def GatherHistory(chat):
    try:
        return client.get_messages(chat, limit=0).total
    except FloodWaitError as e:
        print("We have reached a flood limitation. Waiting for " + str(datetime.timedelta(seconds=e.seconds)))
        time.sleep(e.seconds)
        GatherHistory(chat)
    except Exception as e:
        print("Something went wrong in Telegram's side. This is the full exception:\n\n" + str(e))
        input("Press ENTER to try again the request and continue counting the messages...")
        GatherHistory(chat)

def StartCount(dialogs):
    global TotalDialogs
    global UserCount
    global ChannelCount
    global UserId
    global ConvertedGroupsIDs
    global NewGroupsIDs
    global NumChannel
    global NumUser
    global NumChat
    global NumSuper
    print("\nChecking and processing each chat's data before counting...")
    UserId = client.get_me().id
    for dialog in dialogs:
        client.get_input_entity(dialog.entity)
        if isinstance(dialog.entity, Chat):
            NumChat = NumChat + 1
        if isinstance(dialog.entity, User):
            NumUser = NumUser + 1
        if isinstance(dialog.entity, Channel):
            NumChannel = NumChannel + 1
            if dialog.entity.megagroup == True:
                NumSuper = NumSuper + 1
                gotChatFull = client(GetFullChannelRequest(dialog.entity))
                if gotChatFull.full_chat.migrated_from_chat_id is not None:
                    ConvertedGroupsIDs.append(gotChatFull.full_chat.migrated_from_chat_id)
                    NewGroupsIDs.append(gotChatFull.full_chat.id)
    NumChannel = NumChannel - NumSuper
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
            name = "!--Chat with yourself (Saved Messages)--!"
        else:
            name = get_display_name(dialog.entity)
        if ID not in ConvertedGroupsIDs:
            count = GatherHistory(dialog)
            sprint(' {}: {}'.format(name, count))
            if isinstance(dialog.entity, Channel):
                ChannelCount = ChannelCount + count
            elif isinstance(dialog.entity, (Chat, User)):
                UserCount = UserCount + count
        if ID in NewGroupsIDs:
            index = NewGroupsIDs.index(ID)
            OldChatCount = GatherHistory(ConvertedGroupsIDs[index])
            print("· !--> You also have ", OldChatCount, " messages before '" + name + "' was converted into a supergroup.")
            UserCount = UserCount + OldChatCount

##ENTRY POINT OF THE CODE

print("Welcome to Telegram Chat Counter! This app made by ferferga will count the total number of messages in your account.\n")
print("Loading...")
client.start(force_sms=False)
me = client.get_me()
if me.username is None:
    print ('You are logged in as ' + me.first_name + ' (+' + me.phone + ')')
else:
    print ('You are logged in as ' + me.first_name + ' (' + me.username + '). Your phone is +' + me.phone)

print("Getting your chat list...")
dialogs = client.get_dialogs(limit=None)
print('You have ', dialogs.total, ' chats. Processing...')
print()
StartCount(dialogs)
TotalDialogs = UserCount + ChannelCount
print("\n\n")
print("-----------------------------------------------------")
print("| TOTAL COUNTS                                       |")
print("· Normal groups and chats: ", UserCount)
print("· Channels and supergroups: ", ChannelCount)
print("· TOTAL MESSAGES: ", TotalDialogs)
print()
print("-----------------------------------------------------")
print("| OTHER INTERESTING DETAILS                          |")
print("· Number of converted groups to supergroups: ", len(NewGroupsIDs))
print("· Number of Channels: ", NumChannel)
print("· Number of Supergroups: ", NumSuper)
print("· Number of Normal groups: ", NumChat)
print("· Number of conversations with individual users: ", NumUser)
print("\n\n")
print("If you reach 1 million messages with Users and normal groups, old messages will be archived in your account, but NEVER deleted.\nThat means that they will not be accessible using any client, but you will be able to access them only if you delete some recent messages.\nThat's a Telegram's limitation, unfortunately.")
print("\nChannels and supergroups have their own 1 million message limit, thus, they don't count against your account's quota.")
while True:
    print("\n\nDo you want to log out of TLCounter? If you want to count your messages frequently, you might want to keep your session logged in.")
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
        input("Done! Press ENTER to close TLCounter! ")
        sys.exit(0)
    if (answer == "!1"):
        print("Logging you out of Telegram...")
        client.log_out()
        input("Done! Press ENTER to close TLCounter! ")
        sys.exit(0)