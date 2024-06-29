import pygame
import random

pygame.init()


x = 1000
y = 500


x_width = 15
y_height = 100
speed = 15


boll_r = 10
boll_speed = 6
boll_d = boll_r * 2


boll_start_x = x / 2 - boll_r
boll_start_y = y / 2 - boll_r


point_left = 0
point_right = 0


fps = 60

font = pygame.font.Font(None, 50)


screen = pygame.display.set_mode((x, y))


platform_right = pygame.Rect(x - x_width - 5, y / 2 - y_height / 2, x_width, y_height)
platform_left = pygame.Rect(5, y / 2 - y_height / 2, x_width, y_height)
boll = pygame.Rect(boll_start_x, boll_start_y, boll_d, boll_d)


dx = 1
dy = -1


dark_pink = (230, 150, 170)


clock = pygame.time.Clock()


pygame.display.set_caption("Ping-Pong")


game = True
pause = True  
start_game = False

button_width = 150
button_height = 50
button_x = x / 2 - button_width / 2
button_y = y / 2 - button_height / 2
button_color = (230, 150, 170)  


while game:
    
    screen.fill(dark_pink)

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pause and button_x <= event.pos[0] <= button_x + button_width and \
               button_y <= event.pos[1] <= button_y + button_height:
                start_game = True
                pause = False

    
    if start_game:
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] and platform_right.top > 0:
            platform_right.top -= speed
        elif key[pygame.K_DOWN] and platform_right.bottom < y:
            platform_right.bottom += speed
        elif key[pygame.K_w] and platform_left.top > 0:
            platform_left.top -= speed
        elif key[pygame.K_s] and platform_left.bottom < y:
            platform_left.bottom += speed

    pygame.draw.rect(screen, pygame.Color("white"), platform_right)
    pygame.draw.rect(screen, pygame.Color("white"), platform_left)
    pygame.draw.circle(screen, pygame.Color("white"), boll.center, boll_r)

   
    if start_game:
        boll.x += boll_speed * dx
        boll.y += boll_speed * dy

        
        if boll.top <= 0 or boll.bottom >= y:
            dy = -dy
       
        elif boll.colliderect(platform_left) or boll.colliderect(platform_right):
            dx = -dx

        
        if boll.right >= x:  
            point_left += 1
            boll.x = boll_start_x
            boll.y = boll_start_y
            dx = 0
            dy = 0
            pause = True
            goal_time = pygame.time.get_ticks()
        elif boll.left <= 0:  
            point_right += 1
            boll.x = boll_start_x
            boll.y = boll_start_y
            dx = 0
            dy = 0
            pause = True
            goal_time = pygame.time.get_ticks()

       
        if pause:
            time = pygame.time.get_ticks()
            if time - goal_time > 3000:
                dx = random.choice((1, -1))
                dy = random.choice((1, -1))
                pause = False
                start_game = True  

   
    right_text = font.render(f"{point_right}", True, pygame.Color("white"))
    screen.blit(right_text, (x - 80, 20))
    left_text = font.render(f"{point_left}", True, pygame.Color("white"))
    screen.blit(left_text, (20, 20))

   
    if pause:
        pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height))
        text = font.render("Start", True, (255, 255, 255)) 
        text_rect = text.get_rect(center=(button_x + button_width / 2, button_y + button_height / 2))
        screen.blit(text, text_rect)

   
    pygame.display.flip()
    clock.tick(fps)


pygame.quit()