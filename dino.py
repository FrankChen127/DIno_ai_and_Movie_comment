import pygame
import random
import timeit
import math

dino_run = [pygame.image.load("data/dinorun0000.png"), pygame.image.load("data/dinorun0001.png")]
dino_jump = pygame.image.load("data/dinojump0000.png")
dino_dead = pygame.image.load("data/dinoDead0000.png")
bard = [pygame.image.load("data/berd.png"), pygame.image.load("data/berd2.png")]
cactus = [pygame.image.load("data/cactusBig0000.png"), pygame.image.load("data/cactusSmall0000.png"),
          pygame.image.load("data/cactusSmallMany0000.png")]
dino_low = [pygame.image.load("data/dinoduck0000.png"), pygame.image.load("data/dinoduck0001.png")]
dino_dead = pygame.transform.scale(dino_dead, (96, 100))


class Dino(object):
    def __init__(self, jump_height):
        self.jump_height = 9
        self.x = 85
        self.y = GROUND_Y
        self.jump_count = -9
        self.is_jump = False
        self.run = True
        self.run_count = 0
        self.start = 0
        self.stop = 0
        self.start_speed = 1
        self.is_low = False
        self.jump_down_speed = 0.5
        self.low_jump = False
        self.max_height = 10
        self.width = 96
        self.height = 112
        self.force = 0
        self.velocity = 8
        self.mass = 1
        global alive
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def jump(self):
        if self.jump_count <= 9:
            if self.jump_count < 0:
                self.y -= (self.jump_count ** 2) * 0.5
                self.jump_count += 1
            else:
                self.y += (self.jump_count ** 2) * self.jump_down_speed
                self.jump_count += 1
        else:
            self.is_jump = False
            self.jump_count = -9
            self.low_jump = False
            self.jump_down_speed = 0.5
            self.jump_height = 9

    def jump2(self):
        self.force = 0.5 * self.mass * (self.velocity ** 2)
        self.y -= self.force
        self.velocity -= 1
        if self.velocity < 0:
            self.mass = -1
        if self.velocity == -9:
            self.is_jump = False
            self.velocity = 8
            self.mass = 1

    def change_is_jump(self):
            self.is_jump = True
            self.run = False
            self.width = 96
            self.height = 100
            self.start = timeit.default_timer()

    def change_low_jump(self):
        self.low_jump = True
        self.jump_down_speed = 0.8
        self.jump_height = 8.5
        '''
        if self.jump_count < 0:
            self.jump_count = 0
            self.max_height = 10 + self.jump_count
        '''

    def change_is_low(self):
        self.is_low = True
        self.width = 136
        self.height = 68

    def print(self):
        self.width = 96
        self.height = 100
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        if not alive:
            window.blit(dino_dead, (self.x, self.y))
        elif self.is_jump:
            self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
            window.blit(dino_jump, (self.x, self.y))
        elif self.is_low:
            self.width = 136
            self.height = 68
            self.hitbox = pygame.Rect(self.x, self.y + 50, self.width, self.height)
            if self.run_count < 3:
                window.blit(dino_low[0], (self.x, self.y + 50))
                self.run_count += 1
            else:
                window.blit(dino_low[1], (self.x, self.y + 50))
                self.run_count += 2
            if self.run_count >= 6:
                self.run_count = 0
        else:
            self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
            if self.run_count < 3:
                window.blit(dino_run[0], (self.x, self.y))
                self.run_count += 1
            else:
                window.blit(dino_run[1], (self.x, self.y))

                self.run_count += 1
            if self.run_count >= 6:
                self.run_count = 0
        # pygame.draw.rect(window, BLACK, self.hitbox, 2)


class Cactus(object):
    def __init__(self, vel):
        self.vel = vel
        self.x = 1000
        self.y = GROUND_Y
        self.kind = 0
        self.width = 0
        self.height = 0
        self.plus_x = 0
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.generate(1000)

    def cactus_move(self, velocity):
        if self.x > 0 - self.width:
            self.x -= velocity
        else:
            self.generate()

    def generate(self, x=0):
        self.kind = random.randrange(0, 3)
        self.plus_x = random.randrange(0, 300)
        self.x = 800 + self.plus_x + x
        self.y = GROUND_Y
        if self.kind == 0:
            self.width = 60
            self.height = 120
        elif self.kind == 1:
            self.width = 40
            self.height = 80
            self.y += 30
        else:
            self.width = 120
            self.height = 80
            self.y += 30

    def show_cactus(self):
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        window.blit(cactus[self.kind], (self.x, self.y))
        # pygame.draw.rect(window, BLACK, self.hitbox, 2)


class Bird(object):
    def __init__(self):
        self.height = 80
        self.width = 92
        self.kind = 0  # 1 or 2
        self.x = 10000
        self.y = 0
        self.speed = 0
        self.plus_x = 0
        self.hitbox = pygame.Rect(self.x, self.y, 80, 92)
        self.generate(10000)
        self.run_count = 0

    def generate(self, x=5000):
        self.kind = random.randrange(0, 2)
        self.plus_x = random.randrange(0, 300)
        self.x = x + self.plus_x
        if self.kind == 0:
            self.y = 280
        else:
            self.y = 235

    def move(self, velocity):
        if self.x < 0:
            self.generate()
        else:
            self.x -= velocity

    def print(self):
        if self.run_count < 3:
            self.hitbox = pygame.Rect(self.x, self.y, 80, 70)
            window.blit(bard[0], (self.x, self.y))
            self.run_count += 1
        else:
            self.hitbox = pygame.Rect(self.x, self.y, 80, 70)
            window.blit(bard[1], (self.x, self.y))
            self.run_count += 1
        if self.run_count >= 6:
            self.run_count = 0
        #pygame.draw.rect(window, BLACK, self.hitbox, 2)


def score_board(num):
    font = pygame.font.SysFont("Arial Black", 16, False)
    score = font.render("Score: ", False, BLACK)
    window.blit(score, (630, 20))
    num = font.render(str(num), False, BLACK)
    window.blit(num, (700, 20))


def reload_window(score):
    window.fill(WHITE)
    dino1.print()
    cactus1.show_cactus()
    bird1.print()
    pygame.draw.line(window, BLACK, (0, GROUND_Y + 110), (1000, GROUND_Y + 110))
    dino1.is_low = False
    score_board(score)
    pygame.display.update()


def retry_button(alive):
    button = pygame.Rect(300, 300, 200, 100)
    pygame.draw.rect(window, BLACK, button, 2)
    font = pygame.font.SysFont("SF Mono", 16, True)
    text = font.render("Try Again", True, BLACK)
    window.blit(text, (400, 300))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if button.collidepoint(event.pos):
                    alive = True
                    return alive


WINDOW_SIZE = (800, 500)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GROUND_Y = 320

speed = 25
run = True
clock = pygame.time.Clock()
round_count = 0
alive = True

score = 0

dino1 = Dino(8)
cactus1 = Cactus(speed)
bird1 = Bird()

pygame.init()
window = pygame.display.set_mode(WINDOW_SIZE)
window.fill((0, 0, 0))
pygame.display.update()
while run:
    if alive:
        pygame.time.delay(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        score += 1


        key = pygame.key.get_pressed()
        down = pygame.key.get_pressed()[pygame.K_DOWN]
        if down:
            dino1.change_is_low()
        elif not dino1.is_jump:
            if key[pygame.K_SPACE] or key[pygame.K_UP]:
                dino1.change_is_jump()
        # if dino1.is_low and dino1.is_jump and not dino1.low_jump:
        # dino1.change_low_jump()

        if dino1.is_jump:
            dino1.jump2()

        round_count += 1
        speed += 0.004
        cactus1.cactus_move(speed)
        bird1.move(speed)
        # print(dino1.is_jump)

        distance = cactus1.x - bird1.x
        if 100 > distance > 0:
            cactus1.x += 200
        elif 0 > distance > -200:
            bird1.x += 100
        if pygame.Rect.colliderect(dino1.hitbox, cactus1.hitbox) or pygame.Rect.colliderect(dino1.hitbox, bird1.hitbox):
            alive = False
        reload_window(score)
    else:
        button = pygame.Rect(290, 200, 200, 75)
        pygame.draw.rect(window, BLACK, button, 2)
        font = pygame.font.SysFont("Arial Black", 32, False)
        text = font.render("Try Again", False, BLACK)
        window.blit(text, (300, 200))
        pygame.display.update()
        key = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button.collidepoint(event.pos):
                        alive = True
                        speed = 25
                        dino1 = Dino(8)
                        cactus1 = Cactus(speed)
                        bird1 = Bird()
                        score = 0
            elif key[pygame.K_SPACE] or key[pygame.K_UP]:
                alive = True
                speed = 25
                dino1 = Dino(8)
                cactus1 = Cactus(speed)
                bird1 = Bird()
                score = 0

pygame.quit()
