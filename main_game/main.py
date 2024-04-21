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

class Button:
    """Button class
    """
    def __init__(self, image_center_pos, image, text, text_center_pos = None, font_size=72, text_color=(0, 0, 0)):
        self.image = image
        self.rect = self.image.get_rect(center=image_center_pos)
        self.text = pygame.font.SysFont("godofwar", font_size).render(text, True, text_color)
        self.text_rect = self.text.get_rect(center=image_center_pos) if text_center_pos == None else self.text.get_rect(center=text_center_pos)
        self.pressed = False

    def draw(self, screen):
        adjusted_rect_img = self.rect.move(0, 5 if self.pressed else 0)
        adjusted_rect_text = self.text_rect.move(0, 5 if self.pressed else 0)
        screen.blit(self.image, adjusted_rect_img)
        screen.blit(self.text, adjusted_rect_text)

    def handle_event(self, event, mouse_pos):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(mouse_pos):
                self.pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.pressed and self.rect.collidepoint(mouse_pos):
                self.pressed = False
                return True  # Кнопка активирована
            self.pressed = False
        return False

class Menu:
    """Menu class
    """
    def __init__(self) -> None:
        self.bg = pygame.transform.scale(pygame.image.load("bg_imgs/kbtu.png"), (1600, 900))
        font = pygame.font.SysFont("godofwar", 90)
        self.name1 = font.render("Choose of life:", True, (0, 0, 0))
        self.name1_rect = self.name1.get_rect(center=(800, 50))
        self.name2 = font.render("Teenagers", True, (0, 0, 0))
        self.name2_rect = self.name2.get_rect(center=(800, 150))
        button_image = pygame.transform.scale(pygame.image.load("assets/button/3.png"), (600, 150))
        self.button_offset = 0
 
        self.play_button = Button(image_center_pos=(800, 425), image=button_image, text="Start")
        
        self.conn_button = Button(image_center_pos=(800, 425), image=button_image, text="Continue")
        
        self.settings_button = Button(image_center_pos=(800, 600), image=button_image, text="Settings")
        
        self.exit_button = Button(image_center_pos=(800, 775), image=button_image, text="Exit")

        self.back_button = Button(image_center_pos=(800, 775), image=button_image, text="Menu")

        self.volume_slider = pygame.Rect(0, 0, 1001, 20)
        self.volume_slider.center = (800, 450)
        self.volume_slider_current_level = pygame.Rect(0, 0, 0.1*1000, 20)
        self.volume_slider_current_level.midleft = (300, 450)

        # звуки
        # self.click_sound = pygame.mixer.Sound("click.wav")
        # self.bg_sound = pygame.mixer.music.load("bg.wav")
    def draw(self, screen, state, level_index):
        if state == GAME_MENU:
            screen.blit(self.bg, (0, 0))

            if level_index == 0:
                self.play_button.draw(screen)
            else:
                self.conn_button.draw(screen)
            

            self.settings_button.draw(screen)

            self.exit_button.draw(screen)
        elif state == GAME_PAUSE:
            screen.blit(self.bg, (0, 0))

            self.conn_button.draw(screen)

            self.settings_button.draw(screen)

            self.back_button.draw(screen)
        elif state == GAME_SETTINGS:
            screen.blit(self.bg, (0, 0))

            pygame.draw.rect(screen, (31,36,75), self.volume_slider)
            pygame.draw.rect(screen, (151,160,223), self.volume_slider_current_level)
            font = pygame.font.SysFont("godofwar", 36)
            int_volume_text = font.render(f"{int(pygame.mixer.music.get_volume()*100)}", True, (151,160,223))
            int_volume_text_rect = int_volume_text.get_rect(center=(800, 500))
            volume_text = font.render("Volume", True, (151,160,223))
            volume_text_rect = volume_text.get_rect(center=(800, 400))
            screen.blit(int_volume_text, int_volume_text_rect)
            screen.blit(volume_text, volume_text_rect)

            pygame.draw.circle(screen, (0, 0, 0), (pygame.mixer.music.get_volume()*1000+300, 450), 15)
            pygame.draw.circle(screen, (151,160,223), (pygame.mixer.music.get_volume()*1000+300, 450), 10)

            self.back_button.draw(screen)
        elif state == GAME_OVER:
            screen.fill((0, 0, 0))
            
        screen.blit(self.name1, self.name1_rect)
        screen.blit(self.name2, self.name2_rect)

class Level:
    """Level class
    """
    def __init__(self, bg_img:str = "independence_hall.png", event_info_text:str = "Event contain this information", after_event_text:str = "After event contain this information", first_card_img:str = None, first_card_action: dict = None, 
                 second_card_img:str = None, second_card_action: dict = None, 
                 third_card_img:str = None, third_card_action: dict = None, 
                 n_of_choises = 2, change_status:str = None) -> None:
        self.bg = pygame.transform.scale(pygame.image.load(f"bg_imgs/{bg_img}"), (1600, 900))
        self.bg_rect = self.bg.get_rect()
        font = pygame.font.SysFont("godofwar", 50)

        self.event_info = pygame.transform.scale(pygame.image.load("assets/event/5.png"), (1000, 250))
        self.event_info_rect = self.event_info.get_rect(center=(800, 150))
        
        self.event_info_text = font.render(event_info_text, True, (0, 0, 0))
        self.event_info_text_rect = self.event_info_text.get_rect(center=(800, 150))

        self.after_event_text = font.render(after_event_text, True, (0, 0, 0))
        self.after_evevt_text_rect = self.after_event_text.get_rect(center=(800, 150))

        self.pause_button = pygame.transform.scale(pygame.image.load("assets/settings.png"), (100, 100))
        self.pause_button_rect = self.pause_button.get_rect(topleft=(20, 20))
        
        self.n_of_card = n_of_choises
        # self.click_sound = pygame.mixer.Sound("click.wav")
        # self.bg_sound = pygame.mixer.music.load("bg.wav")
    def draw(self, screen, current_level_index):
        screen.blit(self.bg, (0, 0))
        screen.blit(self.pause_button, self.pause_button_rect)
        screen.blit(self.event_info, self.event_info_rect)
        if self.n_of_card == 0:
            # pygame.draw.rect(screen, (255, 0, 0), self.after_event_info)
            screen.blit(self.after_event_text, self.after_evevt_text_rect)
        elif self.n_of_card == 2:
            screen.blit(self.event_info_text, self.event_info_text_rect)
            
            self.card1 = pygame.Rect(0, 0, 450, 400)
            self.card1.center = (525, 650)
            pygame.draw.rect(screen, (255, 0, 0), self.card1)
            # self.card1 = Button(center_pos=(525, 650), 
            #                     image=pygame.transform.scale(pygame.image.load(f"assets/level{current_level_index+1}/card1.png"), (450, 400)), 
            #                     text="Card1", image_center_pos = (525, 800), text_cfont_size=36)

            self.card2 = pygame.Rect(0, 0, 450, 400)
            self.card2.center = (1075, 650)
            pygame.draw.rect(screen, (255, 0, 0), self.card2)
            # self.card2 = Button(center_pos=(1075, 650), 
            #                     image=pygame.transform.scale(pygame.image.load(f"assets/level{current_level_index+1}/card2.png"), (450, 400)), 
            #                     text="Card2", image_center_pos = (1075, 800), font_size=36)
        elif self.n_of_card == 3:
            screen.blit(self.event_info_text, self.event_info_text_rect)
            
            self.card1 = pygame.Rect(0, 0, 300, 400)
            self.card1.center = (450, 650)
            pygame.draw.rect(screen, (255, 0, 0), self.card1)
            # self.card1 = Button(center_pos=(450, 650), 
            #                     image=pygame.transform.scale(pygame.image.load(f"assets/level{current_level_index+1}/card1.png"), (300, 400)), 
            #                     text="Card1", image_center_pos = (450, 800), text_cfont_size=36)

            self.card2 = pygame.Rect(0, 0, 300, 400)
            self.card2.center = (800, 650)
            pygame.draw.rect(screen, (255, 0, 0), self.card2)
            # self.card2 = Button(center_pos=(800, 650), 
            #                     image=pygame.transform.scale(pygame.image.load(f"assets/level{current_level_index+1}/card1.png"), (300, 400)), 
            #                     text="Card1", image_center_pos = (800, 800), text_cfont_size=36)

            self.card3 = pygame.Rect(0, 0, 300, 400)
            self.card3.center = (1150, 650)
            pygame.draw.rect(screen, (255, 0, 0), self.card3)
            # self.card3 = Button(center_pos=(1150, 650), 
            #                     image=pygame.transform.scale(pygame.image.load(f"assets/level{current_level_index+1}/card1.png"), (300, 400)), 
            #                     text="Card1", image_center_pos = (1150, 800), text_cfont_size=36)
        

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
        self.current_level_index = 0
        self.level_list = [
            Level(event_info_text="0", after_event_text="0", n_of_choises=0), # Предистория
            Level(event_info_text="1", after_event_text="1"), # 1 лвл
            Level(event_info_text="2", after_event_text="2"), # 2 лвл
            Level(event_info_text="3", after_event_text="3"), # 3 лвл
            Level(event_info_text="4", after_event_text="4"), # 4 лвл
            Level(event_info_text="5", after_event_text="5"), # 5 лвл
            Level(event_info_text="6", after_event_text="6"), # 6 лвл
            Level(event_info_text="7", after_event_text="7"), # 7 лвл
            Level(event_info_text="8", after_event_text="8"), # 8 лвл
            Level(event_info_text="9", after_event_text="9"), # 9 лвл
            Level(event_info_text="10", after_event_text="10"), # 10 лвл
            Level(event_info_text="11", after_event_text="11"), # 11 лвл
            Level(event_info_text="12", after_event_text="12"), # 12 лвл
            Level(event_info_text="13", after_event_text="13"), # 13 лвл
            Level(event_info_text="14", after_event_text="14"), # 14 лвл
            Level(event_info_text="15", after_event_text="15"), # 15 лвл
            Level(event_info_text="16", after_event_text="16") # 16 лвл
        ]
        self.menu = Menu()
        self.reset()
        
    def reset(self):
        self.player = Player()
        self.current_level = self.level_list[self.current_level_index]
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
                if event.key == pygame.K_LEFT and self.game_state == GAME_RUNNING:
                    if self.current_level_index > 0:
                        print("force back")
                        self.current_level_index -= 1
                        self.current_level = self.level_list[self.current_level_index]
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_state == GAME_RUNNING:
                    if self.current_level.pause_button_rect.collidepoint(mouse_pos):
                        print("pause")
                        self.game_state = GAME_PAUSE
                        break
                    #!
                    if self.current_level.n_of_card == 0:
                        if self.current_level.bg_rect.collidepoint(mouse_pos):
                            print("bg")
                            if self.current_level_index < len(self.level_list)-1:
                                self.current_level_index += 1
                                self.current_level = self.level_list[self.current_level_index]
                            else:
                                self.game_state = GAME_OVER
                    else:
                        if self.current_level.card1.collidepoint(mouse_pos):
                            if self.current_level.n_of_card != 0:
                                print("card1")
                                self.current_level.n_of_card = 0
                        elif self.current_level.card2.collidepoint(mouse_pos):
                            if self.current_level.n_of_card != 0:
                                print("card2")
                                self.current_level.n_of_card = 0
                    #!
            if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
                if self.game_state == GAME_MENU:
                    if self.menu.play_button.handle_event(event, mouse_pos):
                        self.game_state = GAME_RUNNING
                    elif self.menu.settings_button.handle_event(event, mouse_pos):
                        self.prev_game_state = GAME_MENU
                        self.game_state = GAME_SETTINGS
                    elif self.menu.exit_button.handle_event(event, mouse_pos):
                        pygame.quit()
                        sys.exit()
                elif self.game_state == GAME_SETTINGS:
                    if self.menu.back_button.handle_event(event, mouse_pos):
                        self.game_state = self.prev_game_state
                elif self.game_state == GAME_PAUSE:
                    if self.menu.conn_button.handle_event(event, mouse_pos):
                        self.game_state = GAME_RUNNING
                    elif self.menu.settings_button.handle_event(event, mouse_pos):
                        self.prev_game_state = GAME_PAUSE
                        self.game_state = GAME_SETTINGS
                    elif self.menu.back_button.handle_event(event, mouse_pos):
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
                self.current_level.draw(self.screen, self.current_level_index)
            else:
                self.menu.draw(self.screen, self.game_state, self.current_level_index)
            self.event_handle()
            pygame.display.flip()
            pygame.time.Clock().tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()