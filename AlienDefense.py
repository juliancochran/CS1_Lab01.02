# my first Pygame game, stop the things from killing the dude
__author__ = 'Julian Cochran'
__version__ = '02/12/2025'

# My flint sessions are here:
#https://app.flintk12.com/activity/pygame-debug-le-1fe068/session/1d1aee84-0644-4ab7-8f61-758eec2076ef
#https://app.flintk12.com/activity/pygame-debug-le-1fe068/session/94728db7-1385-4b65-9224-f4a36e9e9d67


# thia is a change I'm making


import pygame
import os
import random

from Bullet import Bullet
from Enemy import *
from HighScore import *

# loads high scores into a list, returns the list
def load_high_scores():
    f = open('highscores.txt')
    scores = []
    for line in f:
        temp = line.split(' ')
        scores.append(HighScore(temp[0], int(temp[1])))
    f.close()
    scores.sort(reverse=True)
    return scores

# After your main game loop ends, assuming the score qualifies for high score list:
def get_initials(screen, font, score, WINDOW_WIDTH, WINDOW_HEIGHT):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    initials = ''
    max_chars = 3  # Limit to 3 characters for initials
    input_active = True

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None  # Player quit game

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(initials) > 0:
                    input_active = False  # Enter key confirms if we have input
                elif event.key == pygame.K_BACKSPACE:
                    initials = initials[:-1]  # Remove last character
                else:
                    # Only allow letters and limit to max_chars
                    if len(initials) < max_chars and event.unicode.isalpha():
                        initials += event.unicode.upper()

        # Clear screen and draw
        screen.fill(BLACK)

        # Display score
        score_text = font.render(f'NEW HIGH SCORE: {score}!', True, WHITE)
        screen.blit(score_text, (WINDOW_WIDTH / 2 - score_text.get_width() / 2, WINDOW_HEIGHT / 2 - 60))

        # Display instructions
        instruction_text = font.render('ENTER YOUR INITIALS:', True, WHITE)
        screen.blit(instruction_text, (WINDOW_WIDTH / 2 - instruction_text.get_width() / 2, WINDOW_HEIGHT / 2 - 20))

        # Display current input (with cursor)
        cursor = '_' if len(initials) < max_chars else ''
        input_text = font.render(initials + cursor, True, WHITE)
        screen.blit(input_text, (WINDOW_WIDTH / 2 - input_text.get_width() / 2, WINDOW_HEIGHT / 2 + 20))

        # Display enter instruction
        if len(initials) > 2:
            enter_text = font.render('PRESS ENTER TO CONTINUE', True, WHITE)
            screen.blit(enter_text, (WINDOW_WIDTH / 2 - enter_text.get_width() / 2, WINDOW_HEIGHT / 2 + 60))

        pygame.display.flip()

    return initials

def spawn_enemies(level, WINDOW_WIDTH, WINDOW_HEIGHT):
    # build enemies here
    enemies = []
    for i in range(10):
        enemies.append(Enemy(random.randint(20, (WINDOW_WIDTH - 50)), -80, WINDOW_HEIGHT))
        enemies[i].set_speed(0, random.randint(4+level, 7+level))
    return enemies

# main method of the program
def main():
    # Initialize Pygame
    pygame.init()
    pygame.mixer.init()

    # Set up the display
    WINDOW_WIDTH = 600
    WINDOW_HEIGHT = 900
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("+ AlIeN dEfEnSe +")
    # Create the clock object
    clock = pygame.time.Clock()
    FPS = 60  # Set your desired frames per second
    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    # keep track of the score
    SCORE = 50
    # font to draw score to the screen
    font = pygame.font.SysFont("Arial Bold", 46)
    # maintain a list of enemy objects
    level = 0
    enemies = spawn_enemies(level, WINDOW_WIDTH, WINDOW_HEIGHT)
    highscores = load_high_scores()

    # Load the image
    try:
        # Load the image
        spaceship_img = pygame.image.load('img/spaceship.png')
        # Optional: if you want to resize the image
        # image = pygame.transform.scale(image, (desired_width, desired_height))
        # Get the rectangle from the image
        spaceship_rect = spaceship_img.get_rect()
        # Position the rect at the center of the screen
        spaceship_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT-80)
        # Load the sound file
        # Note: Replace 'beep.wav' with your actual sound file
        sound_effect = pygame.mixer.Sound('sound/laser.wav')
        boom = pygame.mixer.Sound('sound/boom1.wav')

    except pygame.error as e:
        print(f"Couldn't load external files: {e}")
        return  # Exit the function if image loading fails

    enemy_on_screen = False

    # bullet
    bullet = None

    # MAIN GAME LOOP
    running = True
    while running:
        # Limit the frame rate
        clock.tick(FPS)
        # is the enemies list empty? If yes, re-spawn and make it faster
        if len(enemies) == 0:
            level += 1
            enemies = spawn_enemies(level, WINDOW_WIDTH, WINDOW_HEIGHT)
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(spaceship_rect.x+25, spaceship_rect.y, WINDOW_HEIGHT)
                    sound_effect.play()

        # if there are no enemies on the screen, make one start moving
        if not enemy_on_screen:
            enemy_on_screen = True
            enemies[random.randint(0, len(enemies) - 1)].moving = True

        # Clear the screen
        screen.fill(BLACK)
        # Get the current state of all keyboard buttons
        # clamp image to screen
        # move left or right
        keys = pygame.key.get_pressed()
        spaceship_rect.clamp_ip(screen.get_rect())
        if keys[pygame.K_LEFT]:
            spaceship_rect.move_ip(-4,0)
        if keys[pygame.K_RIGHT]:
            spaceship_rect.move_ip(5,0)

        # drop the enemies from random places
        for enemy in enemies:
            if enemy.moving:
                enemy.move(0, enemy.speed_y)
                enemy.draw(screen)
                if enemy.is_off_screen():
                    enemy_on_screen = False
                    enemies.remove(enemy)
                    running = False
                if bullet is not None and enemy.rect.colliderect(bullet.rect):
                    enemy.die()
                    enemy.draw(screen)
                    enemies.remove(enemy)
                    enemy_on_screen = False
                    bullet = None
                    SCORE += 1
                    boom.play()
        if bullet is not None:
            bullet.update()
            bullet.draw(screen)
        screen.blit(spaceship_img,spaceship_rect)
        # draw text to the screen
        scoredisplay = font.render(str(SCORE), True, WHITE)
        screen.blit(scoredisplay, (WINDOW_WIDTH-80, 20))
        # Update the display
        pygame.display.flip()

    # MAIN GAME LOOP ENDS
    running = True
    high_score_handled = False  # Add this flag
    # SECONDARY END GAME LOOP DISPLAY
    while running:
        if not high_score_handled and SCORE > highscores[-1].score:  # is score > last high score?
            player_initials = get_initials(screen, font, SCORE, WINDOW_WIDTH, WINDOW_HEIGHT)
            if player_initials:
                new_high_score = HighScore(player_initials, SCORE)
                highscores.append(new_high_score)
                highscores.sort(reverse=True)
                del highscores[-1]  # lop off the last high score
            high_score_handled = True  # Set flag to True after handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                running = False
        screen.fill(BLACK)
        scoredisplay = font.render('FINAL SCORE: ' + str(SCORE), True, WHITE)
        screen.blit(scoredisplay, (WINDOW_WIDTH / 2 - 120, 50))

        # Display HIGH SCORES header
        header = font.render('HIGH SCORES', True, WHITE)
        screen.blit(header, (WINDOW_WIDTH / 2 - header.get_width() / 2, 150))

        # Display high scores - using a smaller font
        small_font = pygame.font.SysFont("Arial Bold", 32)
        y_pos = 220  # Starting y position for high scores
        for i, score in enumerate(highscores):
            # Highlight the player's new score if it exists
            color = WHITE
            if high_score_handled and score.initials == player_initials and score.score == SCORE:
                color = (255, 255, 0)  # Yellow for the new high score

            score_text = small_font.render(f"{i + 1}. {score.initials} {score.score}", True, color)
            screen.blit(score_text, (WINDOW_WIDTH / 2 - score_text.get_width() / 2, y_pos))
            y_pos += 40  # Space between each score

        # Display quit message at the bottom
        quit_text = font.render('PRESS ANY KEY TO QUIT', True, WHITE)
        screen.blit(quit_text, (WINDOW_WIDTH / 2 - quit_text.get_width() / 2, WINDOW_HEIGHT - 100))

        pygame.display.flip()

    # write to text file
    f = open('highscores.txt', 'w')
    for highscore in highscores:
        f.write(str(highscore)+'\n')
    f.close()
    # Quit Pygame
    pygame.quit()


if __name__ == '__main__':
    main()