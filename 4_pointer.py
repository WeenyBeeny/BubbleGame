# 발사대 (화살표) 생성
import os
import pygame

# 버블 클래스 생성  Sprite 를 통해 2D 이미지들을 연속적으로 화면에 나타낸다, super를 통해 상속받은 부모클래스의 init 메소드 호출
class Bubble(pygame.sprite.Sprite):
    def __init__(self, image, color, position):
        super().__init__()
        self.image = image
        self.color = color
        self.rect = image.get_rect(center=position)  # Sprite를 상속받기 위해서는 image 와 rect는 꼭 필요하다

# 발사대 클래스 생성
class Pointer(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# 맵 만들기
def setup():
    global map      # global을 통해 지역이 아닌 전역에 map 변수를 사용하겠다.
    map = [
        # ["R", "R", "Y", "Y", "B", "B", "G", "G"]
        list("RRYYBBGG"),   # 윗줄을 문자열 하나로 만들어 리스트로 만들었다.
        list("RRYYBBG/"),   # / : 버블이 위치할 수 없는 곳
        list("BBGGRRYY"),
        list("BGGRRYY/"),
        list("........"),   # . : 비어 있는 곳
        list("......./"),
        list("........"),
        list("......./"),
        list("........"),
        list("......./"),
        list("........")
    ]

    for row_idx, row in enumerate(map):
        for col_idx, col in enumerate(row):
            if col in [".", "/"]:
                continue
            position = get_bubble_position(row_idx, col_idx)  # 구슬이 자리잡는 위치
            image = get_bubble_image(col)            
            bubble_group.add(Bubble(image, col, position))   # Bubble 객체를 (image, col, position)를 통해 만들고, 만들어진 클래스 객체를 bubble_group에 추가한다.

def get_bubble_position(row_idx, col_idx):     # 주어진 맵의 좌표 인덱스를 기준으로 버블이 그려져야할 위치를 게산한다.
    pos_x = col_idx * CELL_SIZE + (BUBBLE_WIDTH // 2)
    pos_y = row_idx * CELL_SIZE + (BUBBLE_HEIGHT // 2)
    if row_idx % 2 == 1:
        pos_x += CELL_SIZE // 2
    return pos_x, pos_y

def get_bubble_image(color):
    if color == "R":
        return bubble_images[0]   # red.png
    elif color == "Y":
        return bubble_images[1]   # yellow.png
    elif color == "B":
        return bubble_images[2]   # blue.png
    elif color == "G":
        return bubble_images[3]   # green.png
    elif color == "P":
        return bubble_images[4]   # purple.png
    else:                         # black.png    
        return bubble_images[-1]  # 뒤에서 1번째              

pygame.init()
# 게임의 창은 가로 448, 세로 720으로 설정하고 pygame에 넘겨주었다.
screen_width = 448     
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Bubble Game")   # 게임이름은 Bubble Game로 설정하였다.
clock = pygame.time.Clock()

# 배경 이미지 불러오기
current_path = os.path.dirname(__file__)  # 지금 실행하고 있는 파일의 경로를 받아온다.
background = pygame.image.load(os.path.join(current_path, "background.png"))

# 버블 이미지 불러오기 , convert_alpha() 를 통한 투명도 설정
bubble_images = [
    pygame.image.load(os.path.join(current_path, "red.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "yellow.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "blue.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "green.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "purple.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "black.png")).convert_alpha()
]

# 발사대 이미지 불러오기
pointer_image = pygame.image.load(os.path.join(current_path, "pointer.png"))
pointer = Pointer(pointer_image, (screen_width // 2, 624))   # 발사대 클래스 객체

# 게임 관련 변수
CELL_SIZE = 56
BUBBLE_WIDTH = 56
BUBBLE_HEIGHT = 62

map = []  # 게임 맵
bubble_group = pygame.sprite.Group()
setup()

running = True   #  running 가 True일 경우 게임루프가 계속 돌도록 설정
while running:
    clock.tick(60)   # FPS 60 으로 설정

    # 게임을 닫았을 경우 실행이 멈추도록 설정
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background, (0, 0))
    bubble_group.draw(screen)   # bubble_group에 있는 모든 sprite를 screen에 그려준다
    pointer.draw(screen)
    pygame.display.update()

pygame.quit()            
