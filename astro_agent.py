import pygame
from sys import exit

pygame.init()




class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        character1 = pygame.image.load("image/astronaut1.png")
        character2 = pygame.image.load("image/astronaut2.png")
        self.character_list = [character1,character2]
        self.character_index = 0
        self.image = self.character_list[self.character_index]
        self.image = pygame.transform.rotozoom(self.image,0,0.20)
        self.rect = self.image.get_rect(midbottom = (260,500))
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
            self.walk_sound.play()
        # Moving Left
        if((keyboard[pygame.K_a] or keyboard[pygame.K_LEFT]) and self.rect.x >=160):
            self.char_push = -5
            self.character_index += 0.1
            if self.character_index >= len(self.character_list): self.character_index = 0
            self.image = self.character_list[int(self.character_index)]
            self.image = pygame.transform.rotozoom(self.image,0,0.20)
            self.image = pygame.transform.flip(self.image, True, False)     
            self.walk_sound.play()

    def update(self):
        # self.animation()
        self.movement()
        self.ground_state()
        # print(f"{self.rect.x}, {self.rect.y} and ", pygame.mouse.get_pos())
        
        
        
              

# bullet.x = character_position.x + (341-158)
# bullet.y = character_position.y + (414-325)




    

        



def leave():
    pygame.quit()
    exit()


# Game Details
display = pygame.display.set_mode((1280,720))
game_icon = pygame.image.load("image/icon.png")
pygame.display.set_icon(game_icon)
pygame.display.set_caption("Agent Astro")
game_event = 0            # 0 --> Intro / Outro Screen    1 --> Main Game
frameRate = pygame.time.Clock()





# Intro Screen
intro_image = pygame.image.load("image/intro_bg.png")
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
main_bg = pygame.image.load("image/background.png")
main_bg = pygame.transform.rotozoom(main_bg,0,0.569)


# Character
player = pygame.sprite.GroupSingle()
player.add(Player())


# Bullet
bullet = pygame.image.load("image/bullet.png")
bullet = pygame.transform.rotozoom(bullet,180,0.1)
p_x = player.sprite.rect.x
p_y = player.sprite.rect.y + 120
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
        
        player.draw(display)
        player.update()







    pygame.display.update()
    frameRate.tick(60)
