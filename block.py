###=================================================
# This file contains the code which creates blocks.
########### everything in the worlds is a block object
########### Each block object has the following attributes:
#################### type: Triangle, square, table
#################### id: "A", "B",....
#################### on = None, Block_object_A, ....
#################### clear = True, False
#################### air = True, False
# I created square and triangle blocks. However, we only use square for the main project
# You can use a triangle block for the extra credit
###=================================================

# single block, a square, a triangle, or a table. These are the blocks of which
# scenes are composed.
# Possible predicates involving blocks:
#   -square(x)
#   -triangle(x)
#   -table(x)
#   -clear(x)
#   -on(x,y)
class Block:
    SQUARE = 1  # constant
    TRIANGLE = 2
    TABLE = 3

    def __init__(self, type, id):
        self.type = type
        self.id = id
        self.on = None
        self.clear = True
        self.air = False

    # place self block onto onto block
    def place(self, onto):

        if self.on:
            self.on.clear()
        self.on = onto
        self.on.unclear()

    # set the block to not clear
    def unclear(self):
        self.clear = False

    # set the block to clear
    def clear(self):
        self.clear = True

    def __str__(self):
        return self.id

    def __repr__(self):
        return self.id

    def __eq__(self, other):
        try:
            if self.id == other.id and self.on.id == other.on.id and self.clear == other.clear and self.air == other.air:
                return True
        except Exception:
            return False

    def __ne__(self, other):
        try:
            if self.id != other.id or self.on != other.on or self.clear != other.clear or self.air != other.air:
                return True
        except Exception:
            return False
