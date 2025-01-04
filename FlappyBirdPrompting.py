import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen Dimensions and Settings
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLUE = (135, 206, 235)
BLACK = (0, 0, 0)
ORANGE = (254, 216, 177)
DARK_BLUE = (25, 25, 112)

# Fonts
FONT = pygame.font.Font(None, 36)

# Initialize Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Clock
clock = pygame.time.Clock()

# Game States
STATE_MENU = 0
STATE_CONTROLS = 1
STATE_PLAYING = 2
STATE_GAME_OVER = 3

game_state = STATE_MENU

# Menu Options
menu_options = ["Play", "Scores", "Exit"]
selected_option = 0

# Player Settings
player_width = 40
player_height = 30
player_x = 50
player_y = SCREEN_HEIGHT // 2
player_velocity = 0
player_gravity = 0.5
jump_strength = -10

# Obstacles
obstacle_width = 60
obstacle_gap = 180  # Increased by 20%
obstacle_speed = 4
obstacles = []

# Score
score = 0
font_score = pygame.font.Font(None, 28)

# Background
background_phase = 0
background_speed = 0.03  # Slowed down by another 500%
def draw_dynamic_background():
    global background_phase

    # Calculate the current background color
    phase = (background_phase // 100) % 3
    t = (background_phase % 100) / 100

    if phase == 0:  # Blue to Orange (Day)
        color = (
            int(BLUE[0] * (1 - t) + ORANGE[0] * t),
            int(BLUE[1] * (1 - t) + ORANGE[1] * t),
            int(BLUE[2] * (1 - t) + ORANGE[2] * t),
        )
    elif phase == 1:  # Orange to Dark Blue (Sunset)
        color = (
            int(ORANGE[0] * (1 - t) + DARK_BLUE[0] * t),
            int(ORANGE[1] * (1 - t) + DARK_BLUE[1] * t),
            int(ORANGE[2] * (1 - t) + DARK_BLUE[2] * t),
        )
    else:  # Dark Blue to Blue (Night to Day)
        color = (
            int(DARK_BLUE[0] * (1 - t) + BLUE[0] * t),
            int(DARK_BLUE[1] * (1 - t) + BLUE[1] * t),
            int(DARK_BLUE[2] * (1 - t) + BLUE[2] * t),
        )

    # Fill the screen with the calculated color
    screen.fill(color)
    background_phase += background_speed

def spawn_obstacle():
    obstacle_height = random.randint(100, SCREEN_HEIGHT - obstacle_gap - 100)
    top_rect = pygame.Rect(SCREEN_WIDTH, 0, obstacle_width, obstacle_height)
    bottom_rect = pygame.Rect(SCREEN_WIDTH, obstacle_height + obstacle_gap, obstacle_width, SCREEN_HEIGHT - obstacle_height - obstacle_gap)
    obstacles.append((top_rect, bottom_rect))

def move_obstacles():
    for obstacle_pair in obstacles:
        obstacle_pair[0].x -= obstacle_speed
        obstacle_pair[1].x -= obstacle_speed
    obstacles[:] = [pair for pair in obstacles if pair[0].x + obstacle_width > 0]

def check_collision():
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    for top_rect, bottom_rect in obstacles:
        if player_rect.colliderect(top_rect) or player_rect.colliderect(bottom_rect):
            return True
    if player_y + player_height > SCREEN_HEIGHT or player_y < 0:
        return True
    return False

def draw_game():
    draw_dynamic_background()

    # Draw Player
    pygame.draw.rect(screen, WHITE, (player_x, player_y, player_width, player_height))

    # Draw Obstacles
    for top_rect, bottom_rect in obstacles:
        pygame.draw.rect(screen, BLACK, top_rect)
        pygame.draw.rect(screen, BLACK, bottom_rect)

    # Draw Score
    score_text = font_score.render(f"Score: {int(score)}", True, WHITE)
    screen.blit(score_text, (10, 10))

def draw_menu():
    draw_dynamic_background()
    title = FONT.render("Flappy Airplane", True, WHITE)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

    for i, option in enumerate(menu_options):
        color = WHITE if i == selected_option else BLACK
        text = FONT.render(option, True, color)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 200 + i * 50))

        # Add an underline for the selected option
        if i == selected_option:
            underline = pygame.Rect(
                SCREEN_WIDTH // 2 - text.get_width() // 2, 200 + i * 50 + text.get_height() + 5, text.get_width(), 2
            )
            pygame.draw.rect(screen, WHITE, underline)

def draw_controls():
    draw_dynamic_background()
    instructions = [
        "Controls:",
        "Press SPACE to jump",
        "Avoid obstacles.",
        "Score increases over time.",
        "Press any key to start.",
    ]
    for i, line in enumerate(instructions):
        text = FONT.render(line, True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 150 + i * 40))

def menu_event_handler():
    global selected_option, game_state
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                selected_option = (selected_option - 1) % len(menu_options)
            elif event.key == pygame.K_DOWN:
                selected_option = (selected_option + 1) % len(menu_options)
            elif event.key == pygame.K_RETURN:
                if selected_option == 0:  # Play
                    game_state = STATE_CONTROLS
                elif selected_option == 1:  # Scores
                    pass  # Scores functionality will be added later
                elif selected_option == 2:  # Exit
                    pygame.quit()
                    sys.exit()

def controls_event_handler():
    global game_state
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            game_state = STATE_PLAYING

def game_event_handler():
    global player_velocity, game_state
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player_velocity = jump_strength

def update_game():
    global player_y, player_velocity, score, game_state

    # Player Movement
    player_velocity += player_gravity
    player_y += player_velocity

    # Obstacles
    move_obstacles()

    # Spawn new obstacles
    if len(obstacles) == 0 or obstacles[-1][0].x < SCREEN_WIDTH - 200:
        spawn_obstacle()

    # Check Collision
    if check_collision():
        game_state = STATE_GAME_OVER

    # Update Score
    global score
    score += 1 / FPS

def draw_game_over():
    draw_dynamic_background()
    game_over_text = FONT.render("Game Over", True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 150))
    retry_text = FONT.render("Press R to Retry or ESC to Exit", True, WHITE)
    screen.blit(retry_text, (SCREEN_WIDTH // 2 - retry_text.get_width() // 2, 250))
    menu_button_text = FONT.render("Press M for Menu", True, WHITE)
    screen.blit(menu_button_text, (SCREEN_WIDTH // 2 - menu_button_text.get_width() // 2, 350))

def game_over_event_handler():
    global game_state, player_y, player_velocity, score, obstacles
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # Reset Game
                player_y = SCREEN_HEIGHT // 2
                player_velocity = 0
                score = 0
                obstacles = []
                game_state = STATE_PLAYING
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_m:
                game_state = STATE_MENU
                player_y = SCREEN_HEIGHT // 2
                player_velocity = 0
                score = 0
                obstacles = []
# Main Game Loop
running = True
while running:
    if game_state == STATE_MENU:
        menu_event_handler()
        draw_menu()
    elif game_state == STATE_CONTROLS:
        controls_event_handler()
        draw_controls()
    elif game_state == STATE_PLAYING:
        game_event_handler()
        update_game()
        draw_game()
    elif game_state == STATE_GAME_OVER:
        game_over_event_handler()
        draw_game_over()

    pygame.display.flip()
    clock.tick(FPS)
