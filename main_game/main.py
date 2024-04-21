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
    def __init__(self, image_center_pos, image, text=None, text_center_pos = None, font_size=72, text_color=(0, 0, 0)):
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

class Slider:
    def __init__(self, center:tuple, basic_volume:float, name:str) -> None:
        self.center = center
        self.name = name
        self.volume = basic_volume
        self.slider = pygame.Rect(0, 0, 1001, 20)
        self.slider.center = self.center
        self.slider_current_level = pygame.Rect(0, 0, self.volume*1000, 20)
        self.slider_current_level.midleft = (300, self.center[1])
        self.light_color = (151,160,223)
        self.dark_color = (31,36,75)
        self.click_sound = pygame.mixer.Sound("sounds/pop.mp3")
    def draw(self, screen):
        pygame.draw.rect(screen, self.dark_color, self.slider)
        pygame.draw.rect(screen, self.light_color, self.slider_current_level)
        font = pygame.font.SysFont("godofwar", 36)
        volume_text_int = font.render(f"{int(self.volume*100)}", True, self.light_color)
        volume_text_int_rect = volume_text_int.get_rect(center=(self.center[0],self.center[1]+50))
        volume_text = font.render(self.name, True, self.light_color)
        volume_text_rect = volume_text.get_rect(center=(self.center[0],self.center[1]-50))
        screen.blit(volume_text_int, volume_text_int_rect)
        screen.blit(volume_text, volume_text_rect)
        pygame.draw.circle(screen, (0, 0, 0), (self.volume*1000+300, self.center[1]), 15)
        pygame.draw.circle(screen, self.light_color, (self.volume*1000+300, self.center[1]), 10)
    def handle_event(self, mouse_pos):
        if pygame.mouse.get_pressed()[0]:
            if self.slider.collidepoint(mouse_pos):
                self.volume = (mouse_pos[0]-300)/1000
                self.slider_current_level = pygame.Rect(0, 0, self.volume*1000, 20)
                self.slider_current_level.midleft = (300, self.center[1])
                self.click_sound.play()

class Menu:
    """Menu class
    """
    def __init__(self) -> None:
        self.bg = pygame.transform.scale(pygame.image.load("bg_imgs/menu.png"), (1600, 900))
        
        font = pygame.font.SysFont("godofwar", 90)
        self.name = font.render("Choice of students", True, (151,160,223))
        self.name_rect = self.name.get_rect(center=(800, 100))
        button_image = pygame.transform.scale(pygame.image.load("assets/button/3.png"), (600, 150))
        self.button_offset = 0
 
        self.play_button = Button(image_center_pos=(800, 425), image=button_image, text="Start")
        
        self.conn_button = Button(image_center_pos=(800, 425), image=button_image, text="Continue")
        
        self.settings_button = Button(image_center_pos=(800, 600), image=button_image, text="Settings")
        
        self.exit_button = Button(image_center_pos=(800, 775), image=button_image, text="Exit")

        self.back_button = Button(image_center_pos=(800, 775), image=button_image, text="Menu")

        self.volume_slider = Slider((800, 400), 0.1, "Music Volume")
        self.sfx_volume_slider = Slider((800, 600), 0.1, "SFX Volume")

        # звуки
        self.click_sound = pygame.mixer.Sound("sounds/click.mp3")
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

            self.volume_slider.draw(screen)
            
            self.sfx_volume_slider.draw(screen)
            
            self.back_button.draw(screen)
        elif state == GAME_OVER:
            screen.fill((0, 0, 0))
            
        screen.blit(self.name, self.name_rect)

class Level:
    """Level class
    """
    def __init__(self, bg_img:str = "independence_hall.png", card1_text:str = "Card1", card2_text:str = "Card2", card3_text:str = "Card3",
                 event_info_text1:str = "Event contain this information1", event_info_text2:str = "Event contain this information2", event_info_text3:str = "Event contain this information3",
                 after_event_text1:str = "After event contain this information1", after_event_text2:str = "After event contain this information2", after_event_text3:str = "After event contain this information3", after_event1_bg:str = "independence_hall.png",
                 after_event_text4:str = "After event contain this information1", after_event_text5:str = "After event contain this information2", after_event_text6:str = "After event contain this information3", after_event2_bg:str = "independence_hall.png",
                 n_of_choises = 2, change_status:str = None) -> None:
        
        self.bg = pygame.transform.scale(pygame.image.load(f"bg_imgs/{bg_img}"), (1600, 900))
        self.after_event1_bg = pygame.transform.scale(pygame.image.load(f"bg_imgs/{after_event1_bg}"), (1600, 900))
        self.after_event2_bg = pygame.transform.scale(pygame.image.load(f"bg_imgs/{after_event2_bg}"), (1600, 900))
        self.bg_rect = self.bg.get_rect()
        self.font = pygame.font.SysFont("godofwar", 50)
        self.choosed_card = 1

        self.event_info = pygame.transform.scale(pygame.image.load("assets/event/5.png"), (1000, 250))
        self.event_info_rect = self.event_info.get_rect(center=(800, 150))
        self.after_event_info_rect = self.event_info.get_rect(center=(800, 450))
        
        self.event_info_text1 = self.font.render(event_info_text1, True, (0, 0, 0))
        self.event_info_text_rect1 = self.event_info_text1.get_rect(center=(800, 100))
        self.event_info_text2 = self.font.render(event_info_text2, True, (0, 0, 0))
        self.event_info_text_rect2 = self.event_info_text2.get_rect(center=(800, 150))
        self.event_info_text3 = self.font.render(event_info_text3, True, (0, 0, 0))
        self.event_info_text_rect3 = self.event_info_text3.get_rect(center=(800, 200))
        
        self.after_event_text1 = self.font.render(after_event_text1, True, (0, 0, 0))
        self.after_evevt_text_rect1 = self.after_event_text1.get_rect(center=(800, 400))
        self.after_event_text2 = self.font.render(after_event_text2, True, (0, 0, 0))
        self.after_evevt_text_rect2 = self.after_event_text2.get_rect(center=(800, 450))
        self.after_event_text3 = self.font.render(after_event_text3, True, (0, 0, 0))
        self.after_evevt_text_rect3 = self.after_event_text3.get_rect(center=(800, 500))
        self.after_event_text4 = self.font.render(after_event_text4, True, (0, 0, 0))
        self.after_evevt_text_rect4 = self.after_event_text4.get_rect(center=(800, 400))
        self.after_event_text5 = self.font.render(after_event_text5, True, (0, 0, 0))
        self.after_evevt_text_rect5 = self.after_event_text5.get_rect(center=(800, 450))
        self.after_event_text6 = self.font.render(after_event_text6, True, (0, 0, 0))
        self.after_evevt_text_rect6 = self.after_event_text6.get_rect(center=(800, 500))
        
        self.pause_button = pygame.transform.scale(pygame.image.load("assets/settings.png"), (100, 100))
        self.pause_button_rect = self.pause_button.get_rect(topleft=(20, 20))
        
        self.n_of_card = n_of_choises
        self.card1_text = card1_text
        self.card2_text = card2_text
        self.card3_text = card3_text
    def draw(self, screen, current_level_index):
        screen.blit(self.bg, (0, 0))
        screen.blit(self.pause_button, self.pause_button_rect)
        if self.n_of_card == 0:
            screen.blit(self.event_info, self.after_event_info_rect)
            if self.choosed_card == 1:
                screen.blit(self.after_event_text1, self.after_evevt_text_rect1)
                screen.blit(self.after_event_text2, self.after_evevt_text_rect2)
                screen.blit(self.after_event_text3, self.after_evevt_text_rect3)
            elif self.choosed_card == 2:
                screen.blit(self.after_event_text4, self.after_evevt_text_rect4)
                screen.blit(self.after_event_text5, self.after_evevt_text_rect5)
                screen.blit(self.after_event_text6, self.after_evevt_text_rect6)
            elif self.choosed_card == 3:
                screen.blit(self.after_event_text4, self.after_evevt_text_rect4)
                screen.blit(self.after_event_text5, self.after_evevt_text_rect5)
                screen.blit(self.after_event_text6, self.after_evevt_text_rect6)
        elif self.n_of_card == 2:
            screen.blit(self.event_info, self.event_info_rect)
            screen.blit(self.event_info_text1, self.event_info_text_rect1)
            screen.blit(self.event_info_text2, self.event_info_text_rect2)
            screen.blit(self.event_info_text3, self.event_info_text_rect3)

            self.card1 = Button(image_center_pos=(525, 650), 
                                image=pygame.image.load(f"assets/level{current_level_index-1}/card1.png"), 
                                text=self.card1_text, text_center_pos=(525, 800), font_size=36, text_color=(151,160,223))
            self.card1.draw(screen)
            
            self.card2 = Button(image_center_pos=(1075, 650), 
                                image=pygame.image.load(f"assets/level{current_level_index-1}/card2.png"), 
                                text=self.card2_text, text_center_pos=(1075, 800), font_size=36, text_color=(151,160,223))
            self.card2.draw(screen)
        elif self.n_of_card == 3:
            screen.blit(self.event_info, self.event_info_rect)
            screen.blit(self.event_info_text1, self.event_info_text_rect1)
            screen.blit(self.event_info_text2, self.event_info_text_rect2)
            screen.blit(self.event_info_text3, self.event_info_text_rect3)
            
            self.card1 = Button(image_center_pos=(250, 650), 
                                image=pygame.image.load(f"assets/level{current_level_index-1}/card1.png"), 
                                text=self.ard1_text, text_center_pos=(450, 800), font_size=36, text_color=(151,160,223))
            self.card1.draw(screen)

            self.card2 = Button(image_center_pos=(800, 650), 
                                image=pygame.image.load(f"assets/level{current_level_index-1}/card2.png"), 
                                text=self.card2_text, text_center_pos=(800, 800), font_size=36, text_color=(151,160,223))
            self.card2.draw(screen)

            self.card3 = Button(image_center_pos=(1350, 650), 
                                image=pygame.image.load(f"assets/level{current_level_index-1}/card3.png"), 
                                text=self.card3_text, text_center_pos=(1150, 800), font_size=36, text_color=(151,160,223))
            self.card3.draw(screen)
        

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
            Level(bg_img="kbtu.png", event_info_text1="0", after_event_text1="Congratulations, you have been", after_event_text2="admitted to KBTU!", after_event_text3="(to skip click anywhere)", n_of_choises=0), # Предистория
            Level(bg_img="independence_hall.png", event_info_text1="0", after_event_text1="Introductory week has begun!", after_event_text2="You went on a tour near uni",  after_event_text3="Now everything is in your hands!", n_of_choises=0), # Предистория
            Level(event_info_text1="After the first meeting", event_info_text2="you approached the guys and thus", event_info_text3="found your first company", card1_text="Go to PS with friends" , card2_text="Choose student club", after_event_text1="The friends turned out to be", after_event_text2="a small group of businessmen", after_event_text3="After playing they called you to work", after_event_text4="You have been asked to join", after_event_text5="many clubs, but you chose one", after_event_text6="Basketball club!", after_event1_bg="businessmans.png", after_event2_bg="basketball.png"), # 1 лвл
            Level(bg_img="home.png" , event_info_text1="Your parents are very happy that you", event_info_text2="received a scholarship for your studies.", event_info_text3="They gave you some money", after_event_text1="", after_event_text2="", after_event_text3="", after_event_text4="", after_event_text5="", after_event_text6=""), # 2 лвл
            Level(event_info_text1="", event_info_text2="", event_info_text3="", card1_text="", card2_text="", after_event_text1="", after_event_text2="", after_event_text3="", after_event_text4="", after_event_text5="", after_event_text6=""), # 3 лвл
            Level(event_info_text1="", event_info_text2="", event_info_text3="", after_event_text1="", after_event_text2="", after_event_text3="", after_event_text4="", after_event_text5="", after_event_text6=""), # 4 лвл
            Level(event_info_text1="", event_info_text2="", event_info_text3="", after_event_text1="", after_event_text2="", after_event_text3="", after_event_text4="", after_event_text5="", after_event_text6=""), # 5 лвл
            Level(event_info_text1="", event_info_text2="", event_info_text3="", after_event_text1="", after_event_text2="", after_event_text3="", after_event_text4="", after_event_text5="", after_event_text6=""), # 6 лвл
            Level(event_info_text1="", event_info_text2="", event_info_text3="", after_event_text1="", after_event_text2="", after_event_text3="", after_event_text4="", after_event_text5="", after_event_text6=""), # 7 лвл
            Level(event_info_text1="", event_info_text2="", event_info_text3="", after_event_text1="", after_event_text2="", after_event_text3="", after_event_text4="", after_event_text5="", after_event_text6="", n_of_choises=3), # 8 лвл
            Level(event_info_text1="", event_info_text2="", event_info_text3="", after_event_text1="", after_event_text2="", after_event_text3="", after_event_text4="", after_event_text5="", after_event_text6=""), # 9 лвл
            Level(event_info_text1="", event_info_text2="", event_info_text3="", after_event_text1="", after_event_text2="", after_event_text3="", after_event_text4="", after_event_text5="", after_event_text6=""), # 10 лвл
            Level(event_info_text1="", event_info_text2="", event_info_text3="", after_event_text1="", after_event_text2="", after_event_text3="", after_event_text4="", after_event_text5="", after_event_text6=""), # 11 лвл
            Level(event_info_text1="", event_info_text2="", event_info_text3="", after_event_text1="", after_event_text2="", after_event_text3="", after_event_text4="", after_event_text5="", after_event_text6=""), # 12 лвл
            Level(event_info_text1="", event_info_text2="", event_info_text3="", after_event_text1="", after_event_text2="", after_event_text3="", after_event_text4="", after_event_text5="", after_event_text6=""), # 13 лвл
            Level(event_info_text1="", event_info_text2="", event_info_text3="", after_event_text1="", after_event_text2="", after_event_text3="", after_event_text4="", after_event_text5="", after_event_text6=""), # 14 лвл
            Level(event_info_text1="", event_info_text2="", event_info_text3="", after_event_text1="", after_event_text2="", after_event_text3="", after_event_text4="", after_event_text5="", after_event_text6="", n_of_choises=3), # 15 лвл
            Level(event_info_text1="", event_info_text2="", event_info_text3="", after_event_text1="", after_event_text2="", after_event_text3="", after_event_text4="", after_event_text5="", after_event_text6="") # 16 лвл
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
                        # if self.current_level.n_of_card == 0:
                        #     if self.current_level_index not in [8, 15]:
                        #         print("2")
                        #         self.current_level.n_of_card == 2
                        #     else:
                        #         print("3")
                        #         self.current_level.n_of_card == 3
                        # else:
                        #     print("level")
                            self.current_level_index -= 1
                            self.current_level = self.level_list[self.current_level_index]
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_state == GAME_RUNNING:
                    if self.current_level.pause_button_rect.collidepoint(mouse_pos):
                        print("pause")
                        self.menu.click_sound.play()
                        self.game_state = GAME_PAUSE
                        break
                    if self.current_level.n_of_card == 0:
                        if self.current_level.bg_rect.collidepoint(mouse_pos):
                            print("bg")
                            self.menu.click_sound.play()
                            if self.current_level_index < len(self.level_list)-1:
                                self.current_level_index += 1
                                self.current_level = self.level_list[self.current_level_index]
                            else:
                                self.game_state = GAME_OVER
                    elif self.current_level.n_of_card == 2:
                        if self.current_level.card1.rect.collidepoint(mouse_pos):
                            if self.current_level.n_of_card != 0:
                                print("card1")
                                self.menu.click_sound.play()
                                self.current_level.choosed_card = 1
                                self.current_level.n_of_card = 0
                                self.current_level.bg = self.current_level.after_event1_bg
                        elif self.current_level.card2.rect.collidepoint(mouse_pos):
                            if self.current_level.n_of_card != 0:
                                print("card2")
                                self.menu.click_sound.play()
                                self.current_level.choosed_card = 2
                                self.current_level.n_of_card = 0
                                self.current_level.bg = self.current_level.after_event2_bg
                    # elif self.current_level.n_of_card == 3:
                    #     if self.current_level.card1.rect.collidepoint(mouse_pos):
                    #         if self.current_level.n_of_card != 0:
                    #             print("card1")
                    #             self.current_level.choosed_card = 1
                    #             self.current_level.n_of_card = 0
                    #     elif self.current_level.card2.rect.collidepoint(mouse_pos):
                    #         if self.current_level.n_of_card != 0:
                    #             print("card2")
                    #             self.current_level.choosed_card = 2
                    #             self.current_level.n_of_card = 0
                    #     elif self.current_level.card3.rect.collidepoint(mouse_pos):
                    #         if self.current_level.n_of_card != 0:
                    #             print("card3")
                    #             self.current_level.choosed_card = 3
                    #             self.current_level.n_of_card = 0
            if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
                if self.game_state == GAME_MENU:
                    if self.menu.play_button.handle_event(event, mouse_pos):
                        self.menu.click_sound.play()
                        self.game_state = GAME_RUNNING
                    elif self.menu.settings_button.handle_event(event, mouse_pos):
                        self.menu.click_sound.play()
                        self.prev_game_state = GAME_MENU
                        self.game_state = GAME_SETTINGS
                    elif self.menu.exit_button.handle_event(event, mouse_pos):
                        self.menu.click_sound.play()
                        pygame.quit()
                        sys.exit()
                elif self.game_state == GAME_SETTINGS:
                    if self.menu.back_button.handle_event(event, mouse_pos):
                        self.menu.click_sound.play()
                        self.game_state = self.prev_game_state
                elif self.game_state == GAME_PAUSE:
                    if self.menu.conn_button.handle_event(event, mouse_pos):
                        self.menu.click_sound.play()
                        self.game_state = GAME_RUNNING
                    elif self.menu.settings_button.handle_event(event, mouse_pos):
                        self.menu.click_sound.play()
                        self.prev_game_state = GAME_PAUSE
                        self.game_state = GAME_SETTINGS
                    elif self.menu.back_button.handle_event(event, mouse_pos):
                        self.menu.click_sound.play()
                        self.game_state = GAME_MENU
        if self.game_state == GAME_SETTINGS:
            self.menu.volume_slider.handle_event(mouse_pos)
            pygame.mixer.music.set_volume(self.menu.volume_slider.volume)
            self.menu.sfx_volume_slider.handle_event(mouse_pos)
            self.menu.click_sound.set_volume(self.menu.sfx_volume_slider.volume)
            self.menu.volume_slider.click_sound.set_volume(self.menu.sfx_volume_slider.volume)
            self.menu.sfx_volume_slider.click_sound.set_volume(self.menu.sfx_volume_slider.volume)
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