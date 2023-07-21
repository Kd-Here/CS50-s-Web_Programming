import sys

class Node():
    def __init__(self, state, parent, action):
        self.state = state          #It represents the current state associated with the node.
        self.parent = parent        #It represents the parent node from which the current node is derived.
        self.action = action        #It represents the action taken to transition from the parent node to the current node.



"""

StackFrontier class creates 
frontier list - Which stores initial node, remove the node from frontier if it's goal state stop 
if not expand node add resulting nodes to frontier

"""
class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(i.state == state for i in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

class Maze():

    def __init__(self, filename):

        # Read file and set height and width of maze
        with open(filename) as f:
            contents = f.read()

        # Validate start and goal
        if contents.count("A") != 1:
            raise Exception("maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one goal")

        # Determine height and width of maze
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(single_line) for single_line in contents)


        # Keep track of walls
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j) #Getting A in i (height),j(width)
                        row.append(False)

                    elif contents[i][j] == "B":
                        self.goal = (i, j)  #Getting B in i (height),j(width)
                        row.append(False)

                    elif contents[i][j] == " ":
                        row.append(False)   #Getting ' ' in i (height),j(width)

                    else:
                        row.append(True)    #Getting # in i (height),j(width)
                except IndexError:
                    row.append(False)
            self.walls.append(row)         #self.walls is list with len 6 and each element is list of len 7
            
        self.solution = None


    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()

        for i, row in enumerate(self.walls): #first loop for considering walls
            for j, col in enumerate(row):    #second loop is for accessing each element of wall


                if col:                      #If columns are true means the are border wall          
                    print("|", end="")

                elif (i, j) == self.start:   # elif row index & column index are (5,0) which is our position for A i.e. start we get it by looking contents
                    print("A", end="")

                elif (i, j) == self.goal:    # elif row index & column index are (0,5) which is our position for B i.e. start we get it by looking contents
                    print("B", end="")

                elif solution is not None and (i, j) in solution:      #This is our path where we can move to reach goal
                    print("*", end="")          

                else:
                    print(" ", end="")
            print()
        print()


    def neighbors(self, Cur_state):
        
        '''
            This function is used to see neighbors i.e (all possible next state we can move from Current state) of Current state
            It takes tuple as Cur_state and split that in row, col
            & returns the result i.e. actions with r & c of possible neighbors state  

            all_possible_actions_in_maze_problem is list of all possible actions and there corresponding row & col changes
            result is list to store neighbors

            So from each Cur_state we perform do check all_possible_actions_in_maze_problem and only possible actions are append in results

            eg. Cur_state = (5,0)
            For loop iteration

            ✔️ 1) For the first tuple: ("up", (5 - 1, 0)) = ("up", (4, 0))
                The condition checks if 0 <= 4 < self.height (True) and 0 <= 0 < self.width (True) and not self.walls[4][0] (not False, which is True). So the condition is True, and it prints ("up", (4, 0)).
            ❌ 2) For the second tuple: ("down", (5 + 1, 0)) = ("down", (6, 0))
                The condition checks if 0 <= 6 < self.height (False) and 0 <= 0 < self.width (True). 
            ❌ 3) For the third tuple: ("left", (5, 0 - 1)) = ("left", (5, -1))
            ❌ 4) For the fourth tuple: ("right", (5, 0 + 1)) = ("right", (5, 1))
                    Here if 0 <= 5 < self.height (True) and 0 <= 1 < self.width (True) and not self.walls[5][1] (not False, which is True).
                    Bcoz see self.walls[5][1] is wall so movement ther

        '''
    
        row, col = Cur_state
        all_possible_actions_in_maze_problem = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []
        for action, (r, c) in all_possible_actions_in_maze_problem:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result


    def solve(self):
        """Finds a solution to maze, if one exists."""

        # Keep track of number of states explored
        self.num_explored = 0

        # Initialize frontier to just the starting position
        start = Node(state=self.start, parent=None, action=None)
        print("\n\nStarting the solution\n")
        frontier = StackFrontier()
        print("Added starting state with A as frontier start whose co-ordinates are",start.state)
        frontier.add(start)

        # Initialize an empty explored set
        self.explored = set()

        # Keep looping until solution found
        while True:

            # If nothing left in frontier, then no path
            if frontier.empty():
                raise Exception("no solution")

            # Choose a node from the frontier
            node = frontier.remove()
            print("Node removed by frontier",node.state)
            self.num_explored += 1

            # If node is the goal, then we have a solution i.e. Curstate == B state
            if node.state == self.goal:
                print("Hurrah we found the current state {} same as goal state {}".format(node.state, self.goal))
                actions = [] 
                cells = []
                print("Now with current node we will backtrack to all parent node and save their state & actions")
                print("This is {} goal state we reached it's parent node state is {}\n Now will retrack our parent state till we at start state".format(node.state,node.parent.state))
                
                while node.parent is not None:
                    #node is current node node.parent is parent &  node action are appended in actions list, cells is current state
                    actions.append(node.action)
                    cells.append(node.state)

                    node = node.parent
                    # Understand the logic node is current node & node.parent is parent we assign node.parent to node (parent now become child find it's parent) means our current node is backtracking 
                
                actions.reverse()
                cells.reverse()
                # We are backtracking thus from starting positions everything must be reversed
                self.solution = (actions, cells)
                print("This are actions {} and this are actions resulting_cells {}".format(actions, cells))
                return

            # If node was not goal state then Current node state as explored
            self.explored.add(node.state)
            print("This is set to keep track of explored nodes",self.explored)


            # Add neighbors to frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)
                    print("New node added to frontier{} whose parent is {} and actions is {}".format(child.state,node.state,action))
            print("\n")

    def output_image(self, filename, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw
        cell_size = 50
        cell_border = 2

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                # Walls
                if col:
                    fill = (40, 40, 40)

                # Start
                elif (i, j) == self.start:
                    fill = (255, 0, 0)

                # Goal
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)

                # Solution
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)

                # Explored
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)

                # Empty cell
                else:
                    fill = (237, 240, 252)

                # Draw cell
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )

        img.save(filename)


if len(sys.argv) != 2:
    sys.exit("Usage: python maze.py maze.txt")

m = Maze(sys.argv[1])
print("Maze:")
m.print()
print("Solving...")
m.solve()
print("States Explored:", m.num_explored)
print("Solution:")
m.print()
m.output_image("maze.png", show_explored=True)
