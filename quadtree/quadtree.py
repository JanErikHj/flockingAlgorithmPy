"""
Module quadtree

"""
__all__ = ['QuadTree', 'Point', 'Rectangle']

# A simple class to represent a point in 2D space.
class Point:
    def __init__(self, x, y, data=None):
        self.x = x
        self.y = y
        self.data = data

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


# A rectangle class that defines a region.
# Here, (x, y) is the center of the rectangle,
# and w and h represent half the width and half the height, respectively.
class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x  # center x-coordinate
        self.y = y  # center y-coordinate
        self.w = w  # half the width
        self.h = h  # half the height

    def contains(self, point):
        """Return True if the point lies inside the rectangle."""
        return (self.x - self.w <= point.x <= self.x + self.w and
                self.y - self.h <= point.y <= self.y + self.h)

    def intersects(self, other):
        """Return True if the rectangle overlaps with another rectangle 'range'."""
        return not (other.x - other.w > self.x + self.w or
                    other.x + other.w < self.x - self.w or
                    other.y - other.h > self.y + self.h or
                    other.y + other.h < self.y - self.h)


# The quadtree class.
class QuadTree:
    def __init__(self, boundary, capacity):
        """
        boundary: Rectangle defining the region covered by this quadtree node.
        capacity: Maximum number of points a node can hold before it subdivides.
        """
        self.boundary = boundary
        self.capacity = capacity
        self.points = []  # list to hold points in this node
        self.divided = False  # flag to indicate whether this node has been subdivided
        self.northeast = None
        self.northwest = None
        self.southeast = None
        self.southwest = None


    def subdivide(self):
        """Subdivide the current node into four children."""
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w
        h = self.boundary.h

        # Create four children: northeast, northwest, southeast, southwest.
        ne = Rectangle(x + w/2, y - h/2, w/2, h/2)
        self.northeast = QuadTree(ne, self.capacity)

        nw = Rectangle(x - w/2, y - h/2, w/2, h/2)
        self.northwest = QuadTree(nw, self.capacity)

        se = Rectangle(x + w/2, y + h/2, w/2, h/2)
        self.southeast = QuadTree(se, self.capacity)

        sw = Rectangle(x - w/2, y + h/2, w/2, h/2)
        self.southwest = QuadTree(sw, self.capacity)

        self.divided = True

    def insert(self, point):
        """
        Insert a point into the quadtree.
        Returns True if the point was added successfully.
        """
        # Ignore points that do not belong in this node.
        if not self.boundary.contains(point):
            return False

        # If there is room in this node, add the point here.
        if len(self.points) < self.capacity:
            self.points.append(point)
            return True
        else:
            # Otherwise, subdivide if necessary and then add the point to a child.
            if not self.divided:
                self.subdivide()

            if self.northeast.insert(point):
                return True
            if self.northwest.insert(point):
                return True
            if self.southeast.insert(point):
                return True
            if self.southwest.insert(point):
                return True

        # If for some reason the point could not be added, return False.
        return False

    def query(self, perception_area, found):
        """
        Find all points that lie within a given range.
        'range' is a Rectangle.
        'found' is a list that will be populated with points found in the range.
        """
        # If the range does not intersect this node's boundary, return immediately.
        if not self.boundary.intersects(perception_area):
            return
        else:
            # Otherwise, check points at this node.
            for p in self.points:
                if perception_area.contains(p):
                    found.append(p)
            # Then, if subdivided, query the children.
            if self.divided:
                self.northwest.query(perception_area, found)
                self.northeast.query(perception_area, found)
                self.southwest.query(perception_area, found)
                self.southeast.query(perception_area, found)

    def clear(self):
        self.points = []
        self.divided = False
        self.northeast = None
        self.northwest = None
        self.southeast = None
        self.southwest = None

