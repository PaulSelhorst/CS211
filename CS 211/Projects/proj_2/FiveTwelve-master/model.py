"""
The game state and logic (model component) of 512, 
a game based on 2048 with a few changes. 
This is the 'model' part of the model-view-controller
construction plan.  It must NOT depend on any
particular view component, but it produces event 
notifications to trigger view updates. 
"""

from game_element import GameElement, GameEvent, EventKind
from typing import List, Tuple, Optional
import random

# Configuration constants
GRID_SIZE = 4

class Vec():
    """A Vec is an (x,y) or (row, column) pair that
    represents distance along two orthogonal axes.
    Interpreted as a position, a Vec represents
    distance from (0,0).  Interpreted as movement,
    it represents distance from another position.
    Thus we can add two Vecs to get a Vec.
    """
    #Fixme:  We need a constructor, and __add__ method, and __eq__.
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
    def __add__(self, other: 'Vec') -> 'Vec':
        return Vec(self.x + other.x, self.y + other.y)
    
    def __eq__(self, other: 'Vec') -> bool:
        return self.x == other.x and self.y == other.y


class Tile(GameElement):
    """A slidy numbered thing."""

    def __init__(self, pos: Vec, value: int):
        super().__init__()
        self.row = pos.x
        self.col = pos.y
        self.value = value

    def __eq__(self, other: "Tile") -> bool:
        if not isinstance(other, Tile):
            return False
        return self.value == other.value
      
    def merge(self, other: "Tile"):
        # This tile incorporates the value of the other tile
        self.value = self.value + other.value
        self.notify_all(GameEvent(EventKind.tile_updated, self))
        # The other tile has been absorbed.  Resistance was futile.
        other.notify_all(GameEvent(EventKind.tile_removed, other))

    def move_to(self, new_pos: Vec):
        self.row = new_pos.x
        self.col = new_pos.y
        self.notify_all(GameEvent(EventKind.tile_updated, self))



class Board(GameElement):
    """The game grid.  Inherits 'add_listener' and 'notify_all'
    methods from game_element.GameElement so that the game
    can be displayed graphically.
    """

    def __init__(self, rows=4, cols=4):
        super().__init__()
        self.tiles = [[None for _ in range(cols)] for _ in range(rows)]
        self.rows = rows
        self.cols = cols
        

    def has_empty(self) -> bool:
        """Write the method has_empty for Board, which returns True if the Board contains at least
        one empty square (False if the Board is full.) This method is straightforward; no points, just
        practice."""
        for row in self.tiles:
            for tile in row:
                if tile is None:
                    return True
        return False
    
    def to_list(self) -> List[List[int]]:
        """Test scaffolding: represent each Tile by its
        integer value and empty positions as 0
        """
        result = [ ]
        for row in self.tiles:
            row_values = []
            for col in row:
                if col is None:
                    row_values.append(0)
                else:
                    row_values.append(col.value)
            result.append(row_values)
        return result
    
    def from_list(self, lst: List[List[int]]):
        """Test scaffolding: set the board from a list
        of lists of integers.
        """
        for i, row in enumerate(lst):
            for j, value in enumerate(row):
                if value == 0:
                    self.tiles[i][j] = None
                else:
                    self.tiles[i][j] = Tile(Vec(i, j), value)

    def slide(self, pos: Vec,  dir: Vec):
        """Slide tile at row,col (if any)
        in direction (dx,dy) until it bumps into
        another tile or the edge of the board.
        """
        if self[pos] is None:
            return
        while True:
            new_pos = pos + dir
            if not self.in_bounds(new_pos):
                break
            if self[new_pos] is None:
                self._move_tile(pos, new_pos)
            elif self[pos] == self[new_pos]:
                self[pos].merge(self[new_pos])
                self._move_tile(pos, new_pos)
                break  # Stop moving when we merge with another tile
            else:
                # Stuck against another tile
                break
            pos = new_pos

    def _move_tile(self, old_pos: Vec, new_pos: Vec):
        """Write a method called _move_tile for Board that factors out the similarities between
        moving onto an empty space and a space occupied by a tile with the same value."""
        if self[old_pos] is None:
            return
        self[old_pos].move_to(new_pos)
        self[new_pos] = self[old_pos]
        self[old_pos] = None

        

    def in_bounds(self, pos: Vec) -> bool:
        """Write a method in_bounds for Board, which receives a position (a vector) and returns True
        if the position is within the Board's boundaries. """
        return 0 <= pos.x < len(self.tiles) and 0 <= pos.y < len(self.tiles[0])
    
    def place_tile(self, value=None):
        """Place a tile on a randomly chosen empty square."""
        empties = self._empty_positions()
        assert len(empties) > 0
        choice = random.choice(empties)
        row, col = choice.x, choice.y
        if value is None:
            # 0.1 probability of 4
            if random.random() < 0.1:
                value = 4
            else:
                value = 2
        self.tiles[row][col] = Tile(Vec(row, col), value)
        self.notify_all(GameEvent(EventKind.tile_created, self.tiles[row][col]))

    def _empty_positions(self) -> list:
        empties = [ ]
        for row in self.tiles:
            for col in row:
                if col is None:
                    empties.append(col)
        return empties

    def score(self) -> int:
        """Calculate a score from the board.
        (Differs from classic 1024, which calculates score
        based on sequence of moves rather than state of
        board.
        """
        return 0
        #FIXME
    
    def __getitem__(self, pos: Vec) -> Tile:
        return self.tiles[pos.x][pos.y]

    def __setitem__(self, pos: Vec, tile: Tile):
        self.tiles[pos.x][pos.y] = tile

    def _empty_positions(self) -> list[Vec]:
        """Return a list of positions of None values,
        i.e., unoccupied spaces.
        """
        empties = [ ]
        for i, row in enumerate(self.tiles):
            for j, tile in enumerate(row):
                if tile is None:
                    empties.append(Vec(i, j))
        return empties

    def right(self):
        for i in range(self.rows):
            for j in range(self.cols-1, -1, -1):
                self.slide(Vec(i, j), Vec(0, 1))
    
    def left(self):
        for i in range(self.rows):
            for j in range(1, self.cols):
                self.slide(Vec(i, j), Vec(0, -1))
    
    def up(self):
        for j in range(self.cols):
            for i in range(1, self.rows):
                self.slide(Vec(i, j), Vec(-1, 0))
    
    def down(self):
        for j in range(self.cols):
            for i in range(self.rows-1, -1, -1):
                self.slide(Vec(i, j), Vec(1, 0))
    
    def score(self) -> int:
        """Calculate a score from the board.
        (Differs from classic 1024, which calculates score
        based on sequence of moves rather than state of
        board.
        """
        score = 0
        for row in self.tiles:
            for tile in row:
                if tile is not None:
                    score += tile.value
        return score