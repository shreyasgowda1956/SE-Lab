import pygame
from game.game_engine import GameEngine

WIDTH, HEIGHT = 500, 700
FPS = 60

def main():
    pygame.init()
    try:
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        audio_available = True
    except pygame.error:
        audio_available = False
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Flappy Bird - Lab 4')
    clock = pygame.time.Clock()
    engine = GameEngine(WIDTH, HEIGHT, audio_available)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                if engine.handle_event(event) == 'quit':
                    running = False
        engine.update()
        engine.render(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()

if __name__ == '__main__':
    main()
