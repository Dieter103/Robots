from tkinter import *
from MotorAction import *
from PauseAction import *
from SpeakAction import *
from WaitForSpeechAction import *
from GameAction import *
from _thread import start_new_thread
from Action import *
import random
from aenum import Enum
import sys
import Server
from Maestro import Controller

controller = Controller()
connection = Server

global currentDirection


class Cell:
    def __init__(self):
        self.type = MazeType.NONE
        self.hidden = True


class PathCell(Cell):
    def __init__(self):
        Cell.__init__(self)
        self.type = MazeType.PATH
        self.hidden = False


class MazeType(Enum):
    RECHARGE_STATION = 0
    WEAK_MONSTER = 1
    HARD_MONSTER = 2
    START = 3
    END = 4
    PATH = 5
    NONE = 6


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class MazeCell(Cell):
    def __init__(self, type):
        Cell.__init__(self)
        self.type = type
        if self.type == MazeType.WEAK_MONSTER:
            self.monster = WeakMonster()
        elif self.type == MazeType.HARD_MONSTER:
            self.monster = HardMonster()


class Entity:
    def __init__(self):
        self.health = 20
        self.damage = 1

    def deal_damage(self, amt):
        self.health -= amt


class WeakMonster(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.damage = 2
        self.health = 1
        self.has_key = False


class HardMonster(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.damage = 5
        self.health = 1


class Player(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.has_key = False

    def attempt_flee(self, maze):
        if random.randint(0, 3) < 3:
            print('success')
            paths = maze.paths_available()
            path = paths[random.randint(0, len(paths) - 1)]
            if path == 'North':
                x, y = maze.position
                maze.position = (x, y - 2)
            elif path == 'South':
                x, y = maze.position
                maze.position = (x, y + 2)
            elif path == 'East':
                x, y = maze.position
                maze.position = (x + 2, y)
            elif path == 'West':
                x, y = maze.position
                maze.position = (x - 2, y)
            return True
        else:
            print('fail')
            return False


class Maze:


    def __init__(self):
        self.maze = []
        self.position = (0, 0)
        self.size = 0
        self.player = Player()

    def __str__(self):
        out = ''
        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                out += {
                    MazeType.RECHARGE_STATION: 'r',
                    MazeType.PATH: 'p',
                    MazeType.WEAK_MONSTER: 'w',
                    MazeType.HARD_MONSTER: 'h',
                    MazeType.NONE: ' ',
                    MazeType.END: 'e',
                    MazeType.START: 's'
                }[self.maze[j][i].type] if not self.maze[j][i].hidden else '?'
            out += '\n'
        return out

    def generate_blank_maze(self, size):
        self.size = size
        self.maze = [[Cell() for i in range(size)] for j in range(size)]

    def generate_maze2(self):
        self.generate_blank_maze(5)
        self.position = {
            0: (0, 0),
            1: (4, 0),
            2: (4, 4),
            3: (0, 4),
        }[random.randint(0, 3)]

        cell = 0
        path = 1

        maze_positions = {
            (0, 0): cell, (1, 0): path, (2, 0): cell, (3, 0): path, (4, 0): cell,
            (0, 1): None, (1, 1): None, (2, 1): path, (3, 1): None, (4, 1): path,
            (0, 2): cell, (1, 2): path, (2, 2): cell, (3, 2): None, (4, 2): cell,
            (0, 3): path, (1, 3): None, (2, 3): path, (3, 3): None, (4, 3): None,
            (0, 4): cell, (1, 4): None, (2, 4): cell, (3, 4): path, (4, 4): cell,
        }

        positions = [
            (0, 0), (2, 0), (4, 0),
            (0, 2), (2, 2), (4, 2),
            (0, 4), (2, 4), (4, 4)
        ]

        recharge_station_left = 1
        weak_enemies_left = 4
        hard_enemies_left = 2

        start_position = {
            0: (0, 0),
            1: (4, 0),
            2: (4, 4),
            3: (0, 4),
        }[random.randint(0, 3)]
        positions.remove(start_position)
        x, y = start_position
        self.maze[x][y] = MazeCell(MazeType.START)
        self.position = start_position
        self.maze[x][y].hidden = False

        end_position = {
            0: (0, 0),
            1: (4, 0),
            2: (4, 4),
            3: (0, 4),
        }[random.randint(0, 3)]

        while start_position == end_position:
            end_position = {
                0: (0, 0),
                1: (4, 0),
                2: (4, 4),
                3: (0, 4),
            }[random.randint(0, 3)]
        positions.remove(end_position)
        x, y = end_position
        self.maze[x][y] = MazeCell(MazeType.END)

        for position in positions:
            cell = {}
            if recharge_station_left > 0 and weak_enemies_left > 0 and hard_enemies_left > 0:
                cell = {
                    0: MazeCell(MazeType.RECHARGE_STATION),
                    1: MazeCell(MazeType.WEAK_MONSTER),
                    2: MazeCell(MazeType.HARD_MONSTER),
                }[random.randint(0, 2)]
            elif recharge_station_left > 0 and weak_enemies_left > 0:
                cell = {
                    0: MazeCell(MazeType.RECHARGE_STATION),
                    1: MazeCell(MazeType.WEAK_MONSTER),
                }[random.randint(0, 1)]
            elif recharge_station_left > 0 and hard_enemies_left > 0:
                cell = {
                    0: MazeCell(MazeType.RECHARGE_STATION),
                    1: MazeCell(MazeType.HARD_MONSTER),
                }[random.randint(0, 1)]
            elif weak_enemies_left > 0 and hard_enemies_left > 0:
                cell = {
                    0: MazeCell(MazeType.WEAK_MONSTER),
                    1: MazeCell(MazeType.HARD_MONSTER),
                }[random.randint(0, 1)]
            elif recharge_station_left > 0:
                cell = MazeCell(MazeType.RECHARGE_STATION)
            elif weak_enemies_left > 0:
                cell = MazeCell(MazeType.WEAK_MONSTER)
            elif hard_enemies_left > 0:
                cell = MazeCell(MazeType.HARD_MONSTER)

            if cell.type == MazeType.RECHARGE_STATION:
                recharge_station_left -= 1
            elif cell.type == MazeType.WEAK_MONSTER:
                hard_enemies_left -= 3
                if hard_enemies_left == 0:
                    cell.monster.has_key = True
            elif cell.type == MazeType.HARD_MONSTER:
                hard_enemies_left -= 1

            x, y = position
            self.maze[x][y] = cell

        for key in maze_positions.keys():
            if maze_positions[key] == path:
                x, y = key
                self.maze[x][y] = PathCell()

    def paths_available(self):
        paths = []
        x, y = self.position

        if x > 0 and self.maze[x - 1][y].type == MazeType.PATH:
            paths.append('West')

        if x < self.size - 1 and self.maze[x + 1][y].type == MazeType.PATH:
            paths.append('East')

        if y > 0 and self.maze[x][y - 1].type == MazeType.PATH:
            paths.append('North')

        if y < self.size - 1 and self.maze[x][y + 1].type == MazeType.PATH:
            paths.append('South')

        return paths


    def turn180(self):
        controller.setAccel(2, 6)
        controller.setTarget(2, 5000)
        print("in 180")
        time.sleep(4)
        controller.setTarget(2,6000)
        time.sleep(1)
        pass

    def turnRight90(self):
        controller.setAccel(2, 6)
        controller.setTarget(2, 5000)
        print("in right 90")
        time.sleep(2)
        controller.setTarget(2, 6000)
        time.sleep(1)
        pass

    def turnLeft90(self):
        controller.setAccel(2, 6)
        controller.setTarget(2, 7000)
        print("in left 90")
        time.sleep(4)
        controller.setTarget(2, 6000)
        time.sleep(1)

        pass

    def forward(self):
        controller.setAccel(1,1)
        controller.setTarget(1,5000)
        time.sleep(1)
        controller.setTarget(1,6000)

    def armMovement(self):
        controller.setTarget(6,9000)
        time.sleep(1)
        controller.setTarget(8, 9000)
        time.sleep(0.75)
        controller.setTarget(8, 6000)
        time.sleep(duration)
        controller.setTarget(6,6000)

    def move(self, direction):
        m = {
            Direction.NORTH: (0, -1),
            Direction.EAST: (1, 0),
            Direction.SOUTH: (0, 1),
            Direction.WEST: (-1, 0)
        }[direction]

        d = {
            Direction.NORTH: (0, -2),
            Direction.EAST: (2, 0),
            Direction.SOUTH: (0, 2),
            Direction.WEST: (-2, 0)
        }[direction]

        dir_vals = {
            Direction.NORTH: 0,
            Direction.EAST: 90,
            Direction.WEST: -90,
            Direction.SOUTH: 180,
        }
        global currentDirection
        rotation_amt = dir_vals[direction] - dir_vals[currentDirection]
        print(rotation_amt)
        currentDirection = direction
        if(rotation_amt == 90):
            self.turnRight90()
            self.forward()

        elif(rotation_amt == -90):
            self.turnLeft90()
            self.forward()

        elif(rotation_amt == 180 or rotation_amt == -180):
            self.turn180()
            self.forward()
        else:
            self.forward()
            

        x, y = self.position

        if x + d[0] < 0 or x + d[0] > self.size or y + d[1] < 0 or y + d[1] > self.size:
            return False

        if self.maze[x + m[0]][y + m[1]].type != MazeType.PATH:
            return False

        self.position = (x + d[0], y + d[1])
        self.on_move()
        x, y = self.position
        return self.maze[x][y].type

    def recharge_player(self):
        print()
        self.speak('You find a bottle of child tears. Mmmmm, the sweet taste of child tears, you\'ve been recharged')
        print()
        self.player.health = 20

    def spawn_weak_monster(self):
        print()
        print('weak monster')
        print()
        x, y = self.position
        monster = self.maze[x][y].monster
        print(monster.health)
        while self.player.health > 0 and monster.health > 0:
            self.speak("A wimpy, sad monster limps into your path.")
            out = ''.join(('you have', str(self.player.health), 'health', 'they have', str(monster.health), 'health,', 'wut u wanna do'))

            self.speak(out)

            action = self.listen()

            if action == 'fight':
                dmg_amt = random.randint(0, 10)
                self.speak("You strike their face with the force of several kielbasa sausages")
                self.armMovement()
                self.speak('you did ' + dmg_amt + "damage")
                monster.deal_damage(dmg_amt)
            elif action == 'run' and self.player.attempt_flee(self):

                break

            dmg_amt = random.randint(0, 10)
            print('you dun got hit', dmg_amt)
            self.player.deal_damage(dmg_amt)

        if self.player.health > 0:
            self.speak('you won the flight, time to keep kicking ass')
        else:
            self.speak('they won the flight, You let me and everyone you know down. Try again')
            sys.exit()

    def speak(self,text):
        connection.clients[0].text = "tts " + ', ' + text
        while connection.clients[0].command != "done":
            pass
        connection.clients[0].reset()

    def listen(self):
        connection.clients[0].text = "sst "
        while (connection.clients[0].command == ''):
            time.sleep(1)
            pass
        out = connection.clients[0].command

        connection.clients[0].reset()

        return out

    def spawn_hard_monster(self):
        print()
        print('hard monster')
        print()
        x, y = self.position
        monster = self.maze[x][y].monster
        while self.player.health > 0 and monster.health > 0:

            print('you has', self.player.health, 'health')
            print('they has', monster.health, 'health')
            self.speak("Holy crap batman, a giant scary ass monster just stomped into your path. Halp, I'm scared.")

            out = ''.join(('you have', str(self.player.health), 'health', 'they have', str(monster.health), 'health,', 'wut u wanna do'))
            self.speak(out)
            action = self.listen()


            if action == 'fight':
                dmg_amt = random.randint(0, 10)
                self.speak("You slam your sword into it's body like a toothpick against Zac Efron's rock hard abs")
                self.armMovement()
                self.speak("You did " + dmg_amt + " damage")
                monster.deal_damage(dmg_amt)
            elif action == 'run' and self.player.attempt_flee(self):

                break

            dmg_amt = random.randint(0, 3)
            self.speak(''.join(('you dun got hit', str(dmg_amt))))
            self.player.deal_damage(dmg_amt)

        if self.player.health > 0:
            if self.player.health > 0:
                self.speak('you won the flight, time to keep kicking ass')
                if monster.has_key:
                    self.player.has_key = True
                    self.speak('Holy crap, that monster had a key for some reason. I guess we\'ll take it just in case.')
        else:
            self.speak('they won the flight, You let me and everyone you know down. Try again')
            sys.exit()

    def end(self):
        if self.player.has_key:
            self.speak('hooray you finished')
        else:
            self.speak('You need the key, go back and find it you bozo')

    def on_move(self):
        x, y = self.position
        self.maze[x][y].hidden = False
        {
            MazeType.RECHARGE_STATION: self.recharge_player,
            MazeType.WEAK_MONSTER: self.spawn_weak_monster,
            MazeType.HARD_MONSTER: self.spawn_hard_monster,
            MazeType.START: lambda: print,
            MazeType.END: self.end,
            MazeType.PATH: lambda: print,
            MazeType.NONE: lambda: print,
        }[self.maze[x][y].type]()




def go(controller, server):

    global connection
    connection = server
    global currentDirection
    currentDirection = Direction.NORTH
    maze = Maze()
    maze.generate_maze2()
    for i in range(10):
        print(maze)
        print(', '.join(maze.paths_available()))
        print(maze.position)
        server.clients[0].text = "tts " + ', '.join(maze.paths_available())
        print('tts ' + ', '.join(maze.paths_available()))
        while server.clients[0].command != "done":
            pass

        server.clients[0].reset()

        server.clients[0].text = "sst "
        while (connection.clients[0].command == ''):
            pass
        print(connection.clients[0].command)

        time.sleep(1)
        inp = server.clients[0].command

        server.clients[0].reset()


        while (
            maze.move(
                {
                    'South': Direction.SOUTH,
                    'North': Direction.NORTH,
                    'East': Direction.EAST,
                    'West': Direction.WEST
                }[inp]
            ) is False
        ):
            maze.speak("Nice, try, that wasn't an option you bozo, try again")

            inp = maze.listen()


# main()
