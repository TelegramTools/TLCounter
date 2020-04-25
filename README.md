<p align="center">
  <img src="https://raw.githubusercontent.com/TelegramTools/TLCounter/master/images/Intro.png">
 </p>

# TLCounter
This tool counts the total number of messages that you have in each of your conversations. It will also divide them in supergroups/channels
and normal groups/single chats.

## Download

You can always grab the latest version heading over the [releases tab](https://github.com/TelegramTools/TLCounter/releases).
I built binaries for **Windows (64 bits)**, **Linux amd64** and **Linux armhf**

* On **Windows**: Simply double click on the ``.exe`` file
* On **Linux**: Download the binary, ``cd`` to the folder where the download is located and do ``chmod +x TLCounter-xxx && ./TLCounter-xxx``

If you're running other systems (like MacOS), you will need to **build the files from source**.

## Build from sources

Make sure that you replace the ``api_id`` and ``api_hash`` variables in the ``TLCounter.py`` file.
Read instructions [here](https://core.telegram.org/api/obtaining_api_id) for getting your own from Telegram.

## Credits

This couldn't be possible without [Telethon](https://github.com/LonamiWebs/Telethon), by Lonami.

Thanks to the [PyInstaller](https://www.pyinstaller.org/) team for their great tool, which I used to build the binaries.

Also, huge acknowledgements to [Telegram](telegram.org) for making such a great messenger!

**Give always credits to all the original authors and owners when using some parts of their hard work in your own projects**