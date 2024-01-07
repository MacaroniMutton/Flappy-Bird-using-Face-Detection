import pygame, sys, time
import random
from scripts.utils import load_image, load_images, load_audio
from scripts.pipes import Pipes
from scripts.bird import Bird
from scripts.score import Score
from scripts.buttons import Buttons
from scripts.face_detection import FaceDetectionWindow

# Press Space in the Flappy bird game window to start the game

SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
SPEED = 2
TIME = time.localtime()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()

        self.assets = {
            "background-day": load_image("background-day.png"),
            "background-night": load_image("background-night.png"),
            "pipe": load_images("pipe"),
            "bluebird": load_images("bluebird"),
            "redbird": load_images("redbird"),
            "yellowbird": load_images("yellowbird"),
            "base": load_image("base.png"),
            "score": load_images("0"),
            "gameover": load_image("gameover.png"),
            "die": load_audio("die.wav"),
            "hit": load_audio("hit.wav"),
            "point": load_audio("point.wav"),
            "swoosh": load_audio("swoosh.wav"),
            "wing": load_audio("wing.wav"),
        }
        pygame.display.set_icon(self.assets["yellowbird"][2])
        self.base = self.assets["base"]
        self.start_base_pos = (0, SCREEN_HEIGHT-self.base.get_height())
        self.base_rect = pygame.Rect(self.start_base_pos[0], self.start_base_pos[1], self.base.get_width(), self.base.get_height())
        self.base_mask = pygame.mask.from_surface(self.base) 
        self.score = 0
        self.scoreObj = Score(self)
        self.game_over = False
        self.highscore = 0
        if 7 <= TIME.tm_hour < 19:
            self.pipes = Pipes(self, self.assets["pipe"][0], 3, SPEED)
            self.bird = Bird(self, self.assets["yellowbird"], (40, (self.screen.get_height()-self.base.get_height())/2))
            self.background = self.assets["background-day"]
        else:
            self.pipes = Pipes(self, self.assets["pipe"][1], 3, SPEED)
            self.bird = Bird(self, self.assets["bluebird"], (40, (self.screen.get_height()-self.base.get_height())/2))
            self.background = self.assets["background-night"]
        self.faceWindow = FaceDetectionWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.fy = (self.screen.get_height()-self.base.get_height())/2
        

    def quit(self):
        self.faceWindow.destroy()
        pygame.quit()
        sys.exit()

    def play_again(self):
        self.base = self.assets["base"]
        self.start_base_pos = (0, SCREEN_HEIGHT-self.base.get_height())
        self.base_rect = pygame.Rect(self.start_base_pos[0], self.start_base_pos[1], self.base.get_width(), self.base.get_height())
        self.base_mask = pygame.mask.from_surface(self.base) 
        self.score = 0
        self.scoreObj = Score(self)
        self.game_over = False
        self.highscore = 0
        if 7 <= TIME.tm_hour < 19:
            self.pipes = Pipes(self, self.assets["pipe"][0], 3, SPEED)
            self.bird = Bird(self, self.assets["yellowbird"], (40, (self.screen.get_height()-self.base.get_height())/2))
            self.background = self.assets["background-day"]
        else:
            self.pipes = Pipes(self, self.assets["pipe"][1], 3, SPEED)
            self.bird = Bird(self, self.assets["bluebird"], (40, (self.screen.get_height()-self.base.get_height())/2))
            self.background = self.assets["background-night"]
        self.faceWindow = FaceDetectionWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.fy = (self.screen.get_height()-self.base.get_height())/2

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.bird.flap()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        quitbtn.isclicked(pygame.mouse.get_pos())
                        playbtn.isclicked(pygame.mouse.get_pos())
                if event.type == pygame.QUIT:
                    self.quit()

            temp = self.faceWindow.update()     # To stop sudden changes in position
            if temp is not None and abs(self.fy - temp) < 20:
                self.fy = temp
            self.screen.blit(self.background, (0, 0))
            self.pipes.render(self.screen)
            self.scoreObj.render_score(self.screen, self.highscore)
            self.screen.blit(self.base, self.base_rect)
            self.bird.render(self.screen)

            if not self.bird.check_collisions(self.base_rect, self.base_mask, self.pipes):
                self.pipes.update(self.bird, self.scoreObj, self.base_rect)
                self.scoreObj.update_score(self.bird, self.pipes)
                self.bird.update()
            else:
                try:
                    file = open("highscore", "r")
                    self.highscore = int(file.read())
                    self.highscore = max(self.highscore, self.score)
                    file.close()
                    file = open("highscore", "w")
                    file.write(str(self.highscore))
                    file.close()
                except Exception as e:
                    print(e)
                    file = open("highscore", "w")
                    self.highscore = self.score
                    file.write(str(self.highscore))
                    file.close()
                self.game_over = True
                playbtn = Buttons(self.screen.get_width()/2, 200, 72, 25, (186, 158, 37), (255, 255, 255), text="Play Again", func=self.play_again)
                playbtn.render(self.screen)
                quitbtn = Buttons(self.screen.get_width()/2, 230, 72, 25, (186, 158, 37), (255, 255, 255), text="Quit", func=self.quit)
                quitbtn.render(self.screen)

            pygame.display.update()
            self.clock.tick(60)

Game().run()
