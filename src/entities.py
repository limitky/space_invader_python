import pygame

class Unit:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def draw(self, screen, image):
        screen.blit(image, (self.x, self.y))

    def collides_with(self, other, self_image, other_image):
        return pygame.Rect(self.x, self.y, self_image.get_width(), self_image.get_height()).colliderect(
            pygame.Rect(other.x, other.y, other_image.get_width(), other_image.get_height())
        )

class Enemy(Unit):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.exploding = False

    def move(self):
        self.y += 1

    def draw(self, screen, image, explosion_images):
        if self.exploding:
            for img in explosion_images:
                screen.blit(img, (self.x, self.y))
        else:
            screen.blit(image, (self.x, self.y))

class Bullet:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

    def move(self):
        self.y += self.direction * 5

    def draw(self, screen, image):
        screen.blit(image, (self.x, self.y))

    def collides_with(self, other, self_image, other_image):
        return pygame.Rect(self.x, self.y, self_image.get_width(), self_image.get_height()).colliderect(
            pygame.Rect(other.x, other.y, other_image.get_width(), other_image.get_height())
        )
