import pygame
from random import randrange as rnd

WIDTH, HEIGHT = 1200, 800
fps = 60

# paddle settings
paddle_w = 330
paddle_h = 35
paddle_speed = 15
paddle = pygame.Rect(WIDTH // 2 - paddle_w // 2, HEIGHT - paddle_h - 10, paddle_w, paddle_h)

# ball settings
ball_radius = 20
ball_speed = 6
ball_rect = int(ball_radius * 2 ** 0.5)
ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect)
dx, dy = 1, -1

# blocks setting
block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(10) for j in range(4)]

# game score
score = 0

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# font settings
font_score = pygame.font.SysFont('Arial', 26, bold = True)
font_game_over = pygame.font.SysFont('Arial', 70, bold = True)

# background image for game
img = pygame.image.load('img/background.jpg').convert()


def detect_collision(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx

    return dx, dy


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    # drawing game desk
    sc.blit(img, (0, 0))
    [pygame.draw.rect(sc, color_list[color], block) for color, block in enumerate(block_list)]
    pygame.draw.rect(sc, pygame.Color('darkorange'), paddle)
    pygame.draw.circle(sc, pygame.Color('white'), ball.center, ball_radius)

    # show score current
    render_score = font_score.render(f'SCORE: {score}', 1, pygame.Color('orange'))
    sc.blit(render_score, (5, 5))

    # ball movement
    ball.x += ball_speed * dx
    ball.y += ball_speed * dy

    # collision left right
    if ball.centerx < ball_radius or ball.centerx > WIDTH - ball_radius:
        dx = -dx
    # collision top
    if ball.centery < ball_radius:
        dy = -dy
    # collision paddle
    if ball.colliderect(paddle) and dy > 0:
        dx, dy = detect_collision(dx, dy, ball, paddle)

    # collision blocks
    hit_index = ball.collidelist(block_list)
    if hit_index != -1:
        hit_rect = block_list.pop(hit_index)
        hit_color = color_list.pop(hit_index)
        dx, dy = detect_collision(dx, dy, ball, hit_rect)
        # special effects
        hit_rect. inflate_ip(ball.width * 3, ball.height * 3)
        pygame.draw.rect(sc, hit_color, hit_rect)
        fps += 1
        # score current
        score +=1

    # win or game over
    if ball.bottom > HEIGHT:
        render_game_over = font_game_over.render('GAME OVER', 1, pygame.Color('Orange'))
        sc.blit(render_game_over, (WIDTH // 2 - 210, HEIGHT // 2 - 50))
        pygame.display.flip()
        #print('GAME OVER!')
        #exit()
    elif not len(block_list):
        render_game_over = font_game_over.render('WIN', 1, pygame.Color('Orange'))
        sc.blit(render_game_over, (WIDTH // 2 - 210, HEIGHT // 2 - 50))
        pygame.display.flip()
    # control
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and paddle.left > 0:
        paddle.left -= paddle_speed
    if key[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.right += paddle_speed

    # update screen
    pygame.display.flip()
    clock.tick(fps)