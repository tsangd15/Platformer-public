"""Player Lives Indicator Module"""
import pygame
from _settings import WHITE, WINDOW_HEIGHT, WINDOW_WIDTH

pygame.init()
resolution = (WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pygame.display.set_mode(resolution)

# import images and convert to pygame surfaces
heart_full = pygame.image.load("assets/heart_full.png").convert()
heart_empty = pygame.image.load("assets/heart_empty.png").convert()


class LivesIndicator(pygame.sprite.Sprite):
    """Class for Player Lives Indicator"""
    def __init__(self, startx, centery):
        super().__init__()
        self.max_value = 3
        self._value = self.max_value

        # heart image dimensions: 30x28
        # surface width with 3 pixels between each heart
        # 30*3+3*2 = 96
        self.image = pygame.Surface((96, 28))
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        color = WHITE

        # draw the rectangle
        pygame.draw.rect(self.image, color, [0, 0, 96, 28])
        self.rect = self.image.get_rect()

        # set spawn location
        self.rect.x, self.rect.centery = startx, centery

        # from left to right
        self.heart1 = Heart(0, 0)
        self.heart2 = Heart(33, 0)
        self.heart3 = Heart(66, 0)

        # sprite group instantiation
        self.hearts = pygame.sprite.Group()
        self.hearts.add(self.heart1, self.heart2, self.heart3)

        # blit hearts to livesindicator sprite surface
        self.update()

    def update(self):
        """Reset all hearts to empty and fill hearts according to self.value"""
        self.image.fill(WHITE)
        status = ["empty"] * len(self.hearts)
        print(status)
        for i in range(self.value):
            status[i] = "full"
        print(status)

        i = 0
        for heart in self.hearts:
            heart.state = status[i]
            i += 1

        # draw updated hearts to surface
        self.hearts.draw(self.image)

    @property
    def value(self):
        """Property decorator for value attribute"""
        return self._value

    @value.setter
    def value(self, new_value):
        if 0 <= new_value <= self.max_value:
            self._value = new_value
            self.update()
        else:
            raise Exception("Invalid new value for health indicator")


class Heart(pygame.sprite.Sprite):
    """Class for each heart sprite"""
    def __init__(self, startx, starty):
        super().__init__()

        # define _state attribute
        self._state = "full"

        # invoke state setter
        self.state = "full"
        self.rect = self.image.get_rect()

        # set start pos and save spawn pos
        self.startx = startx
        self.starty = starty
        self.rect.x = self.startx
        self.rect.y = self.starty

    @property
    def state(self):
        """Property decorator for state attribute"""
        return self._state

    @state.setter
    def state(self, new_state):
        if new_state == "full":
            self.image = heart_full
        elif new_state == "empty":
            self.image = heart_empty
        else:
            raise Exception("Invalid heart state")
        self.image.set_colorkey(WHITE)

        self._state = new_state
