from src import *
import pygame, logging, random, time, json

logging.basicConfig(level=logging.DEBUG)

settings = Settings()

if settings.settings["fullscreen"] == True:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((settings.settings["width"], settings.settings["height"]))

pygame.display.set_caption("Save the Animals!!!") 

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
                            
                            text_box = font.render(text, False, (0, 0, 0), wraplength=900)
                            screen.blit(text_box, (600, 200))
                            screen.blit(img, (1200, 400))

                            pygame.display.flip()

                            time.sleep(5)

                            while True:

                                for event in pygame.event.get(): 
                                    if event.type == pygame.QUIT:
                                        run = False

                                
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

    pygame.display.flip()



