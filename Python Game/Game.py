# This game has a main character, scenery, and enemies. The main character is a cowboy who is trying to defend his home.
# You can move this character up with "w", down with "s", left with "a", and right with "d". You can shoot with
# this character by using your left click on your mouse. The fire rate of your weapon will increase based on the
# distance between the cowboy and the right of the screen, and it will also be based on how many fruits(pineapple) that
# you pick up. The fruits spawn in random locations. While playing, you must consider the fact that when you move closer
# to the enemies, your bullets shoot faster. Essentially, you will be risking your health for extra fire rate.
# Additionally, enemies will come in constant intervals towards you and your house. These enemies will damage you. If
# you take 2 hits from an enemy, you will lose the game. If the enemy reaches your house, you will also lose the game.
# The enemies will gradually receive more health as the game progresses. This means that they will require more bullets
# to kill. There are cacti in the scenery, however, all they do are block the player's ability to move. The main goal
# of this game is for you to keep yourself alive and your house guarded for as long as possible.

# As for the project requirements, I'll be listing them out in this section. For the first basic feature, my game
# implements user inputs like "w", "a", "s", and "d" to walk and "mouseclick" to shoot. For the second basic feature,
# There is a way to lose the game and receive a "Game Over" screen. To get this, you must either take hits from an
# enemy, or allow the enemy to reach your house. The third basic feature is shown through the various png's and graphics
# inside the game itself. Next, I'll be listing the additional features that I have added into the game. The first
# additional feature included in this game is object-oriented code. If you scroll through the code for this game, you
# will be able to see that there are six classes that construct this game. Two of these classes have multiple instances
# (Health and Enemy). The second additional feature that is in the code is a "Restart from Game Over" option. If the
# user clicks the space bar, the game will restart with all its base settings and original positions. A third additional
# feature of this game are enemies. As stated earlier, the enemies have their own class, can damage you, and can raid
# your home. A fourth additional feature are collectibles, which come in the form of fruits that you can pick up.
# These fruit power up you fire rate. The fifth additional feature is the timer. The timer can be seen in the top-left
# corner. The sixth and last additional feature is the health bars on both the cowboy and the enemies. These go down
# based on how much remaining health a unit has.

# The changes I made from CP2 are that I made the concept of the game a little different. I made it so that, instead of
# barriers that increase the amount of damage you do, you have fruits/collectables that increase the fire rate of your
# weapon. Additionally, I made it so that enemies walk towards you rather than you walking towards them.

import os
import random

import uvage

ASSET_DIR = os.path.dirname(os.path.abspath(__file__))

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

BASE_BULLET_SPEED = 15
MAX_BULLET_SPEED = 60
PINEAPPLE_BOOST = 3
FRUIT_INTERVAL = 360  # ticks between pineapple spawns
HIT_FRAMES = 30       # frames of contact that make up one hit
MAX_HITS = 2
HOUSE_X = 50          # an enemy past this x has reached the house
# (ticks survived, bullets to kill), checked from the toughest step down.
ENEMY_HP_STEPS = ((6000, 10), (5000, 8), (4000, 6), (3000, 4), (2000, 2), (0, 1))

camera = uvage.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)


def asset(name):
    return os.path.join(ASSET_DIR, name)


def enemy_hp(ticks):
    for threshold, hp in ENEMY_HP_STEPS:
        if ticks > threshold:
            return hp
    return 1


# TimerAll counts ticks and draws the clock
class TimerAll:

    def __init__(self):
        self.ticks = 0

    @property
    def seconds(self):
        return self.ticks // FPS

    def tick(self):
        self.ticks += 1

    def reset(self):
        self.ticks = 0

    def draw(self):
        camera.draw("Time: " + str(self.seconds), 36, "black", 60, 30)


# Fruit is the pineapple collectible
class Fruit:

    def __init__(self):
        self.pineapple = uvage.from_image(0, 0, asset("pineapple.png"))
        self.active = False

    def spawn(self):
        self.pineapple.x = random.randint(200, 400)
        self.pineapple.y = random.randint(200, 400)
        self.active = True

    def collect_if_touched(self, cowboy):
        if self.active and cowboy.cowman.touches(self.pineapple):
            self.active = False
            return True
        return False

    def draw(self):
        if self.active:
            camera.draw(self.pineapple)


class Cowboy:

    START = (125, 500)

    def __init__(self):
        self.cowman = uvage.from_image(*self.START, asset("cowboy_50x50.png"))
        self.speed = 5
        self.contact_frames = 0

    @property
    def hits(self):
        return self.contact_frames // HIT_FRAMES

    @property
    def dead(self):
        return self.hits >= MAX_HITS

    def reset(self):
        self.cowman.x, self.cowman.y = self.START
        self.contact_frames = 0

    def take_contact(self, enemies):
        for enemy in enemies:
            if self.cowman.touches(enemy.badguy):
                self.contact_frames += 1

    def move(self):
        if uvage.is_pressing("w") and self.cowman.y > 50:
            self.cowman.y -= self.speed
        if uvage.is_pressing("s") and self.cowman.y < 550:
            self.cowman.y += self.speed
        if uvage.is_pressing("a") and self.cowman.x > 50:
            self.cowman.x -= self.speed
        if uvage.is_pressing("d") and self.cowman.x < 750:
            self.cowman.x += self.speed

    def draw(self):
        camera.draw(self.cowman)


# Bullet is a single shot; it flies until it leaves the screen or hits an enemy
class Bullet:

    def __init__(self):
        self.bullet_image = uvage.from_color(-100, -100, "black", 9, 3)
        self.flying = False
        self.speed = BASE_BULLET_SPEED

    def fire(self, cowboy, speed):
        if not self.flying:
            self.bullet_image.x = cowboy.cowman.x + 5
            self.bullet_image.y = cowboy.cowman.y
            self.speed = speed
            self.flying = True

    def update(self, enemies):
        if not self.flying:
            return
        self.bullet_image.x += self.speed
        if self.bullet_image.x > SCREEN_WIDTH:
            self.flying = False
            return
        for enemy in enemies:
            if self.bullet_image.touches(enemy.badguy):
                enemy.hp -= 1
                self.flying = False
                return

    def draw(self):
        if self.flying:
            camera.draw(self.bullet_image)


# Enemy walks toward the house; each instance has its own health
class Enemy:

    def __init__(self):
        self.badguy = uvage.from_image(900, 0, asset("enemy.png"))
        self.speed = 1
        self.hp = 1
        self.max_hp = 1
        self.respawn(0)

    def respawn(self, ticks):
        self.badguy.x = 900
        self.badguy.y = random.randint(55, 545)
        self.max_hp = self.hp = enemy_hp(ticks)

    def update(self, ticks):
        if self.hp <= 0:
            self.respawn(ticks)
        self.badguy.x -= self.speed

    @property
    def reached_house(self):
        return self.badguy.x < HOUSE_X

    def draw(self):
        camera.draw(self.badguy)


# Health draws a health bar under a unit
class Health:

    def __init__(self):
        self.full_health_bar = uvage.from_image(0, 0, asset("full_health_bar.png"))
        self.half_health_bar = uvage.from_image(0, 0, asset("half_health_bar.png"))
        self.dead = uvage.from_image(0, 0, asset("dead.png"))

    def draw(self, x, y, fraction, dead=False):
        bar = self.dead if dead else (
            self.full_health_bar if fraction > 0.5 else self.half_health_bar)
        bar.x = x
        bar.y = y + 35
        camera.draw(bar)


scenery = [uvage.from_image(700, 400, asset("cactus.png")),
           uvage.from_image(400, 124, asset("cactus.png"))]
house = uvage.from_image(70, 300, asset("House.png"))

timer = TimerAll()
cowboy = Cowboy()
fruit = Fruit()
bullet = Bullet()
enemies = [Enemy(), Enemy()]
enemy_bars = [Health(), Health()]
cowboy_bar = Health()

running = True
bullet_speed = BASE_BULLET_SPEED


def reset():
    global running, bullet_speed
    timer.reset()
    cowboy.reset()
    fruit.active = False
    bullet.flying = False
    for enemy in enemies:
        enemy.respawn(0)
    bullet_speed = BASE_BULLET_SPEED
    running = True


def update():
    global running, bullet_speed
    timer.tick()
    for blocker in scenery + [house]:
        cowboy.cowman.move_to_stop_overlapping(blocker)
    cowboy.move()
    if camera.mouseclick:
        bullet.fire(cowboy, bullet_speed)

    if not fruit.active and timer.ticks % FRUIT_INTERVAL == 0:
        fruit.spawn()
    if fruit.collect_if_touched(cowboy):
        bullet_speed = min(bullet_speed + PINEAPPLE_BOOST, MAX_BULLET_SPEED)

    for enemy in enemies:
        enemy.update(timer.ticks)
    bullet.update(enemies)
    cowboy.take_contact(enemies)

    if cowboy.dead or any(enemy.reached_house for enemy in enemies):
        running = False


def draw():
    camera.clear("#EFDD6F")
    for item in scenery:
        camera.draw(item)
    fruit.draw()
    for enemy, bar in zip(enemies, enemy_bars):
        enemy.draw()
        bar.draw(enemy.badguy.x, enemy.badguy.y, enemy.hp / enemy.max_hp)
    cowboy.draw()
    cowboy_bar.draw(cowboy.cowman.x, cowboy.cowman.y,
                    1 - cowboy.contact_frames / (MAX_HITS * HIT_FRAMES), dead=cowboy.dead)
    bullet.draw()
    camera.draw(house)
    timer.draw()
    if not running:
        camera.draw(uvage.from_text(400, 300, "GAME OVER", 50, "red", bold=True))
        camera.draw(uvage.from_text(400, 400, "Click 'space' to restart the game", 30, "red"))
    camera.display()


def tick():
    if running:
        update()
    elif uvage.is_pressing("space"):
        reset()
    draw()


if __name__ == "__main__":
    uvage.timer_loop(FPS, tick)
