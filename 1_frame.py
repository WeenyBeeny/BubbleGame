import pygame

pygame.init()
# 게임의 창은 가로 448, 세로 720으로 설정하고 pygame에 넘겨주었다.
screen_width = 448     
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Bubble Game")   # 게임이름은 Bubble Game로 설정하였다.
clock = pygame.time.Clock()

running = True   #  running 가 True일 경우 게임루프가 계속 돌도록 설정
while running:
    clock.tick(60)   # FPS 60 으로 설정

    # 게임을 닫았을 경우 실행이 멈추도록 설정
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()            
