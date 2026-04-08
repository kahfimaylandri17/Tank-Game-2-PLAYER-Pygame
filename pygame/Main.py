import pygame
import sys

pygame.init()

WIDTH = 1000
HEIGHT = 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tank Game 2 PLAYER")

clock = pygame.time.Clock()
FPS = 60

map_img = pygame.image.load("map.png")
map_img = pygame.transform.scale(map_img, (WIDTH, HEIGHT))

player1_img = pygame.image.load("player1.png").convert_alpha()
player1_img = pygame.transform.scale(player1_img, (50, 50))

player2_img = pygame.image.load("player2.png").convert_alpha()
player2_img = pygame.transform.scale(player2_img, (50, 50))

rock_img = pygame.image.load("rock.png").convert_alpha()
rock_img = pygame.transform.scale(rock_img, (50, 50))

tree_img = pygame.image.load("tree.png").convert_alpha()
tree_img = pygame.transform.scale(tree_img, (50, 50))

BLACK = (0, 0, 0)

class Tank:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.speed = 1
        self.last_shot = 0
        self.cooldown = 500

    def batas(self):
        if self.x < 0:
            self.x = 0
        elif self.x + self.width > WIDTH:
            self.x = WIDTH - self.width
        if self.y < 0:
            self.y = 0
        elif self.y + self.height > HEIGHT:
            self.y = HEIGHT - self.height

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface, image):
        surface.blit(image, (self.x, self.y))

class Player1(Tank):
    def move(self, keys, other, rocks, trees):

        old_x = self.x
        old_y = self.y

        if keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_s]:
            self.y += self.speed

        self.batas()

        if self.rect().colliderect(other.rect()):
            self.x = old_x
            self.y = old_y

        for rock in rocks:
            if self.rect().colliderect(rock.rect()):
                self.x = old_x
                self.y = old_y

        for tree in trees:
            if self.rect().colliderect(tree.rect()):
                self.x = old_x
                self.y = old_y

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot >= self.cooldown and len(bullets1) < 5:
            bullet = Bullet(self.x + self.width, self.y + self.height // 2, 5, 6)
            bullets1.append(bullet)
            self.last_shot = now

class Player2(Tank):
    def move(self, keys, other, rocks, trees):

        old_x = self.x
        old_y = self.y

        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed

        self.batas()

        if self.rect().colliderect(other.rect()):
            self.x = old_x
            self.y = old_y

        for rock in rocks:
            if self.rect().colliderect(rock.rect()):
                self.x = old_x
                self.y = old_y

        for tree in trees:
            if self.rect().colliderect(tree.rect()):
                self.x = old_x
                self.y = old_y

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot >= self.cooldown and len(bullets2) < 5:
            bullet = Bullet(self.x, self.y + self.height // 2, 5, -6)
            bullets2.append(bullet)
            self.last_shot = now

class Bullet:
    def __init__(self, x, y, radius, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed

    def move(self):
        self.x += self.speed

    def draw(self, color):
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)

class Object:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface, image):
        surface.blit(image, (self.x, self.y))

class Rock(Object):
    pass

class Tree(Object):
    pass

player1 = Player1(100, 100)
player2 = Player2(800, 600)

bullets1 = []
bullets2 = []

rocks = [
    Rock(400, 300),
    Rock(600, 500),
    Rock(350, 150),
    Rock(700, 300),
    Rock(150, 250),
    Rock(350, 600),
    Rock(650, 450),
]

trees = [
    Tree(500, 600),
    Tree(400, 500),
    Tree(700, 200),
    Tree(450, 150),
    Tree(300, 400),
    Tree(200, 100),
    Tree(150, 550)
]

game_over = False
winner = ""

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                player1.shoot()
            if event.key == pygame.K_RETURN:
                player2.shoot()

    if not game_over:
        keys = pygame.key.get_pressed()

        player1.move(keys, player2, rocks, trees)
        player2.move(keys, player1, rocks, trees)

        for bullet in bullets1 :
            bullet.move()
            if bullet.x > WIDTH or bullet.x < 0:
                bullets1.remove(bullet)

        for bullet in bullets2 :
            bullet.move()
            if bullet.x > WIDTH or bullet.x < 0:
                bullets2.remove(bullet)

        for bullet in bullets1 :
            for rock in rocks :
                if rock.rect().collidepoint(bullet.x, bullet.y):
                    if bullet in bullets1:
                        bullets1.remove(bullet)
                    rocks.remove(rock)
            for tree in trees :
                if tree.rect().collidepoint(bullet.x, bullet.y):
                    if bullet in bullets1:
                        bullets1.remove(bullet)
                    trees.remove(tree)

        for bullet in bullets2 :
            for rock in rocks :
                if rock.rect().collidepoint(bullet.x, bullet.y):
                    if bullet in bullets2:
                        bullets2.remove(bullet)
                    rocks.remove(rock)

            for tree in trees :
                if tree.rect().collidepoint(bullet.x, bullet.y):
                    if bullet in bullets2:
                        bullets2.remove(bullet)
                    trees.remove(tree)

        for bullet in bullets1 :
            if player2.rect().collidepoint(bullet.x, bullet.y):
                winner = "Player 1 Win"
                game_over = True

        for bullet in bullets2 :
            if player1.rect().collidepoint(bullet.x, bullet.y):
                winner = "Player 2 Win"
                game_over = True

    screen.blit(map_img, (0, 0))

    player1.draw(screen, player1_img)
    player2.draw(screen, player2_img)

    for rock in rocks:
        rock.draw(screen, rock_img)

    for tree in trees:
        tree.draw(screen, tree_img)

    for bullet in bullets1:
        bullet.draw(BLACK)

    for bullet in bullets2:
        bullet.draw(BLACK)

    if game_over:
        font = pygame.font.SysFont(None, 60)
        text = font.render(winner, True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

    pygame.display.flip()
    clock.tick(FPS)
