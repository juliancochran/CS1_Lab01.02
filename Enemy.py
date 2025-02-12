import pygame
from ImageGenerator import *  # Import the function

class Enemy:
    def __init__(self, x, y, screen_height):
        # Get random enemy image using the ImageGenerator
        self.image = get_enemy_img()
        # Create a rectangle for the enemy
        self.rect = self.image.get_rect()
        # Set initial position
        self.rect.x = x
        self.rect.y = y
        # Movement speed
        self.speed_x = 0
        self.speed_y = 0
        self.moving = False
        # Store screen height for boundary checking
        self.screen_height = screen_height

    def is_off_screen(self):
        # Check if the enemy has completely passed the bottom of the screen
        return self.rect.top >= self.screen_height

    def move(self, dx=0, dy=0):
        # Move the enemy by the specified amount
        if self.moving:
            self.rect.x += dx
            self.rect.y += dy

    def set_speed(self, speed_x, speed_y):
        # Set movement speed
        self.speed_x = speed_x
        self.speed_y = speed_y

    def update(self):
        # Update enemy position based on current speed
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def draw(self, screen):
        # Draw the enemy on the screen
        screen.blit(self.image, self.rect)

    def die(self):
        self.image = get_death_img()


# Example usage:
'''
game_screen = pygame.display.set_mode((800, 600))

# Create enemies
enemy1 = Enemy(100, 100, "enemy1.png")
enemy2 = Enemy(200, 200, "enemy2.png")

# Set different speeds for independent movement
enemy1.set_speed(2, 0)  # Move right
enemy2.set_speed(-1, 1)  # Move left and down

# In game loop:
while running:
    # Update enemy positions
    enemy1.update()
    enemy2.update()

    # Draw enemies
    enemy1.draw(game_screen)
    enemy2.draw(game_screen)
'''
