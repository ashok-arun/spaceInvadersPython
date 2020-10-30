"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in
the Alien Invaders game.  Instances of Wave represent a single wave. Whenever
you move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on
screen. These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or
models.py. Whether a helper method belongs in this module or models.py is
often a complicated issue.  If you do not know, ask on Piazza and we will
answer.

Ashok Arun aka68 Christian D Boswell (cdb89)
12/12/2019
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary.
    It also marches the aliens back and forth across the screen until they are
    all destroyed or they reach the defense line (at which point the player
    loses). When the wave is complete, you  should create a NEW instance of
    Wave (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.  This
    class will be similar to than one in how it interacts with the main class
    Invaders.

    All of the attributes of this class are to be hidden. You may find that
    you want to access an attribute in class Invaders. It is okay if you do,
    but you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter
    and/or setter for any attribute that you need to access in Invaders.
    Only add the getters and setters that you need for Invaders. You can keep
    everything else hidden.

    """
    # HIDDEN ATTRIBUTES:
    # Attribute _ship: the player ship to control
    # Invariant: _ship is a Ship object or None
    #
    # Attribute _aliens: the 2d list of aliens in the wave
    # Invariant: _aliens is a rectangular 2d list containing Alien objects or None
    #
    # Attribute _bolts: the laser bolts currently on screen
    # Invariant: _bolts is a list of Bolt objects, possibly empty
    #
    # Attribute _dline: the defensive line being protected
    # Invariant : _dline is a GPath object
    #
    # Attribute _lives: the number of lives left
    # Invariant: _lives is an int >= 0
    #
    # Attribute _time: the amount of time since the last Alien "step"
    # Invariant: _time is a float >= 0s
    #
    # You may change any attribute above, as long as you update the invariant
    # You may also add any new attributes as long as you document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    # Attribute _sounds: sounds for the user to use
    # Invariant: _sounds is a list of sounds in .wav, possibly empty

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getShip(self):
        """
        Returns the _ship attribute of the wave
        """
        return self._ship

    def recenter(self):
        """
        recenter the ship to the middle of the  screen after losing a life
        """
        self._ship=Ship()

    def getLives(self):
        """
        Returns the _lives attribute of the wave
        """
        return self._lives

    def getLevel(self):
        """
        Returns the _level attribute of the wave
        """
        return self._level

    def getScore(self):
        """
        Returns the _score attribute for the wave
        """
        return self._score

    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self, level=1, lives=PLAYER_LIFE, score=0):
        """
        Creats aliens, a ship, and a defensive line

        initializes the _shottimer, _lives, and _time attributes

        Parameter level: The current level of the wave
        Precondition: level is an int >=1

        Parameter lives: the number of lives the player will start with
        Precondition: lives is an int>0
        """
        self.alien_setup()
        self._ship=Ship()
        self._bolts=[]
        self._lives=lives
        self._dline=GPath(points=[0, DEFENSE_LINE, GAME_WIDTH, DEFENSE_LINE],
                          linewidth=1, linecolor='black')
        self._shottimer=random.randint(1, BOLT_RATE)
        self._time=0
        self._level=level
        self._score=score
        self._speed=max(ALIEN_SPEED-((self._level-1)*.1),
                        ALIEN_SPEED/self._level)
        self._sounds = ['pew1.wav', 'pew2.wav',
        'pop1.wav', 'blast1.wav']

    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self, keys, dt):
        """
        Updatesthe ship, aliens, and bolts every t seconds

        Parameter keys: user input
        Precondition: input attribute of Invaders class

        Parameter t: the time in seconds since the last update
        Precondition: t is a number [int or float]
        """
        self.move_aliens(dt)
        if not self.game_over():
            self._ship.move_ship(keys)
            self.ship_bolt(keys)
            self.alien_bolt()
            self.move_bolts()
            for bolt in self._bolts:
                self.check_collisions(bolt)
            self.delete_bolts()

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self, view):
        """
        Draws the ship, aliens, defensive line, and bolts to the screen

        Parameter view: the window to draw objects to
        Precondition: view attribute of Invaders class
        """
        for row in self._aliens:
            for alien in row:
                if alien!=None:
                    alien.draw(view)
        if self._ship!=None:
            self._ship.draw(view)
        self._dline.draw(view)
        for bolt in self._bolts:
            bolt.draw(view)

    def playSound(self, source):
        """
        This method plays a sound.

        Parameter source: a valid .wav file
        Precondition: source is a string with len(source)>0
        """
        pewSound = Sound(source)
        pewSound.play()

    def alien_setup(self):
        """
        Fills a 2d list with Aliens

        _direction=1, the wave is moving to the right.
        """
        self._direction=1
        self._aliens=[]
        for row in range(ALIEN_ROWS):
            self._aliens.append([])
        for col in range(ALIENS_IN_ROW):
            for row in range(ALIEN_ROWS):
                x=(ALIEN_H_SEP+(ALIEN_WIDTH/2))+(col*(ALIEN_WIDTH+ALIEN_H_SEP))
                y=((GAME_HEIGHT-ALIEN_CEILING-ALIEN_HEIGHT/2)
                    -(row*(ALIEN_HEIGHT+ALIEN_V_SEP)))
                source_num=((ALIEN_ROWS-1)-row)//2
                source_num=source_num%3
                source=ALIEN_IMAGES[source_num]
                self._aliens[row].append(Alien(x, y, source))

    def move_aliens(self, dt):
        """
        Moves the aliens

        If the aliens reach the edge of the screen, they readjust so that
        the side of he alien wave is away from the edge and move
        down the screen.

        Parameter dt: the time in seconds since the last update
        Precondition: dt is a number [int or float]
        """
        if self._time<self._speed:
            self._time=self._time+dt
        else:
            self._time=0
            self._shottimer=self._shottimer-1
            if self.alien_edge():
                for row in self._aliens:
                    for alien in row:
                        if alien!=None:
                            alien.y=alien.y-ALIEN_V_WALK
                            alien.x=alien.x+(self.alien_distance()*
                                             self._direction*-1)
                self._direction=self._direction*-1
            else:
                for row in self._aliens:
                    for alien in row:
                        if alien!=None:
                            alien.x=alien.x+(ALIEN_H_WALK*self._direction)

    def alien_edge(self):
        """
        Returns True if alien wave is at the edge of the screen
        """
        right=0
        left=GAME_WIDTH
        for row in self._aliens:
            for alien in row:
                if alien!=None:
                    if self._direction==1 and alien.x>right:
                            right=alien.x
                    elif alien.x<left:
                            left=alien.x
        if self._direction==1:
            return (GAME_WIDTH-(right+ALIEN_WIDTH/2))<ALIEN_H_SEP
        return left-ALIEN_WIDTH/2<ALIEN_H_SEP

    def alien_distance(self):
        """
        Returns the distance between the edge of the wave and the edge of the
        screen
        """
        distance=GAME_WIDTH
        for row in self._aliens:
            for alien in row:
                if alien!=None:
                    if (self._direction == 1 and abs((GAME_WIDTH-
                    (alien.x+ALIEN_WIDTH/2))-ALIEN_H_SEP)<distance):
                        distance=abs((GAME_WIDTH-(alien.x+ALIEN_WIDTH/2))-ALIEN_H_SEP)
                    elif (abs((alien.x-ALIEN_WIDTH/2)-ALIEN_H_SEP)<distance):
                        distance=abs((alien.x-ALIEN_WIDTH/2)-ALIEN_H_SEP)
        return distance

    def ship_bolt(self, keys):
        """
        Fires a bolt from the ship straight upward

        Parameter keys: the user input
        Precondition: keys is the input attribute of Invaders class
        """
        if keys.is_key_down('spacebar'):
            for bolt in self._bolts:
                if bolt._velocity>0:
                    return
            else:
                self.playSound(self._sounds[0])
                bolt=Bolt(self._ship.x, self._ship.y+SHIP_HEIGHT/2+BOLT_HEIGHT/2)
                self._bolts.append(bolt)

    def move_bolts(self):
        """
        Moves each bolt currently onscreen

        Each bolt is moved by adding its corresponding velocity to its vertical
        position y.
        """
        for bolt in self._bolts:
            bolt.y+=bolt.getVelocity()

    def delete_bolts(self):
        """
        deletes any bolts that are offscreen
        """
        count=0
        while count<len(self._bolts):
            if (self._bolts[count].y-BOLT_HEIGHT/2>GAME_HEIGHT or
            self._bolts[count].y+BOLT_HEIGHT/2<0):
                del self._bolts[count]
            else:
                count+=1

    def alien_fires(self):
        """
        Returns a randomly chosen alien to fire a bolt

        This method randomly chooses one alien to fire a bolt. This alien must
        be the first alien in its column.
        """
        cols=list(range(ALIENS_IN_ROW))
        col=random.choice(cols)
        bool=True
        while bool:
            for row in self._aliens:
                if row[col]!=None:
                    bool=False
        aliencol=[]
        length=[]
        for row in self._aliens:
            if row[col]!=None:
                aliencol.append(row[col])
                length.append(row[col].y)
        return aliencol[(length.index(min(length)))]

    def alien_bolt(self):
        """
        Fires a bolt from one of the aliens
        """
        if self._shottimer==0:
            shooter=self.alien_fires()
            bolt=Bolt(shooter.x, shooter.y-ALIEN_HEIGHT/2-BOLT_HEIGHT/2)
            self._bolts.append(bolt)
            self.playSound(self._sounds[1])
            self._shottimer=random.randint(1, BOLT_RATE)

    def check_collisions(self, bolt):
        """
        Destros alien or ship hit by bolt
        Alien speed increases a little

        Parameter bolt: the bolt to check for collisions
        Precondition: bolt is a Bolt object
        """
        for row in self._aliens:
            for alien in row:
                if alien!=None and alien.collides(bolt):
                    row[row.index(alien)]=None
                    self._score=(self._score+(ALIEN_ROWS-self._aliens.index(row))
                                 *self._level*10)
                    self.playSound(self._sounds[2])
                    self._speed=self._speed*0.99
                    del self._bolts[self._bolts.index(bolt)]
                if self._ship!=None and self._ship.collides(bolt):
                    self.playSound(self._sounds[3])
                    self._ship=None
                    del self._bolts[self._bolts.index(bolt)]
                    self._lives=self._lives-1

    def game_over(self):
        """
        Returns True if there is no ship or no lives or the aliens have breached
        the defense line.
        """
        for row in self._aliens:
            for alien in row:
                if alien!=None and alien.y-ALIEN_HEIGHT/2<=DEFENSE_LINE:
                    return True
        return self._ship==None and self._lives==0

    def won(self):
        """
        Return True if player has won the game, else False
        """
        for row in self._aliens:
            for alien in row:
                if alien!=None:
                    return False
        return True
