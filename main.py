import pygame
import sys
import random
import neat
def game_floor():
    screen.blit(floor_base,(floor_x_pos,900))
    screen.blit(floor_base,(floor_x_pos + 576,900))

def check_colision(pipes):
    for pipe in pipes:
        if(bird_rect.colliderect(pipe)):
            return False
    if (bird_rect.top <= -100) or  (bird_rect.bottom >= 900):
        return False
    return True

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (700,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (700,random_pipe_pos-300))
    return bottom_pipe,top_pipe

def move_pipes(pipes):
    newP=[]
    global score
    newscore=0
    for pipe in pipes:
        pipe.centerx -= 5
        if(pipe.centerx<-40):
            newscore +=1
        else :
            newP.append(pipe)
    score+=int(newscore/2)
    return newP

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)
pygame.init()
clock=pygame.time.Clock()
#vars
score=0
gravity = 0.25
bird_movement=0

screen = pygame.display.set_mode((572, 1024))



background = pygame.image.load("assets/sprites/background-night.png").convert()
background = pygame.transform.scale2x(background)

bird = pygame.image.load("assets/sprites/redbird-midflap.png").convert_alpha()
bird = pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center=(100,512))

floor_base=pygame.image.load("assets/sprites/base.png").convert()
floor_base = pygame.transform.scale2x(floor_base)
floor_x_pos = 0
game_active = True

message=pygame.image.load("assets/sprites/message.png").convert_alpha()
message = pygame.transform.scale2x(message)

game_over_rect = message.get_rect(center=(288,512))

#Build pipes

largeFont = pygame.font.SysFont('comicsans', 80)
pipe_surface = pygame.image.load('assets/sprites/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list= []
pipe_height = [400,600,800]
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)

while True:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 10
            if event.key == pygame.K_SPACE and game_active==False:
                bird_rect.center = (100,512)
                score=0
                bird_movement = 0
                pipe_list=[]
                game_active = True
        if event.type == SPAWNPIPE and game_active:
            pipe_list.extend(create_pipe())
            
    screen.blit(background,(0,0))
    #check for collision
    if game_active:
        game_active = check_colision(pipe_list)
        pipe_list=move_pipes(pipe_list)
        draw_pipes(pipe_list)
        bird_movement += gravity
        bird_rect.centery += bird_movement
        screen.blit(bird,bird_rect)
    else :
        screen.blit(message,game_over_rect)
    #Create floor
    floor_x_pos -= 1
    game_floor()
    currentScore = largeFont.render('Score: '+ str(score),1,(255,255,255))
    screen.blit(currentScore,(200,0))
    if floor_x_pos <= -576:
        floor_x_pos=0
    pygame.display.update()
    clock.tick(120)
