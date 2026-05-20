import pygame
import sys

pygame.init()

# ===== 설정 =====
CELL_SIZE = 60
FPS = 60

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Flow Free Mini")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 50)

# 색상 정의
COLORS = {
    0: (30, 30, 30),
    1: (255, 0, 0),
    2: (255, 255, 0),
    3: (0, 0, 255),
    4: (0, 255, 0),
    5: (135, 206, 235),
    6: (255, 165, 0),
    7: (255, 105, 180),
    8: (128, 0, 128),
    9: (139, 69, 19),
    10: (255, 255, 255),
    11: (127, 127, 127),
}

# ===== 스테이지 =====
stages = [
    [
        [0,0,0,0,3],
        [0,2,4,0,2],
        [0,0,0,0,1],
        [0,0,4,0,0],
        [3,0,0,0,1],
    ],
    [
        [2, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 6, 1, 3, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [6, 0, 0, 0, 4, 0, 0],
        [5, 0, 4, 0, 1, 0, 0],
        [0, 0, 0, 0, 3, 0, 0],
        [0, 0, 0, 5, 2, 0, 0],
    ],
    [
        [9, 0, 0, 0, 0, 0, 0, 0, 0],
        [7, 1, 5, 0, 2, 9, 3, 6, 0],
        [0, 0, 0, 0, 0, 8, 0, 0, 0],
        [0, 7, 1, 5, 0, 0, 0, 4, 0],
        [0, 0, 3, 2, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 0, 0, 0, 0, 0],
        [0, 6, 0, 4, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ],
    [
        [0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 7, 1, 0, 6, 0, 0, 0, 0, 0, 0],
        [0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 8, 0, 0, 0, 2, 0],
        [0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 6, 0, 0, 0, 0, 0, 8, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 2, 4, 0],
        [0, 0, 0, 0, 0, 3, 0, 7, 1, 0, 0],
    ],
    [
        [0, 0, 0, 11,0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 7, 0, 8, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 10,0, 0, 0, 0, 4, 0, 2, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 5, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 11,3, 5, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 3, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 7, 10,0, 0, 0, 6, 9, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 9, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ],
]

# ===== 상태 =====
stage_idx = 0
board = []
original = []
paths = {}
endpoints = {}

N = 5
WIDTH = HEIGHT = 0

current_color = None
show_clear_popup = False

LINE_WIDTH = CELL_SIZE // 2
NODE_RADIUS = LINE_WIDTH // 2


def load_stage(idx):
    global board, original, N, WIDTH, HEIGHT, paths, endpoints
    original = [row[:] for row in stages[idx]]
    board = [row[:] for row in stages[idx]]
    N = len(board)
    WIDTH = HEIGHT = N * CELL_SIZE
    pygame.display.set_mode((WIDTH, HEIGHT))

    paths = {}
    endpoints = {}

    for i in range(N):
        for j in range(N):
            if original[i][j] != 0:
                c = original[i][j]
                endpoints.setdefault(c, []).append((i, j))


def cell_center(r, c):
    return (c*CELL_SIZE + CELL_SIZE//2, r*CELL_SIZE + CELL_SIZE//2)


def draw():
    screen.fill((0,0,0))

    # 선
    for color, path in paths.items():
        for i in range(len(path)-1):
            pygame.draw.line(screen, COLORS[color],
                             cell_center(*path[i]),
                             cell_center(*path[i+1]),
                             LINE_WIDTH)

    # 노드
    for i in range(N):
        for j in range(N):
            if board[i][j] != 0:
                pygame.draw.circle(screen, COLORS[board[i][j]],
                                   cell_center(i,j), NODE_RADIUS)

    # 격자
    for i in range(N):
        for j in range(N):
            rect = pygame.Rect(j*CELL_SIZE, i*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, (200,200,200), rect, 1)

    # 시작점 강조
    for i in range(N):
        for j in range(N):
            if original[i][j] != 0:
                pygame.draw.circle(screen, COLORS[original[i][j]],
                                   cell_center(i,j), CELL_SIZE//3)

    # 팝업
    button_rect = None
    if show_clear_popup:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0,0,0))
        screen.blit(overlay, (0,0))

        text = font.render("Solved!", True, (255,255,255))
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 80))

        button_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2, 200, 60)

        if button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (255,255,255), button_rect)
        else:
            pygame.draw.rect(screen, (200,200,200), button_rect)

        btn_text = font.render("Next", True, (0,0,0))
        screen.blit(btn_text, (button_rect.x + 50, button_rect.y + 10))

    pygame.display.flip()
    return button_rect


def get_cell(pos):
    x, y = pos
    return y // CELL_SIZE, x // CELL_SIZE


def is_adjacent(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1]) == 1


def is_clear():
    for row in board:
        if 0 in row:
            return False

    for color in endpoints:
        if color not in paths:
            return False

        path = paths[color]
        ends = endpoints[color]

        if len(path) < 2:
            return False

        if not ((path[0] == ends[0] and path[-1] == ends[1]) or
                (path[0] == ends[1] and path[-1] == ends[0])):
            return False

    return True


# ===== 시작 =====
load_stage(stage_idx)

running = True
while running:
    clock.tick(FPS)

    button_rect = draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if show_clear_popup:
                if button_rect and button_rect.collidepoint(pygame.mouse.get_pos()):
                    stage_idx += 1
                    if stage_idx >= len(stages):
                        print("All Clear!")
                        running = False
                    else:
                        load_stage(stage_idx)
                        show_clear_popup = False
                continue

            r, c = get_cell(pygame.mouse.get_pos())

            if 0 <= r < N and 0 <= c < N and original[r][c] != 0:
                color = original[r][c]

                # 경로 삭제
                for (x, y) in paths.get(color, []):
                    if original[x][y] == 0:
                        board[x][y] = 0

                # ⭐ 클릭한 시작점 기준으로 초기화
                paths[color] = [(r, c)]
                current_color = color

        elif event.type == pygame.MOUSEBUTTONUP:
            current_color = None

        elif event.type == pygame.MOUSEMOTION:
            if current_color is not None and not show_clear_popup:
                r, c = get_cell(pygame.mouse.get_pos())

                if not (0 <= r < N and 0 <= c < N):
                    continue

                path = paths[current_color]
                last = path[-1]

                if not is_adjacent(last, (r, c)):
                    continue

                # 뒤로 가기
                if len(path) >= 2 and (r, c) == path[-2]:
                    board[last[0]][last[1]] = 0
                    path.pop()
                    continue

                if (r, c) in path:
                    continue

                if board[r][c] != 0 and board[r][c] != current_color:
                    continue

                board[r][c] = current_color
                path.append((r, c))

    if is_clear() and not show_clear_popup:
        show_clear_popup = True

pygame.quit()
sys.exit()
