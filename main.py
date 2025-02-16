from src import *
import pygame, logging, random
from src.menu import MenuSecondary
import time, json
logging.basicConfig(level=logging.DEBUG)

pygame.init()
pygame.font.init()

settings = Settings()

if settings.settings["fullscreen"] == True:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((settings.settings["width"], settings.settings["height"]))

pygame.display.set_caption("Save the Animals!!!")

menu = MenuSecondary()
menu_icon_pressed = pygame.image.load("assets/menu assets/Button 1, Pressed.png")
menu_icon_pressed = pygame.transform.scale(menu_icon_pressed, (50, 50))
menu_icon_notpressed = pygame.image.load("assets/menu assets/Button 1, Unpressed.png")
menu_icon_notpressed = pygame.transform.scale(menu_icon_notpressed, (50, 50))

clock = pygame.time.Clock()

# Main game loop
player = Player(screen)
map = Map(screen, player)
zoom = 0.1
run = True
scroll = False

plants = []
for biome in map.biomes:
    for i in range(0, 2):
        coordinates = random.choice(map.biomes[biome])
        if biome == "ocean":
            plants.append(Plant(player, screen, coordinates[0] * 1.6, coordinates[1] * 1.6, dir="assets\\pump.png", scale=4, biome=biome))
        else:
            print(biome)
            plants.append(Plant(player, screen, coordinates[0] * 1.6, coordinates[1] * 1.6, biome=biome))

hover = {"status": False, "obj": None}
dialogue = pygame.image.load("assets\\dialogue.png")
dialogue = pygame.transform.scale(dialogue, (1500, 1000))
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 30)
overlay = pygame.Surface((1920, 1080), pygame.SRCALPHA)  # Enable per-pixel alpha
overlay.fill((0, 0, 0, 128)) 
button = pygame.image.load("assets\\button.png")
button = pygame.transform.scale(button, (800, 200))

button_rect1 = pygame.Rect(100, 600, button.get_width(), button.get_height())  # Button 1
button_rect2 = pygame.Rect(100, 800, button.get_width(), button.get_height())  # Button 2
button_rect3 = pygame.Rect(850, 600, button.get_width(), button.get_height())  # Button 3
button_rect4 = pygame.Rect(850, 800, button.get_width(), button.get_height())  # Button 4

with open("questions.json", 'r') as f:
    questions = json.load(f)

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in [1, 2]:
                if event.button == 1:
                    for plant in plants:
                        if plant.rect.collidepoint(pygame.mouse.get_pos()):
                            
                            background = screen.copy()
                            screen.blit(background, (0, 0))
                            screen.blit(overlay, (0, 0))
                            screen.blit(dialogue, (map.width // 2 - 600, -150))

                            if plant.biome == "grass":
                                text = "Moo-rning, human! I’m here on behalf of Mother Nature, and I’ve got a udderly important mission for you. See that oil power plant over there? It’s polluting the air, ruining the grass, and frankly, it’s a total cow-tastrophe."
                                image = "assets\\cow.png"
                            elif plant.biome == "ocean":
                                image = "assets\\coral.png"
                                text = "Psst! Hey, land-dweller! Yeah, you—the one with the opposable thumbs. I need your help. The ocean’s in trouble, and I’m not just talking about a little seaweed in my hair. That oil rig over there? It’s spewing toxins, killing my friends, and turning this reef into a ghost town. You’ve got to shut it down!"
                            elif plant.biome == "ice":
                                image = "assets\\penguin.png"
                                text = "Hey, you! Yeah, you—the one not wearing a fur coat. I’ve got a problem, and you’re gonna help me solve it. See that oil rig over there? It’s melting my home, poisoning the water, and scaring all the fish away. I’m about two fishes short of losing my cool. You’ve got to shut it down!"
                            else:
                                image = "assets\\camel.png"
                                text = "Hey there, wanderer. Yeah, you—the one who looks like they’ve never gone a day without water. I’ve got a bone to pick with you humans. See that oil operation over there? They’re sucking the desert dry, poisoning the little water we have, and making my sandcastle-building hobby impossible. You’ve got to shut it down!"

                            img = pygame.image.load(image)
                            img = pygame.transform.scale(img, (800, 800))
                            
                            text_box = font.render(text, False, (0, 0, 0), wraplength=900)
                            screen.blit(text_box, (600, 200))
                            screen.blit(img, (1200, 400))

                            pygame.display.flip()

                            time.sleep(3)
                            correct = 0
                            for i in range(0, 3):
                                question = random.choice(questions)
                                button1_text = font.render(question["answers"][0], True, (0, 0, 0))  # Black text
                                button2_text = font.render(question["answers"][1], True, (0, 0, 0))  # Black text
                                button3_text = font.render(question["answers"][2], True, (0, 0, 0))  # Black text
                                button4_text = font.render(question["answers"][3], True, (0, 0, 0))  # Black text

                                correct_answer = question["correct_answer"]
                                question_loop = True
                                while question_loop:
                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            run = False

                                        elif event.type == pygame.MOUSEBUTTONDOWN:
                                            if event.button == 1:
                                                if button_rect1.collidepoint(event.pos):
                                                    if question["answers"][0] == correct_answer:
                                                        text = f"Correct! {question['explanation']}"
                                                        correct += 1
                                                    else:
                                                        text = f"Incorrect! {question['explanation']}"
                                                elif button_rect2.collidepoint(event.pos):
                                                    if question["answers"][1] == correct_answer:
                                                        text = f"Correct! {question['explanation']}"
                                                        correct += 1
                                                    else:
                                                        text = f"Incorrect! {question['explanation']}"
                                                elif button_rect3.collidepoint(event.pos):
                                                    if question["answers"][2] == correct_answer:
                                                        text = f"Correct! {question['explanation']}"
                                                        correct += 1
                                                    else:
                                                        text = f"Incorrect! {question['explanation']}"
                                                elif button_rect4.collidepoint(event.pos):
                                                    if question["answers"][3] == correct_answer:
                                                        text = f"Correct! {question['explanation']}"
                                                        correct += 1
                                                    else:
                                                        text = f"Incorrect! {question['explanation']}"

                                                screen.blit(background, (0, 0))
                                                screen.blit(overlay, (0, 0))
                                                screen.blit(dialogue, (map.width // 2 - 600, -150))
                                                screen.blit(img, (1200, 400))
                                                text_box = font.render(text, False, (0, 0, 0), wraplength=900)
                                                screen.blit(text_box, (600, 200))
                                                pygame.display.flip()
                                                time.sleep(3)
                                                question_loop = False

                                    if question_loop:
                                        screen.blit(background, (0, 0))
                                        screen.blit(overlay, (0, 0))
                                        screen.blit(dialogue, (map.width // 2 - 600, -150))

                                        text_box = font.render(question["question"], False, (0, 0, 0), wraplength=900)
                                        screen.blit(text_box, (600, 200))

                                        screen.blit(button, button_rect1.topleft)  # Button 1
                                        
                                        screen.blit(button, button_rect2.topleft)  # Button 2
                                        screen.blit(button, button_rect3.topleft)  # Button 3
                                        screen.blit(button, button_rect4.topleft)  # Button 4

                                        # Draw text on top of the buttons
                                        screen.blit(button1_text, (button_rect1.x + 50, button_rect1.y + 75))  # Adjust position as needed
                                        screen.blit(button2_text, (button_rect2.x + 50, button_rect2.y + 75))  # Adjust position as needed
                                        screen.blit(button3_text, (button_rect3.x + 50, button_rect3.y + 75))  # Adjust position as needed
                                        screen.blit(button4_text, (button_rect4.x + 50, button_rect4.y + 75))  # Adjust position as needed                      
                                    
                                        pygame.display.flip()
                            
                            if correct >= 3:
                                if plant.biome == "grass":
                                    text = "Moo-velous job, human! Thanks to you, the grass is greener, the air is cleaner, and the cows are doing a happy dance. Mother Nature is proud of you for shutting down that oil power plant. You’ve turned a cow-tastrophe into a cow-mendous victory!"
                                    image = "assets\\cow.png"
                                elif plant.biome == "ocean":
                                    text = "Splash-tastic work, land-dweller! You’ve saved the ocean and its vibrant reefs from becoming a ghost town. The coral and sea creatures are singing your praises—well, as much as fish can sing. You’ve made waves in the fight for a cleaner planet!"
                                    image = "assets\\coral.png"
                                elif plant.biome == "ice":
                                    text = "Ice-solation complete! You’ve saved the penguins’ home from melting away and scared off those pesky toxins. The fish are back, the water’s clean, and the ice is solid once more. You’ve truly earned your cool stripes!"
                                    image = "assets\\penguin.png"
                                else:
                                    text = "Sand-sational effort, wanderer! You’ve stopped the oil operation from sucking the desert dry and poisoning the little water we have. The desert is thriving again, and even the camels are smiling. You’ve made the sands of time a little cleaner!"
                                    image = "assets\\camel.png"
                                plants.remove(plant)
                            
                            else:
                                if plant.biome == "grass":
                                    text = "Moo-ve it along, human! You gave it a good try, but that oil power plant is still causing trouble. Don’t let this cow-tastrophe get you down—Mother Nature believes in you! Take a deep breath and try again. You’ve got this!"
                                    image = "assets\\cow.png"
                                elif plant.biome == "ocean":
                                    text = "Nice try, land-dweller! The ocean’s still in trouble, but don’t let that discourage you. The coral and sea creatures are rooting for you! Take another dive and show that oil rig who’s boss. You’re making waves, even if it doesn’t feel like it yet!"
                                    image = "assets\\coral.png"
                                elif plant.biome == "ice":
                                    text = "Brrr-illiant effort! You gave it your best shot, but that oil rig is still causing trouble. Don’t let the cold freeze your determination—try again! The penguins and fish are counting on you to save their icy home."
                                    image = "assets\\penguin.png"
                                else:
                                    text = "Nice try, wanderer! The desert’s still feeling the heat from that oil operation, but don’t let the sand slip through your fingers. Take another shot, and remember—even camels don’t cross the desert in one stride. You’re closer than you think!"
                                    image = "assets\\camel.png"

                            screen.blit(background, (0, 0))
                            screen.blit(overlay, (0, 0))
                            screen.blit(dialogue, (map.width // 2 - 600, -150))
                            screen.blit(img, (1200, 400))
                            text_box = font.render(text, False, (0, 0, 0), wraplength=900)
                            screen.blit(text_box, (600, 200))
                            pygame.display.flip()
                            time.sleep(3)

                                
                scroll = True
            if event.button == 4:
                player.zoom += zoom
               
            elif event.button == 5:
                player.zoom -= zoom


        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button in [1, 2]:
                scroll = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if menu_icon_notpressed.get_rect(topleft=(20, 20)).collidepoint(event.pos) or menu_icon_pressed.get_rect(topleft=(20, 20)).collidepoint(event.pos):
                menu.menu_open = not menu.menu_open
            if menu.menu_open:
                menu.handleMouseClick(event.pos, screen)
        elif event.type == pygame.MOUSEMOTION:
            if menu.menu_open and menu.dragging:
                menu.handleMouseDrag(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            menu.dragging = False

        if not menu.menu_open:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in [1, 2]:
                    if event.button == 1:
                        for plant in plants:
                            if plant.rect.collidepoint(pygame.mouse.get_pos()):
                                background = screen.copy()
                                while True:
                                    screen.blit(background, (0, 0))
                                    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(map.width // 2 - 450, 300, 900, 300))
                                    screen.blit(dialogue, (map.width // 2 - 450, 300))
                                    pygame.display.flip()
                    scroll = True
                if event.button == 4:
                    player.zoom += zoom
                elif event.button == 5:
                    player.zoom -= zoom
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button in [1, 2]:
                    scroll = False
            elif event.type == pygame.MOUSEMOTION:
                if scroll:
                    rel_x, rel_y = event.rel
                    player.x -= rel_x
                    player.y -= rel_y

    if not menu.menu_open:
        if player.x < 0:
            player.x = 0
        if player.x > player.width:
            player.x = player.width
        if player.y < 0:
            player.y = 0
        if player.y > player.height:
            player.y = player.height

        screen.fill((0, 91, 171))
        map.render()

        for plant in plants:
            if plant.rect.collidepoint(pygame.mouse.get_pos()):
                plant.multiplier = 1.1
            else:
                plant.multiplier = 1
            plant.render()

    if menu.menu_open:
        menu.loadAndPlayAudio()
    else:
        menu.stopAudio()

    menu_icon = menu_icon_pressed if menu.menu_open else menu_icon_notpressed
    menu.drawMenuIcon(screen, menu_icon)

    if menu.menu_open:
        screen_width, screen_height = screen.get_size()
        menu.drawMenu(screen, menu.menu_x, menu.loadMenuBackground(screen_width, screen_height), screen_width, screen_height)

    pygame.display.flip()
    clock.tick(30)



