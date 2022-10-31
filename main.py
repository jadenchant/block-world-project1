###=================================================
# This file is where you need to create a plan to reach the goal state form the initial state
# This file must accept any combination of with the given blocks: A, B, C, D, E
# This file should also reach the final state of any combination with the blocks above
# It must also display all intermediate states
###=================================================

from state import State

class Move:
    def __init__(self, action, block1, block2=None):
        self.block1 = block1
        self.block2 = block2
        self.action = action
        self.neighbours = []

class Plan:

    def __init__(self, initial_state, goal_state):
        """
        Initialize initial state and goal state
        :param initial_state: list of blocks in the initial state
        :type initial_state: list of block.Block objects
        :param goal_state: list of blocks in the goal state
        :type initial_state: list of block.Block objects
        """
        self.initial_state = initial_state
        self.goal_state = goal_state

    def pickup(self, block1):
        """
        Operator to pick up the block off the table
        :param block1: block1 to pick up off the table
        :type block1: Object of block.Block
        :return: None
        """

        # get table object from initial state
        table = State.find(self.initial_state, "table")

        if block1.clear and block1.on == table:
            block1.on = None
            block1.air = True
        else:
            raise ValueError("pickup move is not allowed")

    def putdown(self, block1):
        """
        Operator to put the block on the table
        :param block1: block1 to put on the table
        :type block1: Object of block.Block
        :return: None
        """

        # get table object from initial state
        table = State.find(self.initial_state, "table")

        if block1.air:
            block1.on = table
            block1.clear = True
            block1.air = False
        else:
            raise ValueError("putdown move is not allowed")

    def stack(self, block1, block2):
        """
        Operator to stack block1 on block 2
        :param block1: block1 to stack from block2
        :type block1: Object of block.Block
        :type block2: Object of block.Block
        :return: None
        """

        if block2.clear and block1.air:
            block1.on = block2
            block1.clear = True
            block2.clear = False
            block1.air = False
        else:
            raise ValueError("stack move is not allowed")

    def unstack(self, block1, block2):
        """
        Operator to unstack block1 from block 2
        :param block1: block1 to unstack from block2
        :type block1: Object of block.Block
        :type block2: Object of block.Block
        :return: None
        """

        # if block1 is clear safe to unstack
        if block1.clear:

            # block1 should be in air
            # block1 should not be on block2
            # set block2 to clear (because block1 is in air)
            block1.clear = False
            block1.air = True
            block1.on = None

            block2.clear = True
        else:
            raise ValueError("unstack move is not allowed")

    # Dummy function
    def move(self):
        """
        # Operator to move block1 to a location
        # :param block1: block1 to move
        # :type block1: Object of block.Block
        # :type location: Object of location
        # :return: None
        """

        # if block1.clear:
        #     self.pickup(block1)
        #     if location.clear:
        #         # putdown on location
        #         self.putdown(block1)

    def undo(self, move, block1, block2 = None):
        """
        # Undo last move
        :param move: string of move
        :param block1: Object of block.Block
        :param block2: Object of block.Block
        :return: None
        """

        if move == "pickup":
            self.putdown(block1)
        elif move == "putdown":
            self.pickup(block1)
        elif move == "stack":
            self.unstack(block1, block2)
        elif move == "unstack":
            self.stack(block1, block2)
        else:
            raise ValueError("move is not found")

    # func neighbors(self, current_state):
    def neighbors(self, current_state):
        # Make 5 lists: putdown, unstack, stack, pickup
        putdownList = []
        unstackList = []
        stackList = []
        pickupList = []

        # Make a copy of the current state
        new_state = current_state

        # Make a tables with the initial_state
        table = State.find(self.initial_state, "table")

        # blocks in the air list
        # loop through each block in the state and check whether the block is in the air
        # Add those blocks into the list


        # blocks on the table and clear list
        # loop through each block in the state and check the appropriate conditions for
        # the blocks to be on table and clear
        # Add those blocks into the list

        # blocks that are clear and not on the table
        # loop through each block in the state and check the appropriate conditions for
        # the blocks to be not on table and clear
        # Add those blocks into the list

        # if block in air list have element(s) then only do putdown and stack
        # putdown
        # copy the state
        # get the equivalent block from the copied state
        # apply the operator
        # add those into the putdown list
        # stack
        # it is a combination of (blocks_air & blocks_clear) (itertool recommendation)
        # loop through all combinations:
        # make a copy
        # get the equivalent block from the copied state
        # apply operator for the two blocks in the operator
        # add those into stack list (made in the previous step)

        # if the block is not in the air - options: pickup, unstack, move (the steps for these should be somewhat the same as putdown and stack)
        # pickup options
        # apply pick operator on all blocks that are clear and are on the table
        # Add those into the pick list (made in the previous step)
        # unstack
        # apply unstack operator to all blocks that are clear and are not on table
        # Add those into the unstack list (made in the previous step)
        # move
        # apply move operator to all blocks that are clear and not on the table to any block that is clear
        # it is the combination of blocks that are clear and not on table with blocks are simply clear (itertools recommendation)

        # return all five lists


    # Old Neighbors
    def findNeighbours(self):

        table = State.find(self.initial_state, "table")

        neighbours = []

        for block in State.blocks():
            if block.clear:
                if block.air:
                    neighbours.append(Move("putdown", block))
                    for stackedBlock in State.blocks():
                        if stackedBlock.clear:
                            neighbours.append(Move("stack", block, stackedBlock))
                    # add putdown to queue, add stack to queue
                else:
                    if block.on != table:
                        neighbours.append(Move("unstack", block, block.on))
                         # add unstack to queue
                    else:
                        neighbours.append(Move("pickup", block))
                        # add pickup to queue

        return neighbours
        #for block in blocks:
        # if node.clear:
        #     if node.on == table:
        #         print("blank")
                

    # def heuristic(self):


    # Depth First Search
    def dfs(self, visited, goal, move=None):
        if visited is None:
            visited = []
            #visited.append(move)

        if move is not None:
            if move.action == "putdown":
                self.putdown(move.block1)
            if move.action == "stack":
                self.stack(move.block1, move.block2)
            if move.action == "pickup":
                self.pickup(move.block1)
            if move.action == "unstack":
                self.unstack(move.block1, move.block2)

        if State.blocks() == goal_state.blocks():
            # return path, search complete

        move.neighbours = self.findNeighbours()

        for neighbour in move.neighbours:
            if neighbour not in visited:
                visited.append(move)
                return self.dfs(visited, goal, neighbour)
        self.undo(move.action, move.block1, move.block2)

    # Depth First Search Jaden
    def dfs_jaden(self):
        # Cases
        # If block is on top and not on table and supposed to be on table, then put on table
        # If block is on top and not on
        # If block is in middle of two blocks and the one on top is supposed to be on the block in the middle,
        # then move the top block to the table and then put the block under it on the block it should be on then put the top block on top
        # 3 stacked blocked ???


    # Greedy Best First Search (if time allows)
    # def gbfs(self):

    def sample_plan(self):

        # get the specific block objects
        # Then, write code to understand the block i.e., if it is clear (or) on table, etc.
        # Then, write code to perform actions using the operators (pick-up, stack, unstack).

        # Below I manually hardcoded the plan for the current initial and goal state
        # You must automate this code such that it would produce a plan for any initial and goal states.

        block_c = State.find(self.initial_state, "C")
        block_d = State.find(self.initial_state, "D")

        # Unstack the block
        self.unstack(block_d, block_c)

        # print the state
        action = f"unstack{block_d, block_c}"
        State.display(self.initial_state, message=action)

        # put the block on the table
        self.putdown(block_d)

        # print the state
        action = f"Putdown({block_d}, table)"
        State.display(self.initial_state, message=action)


if __name__ == "__main__":

    # get the initial state
    initial_state = State()
    initial_state_blocks = initial_state.create_state_from_file("input.txt")

    #display initial state
    State.display(initial_state_blocks, message="Initial State")

    # get the goal state
    goal_state = State()
    goal_state_blocks = goal_state.create_state_from_file("goal.txt")

    #display goal state
    State.display(goal_state_blocks, message="Goal State")

    """
    Sample Plan
    """

    p = Plan(initial_state_blocks, goal_state_blocks)
    p.sample_plan()

