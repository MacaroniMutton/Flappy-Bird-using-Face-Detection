import pygame, sys

class Buttons(object):
    def __init__(self, x, y, width, height, colour1, colour2, text='', func=None, arg=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour1 = colour1
        self.colour2 = colour2
        self.text = text
        self.func = func
        self.arg = arg

    def render(self, win):
        font = pygame.font.SysFont('Helvetica', 16, True)
        text = font.render(self.text, True, self.colour2)
        pygame.draw.rect(win, self.colour1, (int(self.x - self.width // 2), int(self.y - self.height // 2), int(self.width), int(self.height)), 2, 5)
        win.blit(text, (int(self.x - text.get_width() // 2), int(self.y - text.get_height() // 2)))

    def isover(self, pos):
        if int(self.x - self.width // 2) < pos[0] < int(self.x + self.width // 2) and int(self.y - self.height // 2) < pos[1] < int(self.y + self.height // 2):
            return True
        return False

    def isclicked(self, pos):  # pos here is mouse position
        if self.isover(pos):
            if self.arg is not None:
                self.func(*self.arg)
            else:
                self.func()

