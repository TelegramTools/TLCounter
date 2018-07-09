<p align="center">
  <img src="https://raw.githubusercontent.com/TelegramTools/TLCounter/master/images/Intro.png">
 </p>

# TLCounter
This simple python script will count you, in seconds, the total number of messages you have in each of your conversations. It will also divide them in supergroups/channels
and normal groups/single chats. That's all.

## Downloads

You can always find the latest version of the app in the [Releases tab](https://github.com/TelegramTools/TLCounter/releases).

Binaries for Windows are included and bundled as an .exe executable. If you want to use this python script in Mac or Linux, you will be able to, using the compiled binaries under the *bin* folder. Whenever you are running the compiled binary, make sure that you have Python3 installed in your system and also pip. Run this command: `pip install -r requirements.txt` before running the app.

## Building sources

Make sure that you replace the `apiID`, `apiHash` and `password` variables in your own script. Read instructions [here](https://core.telegram.org/api/obtaining_api_id) for getting the `apiID` and `apihash` variables of Telegram.

## Credits

This couldn't be possible without [Telethon](https://github.com/LonamiWebs/Telethon), by Lonami, and a also without [PyInstaller](https://www.pyinstaller.org/) which I used to build the Windows binaries.
You can't imagine how much fun I had while I was using Telethon, kudos for Lonami for making such a great library! The best one out there!

Also, huge acknowledgements to [Telegram](telegram.org) for making such a great messenger!
