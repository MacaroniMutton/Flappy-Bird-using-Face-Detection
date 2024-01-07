import pygame, os

BASE_PATH = "assets/sprites/"
BASE_AUDIO_PATH = "assets/audio/"

def load_image(path):
    img = pygame.image.load(BASE_PATH + path).convert_alpha()
    # img.set_colorkey((0, 0, 0))
    return img

def load_images(path):
    imgs = []
    sprites = os.listdir(BASE_PATH)
    for img in sprites:
        if path.isdigit():
            if img[0].isdigit():
                imgs.append(load_image(img))
        elif path in img:
            imgs.append(load_image(img))
    return imgs
        
def load_audio(path):
    return pygame.mixer.Sound(BASE_AUDIO_PATH + path)