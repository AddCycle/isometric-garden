import pygame
import math

WIDTH = 1280
HEIGHT = 720
TILE_SIZE = 32
TILE_HEIGHT = TILE_SIZE / 2
ROWS = 30
COLS = 30

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
tile = pygame.image.load('tile32x32.png').convert_alpha()
ball = pygame.image.load('ball32x32.png').convert_alpha()
ball_pos = (0,0)
tiles = []

u = (1,-1)
v = (0.5,0.5)

def proj(vect:tuple[float,float]):
  x,y = vect
  offsetX = WIDTH / 2
  offsetY = HEIGHT / 2 - TILE_HEIGHT * (COLS / 2)
  x_ = (x * u[0] + y * u[1]) * (TILE_SIZE / 2) + offsetX
  y_ = (x * v[0] + y * v[1]) * (TILE_HEIGHT) + offsetY
  return (x_, y_)

def draw_tile_outline_mask(vect, color=(255,0,0)):
    i,j = vect
    px, py = proj((i,j))
    top_left = (px - TILE_SIZE // 2, py - TILE_HEIGHT / 2)
    
    mask = pygame.mask.from_surface(tile)
    mask_outline = mask.outline()  # list of (x,y) relative to top-left
    
    # offset each point by the tile position
    points = [(x + top_left[0], y + top_left[1]) for x,y in mask_outline]
    
    pygame.draw.polygon(screen, color, points, 2)

def draw_tile_top_outline(vect, color=(255,0,0)):
    i,j = vect
    px, py = proj((i,j))
    # shift to match blit
    px -= TILE_SIZE // 2
    py -= TILE_HEIGHT / 2

    # define the diamond (top face) points
    points = [
        (px + TILE_SIZE // 2, py),             # top middle
        (px + TILE_SIZE, py + TILE_HEIGHT // 2), # right
        (px + TILE_SIZE // 2, py + TILE_HEIGHT), # bottom
        (px, py + TILE_HEIGHT // 2)             # left
    ]

    pygame.draw.polygon(screen, color, points, 2)

def inv_proj(vect:tuple[float,float]):
  a = u[0] * (TILE_SIZE / 2)
  b = u[1] * (TILE_SIZE / 2)
  c = v[0] * (TILE_HEIGHT)
  d = v[1] * (TILE_HEIGHT)
  mat = inv_matrix(a,b,c,d)
  offsetX = WIDTH / 2
  offsetY = HEIGHT / 2 - TILE_HEIGHT * (COLS / 2)
  x_ = (vect[0] - offsetX) * mat[0][0] + (vect[1] - offsetY) * mat[0][1]
  y_ = (vect[0] - offsetX) * mat[1][0] + (vect[1] - offsetY) * mat[1][1]
  return (round(x_), round(y_))

def inv_matrix(a,b,c,d):
  det = 1/(a*d-b*c)
  return ((det*d, det*(-b)), (det*(-c),det*a))

def contains(lst,vect):
  for e in lst:
    if e[0] == vect[0] and e[1] == vect[1]:
      return True
  return False

def draw_grid(n:int):
  # tiles.sort(key=lambda t: (t[1], t[0]))
  # for t in tiles:
  #     px, py = proj((t[0], t[1]))
  for i in range(n):
    for j in range(n):
      px, py = proj((i, j))
      # shift so the diamond is centered on proj
      screen.blit(tile, (px - TILE_SIZE // 2, py - TILE_HEIGHT / 2)) # finally working it needed to shift down by TILE_HEIGHT / 2 so by a fourth of tile_size

def draw_ball(vect:tuple[float,float]):
  i,j = vect
  px, py = proj((i, j))
  screen.blit(ball, (px - TILE_SIZE / 2, py - TILE_HEIGHT * 1.5))

def move_ball(vect:tuple[float,float]):
  global ball_pos
  ball_pos = vect

running = True
highlight_tile = proj((0,0))
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  keys = pygame.key.get_just_pressed()
  if keys[pygame.K_ESCAPE]:
    running = False
  
  if keys[pygame.K_SPACE]:
    tuile = inv_proj(highlight_tile)
    print(tuile)
    if not contains(tiles,tuile):
      tiles.append(tuile)

  if keys[pygame.K_LEFT]:
    # highlighted tile
    x,y = inv_proj(highlight_tile)
    x -= 1
    highlight_tile = proj((x,y))

    # ball
    x_,y_ = ball_pos
    x_ -= 1
    ball_pos = (x_, y_)
    print((x,y))
  
  if keys[pygame.K_RIGHT]:
    x,y = inv_proj(highlight_tile)
    x += 1
    highlight_tile = proj((x,y))

    # ball
    x_,y_ = ball_pos
    x_ += 1
    ball_pos = (x_, y_)
    print((x,y))

  if keys[pygame.K_DOWN]:
    x,y = inv_proj(highlight_tile)
    y += 1
    highlight_tile = proj((x,y))

    # ball
    x_,y_ = ball_pos
    y_ += 1
    ball_pos = (x_, y_)
    print((x,y))

  if keys[pygame.K_UP]:
    x,y = inv_proj(highlight_tile)
    y -= 1
    highlight_tile = proj((x,y))

    # ball
    x_,y_ = ball_pos
    y_ -= 1
    ball_pos = (x_, y_)
    print((x,y))
  
  if pygame.mouse.get_just_pressed()[0]:
    tuile = inv_proj(pygame.mouse.get_pos())
    x,y = tuile
    if x >= 0 and x < ROWS and y >= 0 and y < ROWS:
      highlight_tile = proj(tuile)
      move_ball(tuile)
      print(tuile)
  
  screen.fill('black')
  draw_grid(ROWS)
  draw_tile_top_outline(inv_proj(pygame.mouse.get_pos()))
  draw_tile_top_outline(inv_proj(highlight_tile), (0,255,0))
  draw_ball(ball_pos)

  pygame.display.update()

pygame.quit()