class Point:
    """An (x,y) coordinate pair"""
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def move(self, d: "Point") -> "Point":
        """(x,y).move(dx,dy) = (x+dx, y+dy)"""
        x = self.x + d.x
        y = self.y + d.y
        return Point(x,y)
        
    def move_to(self, new_x, new_y):
        """Change the coordinates of this Point"""
        self.x = new_x
        self.y = new_y

m = Point(3,4)
n = Point(5,6)
d = m.move_to(n)
print()
