import pygame
import math

GRAVITY = 0.19

class Bird:
    def __init__(self, game, images, pos, img_dur=8):
        self.game = game
        self.images = images
        self.pos = list(pos)
        self.prev_pos = self.pos
        self.bird_rect = pygame.Rect(self.pos[0], self.pos[1], self.images[2].get_width(), self.images[2].get_height())
        self.curr_img = self.images[0]
        self.mask = pygame.mask.from_surface(self.curr_img)
        self.masked_img = self.mask.to_surface(unsetcolor=(0, 0, 0, 0))
        self.img_duration = img_dur
        self.frames = 0
        self.velocity = [0, 0]
        self.started = False
        self.collided = False
        self.angle = 0
        self.rotate = 0

    def update(self):
        self.frames = (self.frames+1) % (len(self.images) * self.img_duration)
        self.curr_img = self.images[self.frames // self.img_duration]
        self.mask = pygame.mask.from_surface(self.curr_img)
        self.masked_img = self.mask.to_surface(unsetcolor=(0, 0, 0, 0))
        if self.started:
            self.prev_pos = self.pos.copy()
            if self.collided:  
                self.pos[1] = max(self.pos[1]+self.velocity[1], -60)
                self.velocity[1] = min(self.velocity[1] + GRAVITY, 5)
            else:
                if self.game.fy is not None:
                    self.pos[1] = self.game.fy

            self.bird_rect.x = self.pos[0]
            self.bird_rect.y = self.pos[1]

            # if self.prev_pos[1] < self.pos[1]:
            #     self.angle = 25
            # else:
            #     self.angle = -25

            self.curr_img = pygame.transform.rotozoom(self.curr_img, self.angle, 1)
            self.mask = pygame.mask.from_surface(self.curr_img)
            self.masked_img = self.mask.to_surface(unsetcolor=(0, 0, 0, 0))
            self.bird_rect = self.curr_img.get_rect(center = (self.bird_rect.centerx, self.bird_rect.centery))

            # if self.angle > 0:
            #     self.angle = max(0, self.angle-self.rotate)
            # elif self.angle < 0:
            #     self.angle = min(0, self.angle+self.rotate)
            # self.rotate += 0.05

    def rect(self):
        return self.bird_rect

    def flap(self):
            self.started = True
            # if not self.collided:
            #     self.game.assets["wing"].play()
                # self.velocity[1] = -3.4
                # self.rotate = 0
                # self.angle = 25
                # self.curr_img = pygame.transform.rotozoom(self.curr_img, self.angle, 1)
                # self.bird_rect = self.curr_img.get_rect(center = (self.bird_rect.centerx, self.bird_rect.centery))
                
        

    def check_collisions(self, base_rect, base_mask, pipes):
        # if self.rect().colliderect(base_rect):
        if self.mask.overlap(base_mask, (base_rect.x - self.rect().x, base_rect.y - self.rect().y)):
            if not self.collided:
                self.game.assets["hit"].play()
                self.collided = True
            return True
        if not self.collided:
            for pipe_rect in pipes.rects():
                # if self.rect().colliderect(pipe_rect):
                if self.mask.overlap(pipes.mask, (pipe_rect.x - self.rect().x, pipe_rect.y - self.rect().y)):
                    self.velocity[1] = 0
                    self.collided = True
                    self.game.assets["hit"].play()
                    self.game.assets["die"].play()
        return False
    
    def render(self, surf):
        surf.blit(self.curr_img, self.bird_rect)