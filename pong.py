import pygame
import sys
import os

# Vérification de l'environnement graphique
if os.environ.get('DISPLAY') is None:
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    print("Mode sans affichage activé - Environnement sans interface graphique détecté")
    print("Note: Ce mode est utile pour le développement et les tests.")
    print("Pour jouer au jeu, vous aurez besoin d'un environnement avec interface graphique.")

# Initialisation de Pygame
pygame.init()

# Constantes
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
BALL_SIZE = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60

# Création de la fenêtre
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

class GameState:
    def __init__(self):
        self.ball_x = WINDOW_WIDTH // 2
        self.ball_y = WINDOW_HEIGHT // 2
        self.ball_dx = 5
        self.ball_dy = 5
        self.paddle_x = WINDOW_WIDTH // 2 - PADDLE_WIDTH // 2
        self.score = 0
        self.game_over = False

    def update(self):
        # Mise à jour de la position de la balle
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy

        # Collision avec les murs
        if self.ball_x <= 0 or self.ball_x >= WINDOW_WIDTH:
            self.ball_dx = -self.ball_dx
        if self.ball_y <= 0:
            self.ball_dy = -self.ball_dy

        # Collision avec la raquette
        paddle_rect = pygame.Rect(self.paddle_x, WINDOW_HEIGHT - PADDLE_HEIGHT - 10, 
                                PADDLE_WIDTH, PADDLE_HEIGHT)
        ball_rect = pygame.Rect(self.ball_x - BALL_SIZE//2, self.ball_y - BALL_SIZE//2,
                              BALL_SIZE, BALL_SIZE)
        
        if ball_rect.colliderect(paddle_rect):
            self.ball_dy = -abs(self.ball_dy)  # Fait rebondir la balle vers le haut
            self.score += 1
            # Augmente légèrement la vitesse
            self.ball_dx *= 1.1
            self.ball_dy *= 1.1

        # Balle hors limites (game over)
        if self.ball_y > WINDOW_HEIGHT:
            self.game_over = True

def main():
    game_state = GameState()
    font = pygame.font.Font(None, 36)

    while True:
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and game_state.game_over:
                if event.key == pygame.K_SPACE:
                    game_state = GameState()  # Redémarre le jeu

        # Déplacement de la raquette
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            game_state.paddle_x = max(0, game_state.paddle_x - 10)
        if keys[pygame.K_RIGHT]:
            game_state.paddle_x = min(WINDOW_WIDTH - PADDLE_WIDTH, game_state.paddle_x + 10)

        # Mise à jour du jeu
        if not game_state.game_over:
            game_state.update()

        # Dessin
        screen.fill(BLACK)
        
        # Dessine la raquette
        pygame.draw.rect(screen, WHITE, 
                        (game_state.paddle_x, WINDOW_HEIGHT - PADDLE_HEIGHT - 10,
                         PADDLE_WIDTH, PADDLE_HEIGHT))
        
        # Dessine la balle
        pygame.draw.circle(screen, WHITE, 
                         (int(game_state.ball_x), int(game_state.ball_y)), 
                         BALL_SIZE // 2)

        # Affiche le score
        score_text = font.render(f"Score: {game_state.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Affiche le message de game over
        if game_state.game_over:
            game_over_text = font.render("Game Over! Appuyez sur ESPACE pour recommencer", 
                                       True, WHITE)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            screen.blit(game_over_text, text_rect)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    main()