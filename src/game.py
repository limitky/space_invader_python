import pygame
import os
from entities import Unit, Enemy, Bullet
from utils import load_images, load_sounds, play_sound

def save_score(player_name, score):
    with open("scores.txt", "a") as file:
        file.write(f"{player_name}: {score}\n")

def load_scores():
    if os.path.exists("scores.txt"):
        with open("scores.txt", "r") as file:
            return file.readlines()
    else:
        return []

def main():
    # Initialize Pygame
    pygame.init()

    # Set up screen
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Space Invaders")

    # Load assets
    background, unit_img, enemy_img, explosion_imgs, bullet_img = load_images()
    shoot_sound, explode_sound = load_sounds()

    # Set up game entities
    player = Unit(screen_width // 2 - unit_img.get_width() // 2, screen_height - unit_img.get_height() - 10)
    enemies = []

    # Ask for player's initials
    font = pygame.font.Font(None, 36)
    player_name = ""
    player_name_text = font.render("Enter your name and press Enter: ", True, (255, 255, 255))
    screen.blit(player_name_text, (screen_width // 2 - player_name_text.get_width() // 2, screen_height // 2 - 50))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if len(player_name) > 0:
                        break
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif event.unicode.isalnum() and len(player_name) < 10:
                    player_name += event.unicode.upper()

        player_name_surface = font.render(player_name, True, (255, 255, 255))
        screen.blit(player_name_surface, (screen_width // 2 - player_name_surface.get_width() // 2, screen_height // 2))
        pygame.display.flip()

        if len(player_name) > 0 and pygame.key.get_pressed()[pygame.K_RETURN]:
            break

    # Ask for difficulty level
    difficulty_text = font.render("Choose difficulty level (1, 2, or 3): ", True, (255, 255, 255))
    screen.blit(difficulty_text, (screen_width // 2 - difficulty_text.get_width() // 2, screen_height // 2))
    pygame.display.flip()

    while True:
        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                num_enemies = 15
                break
            elif event.key == pygame.K_2:
                num_enemies = 20
                break
            elif event.key == pygame.K_3:
                num_enemies = 25
                break

    enemies = [Enemy(x, y) for x in range(1, 19) for y in range(num_enemies // 15)]

    # Bullets
    bullets = []

    # Game variables
    score = 0
    lives = 3
    game_over = False
    shooting = False
    shoot_delay = 0

    # Game loop
    running = True
    clock = pygame.time.Clock()

    # Start background music
    pygame.mixer.music.load('assets/background_music.mp3')
    pygame.mixer.music.play(-1)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    shooting = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    shooting = False

        # Handle player movement
        dx = 0
        dy = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            dx = 2  # Aumentado para que el movimiento sea más rápido
        elif keys[pygame.K_LEFT]:
            dx = -2  # Aumentado para que el movimiento sea más rápido
        if keys[pygame.K_DOWN]:
            dy = 2  # Aumentado para que el movimiento sea más rápido
        elif keys[pygame.K_UP]:
            dy = -2  # Aumentado para que el movimiento sea más rápido
        player.move(dx, dy)

        # Ensure player doesn't go out of bounds
        player.x = max(0, min(screen_width - unit_img.get_width(), player.x))
        player.y = max(0, min(screen_height - unit_img.get_height(), player.y))

        # Update game entities
        if not game_over:
            # Shooting logic
            if shooting and shoot_delay <= 0:
                bullets.append(Bullet(player.x + unit_img.get_width() // 2, player.y, -1))
                play_sound(shoot_sound)
                shoot_delay = 10  # Reducido para un disparo más rápido

            shoot_delay = max(0, shoot_delay - 1)

            for enemy in enemies:
                enemy.move()

            for bullet in bullets:
                bullet.move()

            # Collision detection
            for bullet in bullets[:]:
                for enemy in enemies[:]:
                    if enemy.collides_with(bullet):
                        enemy.exploding = True
                        play_sound(explode_sound)
                        enemies.remove(enemy)
                        bullets.remove(bullet)
                        score += 10
                        break

            # Game over conditions
            for enemy in enemies:
                if enemy.y == player.y:
                    game_over = True
                    break

            if not enemies:
                game_over = True

        # Draw everything
        screen.blit(background, (0, 0))
        player.draw(screen, unit_img)
        for enemy in enemies:
            enemy.draw(screen, enemy_img, explosion_imgs)
        for bullet in bullets:
            bullet.draw(screen, bullet_img)

        # Show score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        # Update the display
        pygame.display.flip()
        clock.tick(60)

        # Game over screen
        if game_over:
            screen.fill((0, 0, 0))
            if not enemies:
                game_over_text = font.render("You saved the universe from the invasion!", True, (255, 255, 255))
                save_score(player_name, score)
            else:
                game_over_text = font.render("Game Over", True, (255, 255, 255))
            screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2))

            # Show high scores
            high_scores_text = font.render("High Scores:", True, (255, 255, 255))
            screen.blit(high_scores_text, (screen_width // 2 - high_scores_text.get_width() // 2, screen_height // 2 + 50))

            scores = load_scores()
            y_pos = screen_height // 2 + 100
            for i, score_entry in enumerate(scores[:5]):
                score_entry_text = font.render(score_entry.strip(), True, (255, 255, 255))
                screen.blit(score_entry_text, (screen_width // 2 - score_entry_text.get_width() // 2, y_pos + i * 40))

            pygame.display.flip()

            pygame.time.delay(2000)  # Delay 2 seconds before closing the game
            break

    pygame.quit()

if __name__ == "__main__":
    main()

