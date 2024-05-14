<h1><ins>Autonomous Learning in Engineering through Gamified Activities on Telegram</ins></h1>

- 🗂️ This repository contains the progress and code of the [IE24.1401 Educational Innovation Project](https://innovacioneducativa.upm.es/proyectos-ie/informacion?anyo=2023-2024&id=1160)

- 🎯 Objective: Allow students to perform self-assessment activities in a more autonomous and approachable way.

<br>

### <ins>Documentation</ins>

 - [Telethon Documentation](https://docs.telethon.dev/en/stable/)
 - [Project Report](https://www.overleaf.com/read/nvbqkrzspbjp#ad7e05)

<br>

### <ins>Requirements</ins>

> [!IMPORTANT]
> We need to have `Python` and the `Telethon` library installed.

We can check if Python is installed and which version by running the following in the terminal/PowerShell:

```bash
python --version
```

If installed, it will return the version (it is recommended to use the same or a newer version):

 `Python 3.12.2`

We also need to install the necessary dependencies, in this case, we only need `Telethon`.
```bash
pip install telethon
```

<br>

### <ins>Clone the repository</ins>

From here on, we will use Visual Code. Once opened, press `Ctrl + Shift + P`.

In the search bar of Visual Code, a ">" will appear. With this, search for the action `Git: Clone`.

It will ask for the repository name (or URL), enter it:

```bash
https://github.com/pedrorj2/Telegram-Gamification-UPM/
```

It will open the explorer to choose a local path to clone the repository.

After doing this, a tab will appear asking to open the repository; accept it.

<br>

### <ins>Deploy the bot</ins>

Once the repository is cloned and opened with Visual Code, we need to fill in the identification data of our bot, which can be seen in the first commented lines. We need to fill them in and uncomment these lines.

```bash
# Configuración de tu API de Telegram
# api_id = ' '
# api_hash = ' '
# bot_token = ' '
```

> [!WARNING]
> You would see a import call like this in my code instead:
> 
> ```bash
> from config import api_id, api_hash, bot_token
> ```
> This makes possible to get this data from `config.py`, file which is not uploaded to the repository, as indicated on the `.gitignore` file.


`api_id` y `api_hash` are obtained by creating a "Telegram Application" through https://my.telegram.org/apps.

`bot_token` is obtained directly from the Telegram app via the [@BotFather](https://t.me/BotFather) bot.
o do this, we need to create a bot, choose its name, and we will get this `bot_token` to access the Telegram HTTP API.

With this, we can run our code, and our computer will host the bot's back-end. As long as it is running, our bot will respond to actions. However, if we close Visual Code, the bot will stop working until we restart it.



