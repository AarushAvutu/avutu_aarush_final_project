''' Task schedular
after set amount of time does task
ex: delete unused tabs
running program
backups
Maintenance: disk clear up trash empty
sending automated notifications (calender maybe)
automation w/ smarthome devices (turn lights on and off at time when come home)
updates (checks for needed app updates and updates at night)
timer to remind yourself something
notifications on and off toggle for specifics

or

Multiplayer game
3D
objective: find treasure
platformer
powerups
mobs?
everytime finds treasure at level theif comes and takes to next lvl?
last lvl defeat theif


'''

'''
from panda3d.core import load_prc_file

# Load the configuration file
load_prc_file("final_project_main/config.prc")

from direct.showbase.ShowBase import ShowBase

class MyGame(ShowBase):
    def __init__(self):
        super().__init__()

        print(self.render)
        print(self.camera)
        print(self.cam)

game = MyGame()


game.run()'''

from panda3d.core import load_prc_file_data
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3

class MultiplayerGame(ShowBase):
    def __init__(self):
        super().__init__()

        # Load environment (platforms, terrain, etc.)
        # This might involve loading models, textures, and setting up the world

        # Create player characters for multiplayer
        self.player1 = self.create_player()
        self.player2 = self.create_player()

        # Create treasure
        self.treasure = self.load_treasure()
        self.treasure.set_pos(10, 0, 10)  # Set initial position of treasure

        # Create thief character
        self.thief = self.create_thief()
        self.thief.set_pos(20, 0, 20)  # Set initial position of thief

        # Set up collision detection between players and treasure
        self.setup_collisions()

        # Start the game
        self.run()

    def create_player(self):
        # Create player characters (might involve loading character models and animations)
        player = Actor("player_model")
        player.reparent_to(self.render)
        player.set_pos(0, 0, 0)  # Set initial position of player
        # Add player controls, movements, etc.
        return player

    def load_treasure(self):
        # Load treasure model and return it
        treasure = loader.load_model("treasure_model")
        treasure.reparent_to(self.render)
        return treasure

    def create_thief(self):
        # Create thief character (similar to creating players)
        thief = Actor("thief_model")
        thief.reparent_to(self.render)
        # Add animations, AI for thief movements, etc.
        return thief

    def setup_collisions(self):
        # Set up collision detection between players and treasure
        # This involves creating collision solids, setting collision masks, and handling collisions

        # Example collision detection setup (pseudo-code)
        self.player1_coll = self.player1.attach_new_node(CollisionNode("player1_coll"))
        self.player1_coll.node().add_solid(CollisionSphere(0, 0, 0, 1))
        self.player1_coll.node().set_collide_mask(BitMask32.bit(1))
        self.treasure.set_collide_mask(BitMask32.bit(1))
        self.accept("player1_coll-into-treasure_coll", self.on_treasure_found)

    def on_treasure_found(self, entry):
        # When a player finds the treasure
        # Move the treasure to a new location (next level)
        self.treasure.set_pos(30, 0, 30)  # Example: Move treasure to a new location
        # Bring the thief to take the treasure to the next level
        thief_sequence = Sequence(
            self.thief.posInterval(3, Point3(30, 0, 30)),  # Move thief to treasure
            self.thief.posInterval(3, Point3(40, 0, 40)),  # Example: Move thief to next level
            # Continue with next level setup or actions
        )
        thief_sequence.start()

    # Other game functionalities like power-ups, mobs, levels, etc. can be added here

if __name__ == "__main__":
    # Set Panda3D configuration options
    load_prc_file_data("", "window-title Multiplayer 3D Platformer")
    load_prc_file_data("", "show-frame-rate-meter True")

    # Start the game
    game = MultiplayerGame()

