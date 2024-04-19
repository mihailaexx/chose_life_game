import pygame, sys, re
pygame.mixer.init()
pygame.init()

# CONSTANTS
GAME_MENU, GAME_SETTINGS, GAME_PAUSE, GAME_RUNNING, GAME_OVER = range(5) #* привязать к состояниям игры отрисовку экрана

class Menu:
    def __init__(self) -> None:
        self.bg = pygame.transform.scale(pygame.image.load("imgs/kbtu.png"), (1920, 1080))
        self.play_button = pygame.Rect(0, 0, 800, 220)
        self.play_button_text = pygame.font.Font(None, 72).render("Start", True, (0, 0, 0))
        self.play_button.center = (960, 425)
        self.play_button_text_rect = self.play_button_text.get_rect(center=(960, 425))
        self.conn_button = pygame.Rect(0, 0, 800, 220)
        self.conn_button_text = pygame.font.Font(None, 72).render("Continue", True, (0, 0, 0))
        self.conn_button.center = (960, 425)
        self.conn_button_text_rect = self.conn_button_text.get_rect(center=(960, 425))
        self.settings_button = pygame.Rect(0, 0, 800, 220)
        self.settings_button_text = pygame.font.Font(None, 72).render("Settings", True, (0, 0, 0))
        self.settings_button.center = (960, 680)
        self.settings_button_text_rect = self.settings_button_text.get_rect(center=(960, 680))
        self.exit_button = pygame.Rect(0, 0, 800, 220)
        self.exit_button_text = pygame.font.Font(None, 72).render("Exit", True, (0, 0, 0))
        self.exit_button.center = (960, 935)
        self.exit_button_text_rect = self.exit_button_text.get_rect(center=(960, 935))
        self.volume_slider = pygame.Rect(0, 0, 1240, 20)
        self.volume_slider.center = (960, 540)
        self.back_button = pygame.Rect(0, 0, 800, 220)
        self.back_button_text = pygame.font.Font(None, 72).render("Back to main menu", True, (0, 0, 0))
        self.back_button.center = (960, 935)
        self.back_button_text_rect = self.back_button_text.get_rect(center=(960, 935))
        # звуки
        # self.click_sound = pygame.mixer.Sound("click.wav")
        # self.bg_sound = pygame.mixer.music.load("bg.wav")
    def draw(self, screen, state):
        if state == GAME_MENU: #* в меню отображать 3 кнопки - играть, настройки, выход
            screen.blit(self.bg, (0, 0))
            pygame.draw.rect(screen, (255, 0, 0), self.play_button)
            screen.blit(self.play_button_text, self.play_button_text_rect)
            pygame.draw.rect(screen, (255, 0, 0), self.settings_button)
            screen.blit(self.settings_button_text, self.settings_button_text_rect)
            pygame.draw.rect(screen, (255, 0, 0), self.exit_button)
            screen.blit(self.exit_button_text, self.exit_button_text_rect)
        elif state == GAME_PAUSE: #* в паузе отображать кнопку продолжить, кнопку настройки, кнопку выхода в меню
            screen.blit(self.bg, (0, 0))
            pygame.draw.rect(screen, (255, 0, 0), self.conn_button)
            screen.blit(self.conn_button_text, self.conn_button_text_rect)
            pygame.draw.rect(screen, (255, 0, 0), self.settings_button)
            screen.blit(self.settings_button_text, self.settings_button_text_rect)
            pygame.draw.rect(screen, (255, 0, 0), self.back_button)
            screen.blit(self.back_button_text, self.back_button_text_rect)
        elif state == GAME_SETTINGS: #* в настройках отображать слайдер громкости, кнопку назад
            screen.blit(self.bg, (0, 0))
            pygame.draw.rect(screen, (255, 0, 0), self.volume_slider)
            pygame.draw.rect(screen, (255, 0, 0), self.back_button)
            screen.blit(self.back_button_text, self.back_button_text_rect)
            self.volume_text = pygame.font.Font(None, 36).render(f"{int(pygame.mixer.music.get_volume()*100)}", True, (255, 0, 0))
            self.volume_text_rect = self.volume_text.get_rect(center=(960, 580))
            screen.blit(self.volume_text, self.volume_text_rect)
            pygame.draw.circle(screen, (0, 0, 0), (pygame.mixer.music.get_volume()*1240+340, 540), 15)
            pygame.draw.circle(screen, (255, 0, 0), (pygame.mixer.music.get_volume()*1240+340, 540), 10)
        elif state == GAME_OVER:
            pass

class Level:
    def __init__(self) -> None:
        self.bg = pygame.image.load("imgs/independence_hall.png")
        self.event_bg = pygame.Rect(0, 0, 1240, 220)
        self.event_bg.center = (960, 145)
        self.pause_button = pygame.Rect(0, 0, 220, 220)
        self.pause_button.center = (150, 145)
        self.n_of_card = 2 #* количество карточек на экране(2 или 3)
        # self.click_sound = pygame.mixer.Sound("click.wav")
        # self.bg_sound = pygame.mixer.music.load("bg.wav")
    def draw(self, screen, state):
        screen.blit(self.bg, (0, 0))
        pygame.draw.rect(screen, (255, 0, 0), self.event_bg)
        pygame.draw.rect(screen, (255, 0, 0), self.pause_button)
        if self.n_of_card == 0:
            pass
        elif self.n_of_card == 2:
            self.card1 = pygame.Rect(0, 0, 600, 425)
            self.card1.center = (640, 667)
            self.card2 = pygame.Rect(0, 0, 600, 425)
            self.card2.center = (1280, 667)
            pygame.draw.rect(screen, (255, 0, 0), self.card1)
            pygame.draw.rect(screen, (255, 0, 0), self.card2)
        # elif self.n_of_card == 3:
        #     pygame.draw.rect(screen, (255, 0, 0), self.card1)
        #     pygame.draw.rect(screen, (255, 0, 0), self.card2)
        #     pygame.draw.rect(screen, (255, 0, 0), self.card3)

class Player:
    def __init__(self) -> None:
        self.grades = 0
        self.mood = 0
        self.money = 0
        self.icon = "" #* иконка игрока, будет 3 спрайта - счастливый, нейтральный, грустный

class Game:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((1920, 1080))
        self.screen.fill((255, 255, 255))
        self.game_state = GAME_MENU
        self.menu = Menu()
        self.reset()
        
    def reset(self):
        self.player = Player()
        self.level = Level()
        pygame.mixer.music.set_volume(0.1)

    def event_handle(self):
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_state == GAME_RUNNING:
                        self.game_state = GAME_PAUSE
                    elif self.game_state == GAME_PAUSE:
                        self.game_state = GAME_RUNNING
                    elif self.game_state == GAME_MENU:
                        pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.game_state == GAME_RUNNING:
                    if self.level.card1.collidepoint(mouse_pos):
                        print("card1")
                    elif self.level.card2.collidepoint(mouse_pos):
                        print("card2")
                    elif self.level.pause_button.collidepoint(mouse_pos):
                        print("pause")
                        self.game_state = GAME_PAUSE
                elif self.game_state == GAME_MENU: #* если игра в меню
                    if self.menu.conn_button.collidepoint(mouse_pos):
                        print("conn")
                        self.game_state = GAME_RUNNING
                    elif self.menu.settings_button.collidepoint(mouse_pos):
                        print("settings")
                        self.prev_game_state = GAME_MENU
                        self.game_state = GAME_SETTINGS
                    elif self.menu.back_button.collidepoint(mouse_pos):
                        print("back")
                        pygame.quit()
                elif self.game_state == GAME_SETTINGS: # если игра в настройках
                    # if self.menu.volume_slider.collidepoint(mouse_pos):
                        
                    if self.menu.back_button.collidepoint(mouse_pos):
                        self.game_state = self.prev_game_state
                elif self.game_state == GAME_PAUSE: # если игра на паузе
                    if self.menu.play_button.collidepoint(mouse_pos):
                        print("continue")
                        self.game_state = GAME_RUNNING
                    elif self.menu.settings_button.collidepoint(mouse_pos):
                        print("settings")
                        self.prev_game_state = GAME_PAUSE
                        self.game_state = GAME_SETTINGS
                    elif self.menu.exit_button.collidepoint(mouse_pos):
                        print("exit")
                        self.game_state = GAME_MENU
        if pygame.mouse.get_pressed()[0]:
            if self.game_state == GAME_SETTINGS:
                if self.menu.volume_slider.collidepoint(mouse_pos):
                    pygame.mixer.music.set_volume((mouse_pos[0]-340)/1240)
    def run(self):
        while True:
            if self.game_state == GAME_RUNNING:
                self.level.draw(self.screen, self.game_state)
            else:
                self.menu.draw(self.screen, self.game_state)
            self.event_handle()
            pygame.display.flip()
            pygame.time.Clock().tick(60)
    
if __name__ == "__main__":
    game = Game()
    game.run()