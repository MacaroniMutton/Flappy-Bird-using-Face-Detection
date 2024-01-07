import pygame

class Score:
    def __init__(self, game):
        self.game = game
        self.check_score = True

    def update_score(self, bird, pipes):
        if self.check_score:
            if bird.rect().left >= pipes.rects()[0].right:
                self.game.assets["point"].play()
                self.game.score += 1
                self.check_score = False

    def render_score(self, surf, highscore):
        score = str(self.game.score)
        score_imgs = []
        for ch in score:
            score_imgs.append(self.game.assets["score"][int(ch)])
        width = 0
        for img in score_imgs:
            width += img.get_width() + 3
        score_surf = pygame.Surface((width, score_imgs[0].get_height()))
        x = 0
        for img in score_imgs:
            score_surf.blit(img, (x, 0))
            x += img.get_width() + 3
        score_rect = score_surf.get_rect(center = (surf.get_width()/2, 35))
        if self.game.game_over:
            gameover_img = self.game.assets["gameover"]
            gameover_rect = gameover_img.get_rect(center = (surf.get_width()/2, 35))
            surf.blit(gameover_img, gameover_rect)
            scoreboard = pygame.Surface((200, 150))
            scoreboard.fill((204, 177, 59))

            pygame.draw.rect(scoreboard, (110, 80, 32), (0, 0, scoreboard.get_width(), scoreboard.get_height()), 3, 5)

            font = pygame.font.SysFont('comicsans', 20, True)
            
            curr_score = font.render(f"Your Score : {self.game.score}", True, (255, 255, 255))
            curr_score_rect = curr_score.get_rect(midbottom = (scoreboard.get_width()/2, scoreboard.get_height()/2-5-35))
            scoreboard.blit(curr_score, curr_score_rect)

            high_score = font.render(f"High Score : {highscore}", True, (255, 255, 255))
            high_score_rect = high_score.get_rect(midtop = (scoreboard.get_width()/2, scoreboard.get_height()/2+5-35))
            scoreboard.blit(high_score, high_score_rect)

            scoreboard_rect = scoreboard.get_rect(midbottom = (surf.get_width()/2, surf.get_height()/2))
            surf.blit(scoreboard, scoreboard_rect)
        else:
            surf.blit(score_surf, score_rect)