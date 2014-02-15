__author__ = 'Jonny Elliott'

from pygame import sprite


class MovingBoxSprite(sprite.Sprite):
    """
    A sprite class that is essentially a box that can move. It rebounds off of walls. Meant to make life easier
    when drawing a simple square to the canvas.
    """

    def __init__(self, x=0, y=0, width=50, height=50, colour=(0, 0, 0), vx=0, vy=0, bounds=(0, 0), edge_behaviour=1, chain_number=0):
        # Call the parent class (Sprite) constructor
        sprite.Sprite.__init__(self)
        self._Name = ""
        self._width = width
        self._height = height
        self._colour = colour
        self._edge_behaviour = edge_behaviour
        self._vx = vx
        self._vy = vy
        self._bounds = bounds

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([self._width, self._height])
        self.image.fill(self._colour)
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()

        self._x = x
        self._y = y

        self.rect.x = x
        self.rect.y = y

        # Snake properties
        self.chain_number = chain_number
        self.number_of_chains = 0
        self.hit = False

    def change_position(self, dx, dy):

        hit = False

        if self.rect.x+dx+self._width >= self._bounds[0]:
            dx *= self._edge_behaviour
            hit = True
        elif self.rect.x+dx <= 0:
            dx = abs(dx*self._edge_behaviour)
            hit = True

        if self.rect.y+dy+self._height >= self._bounds[1]:
            dy *= self._edge_behaviour
            hit = True
        elif self.rect.y+dy <= 0:
            dy = abs(dy*self._edge_behaviour)
            hit = True

        self.rect.x += dx
        self.rect.y += dy

        return dx, dy, hit

    def move(self):

        if abs(self._vx) > 0 or abs(self._vy) > 0:
            self._vx, self._vy, self.hit = self.change_position(self._vx, self._vy)

    def get_hit(self):
        return self.hit

    def set_velocity(self, vx, vy):
        self._vx = vx
        self._vy = vy

    def get_velocity(self):
        return self._vx, self._vy


class CanvasProperties(object):
    def __init__(self):

        self.colours = {
            "WHITE": (255, 255, 255),
            "BLACK": (0, 0, 0),
            "RED": (227, 14, 14),
            "GREY": (100, 100, 100),
            "BLUE": (0, 0, 255),
        }