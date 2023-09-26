import pygame
from pygame.locals import *
import random

pygame.init()

# ----------------------
# Game variable Section
# ----------------------

clock = pygame.time.Clock() # Clock funftion for FPS Clock
fps = 32 # Farme Per Second Rate
screen_width = 540 # Screen Witdh 
screen_hight = 700 # Screen Hight

# Variable For Background Screen Looop 
ground_scroll = 0 # Image Scrrolling 
scroll_speed = 4 # scrolling speed
flying = False # For Strting game Bird Just Flyess
game_over = False
pipe_gap = 145
pipe_frequency = 1500
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False
bg_start = False

# Dictionary For Sounds
game_sound = {}
game_sound["wing"] = "assets/audio/wing.ogg"
game_sound["die"] = "assets/audio/die.ogg"
game_sound["hit"] = "assets/audio/hit.ogg"
game_sound["point"] = "assets/audio/point.ogg"
game_sound["swoosh"] = "assets/audio/swoosh.ogg"


# Game Dispaly or Windows Size As Varible
screen = pygame.display.set_mode((screen_width, screen_hight)) # Sreen Size And Its Deployemt

#Image Lode (under variable)
background = pygame.image.load("assets/sprites/background-day.png")
ground = pygame.image.load("assets/sprites/base.png")
button_img = pygame.image.load("assets/sprites/restart.png") 
over_game_img = pygame.image.load("assets/sprites/gameover.png")
wel_mess_img = pygame.image.load("assets/sprites/message.png")

# ----------------------
# Game Title Section
# ----------------------
pygame.display.set_caption("Flappy Bird By Mitranshu Mishra")

# ----------------------
# Function For Reset Game
# ----------------------

def reset_game():
    pipe_group.empty()
    flappy.rect.x = 30
    flappy.rect.y = int(screen_hight / 2.5)
    score = 0
    return score

def tap_start():
    if flying == False and game_over == True:
        screen.blit(wel_mess_img, (0,0))
    
# ----------------------
# Game Classes And Assets Assigmnts Section
# ----------------------

# Created A Bird For Flappy Bird As Player
class Bird(pygame.sprite.Sprite):
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1,4):
            img = (f"assets/sprites/bird{num}.png")
            self.images.append(img)
        self.image = pygame.image.load(self.images[self.index])
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.vel = 0
        self.clicked = False
    def update(self):
        if flying == True:
            # Gravity Bird Falling
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 590:
                self.rect.y += int(self.vel)
        if game_over == False:        
            # Flappy Bird Jump Section
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
                wing = pygame.mixer.Sound(game_sound["wing"])
                wing.play()
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False               
            # Bird Flap Animation
            self.counter += 1
            flap_cooldown = 5
            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = pygame.image.load(self.images[self.index])
            # Rotaion Of Flappy Bird
            self.image = pygame.transform.rotate(pygame.image.load(self.images[self.index]), self.vel * -2)
        else:
             self.image = pygame.transform.rotate(pygame.image.load(self.images[self.index]), -90)   
# Creating Class For Pipes And Pipes Position
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x,y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/sprites/pipe-green.png")
        self.rect = self.image.get_rect()
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x ,y - int(pipe_gap) / 2]
        if position == -1:                            
            self.rect.topleft = [x,y + int(pipe_gap) / 2]
# Creating function to remove passed pipes from memory.
    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()       
# Creating Class For Reset Button
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    def draw(self):
        action = False
        # Get Mouse postion
        pos = pygame.mouse.get_pos()
        # Check if Mouse Is Over The Button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        # Draw Button for visual display.
        screen.blit(self.image, (self.rect.x, self.rect.y))  
        return action
# Creating Class For Game over Image
class Over_game():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    def o_draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))    
# Creating Class For Score Display on Screen  
class Al_score(pygame.sprite.Sprite):
    # Creating List of numbers Images 
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.rect = pygame.Rect(x, y, 0, 0)
    # Function For Creating List of numbers Images    
    def load_digit_images(self):
        for num in range(0,10):
            img_path = f"assets/sprites/{num}.png"
            self.images.append(img_path)
    # Function For Displaying Score Image on Screen         
    def draw_score(self, screen, score):
        score_str = str(score)
        x_offset = 0
        for digit_char in score_str:
            if digit_char.isdigit():
                digit_index = int(digit_char)
                self.load_digit_images()
                img_path = self.images[digit_index]  # Get the image file path
                digit_image = pygame.image.load(img_path).convert_alpha()
                screen.blit(digit_image, self.rect.move(x_offset, 0))
                x_offset += digit_image.get_width()

# Objects Of Bird Class
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()
flappy = Bird(30, int(screen_hight / 2.5))        
bird_group.add(flappy) 

# Create Restart Button Instance
button = Button(screen_width // 2 -70, screen_hight //2 -20, button_img)
s_over = Over_game(screen_width // 2 -115, screen_hight //2 -100, over_game_img)
# Create Score Instance
score_sprite = Al_score(230, 40)

# ---------------------------------
# Game Logic and Funtions Section #
# ---------------------------------
run = True
while run:
    clock.tick(fps)
    screen.blit(background, (0,0))
    if flying == False:
        if game_over == False:
            screen.blit(wel_mess_img, (35,35)) 
# Drawing Pipe And Bird on Screen
    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)
    # Ground or Base Bliting
    screen.blit(ground, (ground_scroll,588))
    # Verifying if the bird passes over a pipe and managing the score 
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
        and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
        and pass_pipe == False:
            pass_pipe = True
        # updating the player's score 
        if pass_pipe == True:    
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
              point = pygame.mixer.Sound(game_sound["point"])
              point.play()
              score += 1              
              pass_pipe = False
    # Checking for collisions in the game
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False):
        game_over = True
    # Checking for bird-ground collision
    if flappy.rect.bottom > 593:
        game_over = True
        flying = False        
    if flappy.rect.top < 0:
       game_over = True     
    if game_over == False and flying == True: 
        # For Generation of new pipes in the game.
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint (-100 , 101)
            btm_pipe = Pipe(screen_width, int(screen_hight / 2.3) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_hight / 2.3) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        # Drawing a scrolling ground for the game's visual display
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 50:
            ground_scroll = 0
        pipe_group.update()    
    # Adding game over detection and reset functionality
    if game_over == True:
        s_over.o_draw()
        if button.draw() == True:
            r_sound = pygame.mixer.Sound(game_sound["swoosh"])
            r_sound.play(0)
            game_over = False
            score = reset_game()
# Main Events Of The Game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True                                  
    if game_over == False:
        kill = pygame.mixer.music.load(game_sound["hit"])
        kill = pygame.mixer.music.play(0)
    if flying == True:    
        score_sprite.draw_score(screen, score)
        score_sprite.update()       
    pygame.display.update()        
pygame.quit()