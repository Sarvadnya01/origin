import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

# Paddle settings
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
PADDLE_SPEED = 5

# Ball settings
BALL_SIZE = 10
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

# Button settings
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50
BUTTON_FONT_SIZE = 24

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pong with Restart')

# Clock to control frame rate
clock = pygame.time.Clock()

# Fonts for displaying the score and button text
score_font = pygame.font.Font(None, 36)
button_font = pygame.font.Font(None, BUTTON_FONT_SIZE)

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = font

    def draw(self, screen):
        # Change color on hover
        current_color = self.hover_color if self.rect.collidepoint(pygame.mouse.get_pos()) else self.color
        pygame.draw.rect(screen, current_color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        # Center the text
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

def main():
    # Paddle positions
    paddle1_y = paddle2_y = (SCREEN_HEIGHT - PADDLE_HEIGHT) // 2

    # Ball position
    ball_x = SCREEN_WIDTH // 2
    ball_y = SCREEN_HEIGHT // 2
    ball_dx = BALL_SPEED_X
    ball_dy = BALL_SPEED_Y

    # Scores
    score1 = 0
    score2 = 0

    # Restart button
    restart_button = Button(
        (SCREEN_WIDTH - BUTTON_WIDTH) // 2,
        SCREEN_HEIGHT - BUTTON_HEIGHT - 20,
        BUTTON_WIDTH,
        BUTTON_HEIGHT,
        'Restart',
        GRAY,
        DARK_GRAY,
        BLACK,
        button_font
    )

    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if restart_button.is_clicked(event):
                # Reset game state
                paddle1_y = paddle2_y = (SCREEN_HEIGHT - PADDLE_HEIGHT) // 2
                ball_x = SCREEN_WIDTH // 2
                ball_y = SCREEN_HEIGHT // 2
                ball_dx = BALL_SPEED_X
                ball_dy = BALL_SPEED_Y
                score1 = 0
                score2 = 0

        # Get keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and paddle1_y > 0:
            paddle1_y -= PADDLE_SPEED
        if keys[pygame.K_s] and paddle1_y < SCREEN_HEIGHT - PADDLE_HEIGHT:
            paddle1_y += PADDLE_SPEED
        if keys[pygame.K_UP] and paddle2_y > 0:
            paddle2_y -= PADDLE_SPEED
        if keys[pygame.K_DOWN] and paddle2_y < SCREEN_HEIGHT - PADDLE_HEIGHT:
            paddle2_y += PADDLE_SPEED

        # Update ball position
        ball_x += ball_dx
        ball_y += ball_dy

        # Ball collision with top and bottom
        if ball_y <= 0 or ball_y >= SCREEN_HEIGHT - BALL_SIZE:
            ball_dy = -ball_dy

        # Ball collision with paddles
        if (ball_x <= PADDLE_WIDTH and paddle1_y < ball_y < paddle1_y + PADDLE_HEIGHT) or \
           (ball_x >= SCREEN_WIDTH - PADDLE_WIDTH - BALL_SIZE and paddle2_y < ball_y < paddle2_y + PADDLE_HEIGHT):
            ball_dx = -ball_dx

        # Ball out of bounds
        if ball_x < 0:
            score2 += 1
            ball_x = SCREEN_WIDTH // 2
            ball_y = SCREEN_HEIGHT // 2
            ball_dx = BALL_SPEED_X
            ball_dy = BALL_SPEED_Y
        elif ball_x > SCREEN_WIDTH:
            score1 += 1
            ball_x = SCREEN_WIDTH // 2
            ball_y = SCREEN_HEIGHT // 2
            ball_dx = -BALL_SPEED_X
            ball_dy = BALL_SPEED_Y

        # Draw everything
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, (0, paddle1_y, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH - PADDLE_WIDTH, paddle2_y, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.ellipse(screen, WHITE, (ball_x, ball_y, BALL_SIZE, BALL_SIZE))
        pygame.draw.aaline(screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))

        # Display scores
        score_text = score_font.render(f"{score1}   {score2}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 20))

        # Draw restart button
        restart_button.draw(screen)

        # Update the display
        pygame.display.flip()

        # Control frame rate
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
