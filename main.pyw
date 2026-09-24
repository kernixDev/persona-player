import pygame
import pygame_gui
import os
from mutagen.easyid3 import EasyID3
from mutagen.id3 import APIC, ID3
from PIL import Image, ImageFilter
from mutagen.mp3 import MP3
import threading
import random
from pypresence import *
from pypresence.types import *
import asyncio
import aiohttp
import json

pygame.mixer.init()

try:
    with open('config.json', 'r') as file:
        jsondata = json.load(file)
    application_id = jsondata[0]["application_id"]
    rpc = Presence(application_id)
    rpc.connect()
except:
    pass

async def geticon():
    if discord_enabled == False:
        return

    url = "https://api.imgbb.com/1/upload"
    params = {
    "expiration": 600,
    "key": "",
    }

    form = aiohttp.FormData()

    with open("assets\\cover.jpg", "rb") as f:
        form.add_field(
            "image",
            f,
            filename="image.png",
            content_type="image/png",
        )

        async with aiohttp.ClientSession() as session:
            async with session.post(url, params=params, data=form) as response:
                result = await response.json()
                return(result["data"]["display_url"])

def upd(content, artist):
    if not discord_enabled:
        return

    def do_update():
        try:
            icon = asyncio.run(geticon())

            if not icon:
                icon = "https://ibb.co/JJYHjWc"

            rpc.update(
                large_image=icon,
                name=artist if artist else "Persona Player",
                activity_type=ActivityType.LISTENING,
                state=artist if artist else "Unknown",
                details=content if content else "Unknown",
            )

        except Exception as e:
            print(e)

    threading.Thread(target=do_update, daemon=True).start()

def play(file):
    f = f"{file}"
    pygame.mixer.music.load(f)
    pygame.mixer.music.play()

def rewind():
    pygame.mixer.music.rewind()

def unpause():
    pygame.mixer.music.unpause()

def pause():
    pygame.mixer.music.pause()

def waitforinput():
    input()
    pygame.mixer.music.stop()

os.system('cls')
def start(file):
    music_thread = threading.Thread(target=play, args=[file,])
    input_thread = threading.Thread(target=waitforinput)
    music_thread.start()
    input_thread.start()

pygame.init()

SCREEN_WIDTH = 300
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_icon(pygame.image.load('assets/icon.png'))

font = pygame.font.SysFont(None, 20)
smallerfont = pygame.font.SysFont(None, 15)
timefont = pygame.font.SysFont(None, 17)
background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
background.fill((0, 0, 0))

manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

music_files = [f for f in os.listdir('music') if f.endswith('.mp3')]
songs = []
for f in music_files:
    try:
        audio = EasyID3(f'music\\{f}')
        artist = str(audio['artist'][0]) if 'artist' in audio else "Unknown"
    except:
        artist = "Unknown"
    songs.append({
        'filename': "music\\" + f,
        'artist': artist,
        'title': f.replace('.mp3', '')
    })

g = random.randint(0, len(songs)-1)
start(songs[g]['filename'])
def title(g, i):
    artist = songs[g]['artist']
    titlesong = songs[g]['filename'].split("\\", 1)[1]
    titlesong = titlesong.replace(".mp3", "")

    artist = songs[g]['artist']
    titlesong = songs[g]['filename'].split("\\", 1)[1]
    titlesong = titlesong.replace(".mp3", "")

    audioicon = ID3(songs[g]['filename'])
    for tag in audioicon.values():
        if isinstance(tag, APIC):
            with open('assets/cover.jpg', 'wb') as img:
                img.write(tag.data)
            break

    update_cover()
    if discord_enabled == True and i == True:
        upd(titlesong, artist)
    pygame.display.set_caption(f"{titlesong} - {artist}")

paused = False
menu = 'player'

UIButton = pygame_gui.elements.UIButton
search_btn = UIButton(pygame.Rect(20, 20, 30, 30), "", manager, object_id="#invisible_button")
search_icon = pygame.image.load('assets/search.png').convert_alpha()
search_icon = pygame.transform.scale(search_icon, (20, 20))
search_btn.colours['normal_bg'] = pygame.Color(0, 0, 0, 0)
search_btn.colours['hovered_bg'] = pygame.Color(0, 0, 0, 0)
search_btn.colours['active_bg'] = pygame.Color(0, 0, 0, 0)
search_btn.rebuild()

last_btn = None
next_btn = None
pause_btn = None
random_btn = None
random_enabled = False
loop_btn = None
loop_enabled = False
discord_btn = None
discord_enabled = True
y = 0

shuffle_icon = pygame.image.load('assets/shuffle.png').convert_alpha()
shuffle_icon = pygame.transform.scale(shuffle_icon, (30, 30))

loop_icon = pygame.image.load('assets/loop.png').convert_alpha()
loop_icon = pygame.transform.scale(loop_icon, (30, 30))

discord_icon = pygame.image.load('assets/discord.png').convert_alpha()
discord_icon = pygame.transform.scale(discord_icon, (30, 30))

search_entry = None
search_container = None
search_buttons = []
prev_query = ""
cover = None
blurcover = None

def update_cover():
    global cover

    try:
        with Image.open('assets/cover.jpg') as coverimg:
            blurcover = coverimg.filter(ImageFilter.BLUR)
            blurcover.save('assets/cover_blur.jpg')

        cover = pygame.image.load('assets/cover_blur.jpg').convert()
        cover = pygame.transform.scale(
            cover,
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )

    except Exception as e:
        print(f"Failed to update cover: {e}")

clock = pygame.time.Clock()
is_running = True
title(g, True)

while is_running:
    
    time_delta = clock.tick(60)/1000.0
    screen.blit(background, (0, 0))
    mx, my = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame.KEYDOWN:
            if menu == 'player':
                if event.key == 32:
                    paused = not paused
                    if paused:
                        artist = songs[g]['artist']
                        titlesong = songs[g]['filename'].split("\\", 1)[1]
                        titlesong = titlesong.replace(".mp3", "")
                        title(g, False)
                        pygame.mixer.music.pause()
                    else:
                        title(g, False)
                        pygame.mixer.music.unpause()

                elif event.key == 1073741903:
                    if not random_enabled:
                        g = (g + 1) % len(songs)
                    elif random_enabled:
                        g = random.randint(0, len(songs)-1)
                    title(g, True)
                    start(songs[g]['filename'])
                    paused = False

                elif event.key == 1073741904:
                    g = (g - 1) % len(songs)
                    title(g, True)
                    start(songs[g]['filename'])
                    paused = False

                elif event.key == 114:
                    random_enabled = not random_enabled

                    if random_enabled:
                        random_btn.colours['normal_bg'] = pygame.Color("#32CD32")
                        random_btn.colours['hovered_bg'] = pygame.Color("#3EE63E")
                        random_btn.colours['active_bg'] = pygame.Color("#2DB82D")

                    else:
                        random_btn.colours['normal_bg'] = pygame.Color("#B22222")
                        random_btn.colours['hovered_bg'] = pygame.Color("#CC3333")
                        random_btn.colours['active_bg'] = pygame.Color("#A11F1F")

                    random_btn.rebuild()

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == search_btn:
                menu = 'search' if menu == 'player' else 'player'

            elif event.ui_element == next_btn:
                if not random_enabled:
                    g = (g + 1) % len(songs)
                elif random_enabled:
                    g = random.randint(0, len(songs)-1)
                title(g, True)
                start(songs[g]['filename'])
                paused = False

            elif event.ui_element == last_btn:
                g = (g - 1) % len(songs)
                title(g, True)
                start(songs[g]['filename'])
                paused = False

            elif event.ui_element == pause_btn:
                paused = not paused
                if paused:
                    artist = songs[g]['artist']
                    titlesong = songs[g]['filename'].split("\\", 1)[1]
                    titlesong = titlesong.replace(".mp3", "")
                    title(g, False)
                    pygame.mixer.music.pause()
                else:
                    title(g, False)
                    pygame.mixer.music.unpause()

            elif event.ui_element == random_btn:
                random_enabled = not random_enabled

                if random_enabled:
                    random_btn.colours['normal_bg'] = pygame.Color("#32CD32")
                    random_btn.colours['hovered_bg'] = pygame.Color("#3EE63E")
                    random_btn.colours['active_bg'] = pygame.Color("#2DB82D")

                else:
                    random_btn.colours['normal_bg'] = pygame.Color("#B22222")
                    random_btn.colours['hovered_bg'] = pygame.Color("#CC3333")
                    random_btn.colours['active_bg'] = pygame.Color("#A11F1F")
                random_btn.rebuild()
                
            elif event.ui_element == loop_btn:
                loop_enabled = not loop_enabled
                
                if not loop_enabled:
                    loop_btn.colours['normal_bg'] = pygame.Color("#B22222") 
                    loop_btn.colours['hovered_bg'] = pygame.Color("#CC3333")
                    loop_btn.colours['active_bg'] = pygame.Color("#A11F1F") 
                else:
                    loop_btn.colours['normal_bg'] = pygame.Color("#32CD32")
                    loop_btn.colours['hovered_bg'] = pygame.Color("#3EE63E")
                    loop_btn.colours['active_bg'] = pygame.Color("#2DB82D")
                loop_btn.rebuild()

            elif event.ui_element == discord_btn:
                try:
                    discord_enabled = not discord_enabled

                    if not discord_enabled:
                        rpc.close()
                        discord_btn.colours['normal_bg'] = pygame.Color("#B22222") 
                        discord_btn.colours['hovered_bg'] = pygame.Color("#CC3333")
                        discord_btn.colours['active_bg'] = pygame.Color("#A11F1F") 
                    else:
                        rpc.connect()
                        title(g, True)
                        discord_btn.colours['normal_bg'] = pygame.Color("#32CD32")
                        discord_btn.colours['hovered_bg'] = pygame.Color("#3EE63E")
                        discord_btn.colours['active_bg'] = pygame.Color("#2DB82D")
                except:
                    pass
                discord_btn.rebuild()

            elif menu == 'search':
                for btn, song in search_buttons:
                    if event.ui_element == btn:
                        g = [s['filename'] for s in songs].index(song['filename'])
                        start(song['filename'])
                        title(g, True)
                        menu = 'player'
                        paused = False
                        break

        manager.process_events(event)

    manager.update(time_delta)

    if menu == 'player':
        if search_entry:
            search_entry.kill()
            search_entry = None

        if search_container:
            search_container.kill()
            search_container = None
            search_buttons.clear()

        if last_btn is None:
            last_btn = UIButton(pygame.Rect(50, 250, 60, 60), "<", manager)
            next_btn = UIButton(pygame.Rect(190, 250, 60, 60), ">", manager)
            pause_btn = UIButton(pygame.Rect(115, 245, 70, 70), "Pause", manager)
            random_btn = UIButton(pygame.Rect(85, 350, 40, 40), "", manager)
            if not random_enabled:
                random_btn.colours['normal_bg'] = pygame.Color("#B22222") 
                random_btn.colours['hovered_bg'] = pygame.Color("#CC3333")
                random_btn.colours['active_bg'] = pygame.Color("#A11F1F") 
            else:
                random_btn.colours['normal_bg'] = pygame.Color("#32CD32")
                random_btn.colours['hovered_bg'] = pygame.Color("#3EE63E")
                random_btn.colours['active_bg'] = pygame.Color("#2DB82D")
            random_btn.rebuild()
            
            loop_btn = UIButton(pygame.Rect(130, 350, 40, 40), "", manager)
            if not loop_enabled:
                loop_btn.colours['normal_bg'] = pygame.Color("#B22222") 
                loop_btn.colours['hovered_bg'] = pygame.Color("#CC3333")
                loop_btn.colours['active_bg'] = pygame.Color("#A11F1F") 
            else:
                loop_btn.colours['normal_bg'] = pygame.Color("#32CD32")
                loop_btn.colours['hovered_bg'] = pygame.Color("#3EE63E")
                loop_btn.colours['active_bg'] = pygame.Color("#2DB82D")
            loop_btn.rebuild()

            discord_btn = UIButton(pygame.Rect(175, 350, 40, 40), "", manager)
            if not discord_enabled:
                discord_btn.colours['normal_bg'] = pygame.Color("#B22222") 
                discord_btn.colours['hovered_bg'] = pygame.Color("#CC3333")
                discord_btn.colours['active_bg'] = pygame.Color("#A11F1F") 
            else:
                discord_btn.colours['normal_bg'] = pygame.Color("#32CD32")
                discord_btn.colours['hovered_bg'] = pygame.Color("#3EE63E")
                discord_btn.colours['active_bg'] = pygame.Color("#2DB82D")
            discord_btn.rebuild()

        artist = songs[g]['artist']

        if cover:
            screen.blit(cover, (0, 0))

        artist_text = smallerfont.render(f"Artist - {artist}", True, (255, 255, 255))
        screen.blit(artist_text, artist_text.get_rect(center=(SCREEN_WIDTH/2, 238)))

        playing_text = font.render(f"Now Playing - {songs[g]['title']}", True, (255, 255, 255))
        screen.blit(playing_text, playing_text.get_rect(center=(SCREEN_WIDTH/2, 225)))

        pygame.draw.rect(screen, (0,0,0), [10, 325, SCREEN_WIDTH-20, 20])
        song_info = MP3(songs[g]['filename'])
        progress = pygame.mixer.music.get_pos() / 1000
        progress_width = int((progress / song_info.info.length) * (SCREEN_WIDTH - 20))
        pygame.draw.rect(screen, (65,105,225), [10, 325, progress_width, 20])

        if not paused:
            mins = int(progress // 60)
            secs = int(progress % 60)
            time_text = f"{mins}:{secs:02d}"
        else:
            time_text = "Paused"

        timeplayed = timefont.render(time_text, True, (255,255,255))
        screen.blit(timeplayed, timeplayed.get_rect(center=(SCREEN_WIDTH/2, 320)))

    elif menu == 'search':
        screen.blit(cover, (0, 0))
        if last_btn:
            last_btn.kill()
            next_btn.kill()
            pause_btn.kill()
            random_btn.kill()
            loop_btn.kill()
            discord_btn.kill()
            last_btn = next_btn = pause_btn = discord_btn = None

        if search_entry is None:
            search_entry = pygame_gui.elements.UITextEntryLine(pygame.Rect(60,20,220,30), manager)
        if search_container is None:
            search_container = pygame_gui.elements.UIScrollingContainer(pygame.Rect(20,60,260,320), manager)

        query = search_entry.get_text().lower()
        if query == "":
            query = " "

        if query != prev_query:
            prev_query = query
            for btn, _ in search_buttons:
                btn.kill()
            search_buttons.clear()
            y = 0
            search_results = [s for s in songs if query in s['title'].lower() or query in s['artist'].lower()]
            for song in search_results:
                btn = UIButton(pygame.Rect(0, y, 260, 30), f"{song['title']} - {song['artist']}", manager, container=search_container.get_container())
                search_buttons.append((btn, song))
                y += 30

    progress = pygame.mixer.music.get_pos() / 1000
    if progress >= song_info.info.length - 0.4:
        if loop_enabled:
            pass
        elif not random_enabled:
            g = (g + 1) % len(songs)
        elif random_enabled:
            g = random.randint(0, len(songs)-1)
        
        title(g, True if loop_enabled == False else False)
        start(songs[g]['filename'])
        paused = False

    manager.draw_ui(screen)

    if menu == 'player' and random_btn is not None:
        screen.blit(shuffle_icon, (random_btn.rect.x + 5, random_btn.rect.y + 5))
        screen.blit(loop_icon, (loop_btn.rect.x + 5, loop_btn.rect.y + 5))
        screen.blit(discord_icon, (discord_btn.rect.x + 5, discord_btn.rect.y + 5))

    screen.blit(search_icon, (search_btn.rect.x + 5, search_btn.rect.y + 5))
    pygame.display.update()
