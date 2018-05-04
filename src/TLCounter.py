from telethon import *
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.errors import FloodWaitError
import telethon
from telethon.utils import *
from telethon.tl.functions.messages import *
import sys

TotalDialogs = 0
UserCount = 0
ChannelCount = 0
api_id = ##ADD YOU APID HERE
api_hash = '' ##ADD YOUR APIHASH HERE
TLdevice_model = 'Desktop device'
TLsystem_version = 'Console'
TLapp_version = '- TLCounter 1.0'
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
        print("We have reached a flood limitation. Waiting for ", e.seconds)
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
    for dialog in dialogs:
        count = GatherHistory(dialog)
        if get_display_name(dialog.entity) == "":
            name = "Deleted Account"
        else:
            name = get_display_name(dialog.entity)
        sprint('{}: {}'.format(name, count))
        client.get_input_entity(dialog.entity)
        if isinstance(dialog.entity, Channel):
            ChannelCount = ChannelCount + count
            gotChatFull = client(GetFullChannelRequest(dialog.entity))
            if gotChatFull.full_chat.migrated_from_chat_id is not None:
                OldChatCount = client.get_messages(gotChatFull.full_chat.migrated_from_chat_id, limit=0).total
                print("\nYou also have ", OldChatCount, " messages before '" + name + "' was converted into a supergroup.")
                UserCount = UserCount + OldChatCount
                TotalDialogs = TotalDialogs + OldChatCount
                
        elif isinstance(dialog.entity, (Chat, User)):
            UserCount = UserCount + count
        TotalDialogs = TotalDialogs + count

##ENTRY POINT OF THE CODE

print("Welcome to Telegram Chat Counter! This app made by ferferga will count the total number of messages in your account.\n")
print("Loading...")
client.start(force_sms=False)
me = client.get_me()
if me.username is None:
    print ('You are logged in as ' + me.first_name + ' (+' + me.phone + ')')
else:
    print ('You are logged in as ' + me.first_name + ' (' + me.username + '). Your phone is +' + me.phone)

dialogs = client.get_dialogs(limit=None)
print('You have ', dialogs.total, ' chats. Counting ', len(dialogs), ' chats now...')
print()
StartCount(dialogs)
print("\n\nYou have in total ", TotalDialogs, " messages in your account.")
print()
print("Of those ", TotalDialogs, " messages, ", UserCount, " were from chats with other users and normal groups; ", ChannelCount, " messages were from channels and supergroups.")
print("\n\n")
print("Take in mind that, if you reached 1 million messages with Users and normal groups, old messages will be archived in your account, but NEVER deleted. That means that they will not be accessible using any client, and you will be able to access them only if you delete some messages. That's a Telegram's limitation, unfortunately")
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