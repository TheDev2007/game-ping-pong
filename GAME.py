import sys
import pygame


def ball_move():
    global speed_y, speed_x, speed_multiplier, game_over, player1_score, player2_score
    if not game_over:
        ball.x += speed_x * speed_multiplier
        ball.y += speed_y * speed_multiplier

        if ball.left <= 0:
            game_over = True
            player2_score += 1
            return "Player 1"
        elif ball.right >= width:
            game_over = True
            player1_score += 1
            return "Player 2"
        if ball.top <= 0 or ball.bottom >= height:
            speed_y *= -1
        if ball.colliderect(player) or ball.colliderect(opponent):
            speed_x *= -1
            increase_speed()


def increase_speed():
    global speed_multiplier
    speed_multiplier += 0.05


def player_move():
    if not game_over:
        player.y += play_speed
        if player.top <= 0:
            player.top = 0
        if player.bottom >= height:
            player.bottom = height


def opp_move_two_player():
    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            opponent.y -= opp_speed
        if keys[pygame.K_s]:
            opponent.y += opp_speed

        if opponent.top <= 0:
            opponent.top = 0
        if opponent.bottom >= height:
            opponent.bottom = height


def opp_move_single_player():
    if not game_over:
        if opponent.centery < ball.centery:
            opponent.y += opp_speed
        if opponent.centery > ball.centery:
            opponent.y -= opp_speed

        if opponent.top <= 0:
            opponent.top = 0
        if opponent.bottom >= height:
            opponent.bottom = height


def display_game_over(winner):
    font = pygame.font.Font(None, 74)
    game_over_text = f"Game Over! {winner} wins!"
    text = font.render(game_over_text, True, (255, 255, 255))
    window.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))

    return_to_menu_text = "Press M to return to menu"
    small_font = pygame.font.Font(None, 36)
    menu_text = small_font.render(return_to_menu_text, True, (255, 255, 255))
    window.blit(menu_text, (width // 2 - menu_text.get_width() // 2, height // 2 + text.get_height()))


def display_scores():
    score_font = pygame.font.Font(None, 36)
    score_text = f"Player 1: {player1_score} | Player 2: {player2_score} | High Score: {high_score}"
    text = score_font.render(score_text, True, (255, 255, 255))
    window.blit(text, (width // 2 - text.get_width() // 2, 10))


def reset_game():
    global ball, player, opponent, speed_x, speed_y, speed_multiplier, game_over
    ball = pygame.Rect((width / 2 - 10, height / 2 - 10, 20, 20))
    player = pygame.Rect((width - 20, height / 2 - 70, 10, 140))
    opponent = pygame.Rect((10, height / 2 - 70, 10, 140))
    speed_x = 5
    speed_y = 5
    speed_multiplier = 1
    game_over = False


def reset_scores():
    global player1_score, player2_score
    player1_score = 0
    player2_score = 0


def display_menu():
    window.fill(bg)
    font = pygame.font.Font(None, 74)
    single_player_text = font.render("1. Single Player", True, (255, 255, 255))
    two_player_text = font.render("2. Two Player", True, (255, 255, 255))
    window.blit(single_player_text, (width // 2 - single_player_text.get_width() // 2, height // 3))
    window.blit(two_player_text, (width // 2 - two_player_text.get_width() // 2, height // 3 + 100))
    pygame.display.flip()


pygame.init()
pygame.display.set_caption('PONG GAME')
width = 1000
height = 700
window = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

ball = pygame.Rect((width / 2 - 10, height / 2 - 10, 20, 20))
player = pygame.Rect((width - 20, height / 2 - 70, 10, 140))
opponent = pygame.Rect((10, height / 2 - 70, 10, 140))
bg = pygame.Color('grey12')
l_grey = (200, 200, 200)

speed_x = 5
speed_y = 5
speed_multiplier = 1
play_speed = 0
opp_speed = 10
game_over = False
single_player = True

player1_score = 0
player2_score = 0
high_score = 0

menu = True

while True:
    if menu:
        display_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    single_player = True
                    menu = False
                    reset_game()
                if event.key == pygame.K_2:
                    single_player = False
                    menu = False
                    reset_game()

    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    play_speed += 10
                if event.key == pygame.K_UP:
                    play_speed -= 10
                if event.key == pygame.K_SPACE and game_over:
                    if player1_score > high_score:
                        high_score = player1_score
                    elif player2_score > high_score:
                        high_score = player2_score
                    reset_game()
                if event.key == pygame.K_m and game_over:
                    menu = True
                    reset_scores()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    play_speed -= 10
                if event.key == pygame.K_UP:
                    play_speed += 10

        if not game_over:
            Winner = ball_move()
            player_move()
            if single_player:
                opp_move_single_player()
            else:
                opp_move_two_player()

        window.fill(bg)
        pygame.draw.rect(window, l_grey, player)
        pygame.draw.rect(window, l_grey, opponent)
        pygame.draw.ellipse(window, l_grey, ball)
        pygame.draw.aaline(window, l_grey, (width / 2, 0), (width / 2, height))

        if game_over:
            display_game_over(Winner)

        display_scores()

        pygame.display.flip()
        pygame.display.update()
        clock.tick(60)
