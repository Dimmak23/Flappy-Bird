import pygame
import os
from os import listdir
from pygame.constants import QUIT, K_ESCAPE, K_DOWN, K_UP, K_LEFT, K_RIGHT
import random


def create_objective(enemy: bool, color: tuple, size: dict,
                     moveRange: tuple) -> dict:

    surface = pygame.Surface((0, 0))
    surface.fill(color)

    initialPos = {"x": 0, "y": 0}
    scoreLabelRect = scoreLabel.get_bounding_rect()

    if enemy:
        surface = pygame.transform.scale(pygame.image.load(
            ENEMY_IMG_PATH).convert_alpha(), (size["width"], size["height"]))
        # Prevent interference enemy with score label
        # also prevent to enemy go outside game box
        initialPos["x"] = width
        initialPos["y"] = random.randint(
            scoreLabelRect.bottom, height - size["height"])
        deltas = {"x": random.randint(*moveRange), "y": 0}
    else:
        surface = pygame.transform.scale(pygame.image.load(
            BONUS_IMG_PATH).convert_alpha(), (size["width"], size["height"]))
        # Prevent interference bonus with score label
        # also prevent to bonus go outside game box
        initialPos["x"] = random.randint(
            0, width - size["width"] - scoreLabelRect.width)
        initialPos["y"] = 0
        deltas = {"x": 0, "y": random.randint(*moveRange)}

    rectangle = pygame.Rect(tuple(initialPos.values()), tuple(size.values()))

    # Let's return dictionary, because we can see what kind of object there by keys
    return {"surface": surface, "rectangle": rectangle, "deltas": deltas}


if __name__ == "__main__":

    #  Clean this pygame message
    os.system("CLS")

    # Initialize pygame
    pygame.init()

    # Screen properties
    screen = width, height = 800, 600

    # Frame rate
    FPS = pygame.time.Clock()

    # Colors
    BLACK = (0, 0, 0)

    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    ORANGE = (255, 165, 0)
    YELLOW = (255, 255, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    SLATEBLUE = (106, 90, 205)
    ROSYBROWN = (188, 143, 143)

    RANDOM_COLORS = [
        WHITE, RED, ORANGE, YELLOW, GREEN, BLUE, SLATEBLUE, ROSYBROWN
    ]

    # Main Window
    mainWindow = pygame.display.set_mode(screen)

    # Score label
    font = pygame.font.SysFont('Gelvetica', 20)
    scorePos = {"x": width - 120, "y": 10}

    # Background sprite
    BACKGROUND_IMG_PATH = '../assets/background.png'
    background = pygame.transform.scale(
        pygame.image.load(BACKGROUND_IMG_PATH).convert(), screen)
    # Initial coordinate
    backgroundPos = {"startX": 0, "endX": background.get_width()}
    backgroundDelta: int = 3

    # PLAYER UTILITY
    score: int = 0
    # Player texture
    # Size:
    playerSize = (120, 60)
    # optimize image convertion
    #! TODO: study methods convert() and convert_alpha()
    PLAYER_IMG_PATH = '../assets/bandera_goose'
    playerImages = [pygame.transform.scale(
        pygame.image.load(PLAYER_IMG_PATH+'/'+file).convert_alpha(), playerSize)
        for file in listdir(PLAYER_IMG_PATH)]
    playerIndex = 0
    player = playerImages[playerIndex]
    # Player geometry
    playerRectangle = player.get_rect()
    playerRectangle = playerRectangle.move(
        (width/2-playerRectangle.width/2, height/2-playerRectangle.height/2))
    playerDeltaPos = {"x": 5, "y": 5}
    # Player event for image updating
    UPDATE_PLAYER = pygame.USEREVENT + 3
    pygame.time.set_timer(UPDATE_PLAYER, 60)

    # ENEMY
    CREATE_ENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(CREATE_ENEMY, 1500)
    enemies = []
    ENEMY_IMG_PATH = '../assets/enemy.png'
    enemiesSizes = {"width": 100, "height": 40}
    enemyMoveRange = (2, 5)

    # BONUS
    CREATE_BONUS = pygame.USEREVENT + 2
    pygame.time.set_timer(CREATE_BONUS, 2500)
    bonuses = []
    BONUS_IMG_PATH = '../assets/bonus.png'
    bonusesSizes = {"width": 45, "height": 90}
    bonusMoveRange = (4, 7)

    # Game cycle
    running = True
    while running:

        # Frame per second settings
        FPS.tick(60)

        # Event handling
        for event in pygame.event.get():
            # Quit game if 'Esc' button pressed
            if event.type == QUIT:
                running = False
            # Create new enemy if it's time
            if event.type == CREATE_ENEMY:
                enemies.append(
                    create_objective(enemy=True, color=RED, size=enemiesSizes, moveRange=enemyMoveRange))
            # Create new bonus if it's time
            if event.type == CREATE_BONUS:
                bonuses.append(
                    create_objective(enemy=False, color=GREEN, size=bonusesSizes, moveRange=bonusMoveRange))
            # Update player if it's time
            if event.type == UPDATE_PLAYER:
                if playerIndex == len(playerImages) - 1:
                    playerIndex = 0
                else:
                    playerIndex += 1
                player = playerImages[playerIndex]

        # RENDERING

        # Redraw to main window background
        # NOTE: Here we fix lectors mistakes
        # "startX" point goes from '0' to -background.get_width()
        if backgroundPos["startX"] < -background.get_width():
            # and returns to '0', like was init before game cycle
            backgroundPos["startX"] = 0
        # "endX" point goes from 'background.get_width()' to 0
        if backgroundPos["endX"] < 0:
            # and returns to 'background.get_width()', like was init before game cycle
            backgroundPos["endX"] = background.get_width()
        # Update two background positions
        backgroundPos["startX"] -= backgroundDelta
        backgroundPos["endX"] -= backgroundDelta
        # Blit two backgrounds
        mainWindow.blit(background, (backgroundPos["startX"], 0))
        mainWindow.blit(background, (backgroundPos["endX"], 0))

        # Redraw player on top of the main window
        mainWindow.blit(player, playerRectangle)

        # Render score label
        scoreLabel = font.render(f"Player score: {score}", True, RED)
        mainWindow.blit(scoreLabel, (scorePos["x"], scorePos["y"]))

        # Redraw enemy on top of the previous
        for enemy in enemies:
            mainWindow.blit(enemy["surface"], enemy["rectangle"])

        # Redraw bouneses on top of the previous
        for bonus in bonuses:
            mainWindow.blit(bonus["surface"], bonus["rectangle"])

        # User controls
        pressedKeys = pygame.key.get_pressed()
        if pressedKeys[K_DOWN] and playerRectangle.bottom < height:
            playerRectangle = playerRectangle.move([0, playerDeltaPos["y"]])
        if pressedKeys[K_UP] and playerRectangle.top > 0:
            playerRectangle = playerRectangle.move([0, -playerDeltaPos["y"]])
        if pressedKeys[K_LEFT] and playerRectangle.left > 0:
            playerRectangle = playerRectangle.move([-playerDeltaPos["x"], 0])
        if pressedKeys[K_RIGHT] and playerRectangle.right < width:
            playerRectangle = playerRectangle.move([playerDeltaPos["x"], 0])

        # Manipulate enemies
        for enemy in enemies:

            # Move enemies
            enemy["rectangle"] = enemy["rectangle"].move(
                [-enemy["deltas"]["x"], enemy["deltas"]["y"]])

            # Delete enemies
            # NOTE: we assume that enemy should be deleted when it's RIGHT side
            # 		go outside the game field, so it's full body go outside
            if enemy["rectangle"].right < 0:
                enemies.pop(enemies.index(enemy))

            # Quit game when hit the enemy
            if playerRectangle.colliderect(enemy["rectangle"]):
                running = False

        # Manipulate bonuses
        for bonus in bonuses:

            # Move bonuses
            bonus["rectangle"] = bonus["rectangle"].move(
                [-bonus["deltas"]["x"], bonus["deltas"]["y"]])

            # Delete bonuses
            # NOTE: we assume that bonus should be deleted when it's TOP side
            # 		go outside the game field, so it's FULL BODY go outside
            if bonus["rectangle"].top > height:
                bonuses.pop(bonuses.index(bonus))

            # Delete bonus if enemy hits it
            for enemy in enemies:
                if bonus["rectangle"].colliderect(enemy["rectangle"]):
                    bonuses.pop(bonuses.index(bonus))

            # Increment score by one when catch bonus
            if playerRectangle.colliderect(bonus["rectangle"]):
                score += 1
                # Also delete this bonus
                bonuses.pop(bonuses.index(bonus))

        # Show every drawing to screen
        pygame.display.flip()

        # Allow to exit by 'Escape' shortcut
        if pressedKeys[K_ESCAPE]:
            running = False
