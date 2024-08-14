import pgzero
import pgzrun
import random
import math



WIDTH = 600
HEIGHT = 800
TILE_SIZE = 32

SPEED = 2
FORCE = 10

LEFT_FACING = 'left_facing'
RIGHT_FACING = "right_facing"

IDLE = "idle"
JUMP = "jump"
RUNNING = "running"

ANIMATION_SPEED = 0.1

LEFT = "left"
RIGHT = "right"

GRAVITY = 1
JUMP_FORCE = 40

PLATFORMS_COUNT = 20
ENEMIES_COUNT = 20
MINIMUM_PLATFORMS_DISTANCE = TILE_SIZE
ENEMY_TRIGGER_DISTANCE = 200

CAMERA_THRESHOLD = HEIGHT // 2
CAMERA_SPEED = 10

INCREASE_DIFFUCULT_HEIGHT = CAMERA_SPEED * 50
ATTEMPS_FOR_CREATION = 20

TITLE = "PHONKY DOODLE"
FONT = "pixeboy.ttf"

TITLE_SIZE = 64
ACCENT_COLOR = "white"
PRIMARY_COLOR = "white"
PARAGRAPH_SIZE = 32

def get_text_rect(screen, text,center_position, font_size):
    char_width = font_size * 0.6  
    text_width = char_width * len(text)
    text_height = font_size

    text_rect = Rect(
        center_position[0] - text_width // 2,
        center_position[1] - text_height // 2,
        text_width,
        text_height
    )
    
    return text_rect

def weighted_choice(buffer):
    choices = []
    for key, value in buffer.items():
        choices.extend([key] * int(value * 100))
    return random.choice(choices)
def calculate_boundary_distance(rect1, rect2):
    dx = max(rect1.left - rect2.right, rect2.left - rect1.right, 0)
    dy = max(rect1.top - rect2.bottom, rect2.top - rect1.bottom, 0)
    
    distance = math.sqrt(dx ** 2 + dy ** 2)
    
    return distance

def calculate_distance_between_centers(rect1, rect2):
    center1 = rect1.center
    center2 = rect2.center
    
    distance = math.sqrt((center1[0] - center2[0]) ** 2 + (center1[1] - center2[1]) ** 2)
    return distance


def normalized_vector_between_rects(rect1: Rect, rect2: Rect) -> list[int]:
    # Вычисляем центры обоих прямоугольников
    center1 = rect1.center
    center2 = rect2.center
    
    # Вычисляем вектор как разницу между центрами
    vector = [center2[0] - center1[0], center2[1] - center1[1]]
    
    # Вычисляем длину вектора
    length = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
    
    # Если длина вектора равна 0 (т.е. прямоугольники имеют одинаковые центры), возвращаем нулевой вектор
    if length == 0:
        return (0, 0)
    
    # Нормализуем вектор
    normalized_vector = [vector[0] / length, vector[1] / length]
    
    return normalized_vector

class Music:
    paused = False
    fx_paused = True

    images = {
        "on" : "./music/sound_on",
        "off" : "./music/sound_off"
    }
    rect = Rect((0,0),(64,64))

    @staticmethod
    def set_volume(volume):
        sounds.hit.set_volume(volume)
        sounds.jump.set_volume(volume)
        sounds.main.set_volume(volume)
        sounds.game_over.set_volume(volume)

    @staticmethod
    def draw(screen):
        screen

    @staticmethod
    def hit():
        if not Music.paused and not Music.fx_paused:
            sounds.hit.play()
    
    @staticmethod
    def jump():
        if not Music.paused and not Music.fx_paused:
            sounds.jump.play()

    @staticmethod
    def main_theme():
        if not Music.paused:
            sounds.main.play(-1)

    @staticmethod
    def game_over():
        if not Music.paused and not Music.fx_paused:
            sounds.game_over.play()

    @staticmethod
    def on():
        Music.paused = False
        Music.main_theme()

    @staticmethod
    def off():
        Music.paused = True
        sounds.main.stop()
    
    @staticmethod
    def on_fx():
        Music.fx_paused = False
    
    @staticmethod
    def off_fx():
        Music.fx_paused = True
    @staticmethod
    def draw(screen):
        if Music.paused:
            screen.blit(Music.images["off"], Music.rect.topleft)
        else:
            screen.blit(Music.images["on"], Music.rect.topleft)
    @staticmethod
    def mouse_event(pos):
        if Music.rect.collidepoint(pos):
            if Music.paused:
                Music.on()
            else:
                Music.off()

class Platform:
    def __init__(self, position, amount_of_blocks = 2):
        self.bounding_rect = Rect(position, (TILE_SIZE * amount_of_blocks, TILE_SIZE))

    def draw(self, screen):
        for size in range(0, self.bounding_rect.width, TILE_SIZE):
            image = ""
            if size == 0:
                image = "./platform/left"
            elif size + TILE_SIZE == self.bounding_rect.width:
                image = "./platform/right"
            else:
                image = "./platform/middle"
            screen.blit(image, (self.bounding_rect.x + size, self.bounding_rect.y))
    
    

    @staticmethod
    def generate_random(h = (TILE_SIZE, HEIGHT - TILE_SIZE), w = (TILE_SIZE, WIDTH - TILE_SIZE)):
        return Platform((random.randint(*w), random.randint(*h)), random.choice([2,3,4,5]))

    def get_rect(self):
        return self.bounding_rect
    
    def collide(self, rect):
        return self.bounding_rect.colliderect(rect)

class Platforms:
    def __init__(self, minimum_platforms_count = PLATFORMS_COUNT):
        self.platforms : list[Platform] = []
        self.minimum_platforms_count = minimum_platforms_count

    def set_platforms_count(self, count):
        self.minimum_platforms_count = max(count, 5)
    
    def get_platforms_count(self):
        return self.minimum_platforms_count
    
    def draw(self, screen):
        for platform in self.platforms:
            platform.draw(screen)
    def move(self, dy):
        for platform in self.platforms:
            platform.get_rect().y += dy
        
        self.update()
    
    def get_the_highest_platform(self):
        highest_platform = self.platforms[0] if len(self.platforms) \
                    else Platform(position = [random.randint(0, WIDTH), random.randint(HEIGHT - TILE_SIZE * 2, HEIGHT - TILE_SIZE)])

        for platform in self.platforms[1:]:
            if platform.bounding_rect.top < highest_platform.bounding_rect.top:
                highest_platform = platform
        
        return highest_platform
    def get_platforms(self):
        return self.platforms
    
    def insert(self, new_platform):
        for platform in self.platforms:
            if platform.collide(new_platform.get_rect()) or calculate_boundary_distance(platform.get_rect(), new_platform.get_rect()) <= MINIMUM_PLATFORMS_DISTANCE:
                return False
            
        self.platforms.append(new_platform)
        return True
    
    def update(self):
        self.platforms = [platform for platform in self.platforms if platform.bounding_rect.top < HEIGHT]
        highest_platform = self.get_the_highest_platform()
        attempts = 0

        while len(self.platforms) < self.minimum_platforms_count and attempts <= ATTEMPS_FOR_CREATION:
            new_platform = Platform.generate_random(h = (TILE_SIZE, max(highest_platform.bounding_rect.top - TILE_SIZE, TILE_SIZE)))
            if not self.insert(new_platform):
                attempts += 1
            
            

    def collide(self, rect):
        for platform in self.platforms:
            bounding_rect = platform.get_rect()

            if rect.bottom >= bounding_rect.top and rect.bottom <= bounding_rect.top + TILE_SIZE and rect.left + TILE_SIZE  >= bounding_rect.left and rect.right - TILE_SIZE <= bounding_rect.right:
                return platform
        return None


class Background:
    images = {
        "clouds" : "./background/cloud"
    }
    def __init__(self):
        self.clouds = []

        self.initialize_clouds()

    def initialize_clouds(self):
        for _ in range(10):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            self.clouds.append((x,y))
    
    def update(self):
        self.clouds = [cloud for cloud in self.clouds if cloud[1] < HEIGHT]
        highest_cloud = self.get_the_highest_cloud()

        while len(self.clouds) < 10:
            x = random.randint(0, WIDTH)
            y = random.randint(0, highest_cloud[1])
            self.clouds.append((x,y))

    def get_the_highest_cloud(self):
        highest_cloud = self.clouds[0]

        for cloud_position in self.clouds:
            if cloud_position[1] < highest_cloud[1]:
                highest_cloud = cloud_position
        return highest_cloud
    def draw(self, screen):
        for cloud_position in self.clouds:
            screen.blit(self.images["clouds"], cloud_position)
    
    def move(self, dy):
        self.clouds = [(x, y + dy) for x,y in self.clouds]
        self.update()
    
        
class PhysicsSprite:
    def __init__(self, images : dict [str : dict[str : list[str]]], position : list[int]) -> None:
        self.images = images
        self.bounding_rect = Rect(position, (TILE_SIZE,TILE_SIZE))

        self.current_frame_index = 0
        self.timer = 0

        self.facing_direction = RIGHT_FACING
        self.state = IDLE

        self.health = 100

        self.velocity = [0,0]

        self.on_ground = False
        self.jumped = False
        self.double_jumped = False

        self.skip_platforms = None

        self.camera_offset = 0
        
    def move(self, direction):
        if direction == LEFT:
            self.velocity[0] = -SPEED
            self.facing_direction = LEFT_FACING

        elif direction == RIGHT:
            self.velocity[0] = SPEED
            self.facing_direction = RIGHT_FACING

        self.state = RUNNING

    def force(self, force_vector):
        if force_vector[0] < 0:
            self.facing_direction = LEFT_FACING
        else:
            self.facing_direction = RIGHT_FACING
        self.velocity = force_vector

        self.state = RUNNING

    def jump(self):
        if not self.jumped:
            self.velocity[1] = -JUMP_FORCE
            self.jumped = True
            self.on_ground = False
            self.state = JUMP
            Music.jump()

        elif not self.double_jumped:
            self.velocity[1] = -JUMP_FORCE
            self.double_jumped = True
            self.state = JUMP
            Music.jump()

    def down(self, platforms):
        if self.on_ground:
            self.skip_platforms = platforms.collide(self.bounding_rect)
            self.on_ground = False

    def update(self, dt):
        if not self.on_ground:
            self.velocity[1] += GRAVITY

        self.timer += dt

        self.bounding_rect.x += self.velocity[0]
        self.bounding_rect.y += self.velocity[1]

        self.check_world_collision()

        if self.bounding_rect.right <= 0 or self.bounding_rect.left >= WIDTH:
            self.bounding_rect.x = (self.bounding_rect.x + WIDTH) % WIDTH

        if self.get_velocity_len() < 0.1:
            self.velocity = [0,0]
            self.state = IDLE
        else:
            self.velocity[0] *= 0.9
            self.velocity[1] *= 0.9

        if self.timer >= ANIMATION_SPEED:
            self.current_frame_index += 1
            self.timer = 0
        
    

    def check_world_collision(self):
        if self.bounding_rect.y + TILE_SIZE >= HEIGHT:

            if self.camera_offset == 0:
                self.accept_landing()
                self.bounding_rect.y = HEIGHT - TILE_SIZE
            
                return True
            else:
                self.die()
        return False

    def die(self):
        pass

    def offset_y(self, dy):
        self.camera_offset += dy
        self.bounding_rect.y += dy
    def accept_landing(self):
        self.on_ground = True
        self.jumped = False
        self.double_jumped = False
        self.skip_platforms = None
        self.velocity[1] = 0

    def check_platforms_collision(self, platforms):
        collided_platform = platforms.collide(self.bounding_rect)

        if self.velocity[1] > 0 and collided_platform is not None and collided_platform != self.skip_platforms:
            self.accept_landing()
            self.bounding_rect.bottom = collided_platform.bounding_rect.top
        else:
            self.on_ground = False            
        
        
    def draw(self, screen):
        screen.blit(self.get_frame(), self.get_position())

    def get_current_frame_index(self):
        self.current_frame_index = (self.current_frame_index) % len(self.images[self.facing_direction][self.state])
        return self.current_frame_index

    def get_position(self):
        return (self.bounding_rect.x,self.bounding_rect.y)
    
    def get_frame(self):
        return self.images[self.facing_direction][self.state][self.get_current_frame_index()]

    def get_velocity_len(self):
        return abs(sum(self.velocity))
    
    def get_rect(self):
        return self.bounding_rect
    
    def is_on_ground(self):
        return self.on_ground
    
    def is_out_of_screen(self):
        return self.bounding_rect.top >= HEIGHT

class Enemy(PhysicsSprite):
    def __init__(self, position: list[int]) -> None:
        super().__init__(
            images = {
                LEFT_FACING : {
                    IDLE : [
                        "./enemy/idle_1",
                        "./enemy/idle_2",
                    ],
                    RUNNING : [
                        "./enemy/run_1",
                        "./enemy/run_2",
                        "./enemy/run_3"
                    ],
                    JUMP : [
                        "./enemy/jump_1",
                        "./enemy/jump_2",
                        "./enemy/jump_3"
                    ]
                },
                RIGHT_FACING : {
                    IDLE : [
                        "./enemy/idle_1",
                        "./enemy/idle_2",
                    ],
                    RUNNING : [
                        "./enemy/run_1",
                        "./enemy/run_2",
                        "./enemy/run_3"
                    ],
                    JUMP : [
                        "./enemy/jump_1",
                        "./enemy/jump_2",
                        "./enemy/jump_3"
                    ]
                }
            },
            position = position
        )
    

    def update(self, dt):
        super().update(dt)

    def check_player_distance(self, player):
        distance_to_player = calculate_distance_between_centers(self.get_rect(), player.get_rect())

        if distance_to_player <= ENEMY_TRIGGER_DISTANCE and self.get_velocity_len() < 0.1:
            if self.get_rect().center >= player.get_rect().center:
                self.force([-FORCE, 0])
            else:
                self.force([FORCE, 0])
            
            if self.get_rect().top > player.get_rect().top:
                self.jump()

    def check_player_collision(self, player):
        if player.get_rect().colliderect(self.get_rect()):
            force_vector : list[int] = normalized_vector_between_rects(self.get_rect(), player.get_rect())
            force_vector = [x * FORCE  for x in force_vector]

            player.force(force_vector)

            Music.hit()

class Enemies:
    def __init__(self, minimum_count_of_enemies = ENEMIES_COUNT):
        self.minimum_count_of_enemies = minimum_count_of_enemies
        self.enemies : list[Enemy] = []

    def set_enemies_count(self, count):
        self.minimum_count_of_enemies = min(20, count)
    def get_enemies_count(self):
        return self.minimum_count_of_enemies
    
    @staticmethod
    def generate_enemy(platforms : list[Platform]):
        chosen_platform = random.choice(platforms)
        return Enemy(position=[chosen_platform.get_rect().x,chosen_platform.get_rect().top + TILE_SIZE])

    def offset_y_enemies(self, dy):
        for enemy in self.enemies:
            enemy.offset_y(dy)

    def update_enemies(self, platforms : list[Platform]):
        self.enemies = [enemy for enemy in self.enemies if enemy.get_rect().top < HEIGHT]
        attempts = 0

        while len(self.enemies) < self.minimum_count_of_enemies and attempts <= ATTEMPS_FOR_CREATION:
            new_enemy = Enemies.generate_enemy(platforms)
            if not self.insert_enemy(new_enemy):
                attempts += 1
    def insert_enemy(self, new_enemy : Enemy):
        for enemy in self.enemies:
            if calculate_distance_between_centers(enemy.get_rect(), new_enemy.get_rect()) <= 100:
                return False
        
        self.enemies.append(new_enemy)
        return False


    def update(self, dt):
        for enemy in self.enemies:
            enemy.update(dt)
    
    def draw(self, screen):
        for enemy in self.enemies:
            enemy.draw(screen)

class Player(PhysicsSprite):
    def __init__(self, position, on_die_callback = None):
        super().__init__(
            images = {
                LEFT_FACING : {
                    IDLE : [
                        "./player/idle_1_left",
                        "./player/idle_2_left",
                    ],
                    RUNNING : [
                        "./player/run_1_left",
                        "./player/run_2_left",
                        "./player/run_3_left"
                    ],
                    JUMP : [
                        "./player/jump_1_left",
                    ]
                },
                RIGHT_FACING : {
                    IDLE : [
                        "./player/idle_1_right",
                        "./player/idle_2_right",
                    ],
                    RUNNING : [
                        "./player/run_1_right",
                        "./player/run_2_right",
                        "./player/run_3_right"
                    ],
                    JUMP : [
                        "./player/jump_1_right",
                    ]
                }
            },
            position = position
        )

        self.pressed_keys = []
        self.on_die_callback = on_die_callback
    
        
    def set_movement(self, direction):
        self.pressed_keys.append(direction)

    def remove_movement(self, direction):
        if direction in self.pressed_keys:
            self.pressed_keys.remove(direction)

    def move(self, direction, is_moving : bool = True):
        if is_moving:
            self.set_movement(direction)
        else:
            self.remove_movement(direction)

    def die(self):
        if self.on_die_callback is not None:
            self.on_die_callback()

    def update(self, dt):
        super().update(dt)

        if LEFT in self.pressed_keys and RIGHT in self.pressed_keys:
            super().move(LEFT if self.pressed_keys.index(LEFT) > self.pressed_keys.index(RIGHT) else RIGHT)
        elif LEFT in self.pressed_keys:
            super().move(LEFT)
        elif RIGHT in self.pressed_keys:
            super().move(RIGHT)
        
                

class App:
    MAIN_WINDOW = "main_window"
    GAME_WINDOW = "game_window"

    def __init__(self):
        self.menu_window = MainMenu(on_start_callback = self.start_game)
        self.game_window = Game(on_game_over_callback = self.stop_game)

        self.active_window = App.MAIN_WINDOW


        self.initialized = False

    def start_game(self):
        self.active_window = App.GAME_WINDOW
        self.game_window.start_game()

        Music.on_fx()

    def stop_game(self, scores = 0):
        Music.game_over()
        Music.off_fx()
        
        self.active_window = App.MAIN_WINDOW
        self.menu_window.set_scores(scores)
    def on_mouse_down(self, pos):
        Music.mouse_event(pos)

        if self.active_window == App.MAIN_WINDOW:
            self.menu_window.on_mouse_down(pos)
    
    def on_key_down(self, key):
        if self.active_window == App.GAME_WINDOW:
            self.game_window.on_key_down(key)
        else:
            self.menu_window.on_key_down(key)

    def on_key_up(self, key):
        if self.active_window == App.GAME_WINDOW:
            self.game_window.on_key_up(key)
    
    def update(self, dt):
        if not self.initialized:
            self.initialized = True
            self.menu_window.initialize_strings(screen)

        if self.active_window == App.MAIN_WINDOW:
            self.menu_window.update(dt)
        else:
            self.game_window.update(dt)

    def draw(self, screen):
        if self.active_window == App.MAIN_WINDOW:
            self.menu_window.draw(screen)
        else:
            self.game_window.draw(screen)

        Music.draw(screen)






class MainMenu:
    def __init__(self, on_start_callback = None): 
        self.player = Player([WIDTH // 2, HEIGHT - TILE_SIZE])
        self.platforms = Platforms()

        self.timer = 0
        self.cursor_blick_time = 0.2
        self.is_cursor_hidden = False

        self.strings = None

        self.on_start_callback = on_start_callback
        self.scores = 0

    def set_scores(self, scores):
        self.strings["scores"] = {
            "text" : f"SCORES: {scores}",
            "rect" : get_text_rect(None, f"SCORES: {scores}", (WIDTH // 2, HEIGHT // 2 - TITLE_SIZE * 2), PARAGRAPH_SIZE)
        }
        
        if len(self.platforms.platforms) > 2: 
            self.platforms.platforms.pop()
        self.platforms.platforms.append(Platform(self.strings["scores"]["rect"].topleft, 7))
   

    def initialize_strings(self, screen):
        self.strings = {
            "title" : {
                "text" : TITLE,
                "rect" : get_text_rect(screen, TITLE, (WIDTH // 2, HEIGHT // 2), TITLE_SIZE)
            },
            "start" : {
                "text" : "START",
                "rect" : get_text_rect(screen, "START", (WIDTH // 2, HEIGHT // 2 + TILE_SIZE * 2), PARAGRAPH_SIZE)
            }
        }

        self.platforms.platforms.extend([
            Platform((self.strings["title"]["rect"].x + TITLE_SIZE,self.strings["title"]["rect"].y), 12),
            Platform(self.strings["start"]["rect"].topleft, 3)
        ]) 

    def update(self, dt):
        self.player.update(dt)
        
        self.player.check_platforms_collision(self.platforms)

        if random.random() < 0.15:  
            direction = random.choice([LEFT, RIGHT])
            self.player.move(direction)

        # Случайные прыжки с задержкой
        if random.random() < .1:  # 2% шанс на прыжок
            self.player.jump()

        self.timer += dt
        
        if self.timer >= self.cursor_blick_time:
            self.timer = 0
            self.is_cursor_hidden = not self.is_cursor_hidden
        
    def on_key_down(self, key):
        if key == keys.RETURN:
            if self.on_start_callback is not None:
                self.on_start_callback()

    def on_mouse_down(self, pos):
        if self.strings["start"]["rect"].collidepoint(pos):
            if self.on_start_callback is not None:
                self.on_start_callback()

    def draw(self, screen):
        screen.draw.text(
            self.strings["title"]["text"], 
            center =  self.strings["title"]["rect"].center, 
            color = ACCENT_COLOR, 
            fontsize = TITLE_SIZE,
            fontname = FONT)
        
        screen.draw.text(
            f"{"> " if self.is_cursor_hidden else "  "}{self.strings["start"]["text"]}",
            center = self.strings["start"]["rect"].center,
            fontsize = PARAGRAPH_SIZE,
            color = PRIMARY_COLOR,
            fontname = FONT
        )

        if "scores" in self.strings:
            screen.draw.text(
                self.strings["scores"]["text"],
                center = self.strings["scores"]["rect"].center,
                fontsize = PARAGRAPH_SIZE,
                color = PRIMARY_COLOR,
                fontname = FONT
            )

        self.player.draw(screen)

class Game:
    def __init__(self, on_game_over_callback = None) -> None:
        self.player = None
        self.enemies = None
        self.platforms = None
        self.world = None

        self.on_game_over_callback = on_game_over_callback

        self.scores = 0
        self.camera_offset = 0

    def start_game(self):
        self.world = Background()

        self.platforms = Platforms(minimum_platforms_count = 10)
        self.platforms.update()

        self.player = Player([WIDTH // 2, HEIGHT - TILE_SIZE], on_die_callback = self.game_over)

        self.enemies = Enemies(minimum_count_of_enemies = 5)
        self.enemies.update_enemies(self.platforms.get_platforms())

        self.camera_offset = 0
        self.scores = 0


    def game_over(self):
        if self.on_game_over_callback is not None:
            self.on_game_over_callback(scores = self.scores)

    def update(self, dt):
        self.player.update(dt)
        self.enemies.update(dt)

        self.player.check_platforms_collision(self.platforms)
        for enemy in self.enemies.enemies:
            enemy.check_platforms_collision(self.platforms)
            enemy.check_player_distance(self.player)
            enemy.check_player_collision(self.player)
        
        self.scroll_screen()
        self.update_scores()

    def update_scores(self):
        self.scores = max(self.scores, HEIGHT - self.player.get_rect().bottom + self.camera_offset)

    def scroll_screen(self):
        if self.player.get_rect().bottom <= CAMERA_THRESHOLD:
            self.platforms.move(CAMERA_SPEED)
            self.world.move(CAMERA_SPEED)

            self.enemies.offset_y_enemies(CAMERA_SPEED)
            self.enemies.update_enemies(self.platforms.get_platforms())

            self.player.offset_y(CAMERA_SPEED)

            self.camera_offset += CAMERA_SPEED
        
    def draw(self, screen):
        self.world.draw(screen)
        self.platforms.draw(screen)
        self.enemies.draw(screen)
        self.player.draw(screen)
        self.draw_score(screen)

    def draw_score(self, screen):
        screen.draw.text(
            f"HEIGHT: {self.scores}",
            topright = (WIDTH, 0),
            color = ACCENT_COLOR,
            fontsize = PARAGRAPH_SIZE,
            fontname = FONT
        )
    def on_key_down(self, key):
        if key == keys.LEFT:
            self.player.move(LEFT)
        if key == keys.RIGHT:
            self.player.move(RIGHT)
        if key == keys.UP:
            self.player.jump()
        if key == keys.DOWN:
            self.player.down(self.platforms)

    def on_key_up(self, key):
        if key == keys.LEFT:
            self.player.move(LEFT, False)
        elif key == keys.RIGHT:
            self.player.move(RIGHT, False)

app = App()

def on_key_down(key):
    app.on_key_down(key)

def on_key_up(key):
    app.on_key_up(key)

def on_mouse_down(pos):
    app.on_mouse_down(pos)

def update(dt):
    app.update(dt)

def draw():
    screen.clear()
    app.draw(screen)

Music.set_volume(0.1)
Music.main_theme()    