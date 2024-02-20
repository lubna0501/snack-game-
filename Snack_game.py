import random
import pygame

# Initialize pygame
pygame.init()

# Set screen dimensions
screen_width = 500
screen_height = 500
block_size = 20  # size of each block
board_width = screen_width // block_size
board_height = screen_height // block_size
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")

# Set snake and food properties
snake_speed = 15
font_style = pygame.font.SysFont(None, 25)

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# Global variables
clock = pygame.time.Clock()
snake_List = []
snake_Length = 1
food_x, food_y = 0, 0  # Initialize food position


def generate_food():
    global food_x, food_y
    food_x = random.randint(0, board_width - 1) * block_size
    food_y = random.randint(0, board_height - 1) * block_size


def snake_movement(x1, y1, x1_change, y1_change):
    x1 += x1_change
    y1 += y1_change
    return x1, y1


def display_score(value):
    value_surface = font_style.render("Your Score: " + str(value), True, white)
    screen.blit(value_surface, [10, 10])


def draw_snake(snake_List):
    for segment in snake_List:
        pygame.draw.rect(screen, green, [segment[0], segment[1], block_size, block_size])


def draw_food():
    pygame.draw.rect(screen, red, [food_x, food_y, block_size, block_size])


def draw_button(text, x, y, width, height, inactive_color, active_color, font_size):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Check if mouse is over the button
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, active_color, [x, y, width, height])
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, inactive_color, [x, y, width, height])

    text_surface = font_style.render(text, True, black)
    text_rect = text_surface.get_rect()
    text_rect.center = (x + width // 2, y + height // 2)
    screen.blit(text_surface, text_rect)

    return False


def message(msg, color, y_offset=0):
    mesg_surface = font_style.render(msg, True, color)
    mesg_rect = mesg_surface.get_rect()
    mesg_rect.center = (screen_width / 2, screen_height / 2 + y_offset)
    screen.blit(mesg_surface, mesg_rect)


def game_loop():
    global snake_Length  # Access global variable
    global food_x, food_y
    game_over = False

    # Reset snake position and length
    snake_List.clear()
    snake_Length = 1

    x1 = screen_width // 2
    y1 = screen_height // 2
    x1_change = 0
    y1_change = 0

    generate_food()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -block_size
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = block_size
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -block_size
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = block_size
                    x1_change = 0

        x1, y1 = snake_movement(x1, y1, x1_change, y1_change)
        if x1 >= screen_width or x1 < 0 or y1 >= screen_height or y1 < 0:
            game_over = True

        screen.fill(black)
        draw_snake(snake_List)
        draw_food()
        display_score(snake_Length - 1)
        pygame.display.update()

        # Check for collision with food
        if x1 == food_x and y1 == food_y:
            generate_food()
            snake_Length += 1
    

        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > snake_Length:
            del snake_List[0]

        for segment in snake_List[:-1]:
            if segment == snake_Head:
                game_over = True

        clock.tick(snake_speed)

    while True:
        screen.fill(black)
        message("Game Over! Your Score: " + str(snake_Length - 1), white, -50)
        if draw_button("Play Again", 150, 300, 200, 50, green, (0, 255, 0), 30):
            game_loop()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


if __name__ == "__main__":
    game_loop()
