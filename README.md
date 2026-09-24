# Persona Player - MP3 / Music player
**Persona Player** is a MP3 file player built in python using the [pygame](https://www.pygame.org/news) package, it has a **discord** rich presence feature which you can turn on and off with the click of a button, it has every features you would expect from a basic mp3 player


Example usage of this script:

<img width="298" height="427" alt="image" src="https://github.com/user-attachments/assets/7cc9892e-fa8f-4139-8706-7a3293fe32eb" />

## 💡 Prerequisite
[Python 3](https://www.python.org/downloads/release/python-3123/)

## 🛠️ Installation

### With Github

```bash
git clone https://github.com/PersonaMind/persona-player/
cd persona-player
pip install -r requirements.txt
```


After cloning the repository, you will need to add mp3 files into the **/music** folder. 
Then, you're free to run **main.py** and use the MP3 player as you wish.

[How can I get mp3 files of my favourite songs using spotify?](https://github.com/PersonaMind/persona-player/tree/main#-how-can-i-extract-my-spotify-songs-into-mp3-files-to-play-locally)

## 🔨 Features


| Feature               | Note
| --------------------- |-----------------------------------------------------------|
| Search Feature        |                                                           |
| Skip to next song     |                                                           |
| Skip to last song     |                                                           |
| Discord Rich Presence | You will need to set it up, you can find a guide [here](https://github.com/PersonaMind/persona-player?tab=readme-ov-file#%EF%B8%8F-discord-activity) |
| Clean UI              | Make sure your songs have an icon in order to use it in the background |

## ⚙️ Discord Activity

Example: 

<img width="253" height="169" alt="Screenshot 2025-10-25 192548" src="https://github.com/user-attachments/assets/eb411621-a06d-4605-94da-055835b5ba4f" />


If you wish to use the discord RPC feature, you will need to follow these steps

### Create an application

You will need to go to [discord's developer portal](https://discord.com/developers/applications) and log in, then press "New Application". After that, copy your Application's ID (it should look like: 0000000000000000000). Open config.json using any file editor and put your Application ID in the dictionary.

## 🎵 How can I extract my spotify songs into mp3 files to play locally?

I will soon release a script that allows you to download your spotify playlists, when I do I will put a link to it in this section.
