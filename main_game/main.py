import pygame, sys, re
pygame.mixer.init()
pygame.init()

# CONSTANTS
GAME_MENU, GAME_SETTINGS, GAME_PAUSE, GAME_RUNNING, GAME_OVER = range(5) #* привязать к состояниям игры отрисовку экрана

class Menu:
    def __init__(self) -> None:
        self.bg = "imgs/kbtu.png"
        self.play_con_button = pygame.Rect(0, 0, 533, 146)
        self.play_con_button.center = (640, 283)
        self.settings_button = pygame.Rect(0, 0, 533, 146)
        self.settings_button.center = (640, 453)
        self.exit_button = pygame.Rect(0, 0, 533, 146)
        self.exit_button.center = (640, 623)
        self.volume_slider = pygame.Rect(0, 0, 826, 20)
        self.volume_slider.center = (640, 360)
        self.back_button = pygame.Rect(0, 0, 533, 146)
        self.back_button.center = (640, 623)
        # звуки
        # self.click_sound = pygame.mixer.Sound("click.wav")
        # self.bg_sound = pygame.mixer.music.load("bg.wav")
    def draw(self, screen, state):
        if state == GAME_MENU: #* в меню отображать 3 кнопки - играть, настройки, выход
            screen.blit(pygame.image.load(self.bg), (0, 0))
            pygame.draw.rect(screen, (255, 0, 0), self.play_con_button)
            pygame.draw.rect(screen, (255, 0, 0), self.settings_button)
            pygame.draw.rect(screen, (255, 0, 0), self.exit_button)
        elif state == GAME_PAUSE: #* в паузе отображать кнопку продолжить, кнопку настройки, кнопку выхода в меню
            screen.blit(pygame.image.load(self.bg), (0, 0))
            pygame.draw.rect(screen, (255, 0, 0), self.play_con_button)
            pygame.draw.rect(screen, (255, 0, 0), self.settings_button)
            pygame.draw.rect(screen, (255, 0, 0), self.exit_button)
        elif state == GAME_SETTINGS: #* в настройках отображать слайдер громкости, кнопку назад
            screen.blit(pygame.image.load(self.bg), (0, 0))
            pygame.draw.rect(screen, (255, 0, 0), self.volume_slider)
            pygame.draw.rect(screen, (255, 0, 0), self.back_button)
        elif state == GAME_OVER:
            pass

class Level:
    def __init__(self) -> None:
        self.bg = "imgs/independence_hall.png"
        self.event_bg = pygame.Rect(0, 0, 826, 146)
        self.event_bg.center = (640, 97)
        self.pause_button = pygame.Rect(0, 0, 146, 146)
        self.pause_button.center = (103, 97)
        self.n_of_card = 2 #* количество карточек на экране(2 или 3)
        # self.click_sound = pygame.mixer.Sound("click.wav")
        # self.bg_sound = pygame.mixer.music.load("bg.wav")
    def draw(self, screen, state):
        screen.blit(pygame.image.load(self.bg), (0, 0))
        pygame.draw.rect(screen, (255, 0, 0), self.event_bg)
        pygame.draw.rect(screen, (255, 0, 0), self.pause_button)
        if self.n_of_card == 2:
            self.card1 = pygame.Rect(0, 0, 400, 146)
            self.card1.center = (427, 445)
            self.card2 = pygame.Rect(0, 0, 400, 146)
            self.card2.center = (853, 445)
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
        self.screen = pygame.display.set_mode((1280, 720))
        self.screen.fill((255, 255, 255))
        self.game_state = GAME_MENU
        self.menu = Menu()
        self.reset()
        
    def reset(self):
        self.player = Player()
        self.level = Level()

    def event_handle(self):
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
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
                    if self.menu.play_con_button.collidepoint(mouse_pos):
                        print("play")
                        self.game_state = GAME_RUNNING
                    elif self.menu.settings_button.collidepoint(mouse_pos):
                        print("settings")
                        self.game_state = GAME_SETTINGS
                    elif self.menu.exit_button.collidepoint(mouse_pos):
                        print("exit")
                        pygame.quit()
                elif self.game_state == GAME_SETTINGS: # если игра в настройках
                    if self.menu.volume_slider.collidepoint(mouse_pos):
                        print((mouse_pos[0]-227)/826) # звук от 0 до 1 поэтому делим на 826
                    elif self.menu.back_button.collidepoint(mouse_pos):
                        self.game_state = GAME_MENU
                elif self.game_state == GAME_PAUSE: # если игра на паузе
                    if self.menu.play_con_button.collidepoint(mouse_pos):
                        print("continue")
                        self.game_state = GAME_RUNNING
                    elif self.menu.settings_button.collidepoint(mouse_pos):
                        print("settings")
                        self.game_state = GAME_SETTINGS
                    elif self.menu.exit_button.collidepoint(mouse_pos):
                        print("exit")
                        self.game_state = GAME_MENU

    def run(self):
        while True:
            self.event_handle()
            if self.game_state == GAME_RUNNING:
                self.level.draw(self.screen, self.game_state)
            else:
                self.menu.draw(self.screen, self.game_state)
            pygame.display.flip()
            pygame.time.Clock().tick(60)
    
if __name__ == "__main__":
    game = Game()
    game.run()