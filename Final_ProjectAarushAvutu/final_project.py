"""
awsd - movement
a - move left
w - walk forward
s- walk backward
d- move right
space - jump
mouse - look around
esc- exit the application
"""
# Import necessary modules
import direct.directbase.DirectStart
from pandac.PandaModules import *
from direct.gui.OnscreenText import OnscreenText
import sys

# Define a Game class
class Game(object):
    def __init__(self):
        # Initialize collision detection
        # manages the traversal through the scene graph to detect collisions
        base.cTrav = CollisionTraverser()
        #  specialized kind of CollisionHandler that simply pushes back on things
        #  that attempt to move into solid walls.
        base.pusher = CollisionHandlerPusher()

        # Load the game level
        # Load the level model and set it to be visible from both sides
        self.level = loader.loadModel("level.egg")
        self.level.reparentTo(render)
        self.level.setTwoSided(True)


        # Initialize the player which will create Player object and 3D vector system
        self.node = MultiPLayer()

        # Enable exiting the application when the 'escape' key is pressed
        base.accept("escape", sys.exit)
        # Disable mouse control in the game window
        base.disableMouse()

        # Display text on the screen explaining the controls
        OnscreenText(
            text=__doc__,
            style=1,
            fg=(1, 1, 1, 1),
            pos=(-1.3, 0.95),
            align=TextNode.ALeft,
            scale=0.05,
        )


# Define a Player class
class MultiPLayer(object):
    # Constants for player movement with this three-component vector distance
    walk = Vec3(0)
    strafe = Vec3(0)
    readyToJump = False
    jump = 0

   # init method which loads model, setup camera, create collisions and attach controls
    def __init__(self):

        # Load the player model
        self.node = NodePath("player")
        self.node.reparentTo(render)
        self.node.setPos(0, 0, 2)
        self.node.setScale(0.05)

        # Set up the camera for the player
        # Set the camera's field of view and parent it to the player node
        pl = base.cam.node().getLens()
        pl.setFov(70)
        base.cam.node().setLens(pl)
        base.camera.reparentTo(self.node)


        # Collision detection for the player
        cn = CollisionNode("player")
        cn.addSolid(CollisionSphere(0, 0, 0, 3))
        solid = self.node.attachNewNode(cn)
        base.cTrav.addCollider(solid, base.pusher)
        base.pusher.addCollider(solid, self.node, base.drive.node())
        # Collision detection for player's floor
        ray = CollisionRay()
        ray.setOrigin(0, 0, -0.2)
        ray.setDirection(0, 0, -1)
        cn = CollisionNode("playerRay")
        cn.addSolid(ray)
        cn.setFromCollideMask(BitMask32.bit(0))
        cn.setIntoCollideMask(BitMask32.allOff())
        solid = self.node.attachNewNode(cn)
        self.nodeGroundHandler = CollisionHandlerQueue()
        base.cTrav.addCollider(solid, self.nodeGroundHandler)


        # Attach controls for player movement
        base.accept("space", self.__setattr__, ["readyToJump", True])
        base.accept("space-up", self.__setattr__, ["readyToJump", False])
        base.accept("s", self.__setattr__, ["walk", Vec3(0)])
        base.accept("w", self.__setattr__, ["walk", Vec3(0, 2, 0)])
        base.accept("s", self.__setattr__, ["walk", Vec3(0, -1, 0)])
        base.accept("s-up", self.__setattr__, ["walk", Vec3(0)])
        base.accept("w-up", self.__setattr__, ["walk", Vec3(0)])
        base.accept("a", self.__setattr__, ["strafe", Vec3(-1, 0, 0)])
        base.accept("d", self.__setattr__, ["strafe",  Vec3(1, 0, 0)])
        base.accept("a-up", self.__setattr__, ["strafe", Vec3(0)])
        base.accept("d-up", self.__setattr__, ["strafe", Vec3(0)])


        # init mouse update task with mouse, move and jump updates as a task.
        # handle the events with task manager in the background.
        taskMgr.add(self._updateMouse, "mouse-task")
        taskMgr.add(self._updateMove, "move-task")
        taskMgr.add(self._updateJump, "jump-task")


    # Method to update player's jump
    def _updateJump(self, task):

        highestZ = -100
        # Check for ground collisions and handle jumping
        for i in range(self.nodeGroundHandler.getNumEntries()):
            entry = self.nodeGroundHandler.getEntry(i)
            z = entry.getSurfacePoint(render).getZ()
            if z > highestZ and entry.getIntoNode().getName() == "Cube":
                highestZ = z
        # Apply gravity and handle jumping
        self.node.setZ(self.node.getZ() + self.jump * globalClock.getDt())
        self.jump -= 1 * globalClock.getDt()
        if highestZ > self.node.getZ() - 0.3:
            self.jump = 0
            self.node.setZ(highestZ + 0.3)
            if self.readyToJump:
                self.jump = 1
        return task.cont

    # Method to update player movement
    def _updateMove(self, task):
        # Update the player's position based on movement keys
        self.node.setPos(self.node, self.walk * globalClock.getDt() * 50)
        self.node.setPos(self.node, self.strafe * globalClock.getDt() * 50)
        return task.cont

    # Method to update mouse movements
    def _updateMouse(self, task):
        # Capture mouse movement and adjust player and camera orientation accordingly
        md = base.win.getPointer(0)

        x = md.getX()
        y = md.getY()

        mouse_x = base.win.getPointer(0).getX()
        mouse_y = base.win.getPointer(0).getY()
        # Adjust player and camera orientation based on mouse movement
        if base.win.movePointer(0, base.win.getXSize() // 2, base.win.getYSize() // 2):
            x_diff = mouse_x - base.win.getXSize() // 2
            y_diff = mouse_y - base.win.getYSize() // 2

            self.node.setH(self.node.getH() - x_diff * 0.1)
            base.camera.setP(base.camera.getP() - y_diff * 0.1)

        return task.cont

Game()
base.run()
