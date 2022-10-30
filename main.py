###=================================================
# This file is where you need to create a plan to reach the goal state form the initial state
# This file must accept any combination of with the given blocks: A, B, C, D, E
# This file should also reach the final state of any combination with the blocks above
# It must also display all intermediate states
###=================================================

from state import State


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

        if block1.clear:
            block1.on = None
            block1.air = True

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
            block2.clear = False
            block1.air = False

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


    def findNeighbours(self, node):

        table = State.find(self.initial_state, "table")

        neighbours = []

        for block in State.blocks():
            if block.clear:
                if block.air:
                    #add putdown to queue, add stack to queue
                else:
                    if block.on:
                         # add unstack to queue
                    else:
                        #add pickup to queue
            # if bottom block is supposed to be on table dont add to list

        #pass in current state of blocks so we can check each block?

        #for block in blocks:
        if node.clear:
            if node.on == table:
                print("blank")
                

    # def heuristic(self):


    # Depth First Search Will
    def dfs(self, node, visited, goal):
        if visited is None:
            visited = []
            visited.append(node)

        node.neighbours = findNeighbours(node)

        for neighbour in node.neighbours:
            if neighbour not in visited:
                visited.append(node)
                if neighbour == goal:
                    print("Solution path: ")
                    #return pathgen(neighbour)
                else:
                    return dfs(neighbour, visited, goal)

    # Depth First Search Jaden
    def dfs_jaden(self):

        # Cases
        # If block is on top and not on table and supposed to be on table, then put on table
        # If block is in middle of two blocks and the one on top is supposed to be on the block in the middle,
        # then move the top block to the table and then put the block under it on the block it should be on then put the top block on top
        # 3 stacked blocked ???


        frontier = [initial_state]
        order = []

        while True:
            if not frontier:
                return ["No Solution"]

            current = frontier.pop()
            order.append(current)
            current.total += current.val

            if current.total == path_sum:
                current.total = 0
                break
            else:
                for child in current.children:
                    child.parent = current
                    child.total += current.total
                    frontier.append(child)
                    current.total = 0

        # Return Path
        path = []
        node = order.pop()
        while node:
            path.insert(0, node)
            node = node.parent

        return path


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

