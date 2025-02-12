import pygame

class Bullet:
    def __init__(self, x, y, screen_height):
        # Create a 3x10 pixel rectangle for the bullet
        self.rect = pygame.Rect(x, y, 3, 12)
        # Set bullet color
        self.color = (255, 255, 0)  # Yellow in RGB
        # Set bullet speed (negative because moving upward)
        self.speed = -10  # Adjust this value to make bullets faster or slower
        self.on_screen = True

    def is_off_screen(self):
        # Check if the bullet has completely passed the top of the screen
        self.on_screen = False
        return self.rect.bottom <= 0

    def update(self):
        # Move the bullet upward
        self.rect.y += self.speed

    def draw(self, screen):
        # Draw the bullet as a yellow rectangle
        pygame.draw.rect(screen, self.color, self.rect)