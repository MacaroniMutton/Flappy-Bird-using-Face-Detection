import random, pygame

DISTANCE_BETWEEN_PIPES = 95

class Pipes:
    def __init__(self, game, image, pipes, speed):
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.masked_img = self.mask.to_surface(unsetcolor=(0, 0, 0, 0))
        self.game = game
        self.pipes = pipes      # Number of pipes on screen at a time
        self.pos = []
        self.velocity = [-speed, 0]
        self.distance = DISTANCE_BETWEEN_PIPES

        x_pos = self.game.screen.get_width() + 70
        for i in range(self.pipes):
            y_pos = random.randint(-260, -70)
            self.pos.append([x_pos, y_pos])
            x_pos = x_pos + self.image.get_width() + self.distance
    
    def update(self, bird, scoreObj, base_rect):  
        if not bird.collided:
            base_rect.left += self.velocity[0]
            if base_rect.right <= self.game.screen.get_width():
                base_rect.left = 0
            if bird.started:
                for i in range(self.pipes):
                    self.pos[i][0] += self.velocity[0]
                    if self.pos[0][0] + self.image.get_width() < 0:
                        scoreObj.check_score = True
                        self.pos[0][0] = self.pos[-1][0] + self.image.get_width() + self.distance
                        self.pos[0][1] = random.randint(-260, -70)
                        self.pos.append(self.pos[0])
                        self.pos.pop(0)
        
    def rects(self):
        return [pygame.Rect(self.pos[i][0], self.pos[i][1], self.image.get_width()-2, self.image.get_height()) for i in range(self.pipes)] + [pygame.Rect(self.pos[i][0], self.image.get_height()+100+self.pos[i][1], self.image.get_width()-2, self.image.get_height()) for i in range(self.pipes)]

    def render(self, surf):
        for i in range(self.pipes):
            surf.blit(pygame.transform.flip(self.image, False, True), (self.pos[i][0], self.pos[i][1]))
            surf.blit(self.image, (self.pos[i][0], self.image.get_height()+100+self.pos[i][1]))