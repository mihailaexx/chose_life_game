import pygame, re, os
pygame.mixer.init()
pygame.init()

# CONSTANTS
GAME_MENU, GAME_SETTINGS, GAME_PAUSE, GAME_RUNNING, GAME_OVER = range(5) #* привязать к состояниям игры отрисовку экрана
FPS = 60
DT = 0
class Menu:
    def __init__(self) -> None:
        self.bg = pygame.transform.scale(pygame.image.load("imgs/kbtu.png"), (1600, 900))
        self.play_button = pygame.Rect(0, 0, 600, 150)
        self.play_button_text = pygame.font.Font(None, 72).render("Start", True, (0, 0, 0))
        self.play_button.center = (800, 425)
        self.play_button_text_rect = self.play_button_text.get_rect(center=(800, 425))
        self.conn_button = pygame.Rect(0, 0, 600, 150)
        self.conn_button_text = pygame.font.Font(None, 72).render("Continue", True, (0, 0, 0))
        self.conn_button.center = (800, 425)
        self.conn_button_text_rect = self.conn_button_text.get_rect(center=(800, 425))
        self.settings_button = pygame.Rect(0, 0, 600, 150)
        self.settings_button_text = pygame.font.Font(None, 72).render("Settings", True, (0, 0, 0))
        self.settings_button.center = (800, 600)
        self.settings_button_text_rect = self.settings_button_text.get_rect(center=(800, 600))
        self.exit_button = pygame.Rect(0, 0, 600, 150)
        self.exit_button_text = pygame.font.Font(None, 72).render("Exit", True, (0, 0, 0))
        self.exit_button.center = (800, 775)
        self.exit_button_text_rect = self.exit_button_text.get_rect(center=(800, 775))
        self.volume_slider = pygame.Rect(0, 0, 1001, 20)
        self.volume_slider.center = (800, 450)
        self.volume_slider_current_level = pygame.Rect(0, 0, 0.1*1000, 20)
        self.volume_slider_current_level.midleft = (300, 450)
        self.int_volume_text = pygame.font.Font(None, 36).render("10", True, (255, 0, 0))
        self.int_volume_text_rect = self.int_volume_text.get_rect(center=(800, 500))
        self.volume_text = pygame.font.Font(None, 36).render("Volume", True, (255, 0, 0))
        self.volume_text_rect = self.volume_text.get_rect(center=(800, 400))
        self.back_button = pygame.Rect(0, 0, 600, 150)
        self.back_button_text = pygame.font.Font(None, 72).render("Back to main menu", True, (0, 0, 0))
        self.back_button.center = (800, 775)
        self.back_button_text_rect = self.back_button_text.get_rect(center=(800, 775))
        # звуки
        # self.click_sound = pygame.mixer.Sound("click.wav")
        # self.bg_sound = pygame.mixer.music.load("bg.wav")
    def animate(self, screen, sprites:list, coords:tuple):
        current_index = 0
        DT += 1
        if DT == 60:
            current_index == (current_index+1)%len(sprites)
            DT = 0
        screen.blit(sprites[current_index], sprites[current_index].get_rect(center=coords))
    def draw(self, screen, state):
        if state == GAME_MENU:
            screen.blit(self.bg, (0, 0))
            pygame.draw.rect(screen, (255, 0, 0), self.play_button)
            screen.blit(self.play_button_text, self.play_button_text_rect)
            pygame.draw.rect(screen, (255, 0, 0), self.settings_button)
            screen.blit(self.settings_button_text, self.settings_button_text_rect)
            pygame.draw.rect(screen, (255, 0, 0), self.exit_button)
            screen.blit(self.exit_button_text, self.exit_button_text_rect)
        elif state == GAME_PAUSE:
            screen.blit(self.bg, (0, 0))
            pygame.draw.rect(screen, (255, 0, 0), self.conn_button)
            screen.blit(self.conn_button_text, self.conn_button_text_rect)
            pygame.draw.rect(screen, (255, 0, 0), self.settings_button)
            screen.blit(self.settings_button_text, self.settings_button_text_rect)
            pygame.draw.rect(screen, (255, 0, 0), self.back_button)
            screen.blit(self.back_button_text, self.back_button_text_rect)
        elif state == GAME_SETTINGS:
            screen.blit(self.bg, (0, 0))
            pygame.draw.rect(screen, (102, 0, 3), self.volume_slider)
            pygame.draw.rect(screen, (255, 0, 0), self.volume_slider_current_level)
            pygame.draw.rect(screen, (255, 0, 0), self.back_button)
            screen.blit(self.back_button_text, self.back_button_text_rect)
            self.int_volume_text = pygame.font.Font(None, 36).render(f"{int(pygame.mixer.music.get_volume()*100)}", True, (255, 0, 0))
            self.int_volume_text_rect = self.int_volume_text.get_rect(center=(800, 500))
            screen.blit(self.int_volume_text, self.int_volume_text_rect)
            screen.blit(self.volume_text, self.volume_text_rect)
            pygame.draw.circle(screen, (0, 0, 0), (pygame.mixer.music.get_volume()*1000+300, 450), 15)
            pygame.draw.circle(screen, (255, 0, 0), (pygame.mixer.music.get_volume()*1000+300, 450), 10)
        elif state == GAME_OVER:
            pass

class Level:
    def __init__(self, bg_img:str = None) -> None:
        self.bg = pygame.transform.scale(pygame.image.load("imgs/independence_hall.png"), (1600, 900))
        self.event = pygame.Rect(0, 0, 1000, 250)
        self.event.center = (800, 165)
        self.event_text = pygame.font.Font(None, 72).render("Event", True, (0, 0, 0))
        self.evevt_text_rect = self.event_text.get_rect(center=(800, 150))
        self.pause_button = pygame.Rect(0, 0, 110, 110)
        self.pause_button.topleft = (40, 40)
        self.n_of_card = 2 #* количество карточек на экране(2 или 3)
        # self.click_sound = pygame.mixer.Sound("click.wav")
        # self.bg_sound = pygame.mixer.music.load("bg.wav")
    def draw(self, screen, state):
        screen.blit(self.bg, (0, 0))
        pygame.draw.rect(screen, (255, 0, 0), self.event)
        pygame.draw.rect(screen, (255, 0, 0), self.pause_button)
        if self.n_of_card == 0:
            pass
        elif self.n_of_card == 2:
            self.card1 = pygame.Rect(0, 0, 450, 400)
            self.card1.center = (525, 650)
            self.card2 = pygame.Rect(0, 0, 450, 400)
            self.card2.center = (1075, 650)
            pygame.draw.rect(screen, (255, 0, 0), self.card1)
            pygame.draw.rect(screen, (255, 0, 0), self.card2)
        elif self.n_of_card == 3:
            self.card1 = pygame.Rect(0, 0, 300, 400)
            self.card1.center = (450, 650)
            self.card2 = pygame.Rect(0, 0, 300, 400)
            self.card2.center = (800, 650)
            self.card3 = pygame.Rect(0, 0, 300, 400)
            self.card3.center = (1150, 650)
            pygame.draw.rect(screen, (255, 0, 0), self.card1)
            pygame.draw.rect(screen, (255, 0, 0), self.card2)
            pygame.draw.rect(screen, (255, 0, 0), self.card3)

class Player:
    def __init__(self) -> None:
        self.grades = 0
        self.mood = 0
        self.money = 0
        self.icon = "" #* иконка игрока, будет 3 спрайта - счастливый, нейтральный, грустный

class Game:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((1600, 900))
        self.screen.fill((255, 255, 255))
        self.game_state = GAME_MENU
        self.menu = Menu()
        self.reset()
        
    def reset(self):
        self.player = Player()
        self.level = Level()
        pygame.mixer.music.set_volume(0.1)
        print(pygame.display.get_window_size())

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
                    pygame.mixer.music.set_volume((mouse_pos[0]-300)/1000)
                    self.menu.volume_slider_current_level = pygame.Rect(0, 0, pygame.mixer.music.get_volume()*1000, 20)
                    self.menu.volume_slider_current_level.midleft = (300, 450)
    def run(self):
        while True:
            if self.game_state == GAME_RUNNING:
                self.level.draw(self.screen, self.game_state)
            else:
                self.menu.draw(self.screen, self.game_state)
            self.event_handle()
            pygame.display.flip()
            pygame.time.Clock().tick(FPS)
    
if __name__ == "__main__":
    game = Game()
    game.run()