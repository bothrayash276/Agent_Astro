import pygame
from sys import exit
import random

pygame.init()




class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        character1 = pygame.image.load("image/astronaut1.png").convert_alpha()
        character2 = pygame.image.load("image/astronaut2.png").convert_alpha()
        self.character_list = [character1,character2]
        self.character_index = 0
        self.image = self.character_list[self.character_index]
        self.image = pygame.transform.rotozoom(self.image,0,0.20)
        self.rect = self.image.get_rect(midbottom = (260,300))
        self.speed = 200
        self.bullet_speed = 100
        self.left = False
        self.jump_sound = pygame.mixer.Sound("sound/jump.mp3")
        self.jump_sound.set_volume(0.5)
        self.walk_sound = pygame.mixer.Sound("sound/footstep.mp3")
        self.walk_sound.set_volume(1)

        
        

        # Gravity
        self.char_gravity = 0   
        self.char_push = 0

    def ground_state(self):
        self.char_gravity += 1
        self.rect.y += self.char_gravity

        if(self.char_push > 0):             # Right Motion
            self.char_push -= 1
            self.rect.x += self.char_push
            self.left = False
        if (self.char_push < 0):             # Left Motion
            self.char_push += 1
            self.rect.x += self.char_push
            self.left = True

        if(self.rect.y >= 325): self.rect.y = 325
        if(self.rect.x <=130): self.rect.x=130
        if(self.rect.x >=600): self.rect.x=600

    def animation(self):
        self.character_index += 0.1
        if self.character_index >= len(self.character_list): self.character_index = 0
        self.image = self.character_list[int(self.character_index)]
        self.image = pygame.transform.rotozoom(self.image,0,0.20)

    def movement(self):
        keyboard = pygame.key.get_pressed()
        
        # Jump
        if((keyboard[pygame.K_SPACE] or keyboard[pygame.K_w] or keyboard[pygame.K_UP]) and self.rect.y>=325):
            self.char_gravity = -20
            self.jump_sound.play()

        # Moving Right
        if((keyboard[pygame.K_d] or keyboard[pygame.K_RIGHT]) and self.rect.x <=600):
            self.char_push = 5
            self.character_index += 0.1
            if self.character_index >= len(self.character_list): self.character_index = 0
            self.image = self.character_list[int(self.character_index)]
            self.image = pygame.transform.rotozoom(self.image,0,0.20)
            if(self.rect.y ==325):
                self.walk_sound.play()
        # Moving Left
        if((keyboard[pygame.K_a] or keyboard[pygame.K_LEFT]) and self.rect.x >=160):
            self.char_push = -5
            self.character_index += 0.1
            if self.character_index >= len(self.character_list): self.character_index = 0
            self.image = self.character_list[int(self.character_index)]
            self.image = pygame.transform.rotozoom(self.image,0,0.20)
            self.image = pygame.transform.flip(self.image, True, False)    
            if(self.rect.y==325): 
                self.walk_sound.play()

    def update(self):
        # self.animation()
        self.movement()
        self.ground_state()
        # print(f"{self.rect.x}, {self.rect.y} and ", pygame.mouse.get_pos())
        
        
        
              

# bullet.x = character_position.x + (341-158)
# bullet.y = character_position.y + (414-325)




class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        enemy1 = pygame.image.load("image/enemy1.png").convert_alpha()
        enemy2 = pygame.image.load("image/enemy2.png") .convert_alpha()
        self.en_sel = random.randint(0,1)
        enemy = [enemy1, enemy2]
        self.image = enemy[self.en_sel]
        self.image = pygame.transform.rotozoom(self.image,0,0.1)
        self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(center = (1200,425))
        enemy1_sound = pygame.mixer.Sound("sound/enemy1_shot.mp3")
        enemy2_sound = pygame.mixer.Sound("sound/enemy2_shot.mp3")
        self.enemy_sound = [enemy1_sound, enemy2_sound]
        self.enemy_speed = 10

    def motion(self):
        if(self.rect.x > 1100):
            if(self.enemy_speed>0):
                self.enemy_speed -= 0.5
                self.rect.x -= self.enemy_speed
            else:
                self.enemy_speed = 10

    def update(self):
        self.motion()



        



def leave():
    pygame.quit()
    exit()

def collision():
    if(bullet_hitbox.colliderect(enemy.sprite.rect)):
        enemy.sprite.rect.x = 1300
        enemy.sprite.motion()
       



# Game Details
display = pygame.display.set_mode((1280,720))
game_icon = pygame.image.load("image/icon.png").convert_alpha()
pygame.display.set_icon(game_icon)
pygame.display.set_caption("Agent Astro")
game_event = 0            # 0 --> Intro / Outro Screen    1 --> Main Game
frameRate = pygame.time.Clock()





# Intro Screen
intro_image = pygame.image.load("image/intro_bg.png").convert_alpha()
intro_image = pygame.transform.rotozoom(intro_image,0,0.67)
title_font = pygame.font.Font("font/title_font.otf", 100)
text_font = pygame.font.Font("font/start_quit.ttf",35)
intro_game_name1 = title_font.render("AGENT", True, "white")
intro_game_name2 = title_font.render("ASTRO", True, "white")
intro_start_text = text_font.render("START", True, "white")
intro_start_text_rect = intro_start_text.get_rect(topleft = (150, 400))
intro_quit_text = text_font.render("QUIT", True, "white")
intro_quit_text_rect = intro_quit_text.get_rect(topleft = (165, 480))
intro_bgm = pygame.mixer.Sound("sound/game_intro.mp3")
intro_bgm.set_volume(0.25)
intro_click_sound = pygame.mixer.Sound("sound/button.mp3")






# Main Screen
main_bg = pygame.image.load("image/background.png").convert_alpha()
main_bg = pygame.transform.rotozoom(main_bg,0,0.569)


# Character
player = pygame.sprite.GroupSingle()
player.add(Player())


# Enemy
enemy = pygame.sprite.GroupSingle()
enemy.add(Enemy())
doKill = False


# Bullet
bullet = pygame.image.load("image/bullet.png").convert_alpha()
bullet = pygame.transform.rotozoom(bullet,180,0.1)
p_x = player.sprite.rect.x
p_y = player.sprite.rect.y + 320
bullet_hitbox = bullet.get_rect(center = (p_x, p_y))
star = False
bullet_sound = pygame.mixer.Sound("sound/gun_shot.mp3")
bullet_sound.set_volume(0.5)


# Main Code
while True:
    for event in pygame.event.get(): 
        if(event.type==pygame.QUIT): leave()



    if game_event==0:
        display.blit(intro_image,(0,0))         # bg image
        display.blit(intro_game_name1, (125, 75))
        display.blit(intro_game_name2, (125, 175))
        display.blit(intro_start_text, intro_start_text_rect)
        display.blit(intro_quit_text, intro_quit_text_rect)
        intro_bgm.play(loops=True)

        mouse_pos = pygame.mouse.get_pos()      # Returns coords (x,y)


        if(event.type==pygame.MOUSEBUTTONDOWN):
            if(intro_quit_text_rect.collidepoint(mouse_pos)): 
                intro_click_sound.play()
                leave()
            elif(intro_start_text_rect.collidepoint(mouse_pos)): 
                game_event = 1
                intro_click_sound.play()
                intro_bgm.stop()


        

        
        
    elif game_event==1:
        display.blit(main_bg,(-150,-70))


        if(event.type == pygame.MOUSEBUTTONDOWN):
            shoot = True
            bullet_hitbox.x = player.sprite.rect.x

       
        if(event.type==pygame.MOUSEBUTTONDOWN):
            star = True

        if(star==True):
            bullet_speed = 50
            if(bullet_hitbox.x<1300 and player.sprite.rect.y == 325 and player.sprite.left==False):
                bullet_sound.play()
                bullet_speed -= 1
                bullet_hitbox.x += bullet_speed
                display.blit(bullet,bullet_hitbox)
            else:
                # bullet_hitbox.x = player.sprite.rect.x
                star=False

        collision()

        
        enemy.draw(display)
        enemy.update()
        player.draw(display)
        player.update()
        # print(pygame.mouse.get_pos())






    pygame.display.update()
    frameRate.tick(60)
