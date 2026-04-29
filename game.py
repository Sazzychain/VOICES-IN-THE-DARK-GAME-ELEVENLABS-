import os
import random
import time

import pygame
from dotenv import load_dotenv

from audio import generate_voice

load_dotenv()

pygame.init()
pygame.mixer.init()

# 🖥️ Bigger screen
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Voices in the Dark")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

# 🎯 Player
player_pos = [WIDTH // 2, HEIGHT // 2]

# 🎭 Voices system
voices = [
    {
        "text": "Move left now...",
        "direction": "LEFT",
        "type": "calm",
        "voice": os.getenv("VOICE_CALM"),
    },
    {
        "text": "Go right quickly!",
        "direction": "RIGHT",
        "type": "panic",
        "voice": os.getenv("VOICE_PANIC"),
    },
    {
        "text": "Stay still... do not move...",
        "direction": "NONE",
        "type": "dark",
        "voice": os.getenv("VOICE_DARK"),
    },
]

current_voice = None
voice_timer = 0
command_time = 0

# ⏱️ 5-second reaction window
reaction_time_limit = 5

score = 0
game_over = False


# 🔊 voice generator
def play_voice():
    global current_voice, command_time

    current_voice = random.choice(voices)

    filename = f"voice_{random.randint(1, 10000)}.mp3"

    generate_voice(current_voice["text"], current_voice["voice"], filename)

    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    command_time = time.time()


# 🔁 reset system
def reset_game():
    global player_pos, score, game_over, current_voice
    player_pos = [WIDTH // 2, HEIGHT // 2]
    score = 0
    game_over = False
    current_voice = None


running = True

while running:
    screen.fill((0, 0, 0))

    # 🧠 EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 🔁 restart after failure
        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            reset_game()

    keys = pygame.key.get_pressed()

    moved = False
    old_pos = player_pos.copy()

    if not game_over:
        # ⏱️ check timeout (5 seconds)
        if current_voice:
            if time.time() - command_time > reaction_time_limit:
                game_over = True

        # 🎮 movement
        if keys[pygame.K_LEFT]:
            player_pos[0] -= 5
            moved = True

        if keys[pygame.K_RIGHT]:
            player_pos[0] += 5
            moved = True

        if keys[pygame.K_UP]:
            player_pos[1] -= 5
            moved = True

        if keys[pygame.K_DOWN]:
            player_pos[1] += 5
            moved = True

        # 🎯 scoring logic
        if current_voice and moved:
            if current_voice["type"] == "calm" and current_voice["direction"] != "NONE":
                score += 10

            elif current_voice["type"] == "panic":
                score += 5

            elif current_voice["type"] == "dark":
                score -= 5

            # 🌑 DARK VOICE SPECIAL RULE
            if current_voice["type"] == "dark" and moved:
                game_over = True

            play_voice()

    # 🔊 first trigger
    if not current_voice and not game_over:
        play_voice()

    # 🎨 PLAYER DRAW
    if game_over:
        pygame.draw.circle(screen, (255, 0, 0), player_pos, 10)  # red
    else:
        pygame.draw.circle(screen, (255, 255, 255), player_pos, 10)  # white

    # 🟢 SCORE DISPLAY
    score_text = font.render(f"Score: {score}", True, (0, 255, 0))
    screen.blit(score_text, (20, 20))

    # ❌ GAME OVER SCREEN
    if game_over:
        msg = font.render("Tap to Try Again", True, (255, 0, 0))
        screen.blit(msg, (WIDTH // 2 - 160, HEIGHT // 2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
