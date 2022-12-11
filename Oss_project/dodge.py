import pygame
import random
import os
import threading
import time
import math
#######################################
pygame.init()

BLACK=(0,0,0)
screen_width = 500
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Dodge")

clock = pygame.time.Clock()


game_font = pygame.font.Font(None, 20)
sys_font=pygame.font.Font(None,100)

background = pygame.image.load("./image/background.png")
background = pygame.transform.scale(background,(800,1000))

player = pygame.image.load("./image/player.png")
player = pygame.transform.scale(player,(20,20))
player_size = player.get_rect().size
player_width = player_size[0]
plyaer_height = player_size[1]

total_running = True



while total_running:
    Timer = 0
    s_time = time.time()
    time.sleep(1)
    e_time = time.time()
    
    total_score = 1
    level_control = 10
    total_level = 0
    total_level_list = [30, 50, 100, 170, 200, 250, 300, 350, 400, 450, 500, 550, 600, 700, 10000000]


    player_x_pos = (screen_width / 2) - (player_width / 2)
    player_y_pos = (screen_height / 2) - (plyaer_height / 2)

    player_speed = 0.5


    player_to_x = 0
    player_to_y = 0

    player_speed = 0.5
    
    shield_mode = False
    shield_count = 0
    
    



    #아이템 클래스
    bomb_list=list()
    class bomb_class:
        bomb_image=pygame.image.load("./image/bomb.png")
        bomb_image=pygame.transform.scale(bomb_image,(30,30))
        bomb_size=bomb_image.get_rect().size
        bomb_width=bomb_size[0]
        bomb_height=bomb_size[1]
        bomb_spawnPoint=None
        bomb_x_pos=0
        bomb_y_pos=0
        

        bomb_rect = bomb_image.get_rect()
        bomb_rect.left=bomb_x_pos
        bomb_rect.top=bomb_y_pos

        def __init__(self):
            self.bomb_spawnPoint = random.choice(['ANY'])

            if self.bomb_spawnPoint == 'ANY':
                self.bomb_x_pos = random.randint(0, screen_width - self.bomb_width)
                self.bomb_y_pos = random.randint(0, screen_height - self.bomb_height)
        

        def bomb_coll(self):
            self.bomb_rect = self.bomb_image.get_rect()
            self.bomb_rect.left = self.bomb_x_pos
            self.bomb_rect.top = self.bomb_y_pos


    shield_list=list()
    class shield_class:
        shield_image=pygame.image.load("./image/shield.png")
        shield_image=pygame.transform.scale(shield_image,(30,30))
        shield_size=shield_image.get_rect().size
        shield_width=shield_size[0]
        shield_height=shield_size[1]
        shield_spawnPoint=None
        shield_x_pos=0
        shield_y_pos=0
        

        shield_rect = shield_image.get_rect()
        shield_rect.left=shield_x_pos
        shield_rect.top=shield_y_pos

        def __init__(self):
            self.shield_spawnPoint = random.choice(['ANY'])

            if self.shield_spawnPoint == 'ANY':
                self.shield_x_pos = random.randint(0, screen_width - self.shield_width)
                self.shield_y_pos = random.randint(0, screen_height - self.shield_height)
        

        def shield_coll(self):
            self.shield_rect = self.shield_image.get_rect()
            self.shield_rect.left = self.shield_x_pos
            self.shield_rect.top = self.shield_y_pos
        
        




    #적(별) 클래스
    enemy_list = list()
    class enemy_class:
        enemy_image = pygame.image.load("./image/star.png")
        enemy_image = pygame.transform.scale(enemy_image,(20,20))
        enemy_size = enemy_image.get_rect().size
        enemy_width = enemy_size[0]
        enemy_height = enemy_size[1]
        enemy_spawnPoint = None
        enemy_speed = 0
        enemy_x_pos = 0
        enemy_y_pos = 0
        enemy_rad = 0

        enemy_rect = enemy_image.get_rect()
        enemy_rect.left = enemy_x_pos
        enemy_rect.top = enemy_y_pos

      

        def __init__(self):
            self.enemy_speed = random.choice([1.0, 1.2, 1.5, 1.8, 2.0])
            self.enemy_spawnPoint = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])

            # 스폰 지점 설정
            if self.enemy_spawnPoint == 'LEFT':
                self.enemy_x_pos = - self.enemy_width
                self.enemy_y_pos = random.randint(0, screen_height - self.enemy_height)
                self.enemy_rad = random.choice([(1, 3), (1, 2), (2, 2), (2, 1), (3, 1), (3, 0), (1, -3), (1, -2), (2, -2), (2, -1), (3, -1)])
            elif self.enemy_spawnPoint == 'RIGHT':
                self.enemy_x_pos = screen_width
                self.enemy_y_pos = random.randint(0, screen_height - self.enemy_height)
                self.enemy_rad = random.choice([(-1, 3), (-1, 2), (-2, 2), (-2, 1), (-3, 1), (-3, 0), (-1, -3), (-1, -2), (-2, -2), (-2, -1), (-3, -1)])
            elif self.enemy_spawnPoint == 'UP':
                self.enemy_x_pos = random.randint(0, screen_width - self.enemy_width)
                self.enemy_y_pos = - self.enemy_height
                self.enemy_rad = random.choice([(3, 1), (2, 1), (2, 2), (1, 2), (1, 3), (0, 3), (-3, 1), (-2, 1), (-2, 2), (-1, 2), (-1, 3)])
            elif self.enemy_spawnPoint == 'DOWN':
                self.enemy_x_pos = random.randint(0, screen_width - self.enemy_width)
                self.enemy_y_pos = screen_height
                self.enemy_rad = random.choice([(3, -1), (2, -1), (2, -2), (1, -2), (1, -3), (0, -3), (-3, -1), (-2, -1), (-2, -2), (-1, -2), (-1, -3)])


        def enemy_move(self):
            self.enemy_x_pos += self.enemy_speed * self.enemy_rad[0]
            self.enemy_y_pos += self.enemy_speed * self.enemy_rad[1]
            global total_score
            
            def boundary_UP():
                if self.enemy_y_pos < -self.enemy_height:
                    return True
            
            def boundary_DOWN():
                if self.enemy_y_pos > screen_height:
                    return True
            
            def boundary_LEFT():
                if self.enemy_x_pos < -self.enemy_width:
                    return True
            
            def boundary_RIGHT():
                if self.enemy_x_pos > screen_width:
                    return True

            if self.enemy_spawnPoint == 'UP':
                if boundary_LEFT() or boundary_RIGHT() or boundary_DOWN():
                    enemy_list.remove(self)
                    total_score += 1

            if self.enemy_spawnPoint == 'DOWN':
                if boundary_LEFT() or boundary_RIGHT() or boundary_UP():
                    enemy_list.remove(self)
                    total_score += 1

            if self.enemy_spawnPoint == 'LEFT':
                if boundary_UP() or boundary_DOWN() or boundary_RIGHT():
                    enemy_list.remove(self)
                    total_score += 1

            if self.enemy_spawnPoint == 'RIGHT':
                if boundary_UP() or boundary_DOWN() or boundary_LEFT():
                    enemy_list.remove(self)
                    total_score += 1

        def enemy_coll(self):
            self.enemy_rect = self.enemy_image.get_rect()
            self.enemy_rect.left = self.enemy_x_pos
            self.enemy_rect.top = self.enemy_y_pos



    event_start = True
    while event_start:
        screen.fill(BLACK)
        startText=pygame.image.load("./image/start.png")
        startText=pygame.transform.scale(startText,(300,300))
        screen.blit(startText,((screen_width/2)-150,(screen_height/2)-150))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                    event_start = False
                    game_running = True
                


    while game_running:
        screen.fill(BLACK)
        dt = clock.tick(60)
        
         
        
        Timer += math.floor(e_time-s_time)
        Timer_sec = math.floor(Timer/60)
        

        for event in pygame.event.get():
            

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_to_x -= player_speed
                if event.key == pygame.K_RIGHT:
                    player_to_x += player_speed
                if event.key == pygame.K_UP:
                    player_to_y -= player_speed
                if event.key == pygame.K_DOWN:
                    player_to_y += player_speed
                
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    player_to_x = 0
                if event.key in [pygame.K_UP, pygame.K_DOWN]:
                    player_to_y = 0
            
        player_x_pos += player_to_x * dt
        player_y_pos += player_to_y * dt


        # 플레이어 경계값
        if player_x_pos < 0:
            player_x_pos = 0
        elif player_x_pos > screen_width - player_width:
            player_x_pos = screen_width - player_width
        if player_y_pos < 0:
            player_y_pos = 0
        elif player_y_pos > screen_height - plyaer_height:
            player_y_pos = screen_height - plyaer_height

        # 적 생성
        if total_score >= total_level_list[total_level]:
            total_level += 1

        if total_level + level_control >= len(enemy_list):
            enemy_list.append(enemy_class())
        
        # 아이템 생성
        if Timer%100 == 0:
            for i in range(1):
                item_type = random.choice(['bomb','shield'])
                if item_type == 'bomb':                
                    bomb_list.append(bomb_class())
                elif item_type == 'shield':
                    shield_list.append(shield_class())        
            


        # 충돌 처리
        player_rect = player.get_rect()
        player_rect.left = player_x_pos
        player_rect.top = player_y_pos

        for i in enemy_list:
            i.enemy_coll()
            if player_rect.colliderect(i.enemy_rect):
                enemy_list.clear()
                
                if shield_mode == False:
                    game_running=False
                    event_end=True
                elif shield_count > 0:
                    shield_count -=1
                
                    
                
                
                
        #아이템 효과 처리
        for i in bomb_list:
            i.bomb_coll()
            if player_rect.colliderect(i.bomb_rect):
                enemy_list.clear()            
                bomb_list.clear()
                total_score+= 20
       
        
        for i in shield_list:
            i.shield_coll()
            if player_rect.colliderect(i.shield_rect):
                shield_mode = True
                shield_count += 1
                       
                shield_list.clear()
                total_score+= 10
        
        if shield_count <= 0:
            shield_mode = False
        
                    



        # 화면에 그리기

        screen.blit(background, (0,-100))
        screen.blit(player, (player_x_pos, player_y_pos))
        
      
        for i in enemy_list:
            i.enemy_move()
            screen.blit(i.enemy_image, (i.enemy_x_pos, i.enemy_y_pos))

        
        for i in bomb_list:
            screen.blit(i.bomb_image,(i.bomb_x_pos, i.bomb_y_pos))
        for i in shield_list:
            screen.blit(i.shield_image,(i.shield_x_pos, i.shield_y_pos))
        

        enemy_count = game_font.render(str(len(enemy_list)-10), True, (255, 255, 255))
        screen.blit(enemy_count, (60, 10))
        
        enemy_count_text=game_font.render("Level : ",True,(255,255,255))
        screen.blit(enemy_count_text,(10,10))
        
        shield_text=game_font.render("Shield : ",True,(255,255,255))
        screen.blit(shield_text,(100,10))
        
        shield_count_text=game_font.render(str(int(shield_count)),True,(255,255,255))
        screen.blit(shield_count_text,(170,10))
        
        

        score = game_font.render(str(int(total_score)), True, (255, 255, 255))
        screen.blit(score, (screen_width - 50, 10))
        
        game_score_text=game_font.render("Score : ",True,(255,255,255))
        screen.blit(game_score_text,(screen_width - 100,10))
                
        g_timer=game_font.render(str(int(Timer_sec)),True,(255,255,255))
        screen.blit(g_timer,(screen_width  - 200,10))
        
        Time_text=game_font.render("Timer : ",True,(255,255,255))
        screen.blit(Time_text,(screen_width - 250,10))

        pygame.display.update()
        
    while event_end:
        screen.fill(BLACK)
        score_sys=sys_font.render(str(int(total_score)),True,(255,255,255))
        score_text=sys_font.render("score",True,(255,255,255))
        screen.blit(score_text,(screen_width/2-120,screen_height/2-200))
        screen.blit(score_sys, (screen_width/2-70, screen_height/2))

        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                    event_end = False
                    event_start = True
                    
        
        



