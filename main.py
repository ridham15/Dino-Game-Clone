# imports
import pygame
import random
from sys import exit


# variables
WIDTH = 900
HEIGHT = 300
FPS = 60
game_active = True
speed = 4
timer = 0
spawn = True
cooldown = 1000
score = 0
high_score = 100

# initializing pygame
pygame.init()

# creating the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill('white')
pygame.display.set_caption('Dino Run')
clock = pygame.time.Clock()
font = pygame.font.Font('Press_Start_2P/PressStart2P-Regular.ttf', 15)


# Dino class
class Dino(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        dino_walk_1 = pygame.image.load('Assets/Dino/1.png').convert_alpha()
        dino_walk_2 = pygame.image.load('Assets/Dino/2.png').convert_alpha()
        dino_walk_3 = pygame.image.load('Assets/Dino/3.png').convert_alpha()
        dino_walk_4 = pygame.image.load('Assets/Dino/4.png').convert_alpha()
        dino_walk_5 = pygame.image.load('Assets/Dino/5.png').convert_alpha()
        dino_walk_6 = pygame.image.load('Assets/Dino/7.png').convert_alpha()
        self.dino_index = 0
        self.dino_jump = dino_walk_1
        self.gravity = 0
        self.dino_walk = [dino_walk_1, dino_walk_2, dino_walk_3]
        self.dino_duck_walk = [dino_walk_4, dino_walk_5]
        self.dino_game_end = dino_walk_6

        self.image = dino_walk_1
        self.rect = self.image.get_rect(midbottom=(100, 272))
        self.standing_height = self.rect.height  # Store original height

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 272:
            self.gravity = -17

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 272:
            self.rect.bottom = 272

    def animate(self):
        keys = pygame.key.get_pressed()
        # when the dino jumps
        if keys[pygame.K_SPACE] and self.rect.bottom < 272:
            self.image = self.dino_jump

        # when the dino is crouching
        elif keys[pygame.K_DOWN] and self.rect.bottom <= 272:
            self.dino_index += 0.15
            if self.dino_index >= len(self.dino_duck_walk):
                self.dino_index = 0
            self.image = self.dino_duck_walk[int(self.dino_index)]

            # Adjust rect position to maintain bottom alignment
            if self.rect.height != self.image.get_height():
                self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

        # when the dino is walking
        else:
            if self.rect.bottom >= 272:
                self.dino_index += 0.2
                if self.dino_index >= len(self.dino_walk):
                    self.dino_index = 0
                self.image = self.dino_walk[int(self.dino_index)]

                # Adjust rect position to maintain bottom alignment
                if self.rect.height != self.image.get_height():
                    self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animate()

    def get_mask(self):
        return pygame.mask.from_surface(self.image)

    def end_game(self):
        self.image = self.dino_game_end
        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)


# ground class
class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Assets/ground.png').convert()
        self.rect = self.image.get_rect(midbottom=(0, 250))

        self.width = self.image.get_width()
        self.x1 = 0
        self.x2 = self.width
        self.y = 250

    def update(self):
        self.x1 -= speed
        self.x2 -= speed

        if self.x1 <= -self.width:
            self.x1 = self.width

        if self.x2 <= -self.width:
            self.x2 = self.width

    def draw(self, surface):
        surface.blit(self.image, (self.x1, self.y))
        surface.blit(self.image, (self.x2, self.y))

    def get_mask(self):
        return pygame.mask.from_surface(self.image)


# Cloud class
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Assets/cloud.png').convert_alpha()
        self.image.set_alpha(128)
        self.rect = self.image.get_rect(center=(random.randint(950, 1000), random.randint(30, 100)))

    def update(self):
        self.rect.x -= 2
        if self.rect.right < 0:
            self.kill()


# Cactus class
class Cactus(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.x = x_pos
        self.y = y_pos
        self.sprites = []
        for i in range(1, 7):
            current_sprite = pygame.image.load(f'Assets/Cactus/{i}.png').convert_alpha()
            self.sprites.append(current_sprite)

        self.image = random.choice(self.sprites)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.destroy()
        self.x -= speed
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def get_mask(self):
        return pygame.mask.from_surface(self.image)


# Ptera class
class Ptera(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 900
        self.y = random.choice([140, 180, 225])
        self.sprites = []
        for i in range(1, 3):
            current_sprite = pygame.transform.scale(pygame.image.load(f'Assets/Ptera/{i}.png').convert_alpha(), (84, 62))
            self.sprites.append(current_sprite)

        self.index = 0
        self.image = self.sprites[self.index]
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def animate(self):
        self.index += 0.07
        if self.index >= len(self.sprites):
            self.index = 0
        self.image = self.sprites[int(self.index)]

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.animate()
        self.destroy()
        self.x -= speed
        self.rect = self.image.get_rect(center=(self.x, self.y))


# groups
dino = pygame.sprite.GroupSingle(Dino())
cloud = pygame.sprite.Group()
obstacle = pygame.sprite.Group()
ptera = pygame.sprite.Group()
ground = Ground()

# cloud logic
cloud_spawn_time = 0
cloud_spawn_interval = 5000

# game over images
game_over = pygame.image.load('Assets/game_over.png').convert_alpha()
game_over_rect = game_over.get_rect(center=(WIDTH // 2, HEIGHT // 3))

restart = pygame.image.load('Assets/replay.png').convert_alpha()
restart_rect = restart.get_rect(center=(WIDTH // 2, 2 * HEIGHT // 3))


# score function
def display_score():
    global score, high_score
    score_surface = font.render(f'{score}', False, (0, 0, 0))
    score_rect = score_surface.get_rect(midleft=(800, 50))
    screen.blit(score_surface, score_rect)

    if high_score != 0:
        high_score_surface = font.render(f'HI {high_score}', False, (0, 0, 0))
        high_score_rect = high_score_surface.get_rect(midleft=(650, 50))
        screen.blit(high_score_surface, high_score_rect)


# game loop
while True:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # detect collisions
    if pygame.sprite.spritecollide(dino.sprite, obstacle, False, pygame.sprite.collide_mask):
        # update high score if score is greater than high score
        if score > high_score:
            high_score = score

        game_active = False

    if game_active:
        if current_time - cloud_spawn_time >=  cloud_spawn_interval:
            cloud.add(Cloud())
            cloud_spawn_time = current_time

        if pygame.time.get_ticks() - timer >= cooldown:
            spawn = True

        if spawn:
            spawn_object = random.randint(0, 100)
            if spawn_object in range(50, 100):
                new_obstacle = Cactus(900, 235)
                obstacle.add(new_obstacle)
                timer = pygame.time.get_ticks()
                spawn = False
            elif spawn_object in range(0, 50):
                new_obstacle = Ptera()
                obstacle.add(new_obstacle)
                timer = pygame.time.get_ticks()
                spawn = False

        # control the speed
        while speed <= 12:
            speed += 0.01

        score += 1

        screen.fill('white')  # Clear the screen first
        ground.update()
        ground.draw(screen)
        dino.update()
        dino.draw(screen)
        obstacle.update()
        obstacle.draw(screen)
        cloud.update()
        cloud.draw(screen)

        display_score()

    else:
        dino.sprite.end_game()
        screen.blit(dino.sprite.image, dino.sprite.rect)
        screen.blit(game_over, game_over_rect)
        screen.blit(restart, restart_rect)

        # check if up or space key pressed to restart the game
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
            obstacle.empty()
            game_active = True

    # update the display
    pygame.display.update()
    clock.tick(FPS)
