###=================================================
# This file is where you need to create a plan to reach the goal state form the initial state
# This file must accept any combination of with the given blocks: A, B, C, D, E
# This file should also reach the final state of any combination with the blocks above
# It must also display all intermediate states
###=================================================

from state import State
import copy

class Move:
    def __init__(self, action, block1, block2=None):
        self.block1 = block1
        self.block2 = block2
        self.action = action
        self.neighbours = []

    def __eq__(self, other):
        if self.block1 == other.block1 and self.action == other.action and self.block2 == other.block2:
            return True
        else:
            return False

    def __ne__(self, other):
        if self.block1 != other.block1 or self.action != other.action or self.block2 != other.block2:
            return True
        else:
            return False


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

        if block1.clear and block1.on and block1.on.id == "table":
            block1.on = None
            block1.air = True
            block1.clear = False
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

    def undo(self, move, block1, block2=None):
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
        """
        Neighbors function
        :param current_state: Object of state.State
        :return: 5 Lists of possible states
        """

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
        airList = []
        # loop through each block in the state and check whether the block is in the air
        # Add those blocks into the list
        for block in current_state.blocks():
            if block.air:
                airList.append(block)

        # blocks on the table and clear list
        table_clearList = []
        # loop through each block in the state and check the appropriate conditions for
        # the blocks to be on table and clear
        # Add those blocks into the list
        for block in current_state.blocks():
            if block.on == table and block.clear:
                table_clearList.append(block)

        # blocks that are clear and not on the table
        not_table_clearList = []
        # loop through each block in the state and check the appropriate conditions for
        # the blocks to be not on table and clear
        # Add those blocks into the list
        for block in current_state.blocks():
            if block.on != table and block.clear:
                not_table_clearList.append(block)

    # Old Neighbors
    def findNeighbours(self, current_state):

        table = State.find(self.initial_state, "table")

        neighbours = []
        handsfull = False

        for block in current_state:
            if block.air:
                handsfull = True

        for block in current_state:
            if block.air:
                neighbours.append(Move("putdown", block))
                for stackedBlock in current_state:
                    if stackedBlock.clear and stackedBlock != block:
                        neighbours.append(Move("stack", block, stackedBlock))
                # add putdown to queue, add stack to queue
            else:
                if handsfull is False and block.clear:
                    if block.on.id != "table":
                        if State.find(goal_state.blocks, block.id).on.id != block.on.id:
                            neighbours.append(Move("unstack", block, block.on))
                        # add unstack to queue
                    else:
                        if State.find(goal_state.blocks, block.id).on.id != "table":
                            neighbours.append(Move("pickup", block))
                        # add pickup to queue

        return neighbours

    # Depth First Search
    def dfs(self, imove=None, istate=None, ivisited=None):
        solutionFound = True

        #initialize variables, set variables equal to parameters being passed in
        move = copy.deepcopy(imove)
        state = copy.deepcopy(istate)
        visited = copy.deepcopy(ivisited)

        if visited is None:
            visited = []

        if state is None:
            state = copy.deepcopy(self.initial_state)

        if move is not None:

            if move.action == "putdown":
                self.putdown(move.block1)
                action = f"putdown{move.block1}"
                print("putdown")
                State.display(state, message=action)
            if move.action == "stack":
                self.stack(move.block1, move.block2)
                action = f"stack{move.block1, move.block2}"
                print("stack")
                State.display(state, message=action)
            if move.action == "pickup":
                self.pickup(move.block1)
                action = f"pickup{move.block1}"
                print("pickup")
                State.display(state, message=action)
            if move.action == "unstack":
                self.unstack(move.block1, move.block2)
                action = f"unstack{move.block1, move.block2}"
                print("unstack")
                State.display(state, message=action)

            updatedState = []
            for block in state:
                if block.id == move.block1.id:
                    updatedState.append(move.block1)
                elif move.block2 is not None:
                    if block.id == move.block2.id:
                        updatedState.append(move.block2)
                    else:
                        updatedState.append(block)
                else:
                    updatedState.append(block)
            state = copy.deepcopy(updatedState)


        if move is None:
            move = Move(None, None)

        move.neighbours = self.findNeighbours(state)


        # this block checks to see if we've found the solution or not
        block_names = []
        for init_block in self.initial_state:
            block_names.append(init_block.id)
        for block in block_names:
            state_block = State.find(state, block)
            goal_block = State.find(self.goal_state, block)
            if state_block.id != goal_block.id or state_block.on != goal_block.on or state_block.air != goal_block.air:
                solutionFound = False

        if solutionFound:
            print("Solution found!")
            #return "Solution found!"
            exit()
        else:
            for neighbour in move.neighbours:
                if neighbour not in visited:
                    visited.append(neighbour)
                    self.dfs(neighbour, state, visited)

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

    p = Plan(initial_state_blocks, goal_state_blocks)
    p.dfs(None)

