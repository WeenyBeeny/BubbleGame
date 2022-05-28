# 게임 종료 처리
# 성공 : 화면 내에 모든 버블이 사라지면 성공
# 실패 : 바닥에 어떤 정해진 높이보다 버블이 낮게 내려오면 실패
# 추후 stage 2 ~ 예정입니다
import os, random, math
import pygame

# 버블 클래스 생성  Sprite 를 통해 2D 이미지들을 연속적으로 화면에 나타낸다, super를 통해 상속받은 부모클래스의 init 메소드 호출
class Bubble(pygame.sprite.Sprite):

    def __init__(self, image, color, position=(0,0), row_idx=-1, col_idx=-1):
        super().__init__()
        self.image = image
        self.color = color
        self.rect = image.get_rect(center=position)  # Sprite를 상속받기 위해서는 image 와 rect는 꼭 필요하다
        self.radius = 18                             # 18보다 더 커지면 버블이 빨리 이동한고, 작아지면 느리게 이동한다.
        self.row_idx = row_idx                       # 버블의 row 위치를 알 수 있다.
        self.col_idx = col_idx                       # 버블의 col 위치를 알 수 있다.
    
    def set_rect(self, position):
        self.rect = self.image.get_rect(center=position)

    def draw(self, screen, to_x=None):
        if to_x:
            screen.blit(self.image, (self.rect.x + to_x, self.rect.y))
        else:
            screen.blit(self.image, self.rect)

    def set_angle(self, angle):
        self.angle = angle   # angle에 값이 들어가면 바로 아래 코드 radians를 통해 호도법으로 바꾸어준다.
        self.rad_angle = math.radians(self.angle)    # 앵글을 60분법으로 계산하기 어려운 상황이 있으니 호도법으로 바꾸주기 위한 radian 활용

    def move(self):  # 발사되는 버블을 움직임을 위해 삼각함수 활용해야 한다.
        to_x = self.radius * math.cos(self.rad_angle)
        to_y = self.radius * math.sin(self.rad_angle) * -1   # pygame의 경우 맨위가 0이고 밑으로 내려갈수록 -이다. 이에 방향의 반전을 계산하기 위해 (버블을 위로 쏘기 위해)

        self.rect.x += to_x
        self.rect.y += to_y

        if self.rect.left < 0 or self.rect.right > screen_width:    # 버블이 게임 화면의 좌우 틀을 벗어나면 반사되도록
            self.set_angle(180 - self.angle)

    def set_map_index(self, row_idx, col_idx):
        self.row_idx = row_idx
        self.col_idx = col_idx

    def drop_downward(self, height):
        self.rect = self.image.get_rect(center=(self.rect.centerx, self.rect.centery + height))

# 발사대 클래스 생성
class Pointer(pygame.sprite.Sprite):
    def __init__(self, image, position, angle):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=position)
        self.angle = angle
        self.original_image = image
        self.position = position

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    # 회전
    def rotate(self, angle):
        self.angle += angle

        if self.angle > 170:  # 발사대의 각도가 170도, 10도를 넘어가려하면 170도, 10도를 넘지못하도록 설정
            self.angle = 170
        elif self.angle < 10:
            self.angle = 10

        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.position)

# 맵 만들기
def setup():
    global map      # global을 통해 지역이 아닌 전역에 map 변수를 사용하겠다.
    map = [
        # ["R", "R", "Y", "Y", "B", "B", "G", "G"]
        list("RRYYBBGG"),   # 윗줄을 문자열 하나로 만들어 리스트로 만들었다.
        list("RRYYBBG/"),   # / : 버블이 위치할 수 없는 곳   RRYYBBGG  RRYYBBG  BBGGRRYY  BGGRRYY
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
            bubble_group.add(Bubble(image, col, position, row_idx, col_idx))   # Bubble 객체를 (image, col, position)를 통해 만들고, 만들어진 클래스 객체를 bubble_group에 추가한다.

def get_bubble_position(row_idx, col_idx):     # 주어진 맵의 좌표 인덱스를 기준으로 버블이 그려져야할 위치를 계산한다.
    pos_x = col_idx * CELL_SIZE + (BUBBLE_WIDTH // 2)
    pos_y = row_idx * CELL_SIZE + (BUBBLE_HEIGHT // 2) + wall_height
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

def prepare_bubbles():                              # 다음 버블을 준비
    global curr_bubble, next_bubble                 # global을 통한 전역함수 선언
    if next_bubble:                                 # next_bubble 버블이 있다면 curr_bubble은 next_bubble로 바꿔준다. 
        curr_bubble = next_bubble                   
    else:
        curr_bubble = create_bubble()               # curr_bubble이 없을 경우 새 버블을 랜덤으로 만들어준다. (게임 시작시 처음)

    curr_bubble.set_rect((screen_width // 2, 624))  # 발사대 위쪽에 현재 쏠 수 있는 버블을 위치시키기 
    next_bubble = create_bubble()
    next_bubble.set_rect((screen_width // 4, 688))  # 다음 예측 버블 색의 위치

def create_bubble():
    color = get_random_bubble_color()
    image = get_bubble_image(color)
    return Bubble(image, color)

def get_random_bubble_color(): # 랜덤으로 버블 색상을 준비, 또한 게임의 원할한 클리어를 위한 남아있는 버블의 색상만 나타나도록 설정
    colors = []
    for row in map:                                         # 맵에서 row를
        for col in row:                                     # row에서 각 색상 중 하나를
            if col not in colors and col not in [".", "/"]: # 비어있는 버블이거나, 넣을 수 없는 위치가 아닌 현재 colors에서 없는 색상만,
                colors.append(col)                          # 소환하도록 한다.
    return random.choice(colors)

def process_collision():   # 버블끼리 충돌하면 발사된 버블은 해당 위치에 머물 수 있도록
    global curr_bubble, fire, curr_fire_count
    hit_bubble = pygame.sprite.spritecollideany(curr_bubble, bubble_group, pygame.sprite.collide_mask)    # 버블 그룹 내에 어떤 것이든 충돌하면 충돌된 대상을 가지고 온다.
    # curr_bubble, bubble_group 가 투명영역(collide_mask)을 제외하고, 존재하는 이미지와 비교시 충돌이 감지되면 충돌된 버블을 hit_bubble에 가져온다.
    if hit_bubble or curr_bubble.rect.top <= wall_height:
        row_idx, col_idx = get_map_index(*curr_bubble.rect.center)  # (x, y) 현재 튜플로 되어있다.  * 언패킹을 통해 x, y 각각 따로 전달
        place_bubble(curr_bubble, row_idx, col_idx)
        remove_adjacent_bubbles(row_idx, col_idx, curr_bubble.color)  # 맵 기준으로 row_idx 와 col_idx 버블색이 같을 경우 방문하도록 설정
        curr_bubble = None
        fire = False
        curr_fire_count -= 1

def get_map_index(x, y):
    row_idx = (y - wall_height) // CELL_SIZE
    col_idx = x // CELL_SIZE
    if row_idx % 2 == 1:
        col_idx = (x - (CELL_SIZE // 2))  // CELL_SIZE
        if col_idx < 0:                       # 좌측 가장자리에 구슬이 위치할 수 프레임을 넘지 않도록
            col_idx = 0
        elif col_idx > MAP_COLUMN_COUNT - 2:  # 우측 가장자리에 구슬이 위치할 수 프레임을 넘지 않도록
            col_idx = MAP_COLUMN_COUNT - 2
    return row_idx, col_idx

def place_bubble(bubble, row_idx, col_idx):   # 발사한 버블이 정착했을시 위치
    map[row_idx][col_idx] = bubble.color
    position = get_bubble_position(row_idx, col_idx)
    bubble.set_rect(position)
    bubble.set_map_index(row_idx, col_idx)
    bubble_group.add(bubble)

def remove_adjacent_bubbles(row_idx, col_idx, color):
    visited.clear()
    visit(row_idx, col_idx, color)
    if len(visited) >= 3:          # 3개가 넘으면 remove_adjacent_bubbles 발동
        remove_visited_bubbles()   # 정착한 버블이 같은 색을 찾기위해 주변을 탐색한다.
        remove_hanging_bubbles()   # 천장에 매달려 있는게 아닌 덩그러니 떠있는 것도 제거해 줘야한다.

def visit(row_idx, col_idx, color=None):  # 3개의 if를 넘겨야 방문처리하는 재귀함수
    # 맵의 범위를 벗어나는지 확인
    if row_idx < 0 or row_idx >= MAP_ROW_COUNT or col_idx < 0 or col_idx >= MAP_COLUMN_COUNT:
        return
    # 현재 Cell 의 색상이 color 와 같은지 확인
    if color and map[row_idx][col_idx] != color:
        return
    # 빈 공간이거나, 버블이 존재할 수 없는 위치인지 확인
    if map[row_idx][col_idx] in [".", "/"]:   # . 비어있는 버블이거나 / 버블이 위치할 수 없는 곳에는 스킵
        return
    # row_idx, col_idx 가 visited 에 이미 방문했는지 여부
    if (row_idx, col_idx) in visited:
        return
    # 방문처리
    visited.append((row_idx, col_idx))

    # 발사된 버블이 정착후 탐색할 수 있는 버블의 좌표 경우의수, 이후 조건에 맞으면 pop
    rows = [0, -1, -1, 0, 1, 1]
    cols = [-1, -1, 0, 1, 0, -1]   
    if row_idx % 2 == 1:  # 발사된 버블이 정착된 곳이 홀수 줄이라면, 해당 좌표로 버블간 조건 검샘
        rows = [0, -1, -1, 0, 1, 1]
        cols = [-1, 0, 1, 1, 1, 0]

    # 정착한 버블이 주변 위치를 방문하여 pop 조건에 맞는지 알아본다.
    for i in range(len(rows)):   
        visit(row_idx + rows[i], col_idx + cols[i], color)
    
def remove_visited_bubbles():
    bubbles_to_remove = [b for b in bubble_group if (b.row_idx, b.col_idx) in visited]
    for bubble in bubbles_to_remove:
        map[bubble.row_idx][bubble.col_idx] = "."
        bubble_group.remove(bubble)

def remove_not_visited_bubbles():  # 떠있는 버블 클리어처리
    bubbles_to_remove = [b for b in bubble_group if (b.row_idx, b.col_idx) not in visited] # b.row_idx, b.col_idx 가 visited 에 포함이 안되어있으면 가져온다.
    for bubble in bubbles_to_remove:
        map[bubble.row_idx][bubble.col_idx] = "."
        bubble_group.remove(bubble)

def remove_hanging_bubbles():      # 떠있는 버블 클리어처리
    visited.clear()
    for col_idx in range(MAP_COLUMN_COUNT):
        if map[0][col_idx] != ".":
            visit(0, col_idx)   # color는 보지 않는다. 색상 상관없이 떠있는 버블은 클리어처리해준다.
    remove_not_visited_bubbles()

def draw_bubbles():
    to_x = None
    if curr_fire_count == 2:
        to_x = random.randint(0, 4) - 2 # -2 ~ 2     음수의 경우 좌로 흔들림, 양수의 경우 우로 흔들림
    elif curr_fire_count == 1:
        to_x = random.randint(0, 12) - 6 # -6 ~ 6    음수의 경우 좌로 흔들림, 양수의 경우 우로 흔들림
    
    for bubble in bubble_group:
        bubble.draw(screen, to_x)

def drop_wall():
    global wall_height, curr_fire_count   # 7발이 발사되었을시 벽(버블 1줄의 셀)이 내려오도록하였다.
    wall_height += CELL_SIZE
    for bubble in bubble_group:
        bubble.drop_downward(CELL_SIZE)
    curr_fire_count = FIRE_COUNT

def get_lowest_bubble_bottom():           # 가장 밑에 위치하고 있는 버블을 호출
    bubble_bottoms = [bubble.rect.bottom for bubble in bubble_group]
    return max(bubble_bottoms)

def change_bubble_image(image):
    for bubble in bubble_group:
        bubble.image = image

def display_game_over():
    txt_game_over = game_font.render(game_result, True, WHITE)
    rect_game_over = txt_game_over.get_rect(center=(screen_width//2, screen_height//2))
    screen.blit(txt_game_over, rect_game_over)

pygame.init()
# 게임의 창은 가로 448, 세로 720으로 설정하고 pygame에 넘겨주었다.
screen_width = 448     
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Bubble Game")   # 게임이름은 Bubble Game로 설정하였다.
clock = pygame.time.Clock()

# 배경 이미지 불러오기
current_path = os.path.dirname(__file__)  # 지금 실행하고 있는 파일의 경로를 받아온다.
background = pygame.image.load(os.path.join(current_path, "background.jpg"))
pikachu = pygame.image.load(os.path.join(current_path, "pika.png"))
gigidae = pygame.image.load(os.path.join(current_path, "gigidae.png"))
turtle = pygame.image.load(os.path.join(current_path, "turtle.png"))
rice = pygame.image.load(os.path.join(current_path, "rice.png"))

# 벽 이미지 불러오기
wall = pygame.image.load(os.path.join(current_path, "wall.png"))

# 버블 이미지 불러오기 , convert_alpha() 를 통한 투명도 설정
bubble_images = [
    pygame.image.load(os.path.join(current_path, "Red.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "Yellow.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "Blue.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "Green.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "Purple.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "Black.png")).convert_alpha()
]

# 발사대 이미지 불러오기 
pointer_image = pygame.image.load(os.path.join(current_path, "pointer.png"))
pointer = Pointer(pointer_image, (screen_width // 2, 624), 90)   # 발사대 클래스 객체,  최초값은 90도로 설정하였다.

# 게임 관련 변수
CELL_SIZE = 56
BUBBLE_WIDTH = 56
BUBBLE_HEIGHT = 62
RED = (255,0,0)
WHITE = (255,255,255)
MAP_ROW_COUNT = 11
MAP_COLUMN_COUNT = 8
FIRE_COUNT = 7

# 발사대 움직임 변수
# to_angle = 0 # 좌우로 움직일 각도 정보
to_angle_left = 0  # 왼쪽으로 움직일 각도 정보
to_angle_right = 0 # 오른쪽으로 움직일 각도 정보
angle_speed = 1.5  # 1.5도씩 움직이도록 설정

curr_bubble = None  # 이번에 쏠 버블
next_bubble = None  # 다음에 쏠 버블
fire = False        # 발사 여부, True라면 버블이 발사되고 있는 상황
curr_fire_count = FIRE_COUNT
wall_height = 0     # 화면에 보여지는 벽의 높이

is_game_over = False
game_font = pygame.font.SysFont("arialrounded", 40)   # 게임오버 메세지를 위한 폰트
game_result = None

map = []      # 게임 맵
visited = []  # 방문 위치 기록
bubble_group = pygame.sprite.Group()
setup()

running = True   #  running 가 True일 경우 게임루프가 계속 돌도록 설정
while running:
    clock.tick(65)   # FPS 65 으로 설정

    # 게임을 닫았을 경우 실행이 멈추도록 설정
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:   # 대문자 KEYDOWN 를 통해 어떤 키를 눌렀을시 이벤트가 발생하도록 설정
            if event.key == pygame.K_LEFT:
                to_angle_left += angle_speed
            elif event.key == pygame.K_RIGHT:
                to_angle_right -= angle_speed
            elif event.key == pygame.K_SPACE:
                if curr_bubble and not fire:
                    fire = True              # 버블을 쏘고 있지 않은 상황이면 쏠 수 있도록
                    curr_bubble.set_angle(pointer.angle)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                to_angle_left = 0       
            elif event.key == pygame.K_RIGHT:
                to_angle_right = 0       

    if not curr_bubble:     # 지금 쏠 버블이 없다면? 다시 만들어야지~
        prepare_bubbles()

    if fire:
        process_collision() # 충돌 처리

    if curr_fire_count == 0:
        drop_wall()

    if not bubble_group:                                       # 게임 성공 조건 : 모든 버블을 사라지게 했을 때
        game_result = "Mission Complete"
        is_game_over = True
    elif get_lowest_bubble_bottom() > len(map) * CELL_SIZE:    # 게임 실패 조건 : 버블이 발사대 선을 넘었을 때
        game_result = "Game Over"
        is_game_over = True
        change_bubble_image(bubble_images[-1])      # 게임 오버시 모든 버블을 검은색으로

    screen.blit(background, (0, 0))
    screen.blit(wall, (0, wall_height - screen_height))
    screen.blit(pikachu, (290, 655))
    screen.blit(gigidae, (186, 655))
    screen.blit(turtle, (140, 667))
    screen.blit(rice, (0, 655))


    draw_bubbles()
    pointer.rotate(to_angle_left + to_angle_right)    # rotate pointer 이미지를 to_angle 각도에 맞춰 회전을 시켜주는 메소드, left + right를 통해 겹치는 동작을 최소화하였다.
    pointer.draw(screen)
    if curr_bubble:   
        if fire:      # 발사가 되고있는 상태라면 move함수를 발동
            curr_bubble.move()
        curr_bubble.draw(screen)

    if next_bubble:
        next_bubble.draw(screen)

    if is_game_over:
        display_game_over()
        running = False
    
    pygame.display.update()

pygame.time.delay(2000)  # 게임 종료 전 2초간 딜레이 후 종료
pygame.quit()            