import asyncio
import platform
import pygame
import sys
import random

# --- Initialization ---
pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pokémon FireRed-Inspired Overworld (Kanto)")
clock = pygame.time.Clock()

# --- Constants ---
TILE_SIZE = 16
FPS = 60
PLAYER_SPEED = 2

# --- Color Palette ---
palette = [
    (0, 0, 0, 0),      # 0: transparent
    (0, 255, 0, 255),  # 1: green (grass)
    (139, 69, 19, 255),# 2: brown (path)
    (0, 0, 255, 255),  # 3: blue (water)
    (255, 0, 0, 255),  # 4: red (building)
    (0, 128, 0, 255),  # 5: dark green (tree)
    (255, 255, 0, 255),# 6: yellow (sign)
]

# --- Tile Definitions ---
grass_tile = [[1 for _ in range(16)] for _ in range(16)]
path_tile = [[2 for _ in range(16)] for _ in range(16)]
water_tile = [[3 for _ in range(16)] for _ in range(16)]
building_tile = [[4 for _ in range(16)] for _ in range(16)]
tree_tile = [[5 for _ in range(16)] for _ in range(16)]
sign_tile = [[6 for _ in range(16)] for _ in range(16)]

# --- Player Sprite Definition ---
player_data = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,4,4,4,4,4,4,4,4,0,0,0,0],
    [0,0,0,4,4,4,4,4,4,4,4,4,4,0,0,0],
    [0,0,0,4,4,4,4,4,4,4,4,4,4,0,0,0],
    [0,0,0,4,4,4,4,4,4,4,4,4,4,0,0,0],
    [0,0,0,0,4,4,4,4,4,4,4,4,0,0,0,0],
    [0,0,0,0,0,2,2,2,2,2,2,0,0,0,0,0],
    [0,0,0,0,0,2,2,2,2,2,2,0,0,0,0,0],
    [0,0,0,0,0,2,2,2,2,2,2,0,0,0,0,0],
    [0,0,0,0,0,2,2,2,2,2,2,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
]

# --- Helper Function to Create Surfaces ---
def create_surface(data, palette, size):
    surf = pygame.Surface(size, pygame.SRCALPHA)
    for y in range(len(data)):
        for x in range(len(data[0])):
            color_index = data[y][x]
            if color_index != 0:
                surf.set_at((x, y), palette[color_index][:3])
    return surf

# --- Setup Tiles and Player ---
tile_surfaces = [
    create_surface(grass_tile, palette, (TILE_SIZE, TILE_SIZE)),
    create_surface(path_tile, palette, (TILE_SIZE, TILE_SIZE)),
    create_surface(water_tile, palette, (TILE_SIZE, TILE_SIZE)),
    create_surface(building_tile, palette, (TILE_SIZE, TILE_SIZE)),
    create_surface(tree_tile, palette, (TILE_SIZE, TILE_SIZE)),
    create_surface(sign_tile, palette, (TILE_SIZE, TILE_SIZE)),
]
player_surf = create_surface(player_data, palette, (TILE_SIZE, TILE_SIZE))
walkable_tiles = [0, 1]  # Grass and path are walkable

# --- Map Data (Simplified Kanto Maps) ---
map_data = {
    'pallet_town': [
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 0, 0, 0, 0, 0, 0, 0, 0, 3],
        [3, 0, 4, 4, 0, 0, 4, 4, 0, 3],
        [3, 0, 4, 4, 0, 0, 4, 4, 0, 3],
        [3, 0, 0, 0, 0, 0, 0, 0, 0, 3],
        [3, 0, 0, 0, 1, 1, 0, 0, 0, 3],
        [3, 0, 0, 0, 1, 1, 0, 0, 0, 3],
        [3, 0, 0, 0, 0, 0, 0, 0, 0, 3],
        [3, 0, 0, 0, 0, 0, 0, 0, 0, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    ],
    'route_1': [
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 5, 5, 1, 1, 5, 5, 0, 0],
        [0, 0, 5, 5, 1, 1, 5, 5, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    ],
    'viridian_city': [
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 0, 0, 0, 0, 0, 0, 0, 0, 3],
        [3, 0, 4, 4, 4, 4, 4, 4, 0, 3],
        [3, 0, 4, 4, 4, 4, 4, 4, 0, 3],
        [3, 0, 0, 0, 0, 0, 0, 0, 0, 3],
        [3, 0, 0, 0, 1, 1, 0, 0, 0, 3],
        [3, 0, 0, 0, 1, 1, 0, 0, 0, 3],
        [3, 0, 0, 0, 0, 0, 0, 0, 0, 3],
        [3, 0, 0, 0, 0, 0, 0, 0, 0, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    ],
}

# --- Map Connections ---
connections = {
    'pallet_town': {'north': 'route_1'},
    'route_1': {'south': 'pallet_town', 'north': 'viridian_city'},
    'viridian_city': {'south': 'route_1'},
}

# --- Collision Detection ---
def check_collision(x, y, map_data):
    map_width = len(map_data[0])
    map_height = len(map_data)
    left_tile = int(x // TILE_SIZE)
    right_tile = int((x + TILE_SIZE - 1) // TILE_SIZE)
    top_tile = int(y // TILE_SIZE)
    bottom_tile = int((y + TILE_SIZE - 1) // TILE_SIZE)
    for ty in range(top_tile, bottom_tile + 1):
        for tx in range(left_tile, right_tile + 1):
            if 0 <= tx < map_width and 0 <= ty < map_height:
                if map_data[ty][tx] not in walkable_tiles:
                    return True
    return False

# --- Game State ---
current_map = 'pallet_town'
player_x, player_y = 5 * TILE_SIZE, 5 * TILE_SIZE  # Start in Pallet Town

def setup():
    pass  # Initialization already handled above

async def update_loop():
    global current_map, player_x, player_y

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()

    # Player Movement
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    if keys[pygame.K_LEFT]:
        dx = -PLAYER_SPEED
    elif keys[pygame.K_RIGHT]:
        dx = PLAYER_SPEED
    if keys[pygame.K_UP]:
        dy = -PLAYER_SPEED
    elif keys[pygame.K_DOWN]:
        dy = PLAYER_SPEED

    # Handle horizontal movement
    if dx != 0:
        new_x = player_x + dx
        map_width = len(map_data[current_map][0])
        if dx > 0:  # Moving right
            if new_x + TILE_SIZE > map_width * TILE_SIZE:
                if 'east' in connections.get(current_map, {}):
                    next_map = connections[current_map]['east']
                    next_map_data = map_data[next_map]
                    next_map_width = len(next_map_data[0])
                    next_player_x = new_x - map_width * TILE_SIZE
                    if not check_collision(next_player_x, player_y, next_map_data):
                        current_map = next_map
                        player_x = next_player_x
            else:
                if not check_collision(new_x, player_y, map_data[current_map]):
                    player_x = new_x
        elif dx < 0:  # Moving left
            if new_x < 0:
                if 'west' in connections.get(current_map, {}):
                    next_map = connections[current_map]['west']
                    next_map_data = map_data[next_map]
                    next_map_width = len(next_map_data[0])
                    next_player_x = new_x + next_map_width * TILE_SIZE
                    if not check_collision(next_player_x, player_y, next_map_data):
                        current_map = next_map
                        player_x = next_player_x
            else:
                if not check_collision(new_x, player_y, map_data[current_map]):
                    player_x = new_x

    # Handle vertical movement
    if dy != 0:
        new_y = player_y + dy
        map_height = len(map_data[current_map])
        if dy > 0:  # Moving down
            if new_y + TILE_SIZE > map_height * TILE_SIZE:
                if 'south' in connections.get(current_map, {}):
                    next_map = connections[current_map]['south']
                    next_map_data = map_data[next_map]
                    next_map_height = len(next_map_data)
                    next_player_y = new_y - map_height * TILE_SIZE
                    if not check_collision(player_x, next_player_y, next_map_data):
                        current_map = next_map
                        player_y = next_player_y
            else:
                if not check_collision(player_x, new_y, map_data[current_map]):
                    player_y = new_y
        elif dy < 0:  # Moving up
            if new_y < 0:
                if 'north' in connections.get(current_map, {}):
                    next_map = connections[current_map]['north']
                    next_map_data = map_data[next_map]
                    next_map_height = len(next_map_data)
                    next_player_y = new_y + next_map_height * TILE_SIZE
                    if not check_collision(player_x, next_player_y, next_map_data):
                        current_map = next_map
                        player_y = next_player_y
            else:
                if not check_collision(player_x, new_y, map_data[current_map]):
                    player_y = new_y

    # Camera Movement
    map_width = len(map_data[current_map][0])
    map_height = len(map_data[current_map])
    map_pixel_width = map_width * TILE_SIZE
    map_pixel_height = map_height * TILE_SIZE
    cam_x = max(0, min(player_x - WIDTH // 2, map_pixel_width - WIDTH))
    cam_y = max(0, min(player_y - HEIGHT // 2, map_pixel_height - HEIGHT))

    # Rendering
    screen.fill((0, 0, 0))
    start_tx = max(0, int(cam_x // TILE_SIZE))
    end_tx = min(map_width, int((cam_x + WIDTH) // TILE_SIZE) + 1)
    start_ty = max(0, int(cam_y // TILE_SIZE))
    end_ty = min(map_height, int((cam_y + HEIGHT) // TILE_SIZE) + 1)
    for ty in range(start_ty, end_ty):
        for tx in range(start_tx, end_tx):
            tile_index = map_data[current_map][ty][tx]
            screen.blit(tile_surfaces[tile_index], (tx * TILE_SIZE - cam_x, ty * TILE_SIZE - cam_y))
    screen.blit(player_surf, (player_x - cam_x, player_y - cam_y))
    pygame.display.flip()

async def main():
    setup()
    while True:
        await update_loop()
        await asyncio.sleep(1.0 / FPS)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())
