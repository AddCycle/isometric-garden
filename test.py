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

def draw_grid(n:int):
  for i in range(n):
    for j in range(n):
      px, py = proj((i, j))
      # shift so the diamond is centered on proj
      screen.blit(tile, (px - TILE_SIZE // 2, py - TILE_HEIGHT / 2)) # finally working it needed to shift down by TILE_HEIGHT / 2 so by a fourth of tile_size

running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  keys = pygame.key.get_just_pressed()
  if keys[pygame.K_ESCAPE]:
    running = False
  
  if pygame.mouse.get_just_pressed()[0]:
    print(inv_proj(pygame.mouse.get_pos()))
  
  screen.fill('black')
  draw_grid(ROWS)
  draw_tile_top_outline(inv_proj(pygame.mouse.get_pos()))

  pygame.display.update()

pygame.quit()