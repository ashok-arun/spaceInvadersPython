"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything
that you interact with on the screen is model: the ship, the laser bolts, and
the aliens.

Just because something is a model does not mean there has to be a special
class for it. Unless you need something special for your extra gameplay
features, Ship and Aliens could just be an instance of GImage that you move
across the screen. You only need a new class when you add extra features to
an object. So technically Bolt, which has a velocity, is really the only model
that needs to have its own class.

With that said, we have included the subclasses for Ship and Aliens. That is
because there are a lot of constants in consts.py for initializing the
objects, and you might want to add a custom initializer.  With that said,
feel free to keep the pass underneath the class definitions if you do not want
to do that.

You are free to add even more models to this module.  You may wish to do this
when you add new features to your game, such as power-ups.  If you are unsure
about whether to make a new class or not, please ask on Piazza.

Ashok Arun aka68 Christian D Boswell (cdb89)
12/12/2019
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other
# than consts.py.  If you need extra information from Gameplay, then it should
# be a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GImage):
    """
    A class to represent the game ship.

    At the very least, you want a __init__ method to initialize the ships
    dimensions. These dimensions are all specified in consts.py.

    You should probably add a method for moving the ship.  While moving a
    ship just means changing the x attribute (which you can do directly),
    you want to prevent the player from moving the ship offscreen.  This
    is an ideal thing to do in a method.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like animation).
    """
    #  IF YOU ADD ATTRIBUTES, LIST THEM BELOW
    def __init__(self):
        """
        Creates an instance of Ship
        """
        super().__init__(x=GAME_WIDTH/2, y=SHIP_BOTTOM+SHIP_HEIGHT/2,
                         width=SHIP_WIDTH, height=SHIP_HEIGHT,
                         source='ship.png')

    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS
    def move_ship(self, keys):
        """
        Moves the ship back and forth on the screen

        The ship moves SHIP_MOVEMENT in the corresponding arrow direction. If
        doing this would move the ship off screen, the ship stops at the edge of
        the screen. If both right and left arrows are pressed, the ship does not
        move.

        Parameter keys: the user input
        Precondition: keys is the input attribute of Invaders class
        """
        if keys.is_key_down('left'):
            self.x=max(self.x-SHIP_MOVEMENT, SHIP_WIDTH/2)
        elif keys.is_key_down('right'):
            self.x=min(self.x+SHIP_MOVEMENT, GAME_WIDTH-SHIP_WIDTH/2)

    def collides(self,bolt):
        """
        Returns: True if the bolt was fired by an alien and collides with ship

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        left_x=bolt.x-BOLT_WIDTH/2
        right_x=bolt.x+BOLT_WIDTH/2
        upper_y=bolt.y+BOLT_HEIGHT/2
        lower_y=bolt.y-BOLT_HEIGHT/2
        return (self.contains((left_x, upper_y)) or self.contains((left_x, lower_y)) or
        self.contains((right_x, upper_y)) or self.contains((right_x, lower_y)))


class Alien(GImage):
    """
    A class to represent a single alien.

    At the very least, you want a __init__ method to initialize the alien
    dimensions. These dimensions are all specified in consts.py.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like giving each alien a score value).
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self, x, y , source):
        """
        Initializes a GImage as an alien.
        Parameter x: the x-coordinate of an alien
        Precondition: x is an int greater than 0 and less than the width of the window
        Paramater y: the y-coordinate of the alien
        Precondition: y is an int greater than 0 and less than the height of the window
        Paramater source: the image source for the alien
        Precondition: A string that points to a valid image location

        """
        super().__init__(x=x, y=y, width=ALIEN_WIDTH, height=ALIEN_HEIGHT,
                         source=source)

    def collides(self,bolt):
        """
        Returns: True if the bolt was fired by the ship and collides with alien

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        left_x=bolt.x-BOLT_WIDTH/2
        right_x=bolt.x+BOLT_WIDTH/2
        upper_y=bolt.y+BOLT_HEIGHT/2
        lower_y=bolt.y-BOLT_HEIGHT/2
        return (self.contains((left_x, upper_y)) or self.contains((left_x, lower_y)) or
        self.contains((right_x, upper_y)) or self.contains((right_x, lower_y)))


class Bolt(GRectangle):
    """
    A class representing a laser bolt.

    Laser bolts are often just thin, white rectangles. The size of the bolt
    is determined by constants in consts.py. We MUST subclass GRectangle,
    because we need to add an extra (hidden) attribute for the velocity of
    the bolt.

    The class Wave will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with
    no setters for the velocities.  That is because the velocity is fixed and
    cannot change once the bolt is fired.

    In addition to the getters, you need to write the __init__ method to set
    the starting velocity. This __init__ method will need to call the __init__
    from GRectangle as a  helper.

    You also MIGHT want to create a method to move the bolt.  You move the
    bolt by adding the velocity to the y-position.  However, the getter
    allows Wave to do this on its own, so this method is not required.
    """
    # INSTANCE ATTRIBUTES:
    # Attribute _velocity: the velocity in y direction
    # Invariant: _velocity is an int or float

    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getVelocity(self):
        """
        Returns the _velocity attribute of the Bolt object
        """
        return self._velocity

    # INITIALIZER TO SET THE VELOCITY
    def __init__(self, x, y):
        """
        Creates an instance of Bolt

        Parameter x: the initial x coordinate of the Bolt
        Precondition: x is a number [int or float]

        Parameter y: the initial y coordinate of the Bolt
        Precondition: y is a number [int or float]
        """
        super().__init__(x=x, y=y, width=BOLT_WIDTH, height=BOLT_HEIGHT,
                       fillcolor='red', linecolor='red')
        if y+BOLT_HEIGHT/2<DEFENSE_LINE:
            self._velocity=BOLT_SPEED
        else:
            self._velocity=-BOLT_SPEED
# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE
