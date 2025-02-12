import pygame
import random
# return a random image for the alien generation
def get_enemy_img():
    try:
        img_src = ['img/alien1.png', 'img/alien2.png', 'img/alien3.png']
        images = []
        images.append(pygame.image.load(img_src[0]))
        images.append(pygame.image.load(img_src[1]))
        images.append(pygame.image.load(img_src[2]))
        return random.choice(images)
    except pygame.error as e:
        print(f"Couldn't load image: {e}")
        return  # Exit the function if image loading fails

def get_death_img():
    try:
        img = pygame.image.load('img/ring.png')
        return img
    except pygame.error as e:
        print(f"Couldn't load image: {e}")
        return