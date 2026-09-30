import math
import struct
import pygame
from .bird import Bird
from .pipe import Pipe

WHITE = (255, 255, 255)
GREEN = (0, 150, 0)
DARK = (20, 30, 45)
YELLOW = (255, 220, 80)

class GameEngine:
    DIFFICULTIES = {
        1: ("Easy", 3.0, 175),
        2: ("Medium", 4.0, 150),
        3: ("Hard", 5.5, 125),
    }

    def __init__(self, width, height, audio_available=True):
        self.width = width
        self.height = height
        self.audio_available = audio_available
        self.font = pygame.font.SysFont("Arial", 30)
        self.big_font = pygame.font.SysFont("Arial", 54, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 24)
        self.difficulty = 2
        self.state = "playing"
        self._setup_round()
        self.sounds = self._make_sounds() if audio_available else {}

    def _setup_round(self):
        _, speed, gap = self.DIFFICULTIES[self.difficulty]
        self.bird = Bird(self.width // 4, self.height // 2)
        self.pipe_speed = speed
        self.pipe_gap = gap
        self.pipe_interval = 90
        self._spawn_timer = 0
        self.pipes = [Pipe(self.width + 100, self.height, gap=gap, speed=speed)]
        self.score = 0
        self.state = "playing"

    def _make_sounds(self):
        try:
            return {
                "flap": self._tone(700, 0.07, 0.25),
                "score": self._tone(1000, 0.10, 0.30),
                "death": self._tone(180, 0.22, 0.35),
            }
        except pygame.error:
            return {}

    def _tone(self, frequency, duration, volume):
        sample_rate = 44100
        count = int(sample_rate * duration)
        frames = bytearray()
        for i in range(count):
            envelope = 1.0 - (i / count)
            value = int(32767 * volume * envelope * math.sin(2 * math.pi * frequency * i / sample_rate))
            frames.extend(struct.pack("<hh", value, value))
        return pygame.mixer.Sound(buffer=bytes(frames))

    def _play(self, name):
        sound = self.sounds.get(name)
        if sound:
            sound.play()

    def _game_over(self):
        if self.state != "game_over":
            self.state = "game_over"
            self._play("death")

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.state == "playing" and event.key == pygame.K_SPACE:
                self.bird.flap()
                self._play("flap")
            elif self.state == "game_over":
                if event.key == pygame.K_1:
                    self.difficulty = 1
                    self._setup_round()
                elif event.key == pygame.K_2:
                    self.difficulty = 2
                    self._setup_round()
                elif event.key == pygame.K_3:
                    self.difficulty = 3
                    self._setup_round()
                elif event.key == pygame.K_ESCAPE:
                    return "quit"
        elif event.type == pygame.MOUSEBUTTONDOWN and self.state == "playing":
            self.bird.flap()
            self._play("flap")
        return None

    def handle_input(self):
        pass

    @staticmethod
    def _swept_rect(previous_rect, current_rect):
        return previous_rect.union(current_rect)

    def _check_pipe_collision(self, pipe, previous_bird_rect):
        current_bird_rect = self.bird.rect()
        swept_bird = self._swept_rect(previous_bird_rect, current_bird_rect)
        old_top = pygame.Rect(round(pipe.previous_x), 0, pipe.width, pipe.gap_y)
        old_bottom_y = pipe.gap_y + pipe.gap
        old_bottom = pygame.Rect(round(pipe.previous_x), old_bottom_y, pipe.width, self.height - old_bottom_y)
        new_top = pipe.top_rect()
        new_bottom = pipe.bottom_rect()
        return (swept_bird.colliderect(old_top.union(new_top)) or
                swept_bird.colliderect(old_bottom.union(new_bottom)))

    def update(self):
        if self.state != "playing":
            return

        previous_bird_rect = self.bird.rect()
        self.bird.update()

        if self.bird.y - self.bird.radius <= 0 or self.bird.y + self.bird.radius >= self.height:
            self._game_over()
            return

        self._spawn_timer += 1
        if self._spawn_timer >= self.pipe_interval:
            self._spawn_timer = 0
            self.pipes.append(Pipe(self.width, self.height, gap=self.pipe_gap, speed=self.pipe_speed))

        for pipe in self.pipes:
            pipe.move()
            if self._check_pipe_collision(pipe, previous_bird_rect):
                self._game_over()
                return

            if not pipe.scored and pipe.x + pipe.width < self.bird.x:
                pipe.scored = True
                self.score += 1
                self._play("score")

        self.pipes = [p for p in self.pipes if not p.off_screen()]

    def render(self, screen):
        screen.fill((135, 206, 235))
        for pipe in self.pipes:
            pygame.draw.rect(screen, GREEN, pipe.top_rect())
            pygame.draw.rect(screen, GREEN, pipe.bottom_rect())

        pygame.draw.circle(screen, WHITE, (int(self.bird.x), int(self.bird.y)), self.bird.radius)
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if self.state == "game_over":
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))

            title = self.big_font.render("GAME OVER", True, WHITE)
            score = self.font.render(f"Final Score: {self.score}", True, WHITE)
            choose = self.small_font.render("Choose difficulty to replay", True, WHITE)
            easy = self.small_font.render("1 - Easy   2 - Medium   3 - Hard", True, YELLOW)
            exit_text = self.small_font.render("ESC - Exit", True, WHITE)

            screen.blit(title, title.get_rect(center=(self.width // 2, 230)))
            screen.blit(score, score.get_rect(center=(self.width // 2, 300)))
            screen.blit(choose, choose.get_rect(center=(self.width // 2, 370)))
            screen.blit(easy, easy.get_rect(center=(self.width // 2, 415)))
            screen.blit(exit_text, exit_text.get_rect(center=(self.width // 2, 455)))
