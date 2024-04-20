import pygame, re, sys, random
pygame.mixer.init()
pygame.init()

# CONSTANTS
NAME = None
GAME_MENU, GAME_SETTINGS, GAME_PAUSE, GAME_RUNNING, GAME_OVER = range(5)
FPS = 60
DT = 0

def animate(screen, sprites:list, coords:tuple, current_index:int = 0):
    """Change a sprite every second

    Args:
        screen (pygame.Surface): in what surface to draw
        sprites (list): list of sprites
        coords (tuple): center of the sprite
        current_index (int): index of the current sprite. Defaults to 0.
    """
    if current_index == len(sprites):
        return
    DT += 1
    if DT == 60:
        current_index += 1
        DT = 0
    screen.blit(sprites[current_index], sprites[current_index].get_rect(center=coords))

class Menu:
    def __init__(self) -> None:
        self.bg = pygame.transform.scale(pygame.image.load("imgs/kbtu.png"), (1600, 900))
        self.name1 = pygame.font.SysFont("godofwar", 90).render("Choose of life:", True, (0, 0, 0))
        self.name1_rect = self.name1.get_rect(center=(800, 50))
        self.name2 = pygame.font.SysFont("godofwar", 90).render("Teenages", True, (0, 0, 0))
        self.name2_rect = self.name2.get_rect(center=(800, 150))
        self.button = pygame.transform.scale(pygame.image.load("assets/button/3.png"), (600, 150))
        
        self.play_button = self.button
        self.play_button_rect = self.play_button.get_rect(center=(800, 425))
        self.play_button_text = pygame.font.SysFont("godofwar", 72).render("Start", True, (0, 0, 0))
        self.play_button_text_rect = self.play_button_text.get_rect(center=(800, 425))
        
        self.conn_button = self.button
        self.conn_button_rect = self.conn_button.get_rect(center=(800, 425))
        self.conn_button_text = pygame.font.SysFont("godofwar", 72).render("Continue", True, (0, 0, 0))
        self.conn_button_text_rect = self.conn_button_text.get_rect(center=(800, 425))
        
        self.settings_button = self.button
        self.settings_button_rect = self.settings_button.get_rect(center=(800, 600))
        self.settings_button_text = pygame.font.SysFont("godofwar", 72).render("Settings", True, (0, 0, 0))
        self.settings_button_text_rect = self.settings_button_text.get_rect(center=(800, 600))
        
        self.exit_button = self.button
        self.exit_button_rect = self.exit_button.get_rect(center=(800, 775))
        self.exit_button_text = pygame.font.SysFont("godofwar", 72).render("Exit", True, (0, 0, 0))
        self.exit_button_text_rect = self.exit_button_text.get_rect(center=(800, 775))

        self.volume_slider = pygame.Rect(0, 0, 1001, 20)
        self.volume_slider.center = (800, 450)
        self.volume_slider_current_level = pygame.Rect(0, 0, 0.1*1000, 20)
        self.volume_slider_current_level.midleft = (300, 450)
        self.int_volume_text = pygame.font.SysFont("godofwar", 36).render("10", True, (151,160,223))
        self.int_volume_text_rect = self.int_volume_text.get_rect(center=(800, 500))
        self.volume_text = pygame.font.SysFont("godofwar", 36).render("Volume", True, (151,160,223))
        self.volume_text_rect = self.volume_text.get_rect(center=(800, 400))

        self.back_button = self.button
        self.back_button_rect = self.back_button.get_rect(center=(800, 775))
        self.back_button_text = pygame.font.SysFont("godofwar", 72).render("Menu", True, (0, 0, 0))
        self.back_button_text_rect = self.back_button_text.get_rect(center=(800, 775))
        # звуки
        # self.click_sound = pygame.mixer.Sound("click.wav")
        # self.bg_sound = pygame.mixer.music.load("bg.wav")
    def draw(self, screen, state):
        if state == GAME_MENU:
            screen.blit(self.bg, (0, 0))

            screen.blit(self.play_button, self.play_button_rect)
            screen.blit(self.play_button_text, self.play_button_text_rect)

            screen.blit(self.settings_button, self.settings_button_rect)
            screen.blit(self.settings_button_text, self.settings_button_text_rect)

            screen.blit(self.exit_button, self.exit_button_rect)
            screen.blit(self.exit_button_text, self.exit_button_text_rect)
        elif state == GAME_PAUSE:
            screen.blit(self.bg, (0, 0))

            screen.blit(self.conn_button, self.conn_button_rect)
            screen.blit(self.conn_button_text, self.conn_button_text_rect)

            screen.blit(self.settings_button, self.settings_button_rect)
            screen.blit(self.settings_button_text, self.settings_button_text_rect)

            screen.blit(self.back_button, self.back_button_rect)
            screen.blit(self.back_button_text, self.back_button_text_rect)
        elif state == GAME_SETTINGS:
            screen.blit(self.bg, (0, 0))

            pygame.draw.rect(screen, (31,36,75), self.volume_slider)
            pygame.draw.rect(screen, (151,160,223), self.volume_slider_current_level)
            self.int_volume_text = pygame.font.SysFont("godofwar", 36).render(f"{int(pygame.mixer.music.get_volume()*100)}", True, (151,160,223))
            self.int_volume_text_rect = self.int_volume_text.get_rect(center=(800, 500))
            screen.blit(self.int_volume_text, self.int_volume_text_rect)
            screen.blit(self.volume_text, self.volume_text_rect)

            pygame.draw.circle(screen, (0, 0, 0), (pygame.mixer.music.get_volume()*1000+300, 450), 15)
            pygame.draw.circle(screen, (151,160,223), (pygame.mixer.music.get_volume()*1000+300, 450), 10)

            screen.blit(self.back_button, self.back_button_rect)
            screen.blit(self.back_button_text, self.back_button_text_rect)
        elif state == GAME_OVER:
            pass
        screen.blit(self.name1, self.name1_rect)
        screen.blit(self.name2, self.name2_rect)

class Level:
    def __init__(self, bg_img:str = None, first_card_img:str = None, first_card_cation: dict = None, 
                 second_card_img:str = None, second_card_cation: dict = None, 
                 third_card_img:str = None, third_card_cation: dict = None, 
                 n_of_choises = 2, change_status:str = None) -> None:
        self.bg = pygame.transform.scale(pygame.image.load("imgs/independence_hall.png"), (1600, 900))

        self.event_info = pygame.transform.scale(pygame.image.load("assets/event/5.png"), (1000, 250))
        self.event_info_rect = self.event_info.get_rect(center=(800, 150))
        self.event_info_text = pygame.font.SysFont("godofwar", 72).render("Event", True, (0, 0, 0))
        self.evevt_info_text_rect = self.event_info_text.get_rect(center=(800, 150))

        self.after_event_info = pygame.Rect(0, 0, 1000, 250)
        self.after_event_info.center = (800, 165)
        self.after_event_info_text = pygame.font.SysFont("godofwar", 72).render("Event", True, (0, 0, 0))
        self.after_evevt_info_text_rect = self.event_info_text.get_rect(center=(800, 165))

        self.pause_button = pygame.transform.scale(pygame.image.load("assets/settings.png"), (100, 100))
        self.pause_button_rect = self.pause_button.get_rect(topleft=(20, 20))
        
        self.n_of_card = n_of_choises
        # self.click_sound = pygame.mixer.Sound("click.wav")
        # self.bg_sound = pygame.mixer.music.load("bg.wav")
    def draw(self, screen):
        screen.blit(self.bg, (0, 0))
        screen.blit(self.pause_button, self.pause_button_rect)
        if self.n_of_card == 0:
            pygame.draw.rect(screen, (255, 0, 0), self.after_event_info)
        elif self.n_of_card == 2:
            screen.blit(self.event_info, self.event_info_rect)
            self.card1 = pygame.Rect(0, 0, 450, 400)
            self.card1.center = (525, 650)
            pygame.draw.rect(screen, (255, 0, 0), self.card1)

            self.card2 = pygame.Rect(0, 0, 450, 400)
            self.card2.center = (1075, 650)
            pygame.draw.rect(screen, (255, 0, 0), self.card2)
        elif self.n_of_card == 3:
            pygame.draw.rect(screen, (255, 0, 0), self.event_info)
            self.card1 = pygame.Rect(0, 0, 300, 400)
            self.card1.center = (450, 650)
            pygame.draw.rect(screen, (255, 0, 0), self.card1)

            self.card2 = pygame.Rect(0, 0, 300, 400)
            self.card2.center = (800, 650)
            pygame.draw.rect(screen, (255, 0, 0), self.card2)

            self.card3 = pygame.Rect(0, 0, 300, 400)
            self.card3.center = (1150, 650)
            pygame.draw.rect(screen, (255, 0, 0), self.card3)

class Player:
    def __init__(self) -> None:
        self.knowledge = 0
        self.mood = 0
        self.money = 0
        self.status = None
        self.icon = "" #* иконка игрока, будет 3 спрайта - счастливый, нейтральный, грустный

class Game:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((1600, 900))
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
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_state == GAME_RUNNING:
                        self.game_state = GAME_PAUSE
                    elif self.game_state == GAME_PAUSE:
                        self.game_state = GAME_RUNNING
                    elif self.game_state == GAME_MENU:
                        pygame.quit()
                        sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.game_state == GAME_RUNNING:
                    if self.level.card1.collidepoint(mouse_pos):
                        print("card1")
                    elif self.level.card2.collidepoint(mouse_pos):
                        print("card2")
                    elif self.level.pause_button_rect.collidepoint(mouse_pos):
                        print("pause")
                        self.game_state = GAME_PAUSE
                elif self.game_state == GAME_MENU:
                    if self.menu.conn_button_rect.collidepoint(mouse_pos):
                        print("conn")
                        self.game_state = GAME_RUNNING
                    elif self.menu.settings_button_rect.collidepoint(mouse_pos):
                        print("settings")
                        self.prev_game_state = GAME_MENU
                        self.game_state = GAME_SETTINGS
                    elif self.menu.back_button_rect.collidepoint(mouse_pos):
                        print("back")
                        pygame.quit()
                elif self.game_state == GAME_SETTINGS:
                    if self.menu.back_button_rect.collidepoint(mouse_pos):
                        self.game_state = self.prev_game_state
                elif self.game_state == GAME_PAUSE:
                    if self.menu.play_button_rect.collidepoint(mouse_pos):
                        print("continue")
                        self.game_state = GAME_RUNNING
                    elif self.menu.settings_button_rect.collidepoint(mouse_pos):
                        print("settings")
                        self.prev_game_state = GAME_PAUSE
                        self.game_state = GAME_SETTINGS
                    elif self.menu.exit_button_rect.collidepoint(mouse_pos):
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
                self.level.draw(self.screen)
            else:
                self.menu.draw(self.screen, self.game_state)
            self.event_handle()
            pygame.display.flip()
            pygame.time.Clock().tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()