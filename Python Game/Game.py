# Jason Park hbv6np

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

# Import necessary modules
import uvage
import random

# Define screen dimensions and initialize camera
screen_height = 600
screen_width = 800
camera = uvage.Camera(screen_width, screen_height)

# Time variables
time = 0
second_time = 0
third_time = 0

# Constant variables
b = 15  # Bullet base speed value
time_kill = 1  # Base number of bullets it takes to kill
time_kill2 = 1  # Base number of bullets it takes to kill for second enemy
x = 0  # Number of times cowboy has been hit by enemy

# Scenery setup
scenery = [uvage.from_image(700, 400, "cactus.png"),
           uvage.from_image(400, 124, "cactus.png")]
house = uvage.from_image(70, 300, "House.png")

# Game flags and status variables
GameTrue = True
enemy_killed = False
enemy_killed2 = False
bullet_shooting = False


# TimerAll class handles game timing
class TimerAll:

    def __init__(self):
        global GameTrue
        self.second = uvage.from_color(1000, 600, "red", 5, 5)
        self.second1 = uvage.from_color(1000, 600, "red", 5, 5)
        self.second2 = uvage.from_color(1000, 600, "red", 5, 5)

    def time_move(self):
        global time
        global second_time
        global third_time
        if GameTrue:
            if self.second.y <= 600:
                self.second.y -= 12
                if self.second.y <= 0:
                    time += 1
                    self.second.y = 600
            if self.second1.y <= 600:
                self.second1.y -= 100
                if self.second1.y <= 0:
                    second_time += 1
                    self.second1.y = 600
            if self.second2.y <= 600:
                self.second2.y -= 6000
                if self.second2.y <= 0:
                    third_time += 1
                    self.second2.y = 600
        camera.draw("Time: " + str(int(time)), 36, "black", 60, 30)


# Fruit class represents collectible items
class Fruit:

    def __init__(self, x, y):
        x = random.randint(55, (screen_width - 55))
        y = random.randint(55, (screen_height - 55))

        self.pineapple = uvage.from_image(x, y, "pineapple.png")
        self.active = False

    def activate(self, x, y):
        self.pineapple.x = x
        self.pineapple.y = y
        self.active = True

    def existing(self):
        global b
        if cowboy.cowman.touches(self.pineapple):
            if b < 60:
                b += 3
            self.active = False
            fruits.clear()


# Cowboy class manages the main character's actions
class Cowboy:

    def __init__(self, x, y):
        self.cowman = uvage.from_image(x, y, "cowboy_50x50.png")
        self.speed = 5
        self.is_walking = False

    def cowboy_die(self):
        global x
        if self.cowman.touches(enemy1.badguy):
            x += 1
        if self.cowman.touches(enemy2.badguy):
            x += 1

    def move_up(self):
        global GameTrue
        if self.cowman.y > 50:
            self.cowman.y -= self.speed
            self.is_walking = True
        elif self.cowman.y <= 50 or not GameTrue:
            self.cowman.speedy = 0
            self.is_walking = False

    def move_right(self):
        global GameTrue
        if self.cowman.x < 750:
            self.cowman.x += self.speed
            self.is_walking = True
        elif self.cowman.y >= 750 or not GameTrue:
            self.cowman.speedx = 0
            self.is_walking = False

    def move_left(self):
        global GameTrue
        if self.cowman.x > 50:
            self.cowman.x -= self.speed
            self.is_walking = True
        elif self.cowman.x <= 50 or not GameTrue:
            self.cowman.speedx = 0
            self.is_walking = False

    def move_down(self):
        global GameTrue
        if self.cowman.y < 550:
            self.cowman.y += self.speed
            self.is_walking = True

    def touch(self):
        fruit = Fruit(random.randint(200, 400), random.randint(200, 400))
        return fruit


# Bullet class controls the behavior of bullets
class Bullet:
    global b

    def __init__(self, x, y):
        self.bullet_image = uvage.from_color(x, y, "black", 9, 3)
        self.speed = b

    def move(self):
        global bullet_shooting
        if not bullet_shooting:
            self.bullet_image.x = cowboy.cowman.x + 100000
            self.bullet_image.y = cowboy.cowman.y
        if bullet_shooting:
            camera.draw(self.bullet_image)
            self.bullet_image.x += self.speed
            self.bullet_image.y += 0
            if self.bullet_image.x > 800:
                self.bullet_image.x = cowboy.cowman.x + 5
                self.bullet_image.y = cowboy.cowman.y
                bullet_shooting = False

    def bulletkills(self):
        global enemy_killed
        global time
        global time_kill
        if self.bullet_image.right_touches(enemy1.badguy, 5, 5):
            time_kill -= 1
        if time_kill == 0:
            enemy_killed = True

    def bulletkills2(self):
        global enemy_killed2
        global time
        global time_kill2
        if self.bullet_image.right_touches(enemy2.badguy, 5, 5):
            time_kill2 -= 1
        if time_kill2 == 0:
            enemy_killed2 = True


# Enemy class defines enemy behavior
class Enemy:

    def __init__(self):
        self.badguy = uvage.from_image(900, random.randint(55, 545), "enemy.png")
        self.speed = 1

    def move(self):
        global GameTrue
        global enemy_killed
        global time_kill
        if GameTrue:
            if enemy_killed:
                self.badguy.x = 900
                self.badguy.y = (random.randint(55, 545))
                if self.badguy.x == 900:
                    enemy_killed = False
                    if third_time > 0:
                        time_kill = 1
                        if third_time > 2000:
                            time_kill = 2
                            if third_time > 3000:
                                time_kill = 4
                                if third_time > 4000:
                                    time_kill = 6
                                    if third_time > 5000:
                                        time_kill = 8
                                        if third_time > 6000:
                                            time_kill = 10
            self.badguy.x -= self.speed
            if self.badguy.x < 50:
                GameTrue = False

    def move2(self):
        global GameTrue
        global enemy_killed2
        global time_kill2
        if GameTrue:
            if enemy_killed2:
                self.badguy.x = 900
                self.badguy.y = (random.randint(55, 545))
                if self.badguy.x == 900:
                    enemy_killed2 = False
                    if third_time > 0:
                        time_kill2 = 1
                        if third_time > 2000:
                            time_kill2 = 2
                            if third_time > 3000:
                                time_kill2 = 4
                                if third_time > 4000:
                                    time_kill2 = 6
                                    if third_time > 5000:
                                        time_kill2 = 8
                                        if third_time > 6000:
                                            time_kill2 = 10
            self.badguy.x -= self.speed
            if self.badguy.x < 50:
                GameTrue = False


# Health class manages health-related and health bar functionalities
class Health:

    def __init__(self, x, y):
        self.full_health_bar = uvage.from_image(x, y, "full_health_bar.png")
        self.half_health_bar = uvage.from_image(x, y, "half_health_bar.png")
        self.dead = uvage.from_image(x, y, "dead.png")
        self.full_health_on = False
        self.half_health_on = False

    def cowboy_health(self):
        global GameTrue
        global x
        if 30 > x >= 0:
            self.full_health_bar.x = cowboy.cowman.x
            self.full_health_bar.y = cowboy.cowman.y + 35

        if 60 > x >= 30:
            self.full_health_bar.x = 1000
            self.full_health_bar.y = 1000
            self.half_health_bar.x = cowboy.cowman.x
            self.half_health_bar.y = cowboy.cowman.y + 35

        if x >= 60:
            self.half_health_bar.x = 1000
            self.half_health_bar.y = 1000
            self.dead.x = cowboy.cowman.x
            self.dead.y = cowboy.cowman.y + 35
            GameTrue = False

    def moving_healthbars(self):
        if self.full_health_on:
            self.full_health_bar.x = enemy1.badguy.x
            self.full_health_bar.y = enemy1.badguy.y + 35
        if not self.full_health_on:
            self.full_health_bar.x = 10000
            self.full_health_bar.y = 10000
        if self.half_health_on:
            self.half_health_bar.x = enemy1.badguy.x
            self.half_health_bar.y = enemy1.badguy.y + 35
        if not self.half_health_on:
            self.half_health_bar.x = 10000
            self.half_health_bar.y = 10000

    def moving_healthbars2(self):
        if self.full_health_on:
            self.full_health_bar.x = enemy2.badguy.x
            self.full_health_bar.y = enemy2.badguy.y + 35
        if not self.full_health_on:
            self.full_health_bar.x = 10000
            self.full_health_bar.y = 10000
        if self.half_health_on:
            self.half_health_bar.x = enemy2.badguy.x
            self.half_health_bar.y = enemy2.badguy.y + 35
        if not self.half_health_on:
            self.half_health_bar.x = 10000
            self.half_health_bar.y = 10000

    def health_changing_enemy_1(self):

        global third_time
        global time_kill

        if 2000 > third_time > 0:
            if time_kill == 1:
                self.full_health_on = True
                self.half_health_on = False
        elif 3000 > third_time > 2000:
            if time_kill == 2:
                self.full_health_on = True
                self.half_health_on = False
            elif time_kill == 1:
                self.full_health_on = False
                self.half_health_on = True
        elif 4000 > third_time > 3000:
            if time_kill == 4:
                self.full_health_on = True
                self.half_health_on = False
            elif time_kill == 2:
                self.full_health_on = False
                self.half_health_on = True
        elif 5000 > third_time > 4000:
            if time_kill == 6:
                self.full_health_on = True
                self.half_health_on = False
            elif time_kill == 3:
                self.full_health_on = False
                self.half_health_on = True
        elif 6000 > third_time > 5000:
            if time_kill == 8:
                self.full_health_on = True
                self.half_health_on = False
            elif time_kill == 4:
                self.full_health_on = False
                self.half_health_on = True
        elif third_time > 6000:
            if time_kill == 10:
                self.full_health_on = True
                self.half_health_on = False
            elif time_kill == 5:
                self.full_health_on = False
                self.half_health_on = True

    def health_changing_enemy_2(self):

        global third_time
        global time_kill2

        if 2000 > third_time > 0:
            if time_kill2 == 1:
                self.full_health_on = True
                self.half_health_on = False
        elif 3000 > third_time > 2000:
            if time_kill2 == 2:
                self.full_health_on = True
                self.half_health_on = False
            elif time_kill2 == 1:
                self.full_health_on = False
                self.half_health_on = True
        elif 4000 > third_time > 3000:
            if time_kill2 == 4:
                self.full_health_on = True
                self.half_health_on = False
            elif time_kill2 == 2:
                self.full_health_on = False
                self.half_health_on = True
        elif 5000 > third_time > 4000:
            if time_kill2 == 6:
                self.full_health_on = True
                self.half_health_on = False
            elif time_kill2 == 3:
                self.full_health_on = False
                self.half_health_on = True
        elif 6000 > third_time > 5000:
            if time_kill2 == 8:
                self.full_health_on = True
                self.half_health_on = False
            elif time_kill2 == 4:
                self.full_health_on = False
                self.half_health_on = True
        elif third_time > 6000:
            if time_kill2 == 10:
                self.full_health_on = True
                self.half_health_on = False
            elif time_kill2 == 5:
                self.full_health_on = False
                self.half_health_on = True


# Initialize game elements and objects
cowboy = Cowboy(125, 500)
fruits = []
bullets = Bullet((cowboy.cowman.x + 2), cowboy.cowman.y)
timer = TimerAll()
enemy1 = Enemy()
enemy2 = Enemy()
health = Health(10000, 100000)
health2 = Health(10000, 100000)
health_cowboy = Health(10000, 10000)


# Main game loop
def tick():
    global time
    global second_time
    global third_time
    global b
    global GameTrue
    global enemy_killed
    global enemy_killed2
    global bullet_shooting
    global time_kill
    global time_kill2
    global x
    camera.clear('#EFDD6F')
    cowboy.cowman.move_to_stop_overlapping(scenery[0])
    cowboy.cowman.move_to_stop_overlapping(scenery[1])
    cowboy.cowman.move_to_stop_overlapping(house)
    timer.time_move()
    cowboy.cowboy_die()
    enemy1.move()
    enemy2.move2()
    bullets.move()
    bullets.bulletkills()
    bullets.bulletkills2()
    health_cowboy.cowboy_health()
    health.health_changing_enemy_1()
    health2.health_changing_enemy_2()
    health.moving_healthbars()
    health2.moving_healthbars2()
    if GameTrue:
        camera.draw(health_cowboy.dead)
        if uvage.is_pressing("w"):
            cowboy.move_up()
        if uvage.is_pressing("s"):
            cowboy.move_down()
        if uvage.is_pressing("a"):
            cowboy.move_left()
        if uvage.is_pressing("d"):
            cowboy.move_right()
        if camera.mouseclick:
            bullet_shooting = True
        if (second_time % 60) == 0:
            if not any(fruit.active for fruit in fruits):
                new_fruit = cowboy.touch()
                fruits.append(new_fruit)
                new_fruit.activate((random.randint(200, 400)),
                                   (random.randint(200, 400)))
        for fruit in fruits:
            fruit.existing()
            camera.draw(fruit.pineapple)
    if not GameTrue:
        gameovertext = [uvage.from_text(400, 300, "GAME OVER", 50, "red", bold=True),
                        uvage.from_text(400, 400, "Click 'space' to restart the game", 30, "red")]
        camera.draw(gameovertext[0])
        camera.draw(gameovertext[1])
        if uvage.is_pressing("space"):
            health_cowboy.dead.x = 10000
            enemy_killed = True
            enemy_killed2 = True
            time_kill1 = 1
            time_kill2 = 1
            time = 0
            second_time = 0
            third_time = 0
            b = 15
            x = 1
            cowboy.cowman.x = 125
            cowboy.cowman.y = 500
            GameTrue = True

    camera.draw(scenery[0])
    camera.draw(scenery[1])
    camera.draw(cowboy.cowman)
    camera.draw(timer.second)
    camera.draw(timer.second1)
    camera.draw(timer.second2)
    camera.draw(enemy1.badguy)
    camera.draw(enemy2.badguy)
    camera.draw(health_cowboy.full_health_bar)
    camera.draw(health_cowboy.half_health_bar)
    camera.draw(health.full_health_bar)
    camera.draw(health.half_health_bar)
    camera.draw(health2.full_health_bar)
    camera.draw(health2.half_health_bar)
    camera.draw(house)
    camera.draw(health_cowboy.dead)
    camera.display()


uvage.timer_loop(100000060, tick)
