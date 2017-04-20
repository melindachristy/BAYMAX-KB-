import sys, pygame, random, math

pygame.init()

size = width, height = 800, 600
black = 0, 0, 0

maxVelocity = 10
numFish = 20
fishes = []

numPredators = 2
predators = []

class Fish:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocityX = 0.01
        self.velocityY = 0.01

    def distance(self, fish):
        distX = self.x - fish.x
        distY = self.y - fish.y
        return math.sqrt(distX * distX + distY * distY)

    def moveCloser(self, fishes):
        if len(fishes) < 1: return

        avgX = 0
        avgY = 0
        for fish in fishes:
            if fish.x == self.x and fish.y == self.y:
                continue

            avgX += (self.x - fish.x)
            avgY += (self.y - fish.y)

        avgX /= len(fishes)
        avgY /= len(fishes)

        distance = math.sqrt((avgX * avgX) + (avgY * avgY)) * -1.0

        self.velocityX -= (avgX / 100)
        self.velocityY -= (avgY / 100)

    def moveWith(self, fishes):
        if len(fishes) < 1: return
        avgX = 0
        avgY = 0

        for fish in fishes:
            avgX += fish.velocityX
            avgY += fish.velocityY

        avgX /= len(fishes)
        avgY /= len(fishes)

        self.velocityX += (avgX / 40)
        self.velocityY += (avgY / 40)

    def moveAway(self, fishes, minDistance):
        if len(fishes) < 1: return

        distanceX = 0
        distanceY = 0
        numClose = 0

        for fish in fishes:
            distance = self.distance(fish)
            if  distance < minDistance:
                numClose += 1
                xdiff = (self.x - fish.x)
                ydiff = (self.y - fish.y)

                if xdiff >= 0: xdiff = math.sqrt(minDistance) - xdiff
                elif xdiff < 0: xdiff = -math.sqrt(minDistance) - xdiff

                if ydiff >= 0: ydiff = math.sqrt(minDistance) - ydiff
                elif ydiff < 0: ydiff = -math.sqrt(minDistance) - ydiff

                distanceX += xdiff
                distanceY += ydiff

        if numClose == 0:
            return

        self.velocityX -= distanceX / 5
        self.velocityY -= distanceY / 5

    def move(self):
        if abs(self.velocityX) > maxVelocity or abs(self.velocityY) > maxVelocity:
            scaleFactor = maxVelocity / max(abs(self.velocityX), abs(self.velocityY))
            self.velocityX *= scaleFactor
            self.velocityY *= scaleFactor

        self.x += self.velocityX
        self.y += self.velocityY

class Predator:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocityX = 0.01
        self.velocityY = 0.01

    def distancePredator(self, predator):
        distX = self.x - predator.x
        distY = self.y - predator.y
        return math.sqrt(distX * distX + distY * distY)

    def moveCloserPredator(self, predators):
        if len(predators) < 1: return

        avgX = 0
        avgY = 0
        for predator in predators:
            if predator.x == self.x and predator.y == self.y:
                continue

            avgX += (self.x - predator.x)
            avgY += (self.y - predator.y)

        avgX /= len(predators)
        avgY /= len(predators)

        distance = math.sqrt((avgX * avgX) + (avgY * avgY)) * -1.0

        self.velocityX -= (avgX / 100)
        self.velocityY -= (avgY / 100)

    def moveWithPredator(self, predators):
        if len(predators) < 1: return

        avgX = 0
        avgY = 0

        for predator in predators:
            avgX += predator.velocityX
            avgY += predator.velocityY

        avgX /= len(predators)
        avgY /= len(predators)

        self.velocityX += (avgX / 40)
        self.velocityY += (avgY / 40)

    def moveAwayPredator(self, predators, minDistance):
        if len(predators) < 1: return

        distanceX = 0
        distanceY = 0
        numClose = 0

        for predator in predators:
            distance = self.distancePredator(predator)
            if  distance < minDistance:
                numClose += 1
                xdiff = (self.x - predator.x)
                ydiff = (self.y - predator.y)

                if xdiff >= 0: xdiff = math.sqrt(minDistance) - xdiff
                elif xdiff < 0: xdiff = -math.sqrt(minDistance) - xdiff

                if ydiff >= 0: ydiff = math.sqrt(minDistance) - ydiff
                elif ydiff < 0: ydiff = -math.sqrt(minDistance) - ydiff

                distanceX += xdiff
                distanceY += ydiff

        if numClose == 0:
            return

        self.velocityX -= distanceX / 5
        self.velocityY -= distanceY / 5

    def movePredator(self):
        if abs(self.velocityX) > maxVelocity or abs(self.velocityY) > maxVelocity:
            scaleFactor = maxVelocity / max(abs(self.velocityX), abs(self.velocityY))
            self.velocityX *= scaleFactor
            self.velocityY *= scaleFactor

        self.x += self.velocityX
        self.y += self.velocityY

screen = pygame.display.set_mode(size)

fishh = pygame.image.load("iwak1.png")
fishrect = fishh.get_rect()

enemy = pygame.image.load("hiu1.png")
enemyrect = enemy.get_rect()

for i in range(numFish):
    fishes.append(Fish(random.randint(0, width), random.randint(0, height)))

for i in range(numPredators):
    predators.append(Predator(random.randint(0, width), random.randint(0, height)))

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

#Iwak supaya arisan
    for fish in fishes:
        closeFishes = []
        for otherFish in fishes:
            if otherFish == fish: continue
            distance = fish.distance(otherFish)
            if distance < 500:
                closeFishes.append(otherFish)
                fish.moveCloser(closeFishes)
                fish.moveWith(closeFishes)

        for predator in predators:
            distance = fish.distance(predator)
            if distance < 500:
                closeFishes.append(otherFish)

        fish.moveAway(closeFishes, 20)

        border = 25
        if fish.x < border and fish.velocityX < 0:
            fish.velocityX = -fish.velocityX * random.random()
        if fish.x > width - border and fish.velocityX > 0:
            fish.velocityX = -fish.velocityX * random.random()
        if fish.y < border and fish.velocityY < 0:
            fish.velocityY = -fish.velocityY * random.random()
        if fish.y > height - border and fish.velocityY > 0:
            fish.velocityY = -fish.velocityY * random.random()

        fish.move()

#predator nyedek iwak
    for predator in predators:
        closePredators = []
        for fish in fishes:
            distance = fish.distance(predator)
            if(distance < 100):
                closePredators.append(fish)

        predator.moveCloserPredator(closePredators)
        predator.moveWithPredator(closePredators)

        border = 25
        if predator.x < border and predator.velocityX < 0:
            predator.velocityX = -predator.velocityX * random.random()
        if predator.x > width - border and predator.velocityX > 0:
            predator.velocityX = -predator.velocityX * random.random()
        if predator.y < border and predator.velocityY < 0:
            predator.velocityY = -predator.velocityY * random.random()
        if predator.y > height - border and predator.velocityY > 0:
            predator.velocityY = -predator.velocityY * random.random()

        predator.movePredator()

    screen.fill(black)
    for fish in fishes:
        fishRect = pygame.Rect(fishrect)
        fishRect.x = fish.x
        fishRect.y = fish.y
        screen.blit(fishh, fishRect)
    for predator in predators:
        predatorRect = pygame.Rect(enemyrect)
        predatorRect.x = predator.x
        predatorRect.y = predator.y
        screen.blit(enemy, predatorRect)
    pygame.display.flip()
    pygame.time.delay(10)
