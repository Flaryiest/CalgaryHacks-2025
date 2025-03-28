from src import *
import pygame, logging, random, time, json
import pygame.freetype
from pygame import mixer 

logging.basicConfig(level=logging.DEBUG)

settings = Settings()

if settings.settings["fullscreen"]:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen_width, screen_height = screen.get_size()
else:
    screen_width = settings.settings["width"]
    screen_height = settings.settings["height"]
    screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Save the Animals!!!")

player = Player(screen)
player.zoom = 1.4
map = Map(screen, player)
zoom = 0.1
run = True
scroll = False

plants = []
for biome in map.biomes:

    coordinates = random.choice(map.biomes[biome])
    if biome == "ocean":
        plants.append(
            Plant(
                player,
                screen,
                coordinates[0] * 1.6,
                coordinates[1] * 1.6,
                dir="assets\\pump.png",
                scale=4,
                biome=biome,
            )
        )
    else:
        print(biome)
        plants.append(
            Plant(
                player,
                screen,
                coordinates[0] * 1.6,
                coordinates[1] * 1.6,
                biome=biome,
            )
        )

        

hover = {"status": False, "obj": None}
dialogue = pygame.image.load("assets\\dialogue.png")
dialogue = pygame.transform.scale(dialogue, (1500, 1000))
pygame.font.init()
font = pygame.font.Font('assets\\Fonts\\TepidTerminalFont_v231106\\TepidTerminal.ttf', 32)
overlay = pygame.Surface((1920, 1080), pygame.SRCALPHA)  # Enable per-pixel alpha
overlay.fill((0, 0, 0, 128))
button = pygame.image.load("assets\\button.png")
button = pygame.transform.scale(button, (800, 200))

mixer.init() 
mixer.music.load("audio\\music.mp3") 
mixer.music.set_volume(0.5) 
  
mixer.music.play(-1) 

def fade_in(asset="assets/Coverpage.jpg", asset2="assets/Cover Text (1).png"):
    alpha = 0
    fade_surface = pygame.image.load(asset).convert()
    fade_surface = pygame.transform.scale(fade_surface, (screen_width, screen_height))
    fade_surface = pygame.image.load(asset2).convert()
    fade_surface = pygame.transform.scale(fade_surface, (screen_width, screen_height))
    fade_surface.set_alpha(alpha)

    while alpha < 255:
        screen.fill((0, 0, 0))
        alpha += 5
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(50)
        if alpha >= 255:
            break


fade_in()
start_button = pygame.Rect(1920 // 2 - 300, 600, button.get_width(), button.get_height())  # Button 1
start_button_text = font.render("START SAVING ANIMALS!!!", True, (0, 0, 0))
start = True
while start:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in [1, 2]:
                if event.button == 1:
                    if start_button.collidepoint(pygame.mouse.get_pos()):
                        start = False

    screen.blit(button, start_button.topleft)                          
    screen.blit(start_button_text, (start_button.x + 150, start_button.y + 75))
    
    pygame.display.flip()


for i in range(0, 9):
    back = pygame.image.load(f"assets\\{i}.png")
    back = pygame.transform.scale(back, (1920, 1080))
    t = time.time()
    while time.time() - t < 3:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                run = False
        screen.blit(back, (0, 0))
        pygame.display.update()


button_rect1 = pygame.Rect(100, 600, button.get_width(), button.get_height())  # Button 1
button_rect2 = pygame.Rect(100, 800, button.get_width(), button.get_height())  # Button 2
button_rect3 = pygame.Rect(850, 600, button.get_width(), button.get_height())  # Button 3
button_rect4 = pygame.Rect(850, 800, button.get_width(), button.get_height())  # Button 4


with open("questions.json", "r") as f:
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

                            text_box = font.render(
                                text, False, (0, 0, 0), wraplength=900
                            )
                            screen.blit(text_box, (600, 200))
                            screen.blit(img, (1200, 400))

                            pygame.display.flip()

                            time.sleep(5)
                            correct = 0
                            for i in range(0, 3):
                                question = random.choice(questions)
                                button1_text = font.render(
                                    question["answers"][0], True, (0, 0, 0)
                                )  # Black text
                                button2_text = font.render(
                                    question["answers"][1], True, (0, 0, 0)
                                )  # Black text
                                button3_text = font.render(
                                    question["answers"][2], True, (0, 0, 0)
                                )  # Black text
                                button4_text = font.render(
                                    question["answers"][3], True, (0, 0, 0)
                                )  # Black text

                                correct_answer = question["correct_answer"]
                                question_loop = True
                                while question_loop:
                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            run = False

                                        elif event.type == pygame.MOUSEBUTTONDOWN:
                                            if event.button == 1:
                                                if button_rect1.collidepoint(event.pos):
                                                    if (
                                                        question["answers"][0]
                                                        == correct_answer
                                                    ):
                                                        text = f"Correct! {question['explanation']}"
                                                        correct += 1
                                                    else:
                                                        text = f"Incorrect! {question['explanation']}"
                                                elif button_rect2.collidepoint(
                                                    event.pos
                                                ):
                                                    if (
                                                        question["answers"][1]
                                                        == correct_answer
                                                    ):
                                                        text = f"Correct! {question['explanation']}"
                                                        correct += 1
                                                    else:
                                                        text = f"Incorrect! {question['explanation']}"
                                                elif button_rect3.collidepoint(
                                                    event.pos
                                                ):
                                                    if (
                                                        question["answers"][2]
                                                        == correct_answer
                                                    ):
                                                        text = f"Correct! {question['explanation']}"
                                                        correct += 1
                                                    else:
                                                        text = f"Incorrect! {question['explanation']}"
                                                elif button_rect4.collidepoint(
                                                    event.pos
                                                ):
                                                    if (
                                                        question["answers"][3]
                                                        == correct_answer
                                                    ):
                                                        text = f"Correct! {question['explanation']}"
                                                        correct += 1
                                                    else:
                                                        text = f"Incorrect! {question['explanation']}"

                                                screen.blit(background, (0, 0))
                                                screen.blit(overlay, (0, 0))
                                                screen.blit(
                                                    dialogue,
                                                    (map.width // 2 - 600, -150),
                                                )
                                                screen.blit(img, (1200, 400))
                                                text_box = font.render(
                                                    text,
                                                    False,
                                                    (0, 0, 0),
                                                    wraplength=900,
                                                )
                                                screen.blit(text_box, (600, 200))
                                                pygame.display.flip()
                                                time.sleep(5)
                                                question_loop = False

                                    if question_loop:
                                        screen.blit(background, (0, 0))
                                        screen.blit(overlay, (0, 0))
                                        screen.blit(
                                            dialogue, (map.width // 2 - 600, -150)
                                        )

                                        text_box = font.render(
                                            question["question"],
                                            False,
                                            (0, 0, 0),
                                            wraplength=900,
                                        )
                                        screen.blit(text_box, (600, 200))

                                        screen.blit(
                                            button, button_rect1.topleft
                                        )  # Button 1

                                        screen.blit(
                                            button, button_rect2.topleft
                                        )  # Button 2
                                        screen.blit(
                                            button, button_rect3.topleft
                                        )  # Button 3
                                        screen.blit(
                                            button, button_rect4.topleft
                                        )  # Button 4

                                        # Draw text on top of the buttons
                                        screen.blit(
                                            button1_text,
                                            (button_rect1.x + 50, button_rect1.y + 75),
                                        )  # Adjust position as needed
                                        screen.blit(
                                            button2_text,
                                            (button_rect2.x + 50, button_rect2.y + 75),
                                        )  # Adjust position as needed
                                        screen.blit(
                                            button3_text,
                                            (button_rect3.x + 50, button_rect3.y + 75),
                                        )  # Adjust position as needed
                                        screen.blit(
                                            button4_text,
                                            (button_rect4.x + 50, button_rect4.y + 75),
                                        )  # Adjust position as needed

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
                            text_box = font.render(
                                text, False, (0, 0, 0), wraplength=900
                            )
                            screen.blit(text_box, (600, 200))
                            pygame.display.flip()
                            time.sleep(5)

                scroll = True
            if event.button == 4:
                if player.zoom < 2:
                    player.zoom += zoom
               
            elif event.button == 5:
                if player.zoom > 1.4:
                    player.zoom -= zoom
        

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button in [1, 2]:
                scroll = False

        elif event.type == pygame.MOUSEMOTION:
            if scroll:
                rel_x, rel_y = event.rel

                player.x -= rel_x
                player.y -= rel_y

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

    if len(plants) == 0:
        fade_in("assets\\sucess.png")
        time.sleep(5)
        run = False
    
    print(player.zoom)
    pygame.display.flip()
