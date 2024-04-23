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
        
        self.player_0fx = pygame.image.load("assets/player/mc_joyful.png")
        self.player_1fx = pygame.image.load("assets/player/mc_normal.png")
        self.player_2fx = pygame.image.load("assets/player/mc_tired_extremally.png")
        
        self.font = pygame.font.SysFont("godofwar", 90)
        self.name = self.font.render("Choice of students", True, (151,160,223))
        self.name_rect = self.name.get_rect(center=(800, 100))
        button_image = pygame.transform.scale(pygame.image.load("assets/button/3.png"), (600, 150))
        self.button_offset = 0
 
        self.play_button = Button(image_center_pos=(800, 425), image=button_image, text="Start")
        
        self.conn_button = Button(image_center_pos=(800, 425), image=button_image, text="Continue")
        
        self.settings_button = Button(image_center_pos=(800, 600), image=button_image, text="Settings")
        
        self.exit_button = Button(image_center_pos=(800, 775), image=button_image, text="Exit")

        self.back_button = Button(image_center_pos=(800, 775), image=button_image, text="Menu")

        self.volume_slider = Slider((800, 400), 0.5, "Music Volume")
        self.sfx_volume_slider = Slider((800, 600), 0.5, "SFX Volume")

        # звуки
        self.click_sound = pygame.mixer.Sound("sounds/click.mp3")
        # self.bg_sound = pygame.mixer.music.load("bg.wav")
    def change_volume(self, mouse_pos):
        self.volume_slider.handle_event(mouse_pos)
        pygame.mixer.music.set_volume(self.volume_slider.volume)
        self.sfx_volume_slider.handle_event(mouse_pos)
        self.click_sound.set_volume(self.sfx_volume_slider.volume)
        self.volume_slider.click_sound.set_volume(self.sfx_volume_slider.volume)
        self.sfx_volume_slider.click_sound.set_volume(self.sfx_volume_slider.volume)
    def draw(self, screen, state, level_index, fx):
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
            screen.blit(self.bg, (0, 0))
            game_over = self.font.render("game over, thx you <3", True, (151,160,223))
            screen.blit(game_over, game_over.get_rect(center=(800, 150)))
            exit_text = self.font.render("click anywhere to exit", True, (151,160,223))
            screen.blit(exit_text, exit_text.get_rect(center=(800, 850)))
            if fx == 0:
                fx0_text = self.font.render("You don't have FX!!!", True, (151,160,223))
                screen.blit(fx0_text, fx0_text.get_rect(center=(800, 350)))
                screen.blit(self.player_0fx, self.player_0fx.get_rect(center=(800, 550)))
            elif fx == 1:
                fx1_text = self.font.render("One FX, normal for first semester", True, (151,160,223))
                screen.blit(fx1_text, fx1_text.get_rect(center=(800, 350)))
                screen.blit(self.player_1fx, self.player_1fx.get_rect(center=(800, 550)))
            elif fx == 2:
                fx2_text = self.font.render("Two FX, try to learn more", True, (151,160,223))
                screen.blit(fx2_text, fx2_text.get_rect(center=(800, 350)))
                screen.blit(self.player_2fx, self.player_2fx.get_rect(center=(800, 550)))
        screen.blit(self.name, self.name_rect)

class Level:
    """Level class
    """
    def __init__(self, bg_img:str = "independence_hall.png", card1_text:str = "Card1", card2_text:str = "Card2", card3_text:str = "Card3",
                 event_info_text1:str = "Event contain this information1", event_info_text2:str = "Event contain this information2", event_info_text3:str = "Event contain this information3",
                 after_event_text1:str = "After event contain this information1", after_event_text2:str = "After event contain this information2", after_event_text3:str = "After event contain this information3", after_event1_bg:str = "independence_hall.png",
                 after_event_text4:str = "After event contain this information1", after_event_text5:str = "After event contain this information2", after_event_text6:str = "After event contain this information3", after_event2_bg:str = "independence_hall.png",
                 card1_img:str = "card1.png", card2_img:str = "card2.png", card3_img:str = "card3.png",
                 card1_stat:list = 0, card2_stat:list = 0, 
                 n_of_choises = 2, change_stats:list = None) -> None:
        
        self.bg = pygame.transform.scale(pygame.image.load(f"bg_imgs/{bg_img}"), (1600, 900))
        self.after_event1_bg = pygame.transform.scale(pygame.image.load(f"bg_imgs/{after_event1_bg}"), (1600, 900))
        self.after_event2_bg = pygame.transform.scale(pygame.image.load(f"bg_imgs/{after_event2_bg}"), (1600, 900))
        self.bg_rect = self.bg.get_rect()
        self.font = pygame.font.SysFont("godofwar", 50)
        self.choosed_card = 1
        self.card1_img = card1_img
        self.card2_img = card2_img
        self.card3_img = card3_img
        self.change_stats = change_stats
        
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
                                image=pygame.image.load(f"assets/level{current_level_index-1}/{self.card1_img}"), 
                                text=self.card1_text, text_center_pos=(525, 800), font_size=36, text_color=(151,160,223))
            self.card1.draw(screen)
            
            self.card2 = Button(image_center_pos=(1075, 650), 
                                image=pygame.image.load(f"assets/level{current_level_index-1}/{self.card2_img}"), 
                                text=self.card2_text, text_center_pos=(1075, 800), font_size=36, text_color=(151,160,223))
            self.card2.draw(screen)
        elif self.n_of_card == 3:
            screen.blit(self.event_info, self.event_info_rect)
            screen.blit(self.event_info_text1, self.event_info_text_rect1)
            screen.blit(self.event_info_text2, self.event_info_text_rect2)
            screen.blit(self.event_info_text3, self.event_info_text_rect3)
            
            self.card1 = Button(image_center_pos=(250, 650), 
                                image=pygame.image.load(f"assets/level{current_level_index-1}/{self.card1_img}"), 
                                text=self.card1_text, text_center_pos=(450, 800), font_size=36, text_color=(151,160,223))
            self.card1.draw(screen)

            self.card2 = Button(image_center_pos=(800, 650), 
                                image=pygame.image.load(f"assets/level{current_level_index-1}/{self.card2_img}"), 
                                text=self.card2_text, text_center_pos=(800, 800), font_size=36, text_color=(151,160,223))
            self.card2.draw(screen)

            self.card3 = Button(image_center_pos=(1350, 650), 
                                image=pygame.image.load(f"assets/level{current_level_index-1}/{self.card3_img}"), 
                                text=self.card3_text, text_center_pos=(1150, 800), font_size=36, text_color=(151,160,223))
            self.card3.draw(screen)
        

class Player:
    def __init__(self) -> None:
        self.knowledge = 0
        self.mood = 0
        self.money = 0
        self.status = None
        self.basket = False
        self.job = False
        self.fx = 0
        self.icon = "" #* иконка игрока, будет 3 спрайта - счастливый, нейтральный, грустный
    def apply_changes(self, changes):
        for attribute, value in changes.items():
            if hasattr(self, attribute):
                setattr(self, attribute, getattr(self, attribute) + value)
                print(f"{attribute} changed to {getattr(self, attribute)}")
            else:
                print(f"No such attribute: {attribute}")

class Game:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((1600, 900))
        self.menu = Menu()
        self.reset()
    def update_levels(self, current_level_index):
        self.level_list = [
            Level(bg_img="kbtu.png", event_info_text1="0", after_event_text1="Congratulations, you have been", after_event_text2="admitted to KBTU!", after_event_text3="(to skip click anywhere)", n_of_choises=0), # Предистория
            Level(bg_img="independence_hall.png", event_info_text1="0", after_event_text1="Introductory week has begun!", after_event_text2="You went on a tour near uni",  after_event_text3="Now everything is in your hands!", n_of_choises=0), # Предистория
            Level(event_info_text1="After the first meeting", event_info_text2="you approached the guys and thus", event_info_text3="found your first company", card1_text="Go to PS with friends" , card2_text="Choose student club", after_event_text1="The friends turned out to be", after_event_text2="a small group of businessmen", after_event_text3="After playing they called you to work", after_event_text4="You have been asked to join", after_event_text5="many clubs, but you chose one", after_event_text6="Basketball club!", after_event1_bg="businessmans.png", after_event2_bg="basketball.png", change_stats=[{"job": True}, {"basket": True}]), # 1 лвл
            Level(bg_img="home.png" , event_info_text1="Your parents are happy that you", event_info_text2="received a scholarship for studies", event_info_text3="They gave you some money", card1_text="Buy programming course" , card2_text="Keep money for yourself", after_event_text1="Your fingers ran across", after_event_text2="the keyboard", after_event_text3="You gain knowledge", after_event_text4="You kept the money for yourself", after_event_text5="If you don't study, they will be", after_event_text6="useful to you", after_event1_bg="programm_course.png", after_event2_bg="ez_money.png"), # 2 лвл
            Level(bg_img="study.png" , event_info_text1="The introductory week flew by,", event_info_text2="you just went to classes and understand", event_info_text3="that you need to learn discrete", card1_text="Buy a course from an ad" , card2_text="Learn subject yourself", after_event_text1="You were unlucky :(", after_event_text2="The course you bought turned out ", after_event_text3="to be a dud and you lose money", after_event_text4="You decided to sit down and", after_event_text5="read the books on your own", after_event_text6="It was a good decision", after_event1_bg="loser.png", after_event2_bg="brain_power.png"), # 3 лвл
            Level(bg_img="beach.png" , event_info_text1="You are at the student initiation", event_info_text2="on the shore of the reservoir", event_info_text3="Suddenly it started to rain", card1_text="Watch concert in the rain" , card2_text="Hide from the rain", after_event_text1="", after_event_text2="You are wet but happy!", after_event_text3="", after_event_text4="Nothing much happened while", after_event_text5="you were in the building", after_event_text6="You missed the best part :(", after_event1_bg="wetnhappy.png", after_event2_bg="inbuilding.png"), # 4 лвл
            Level(bg_img="independence_hall.png" , event_info_text1="", event_info_text2="After a week of midterms", event_info_text3="you have free time", card1_text=("Play basketball game" if self.player.basket else "Go to work") , card2_text="Go to club", after_event_text1="" if self.player.basket else "You have successfully completed", after_event_text2=("Your team won the championship" if self.player.basket else "your working day"), after_event_text3=("" if self.player.basket else "You were given a bonus"), after_event_text4="", after_event_text5="You had a great times", after_event_text6="hanging out with friend", after_event1_bg=("basket_win.png" if self.player.basket else "bonus.png"), after_event2_bg="club.png", card1_img=("basketball.png" if self.player.basket else "work.png")), # 5 лвл
            Level(bg_img="snow_almaty.png" , event_info_text1="It's been getting colder in Almaty lately", event_info_text2="The first snow even fell!", event_info_text3="But unfortunately you are sick", card1_text="Stay home" , card2_text="Still go to the lecture", after_event_text1="you missed one day and", after_event_text2="successfully recovered", after_event_text3="maybe the disease wasn't that bad", after_event_text4="You've completed today's classes", after_event_text5="There weren't many of them today", after_event_text6="and you didn't get sicker.", after_event1_bg="home_with_ill.png", after_event2_bg="snow_kbtu.png"), # 6 лвл
            Level(bg_img="deep_snow.png" , event_info_text1="Weekend passed and snow fell knee-deep", event_info_text2="Many students order a taxi", event_info_text3="Follow their example?", card1_text="Choose Taxi" , card2_text="Choose Bus", after_event_text1="You got to the university", after_event_text2="comfortably and made it to", after_event_text3="your classes on time", after_event_text4="Your feet were trampled and", after_event_text5="you were late for the lecture", after_event_text6="There are bad days in life :(", after_event1_bg="snow_kbtu.png", after_event2_bg="crowded_bus.png"), # 7 лвл
            Level(bg_img="final_exam.png" , event_info_text1="You are sitting for an exam", event_info_text2="Solve the last problem", event_info_text3="1573 mod 341", card1_text="207" , card2_text="189", card3_text="217", after_event_text1="", after_event_text2="Correct answer", after_event_text3="", after_event_text4="", after_event_text5="Incorrect answer", after_event_text6="", after_event1_bg="green.png", after_event2_bg="red.png", n_of_choises=3, change_stats=[{"fx": 0}, {"fx": 1}, {"fx": 1}]), # 8 лвл
            Level(bg_img="new_year.png" if not self.player.fx else "final_exam.png", event_info_text1="" if not self.player.fx else "Exam again...", event_info_text2="" if not self.player.fx else "You have 2nd attempt", event_info_text3="" if not self.player.fx else "1573 mod 341", card1_text="" if not self.player.fx else "189", card2_text="" if not self.player.fx else "207", after_event_text1="", after_event_text2="After successfully passing the exams" if not self.player.fx else "Incorrect answer", after_event_text3="you went home to your friends!" if not self.player.fx else "", after_event_text4="", after_event_text5="" if not self.player.fx else "Correct answer", after_event_text6="" if self.player.fx else "", after_event1_bg="red.png", after_event2_bg="green.png", n_of_choises=(2 if self.player.fx else 0), change_stats=[{"fx": 0}, {"fx": -1}]), # 9 лвл
            # Level(bg_img="" , event_info_text1="", event_info_text2="", event_info_text3="", card1_text="" , card2_text="", after_event_text1="", after_event_text2="", after_event_text3="", after_event_text4="", after_event_text5="", after_event_text6="", after_event1_bg="", after_event2_bg=""), # 10 лвл
            # Level(bg_img="" , event_info_text1="", event_info_text2="", event_info_text3="", card1_text="" , card2_text="", after_event_text1="", after_event_text2="", after_event_text3="", after_event_text4="", after_event_text5="", after_event_text6="", after_event1_bg="", after_event2_bg=""), # 11 лвл
            # Level(bg_img="" , event_info_text1="", event_info_text2="", event_info_text3="", card1_text="" , card2_text="", after_event_text1="", after_event_text2="", after_event_text3="", after_event_text4="", after_event_text5="", after_event_text6="", after_event1_bg="", after_event2_bg=""), # 12 лвл
            # Level(bg_img="" , event_info_text1="", event_info_text2="", event_info_text3="", card1_text="" , card2_text="", after_event_text1="", after_event_text2="", after_event_text3="", after_event_text4="", after_event_text5="", after_event_text6="", after_event1_bg="", after_event2_bg=""), # 13 лвл
            # Level(bg_img="" , event_info_text1="", event_info_text2="", event_info_text3="", card1_text="" , card2_text="", after_event_text1="", after_event_text2="", after_event_text3="", after_event_text4="", after_event_text5="", after_event_text6="", after_event1_bg="", after_event2_bg=""), # 14 лвл
            # Level(bg_img="" , event_info_text1="", event_info_text2="", event_info_text3="", card1_text="" , card2_text="", after_event_text1="", after_event_text2="", after_event_text3="", after_event_text4="", after_event_text5="", after_event_text6="", after_event1_bg="", after_event2_bg="", n_of_choises=3), # 15 лвл
            # Level(bg_img="" , event_info_text1="", event_info_text2="", event_info_text3="", card1_text="" , card2_text="", after_event_text1="", after_event_text2="", after_event_text3="", after_event_text4="", after_event_text5="", after_event_text6="", after_event1_bg="", after_event2_bg="") # 16 лвл
        ]
        self.current_level = self.level_list[current_level_index]
    def reset(self):
        self.game_state = GAME_MENU
        self.current_level_index = 0
        self.player = Player()
        self.update_levels(self.current_level_index)
        self.menu.change_volume((800, 450))
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
                            self.current_level_index -= 1
                            self.current_level = self.level_list[self.current_level_index]
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_state == GAME_RUNNING:
                    if self.current_level.pause_button_rect.collidepoint(mouse_pos):
                        self.menu.click_sound.play()
                        self.game_state = GAME_PAUSE
                        break
                    if self.current_level.n_of_card == 0:
                        if self.current_level.bg_rect.collidepoint(mouse_pos):
                            self.menu.click_sound.play()
                            if self.current_level_index < len(self.level_list)-1:
                                self.current_level_index += 1
                                self.update_levels(self.current_level_index)
                            else:
                                self.game_state = GAME_OVER
                    elif self.current_level.n_of_card == 2:
                        if self.current_level.card1.rect.collidepoint(mouse_pos):
                            if self.current_level.n_of_card != 0:
                                if self.current_level.change_stats:
                                    self.player.apply_changes(self.current_level.change_stats[0])
                                self.menu.click_sound.play()
                                self.current_level.choosed_card = 1
                                self.current_level.n_of_card = 0
                                self.current_level.bg = self.current_level.after_event1_bg
                        elif self.current_level.card2.rect.collidepoint(mouse_pos):
                            if self.current_level.n_of_card != 0:
                                if self.current_level.change_stats:
                                    self.player.apply_changes(self.current_level.change_stats[1])
                                self.menu.click_sound.play()
                                self.current_level.choosed_card = 2
                                self.current_level.n_of_card = 0
                                self.current_level.bg = self.current_level.after_event2_bg
                    elif self.current_level.n_of_card == 3:
                        if self.current_level.card1.rect.collidepoint(mouse_pos):
                            if self.current_level.n_of_card != 0:
                                if self.current_level.change_stats:
                                    self.player.apply_changes(self.current_level.change_stats[0])
                                self.menu.click_sound.play()
                                self.current_level.choosed_card = 1
                                self.current_level.n_of_card = 0
                                self.current_level.bg = self.current_level.after_event1_bg
                        elif self.current_level.card2.rect.collidepoint(mouse_pos):
                            if self.current_level.n_of_card != 0:
                                if self.current_level.change_stats:
                                    self.player.apply_changes(self.current_level.change_stats[1])
                                self.menu.click_sound.play()
                                self.current_level.choosed_card = 2
                                self.current_level.n_of_card = 0
                                self.current_level.bg = self.current_level.after_event2_bg
                        elif self.current_level.card3.rect.collidepoint(mouse_pos):
                            if self.current_level.n_of_card != 0:
                                if self.current_level.change_stats:
                                    self.player.apply_changes(self.current_level.change_stats[2])
                                self.menu.click_sound.play()
                                self.current_level.choosed_card = 3
                                self.current_level.n_of_card = 0
                                self.current_level.bg = self.current_level.after_event2_bg
                elif self.game_state == GAME_OVER:
                    if self.current_level.bg_rect.collidepoint(mouse_pos):
                            self.reset()
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
            self.menu.change_volume(mouse_pos)
    def run(self):
        while True:
            if self.game_state == GAME_RUNNING:
                self.current_level.draw(self.screen, self.current_level_index)
            else:
                self.menu.draw(self.screen, self.game_state, self.current_level_index, self.player.fx)
            self.event_handle()
            pygame.display.flip()
            pygame.time.Clock().tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()