import os

import time

import resource

import sys

import math

import Queue as Q

def memory_usage_resource():
    rusage_denom = 1024.
    if sys.platform == 'darwin':
        rusage_denom = rusage_denom * rusage_denom
    mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / rusage_denom
    return mem


class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def put(self, item):
        self.items.insert(0,item)

    def get(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

    def getList(self):
        return self.items

    def exists(self, item):
        return item in self.items


class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

    def getList(self):
        return self.items

    def exists(self, item):
        return item in self.items

class StatePQ(object):

    def __init__(self):
        self.queue = []

    def __str__(self):
        return ' '.join([state.display() for state in self.queue])

    # for checking if the queue is empty
    def isEmpty(self):
        return len(self.queue) == []

    # for inserting an element in the queue
    def push(self, state):
        self.queue.append(state)

    # for popping an element based on Priority
    def pop(self):
        try:
            min = len(self.queue) -1
            min_cost = 0

            for i in reversed(range(len(self.queue))):
                if self.queue[i].cost < self.queue[min].cost:
                    min = i
                    min_cost = self.queue[min].cost

            state = self.queue[min]
            del self.queue[min]

            return state
        except IndexError:
            print()
            exit()

class Visited:
    def __init__(self):
        self.visited = {}

    def addVisited(self, config_list):

        #### DEBUG:
        ##print config_list

        self.visited = addElem(config_list, self.visited)

        #### DEBUG:
        ##print self.visited

    def isVisited(self, config_list):

        return checkElem(config_list, self.visited)


def addElem(config_list, dictionary): ## it took me 3 DAYS to think of this!!!!


    num = config_list.pop(0)

    if len(config_list) == 0: ## if its the end of the line just put an OK

        dictionary[num] = 'OK'

    elif dictionary is None or dictionary.get(num) is None: ## if there is no existing route

        subdict = {}

        dictionary[num] = addElem(config_list, subdict) ## add route

    else:

        addElem(config_list, dictionary.get(num)) ## if there is skip and go to the next level

    return dictionary


def checkElem(config_list, dictionary):

    num = config_list.pop(0)

    if dictionary.get(num) == 'OK':
        return 1

    elif dictionary is None or dictionary.get(num) is None:
        return 0

    if checkElem(config_list, dictionary.get(num)):
        return 1

    else:
        return 0

#### SKELETON CODE ####

## The Class that Represents the Puzzle

class PuzzleState(object):

    """docstring for PuzzleState"""

    def __init__(self, config, n, parent=None, action="Initial", cost=0):

        if n*n != len(config) or n < 2:

            raise Exception("the length of config is not correct!")

        self.n = n

        self.cost = cost

        self.parent = parent

        self.action = action

        self.dimension = n

        self.config = config

        self.children = []

        self.level = 0

        for i, item in enumerate(self.config):

            if item == 0:

                self.blank_row = i / self.n

                self.blank_col = i % self.n

                break

    def display(self):

        for i in range(self.n):  ## iterates the number of times of n

            line = []  ## creates n lines, each line an array of positions

            offset = i * self.n  ## each line n positions

            for j in range(self.n):

                line.append(self.config[offset + j])  ##insert configuration in each position

            print line ## print a line each time

    def move_left(self):

        if self.blank_col == 0: ## if blank is on the leftmost column...

            return None  ## can't go left

        else:

            blank_index = self.blank_row * self.n + self.blank_col  ## get position of left to blanck in the array

            target = blank_index - 1  ## this is the position where blank currently is

            new_config = list(self.config)  ## create new state

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]  ## switch numbers

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Left", cost=self.cost + 1)

    def move_right(self):

        if self.blank_col == self.n - 1:

            return None

        else:

            blank_index = self.blank_row * self.n + self.blank_col

            target = blank_index + 1

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Right", cost=self.cost + 1)

    def move_up(self):

        if self.blank_row == 0:

            return None

        else:

            blank_index = self.blank_row * self.n + self.blank_col

            target = blank_index - self.n

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Up", cost=self.cost + 1)

    def move_down(self):

        if self.blank_row == self.n - 1:

            return None

        else:

            blank_index = self.blank_row * self.n + self.blank_col

            target = blank_index + self.n

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Down", cost=self.cost + 1)


    def expand(self):

        """expand the node"""

        # add child nodes in order of UDLR

        if len(self.children) == 0:

            up_child = self.move_up()

            if up_child is not None:

                self.children.append(up_child)

            down_child = self.move_down()

            if down_child is not None:

                self.children.append(down_child)

            left_child = self.move_left()

            if left_child is not None:

                self.children.append(left_child)

            right_child = self.move_right()

            if right_child is not None:

                self.children.append(right_child)

        return self.children

    def expand_reverse(self):

        """expand the node"""

        # add child nodes in order of RLDU

        if len(self.children) == 0:

            right_child = self.move_right()

            if right_child is not None:

                self.children.append(right_child)

            left_child = self.move_left()

            if left_child is not None:

                self.children.append(left_child)

            down_child = self.move_down()

            if down_child is not None:

                self.children.append(down_child)

            up_child = self.move_up()

            if up_child is not None:

                self.children.append(up_child)

        return self.children

# Function that Writes to output.txt

### Students need to change the method to have the corresponding parameters

def writeOutput(path_to_goal, cost_of_path, nodes_expanded, search_depth, max_search_depth, running_time, max_ram_usage ):

    filename = "output.txt"

    if os.path.exists(filename):
        append_write = 'a' # append if already exists
    else:
        append_write = 'w' # make a new file if not

    file = open(filename,append_write)
    file.write("path_to_goal: " + str(path_to_goal))
    file.write("\ncost_of_path: " + str(cost_of_path))
    file.write("\nnodes_expanded: " + str(nodes_expanded))
    file.write("\nsearch_depth: " + str(search_depth))
    file.write("\nmax_search_depth: " + str(max_search_depth))
    file.write("\nrunning_time: " + str(round(running_time,8)))
    file.write("\nmax_ram_usage: " + str(round(max_ram_usage,8)))
    file.write("\n")
    file.close()


def bfs_search(initial_state):

    """BFS search"""

    ## Output variables initialize
    starting_time = time.time()
    nodes_expanded = 0
    max_search_depth = 0

    ## Initialize Frontier and Explored lists
    frontier = Queue()
    frontier.put(initial_state)
    visited = Visited()
    visited.addVisited(list(initial_state.config))

    while not frontier.isEmpty():

        ##Explore state
        state = frontier.get()
        visited.addVisited(list(state.config))

        #### DEBUG:
        ##print('Getting: ')
        ##state.display()

        if test_goal(state):

            ##Stop Clock
            running_time = time.time() - starting_time

            ##Log Depth of Solution
            search_depth = state.level

            ##Calculate path to goal
            path_to_goal = []
            path_to_goal.append(state.action)
            cost_of_path = state.cost
            parent_state = state.parent

            while parent_state.parent != None:

                path_to_goal.append(parent_state.action)
                cost_of_path += parent_state.cost

                parent_state = parent_state.parent

            path_to_goal.reverse()

            ##Calculate max memory usage
            max_ram_usage = memory_usage_resource()

            ##Write File
            writeOutput(path_to_goal, cost_of_path , nodes_expanded, search_depth, max_search_depth, running_time, max_ram_usage)

            ##Exist program
            return 1

        ##Goal not achieved, expand state and increase number of expanded nodes
        state.expand()
        nodes_expanded +=  1

        #### DEBUG:
        ##print nodes_expanded

        for child_state in state.children:

            ## Update output variables
            child_state.level = state.level + 1
            child_state.parent = state
            child_state.cost = 1

            ## Reset state skipping flag
            repeated_state = 0


            ## Check if state already exists in frontier
            for child_state in state.children:

                if not visited.isVisited(list(child_state.config)):

                    #### DEBUG:
                    ##print('Pushing: ')
                    ##child_state.display()

                    ## Update output variables
                    child_state.level = state.level + 1
                    child_state.parent = state

                    ## Put child in frontier
                    frontier.put(child_state)
                    visited.addVisited(list(child_state.config))

                    ## Update max depth if needed
                    if child_state.level > max_search_depth:
                        max_search_depth = child_state.level


    return 0


def dfs_search(initial_state):

    """DFS search"""

    ## Output variables initialize
    starting_time = time.time()
    nodes_expanded = 0
    max_search_depth = 0

    ## Initialize Frontier and Explored lists
    frontier = Stack()
    frontier.push(initial_state)
    visited = Visited()  ## will include frontier and explored states
    visited.addVisited(list(initial_state.config))

    while not frontier.isEmpty():

        ##Explore state
        state = frontier.pop()

        #### DEBUG:
        ##print('Popping: ')
        ##state.display()

        visited.addVisited(list(state.config))

        if test_goal(state):

            ##Stop Clock
            running_time = time.time() - starting_time

            ##Log Depth of Solution
            search_depth = state.level

            ##Calculate path to goal
            path_to_goal = []
            path_to_goal.append(state.action)
            cost_of_path = state.cost
            parent_state = state.parent

            while parent_state.parent != None:

                path_to_goal.append(parent_state.action)
                cost_of_path += parent_state.cost

                parent_state = parent_state.parent


            path_to_goal.reverse()

            ##Calculate max memory usage
            max_ram_usage = memory_usage_resource()

            ##Write File
            writeOutput(path_to_goal, cost_of_path , nodes_expanded, search_depth, max_search_depth, running_time, max_ram_usage)

            ##Exist program
            return 1

        ##Goal not achieved, expand state and increase number of expanded nodes
        state.expand_reverse()  ##Reverse UDLR expansion
        nodes_expanded +=  1

        #### DEBUG:
        ##print nodes_expanded

        for child_state in state.children:

            if not visited.isVisited(list(child_state.config)):

                #### DEBUG:
                ##print('Pushing: ')
                ##child_state.display()

                ## Update output variables
                child_state.level = state.level + 1
                child_state.parent = state
                child_state.cost = 1

                ## Put child in frontier
                frontier.push(child_state)
                visited.addVisited(list(child_state.config))

                ## Update max depth if needed
                if child_state.level > max_search_depth:
                    max_search_depth = child_state.level

    return 0

def HeuristicCalc(state):

    heuristic_cost = 0

    for i, item in enumerate(state.config):

        if item != 0:

            cur_row = i / state.n
            cur_col = i % state.n

            target_row = item / state.n
            target_col = item % state.n

            ### DEBUG:
            ##print "current row: " + str(cur_row)
            ##print "target row: " + str(target_row)
            ##print "current col: " + str(cur_col)
            ##print "target col: " + str(target_col)

            item_cost = abs(cur_row - target_row) + abs(cur_col - target_col)

            ### DEBUG:
            ##print "cost of item " + str(item) + " is " + str(item_cost)

            heuristic_cost += item_cost

    return heuristic_cost


def A_star_search(initial_state):

    """A * search"""

    ## Output variables initialize
    starting_time = time.time()
    nodes_expanded = 0
    max_search_depth = 0

    ## Initialize Frontier and Explored lists
    frontier = StatePQ()
    frontier.push(initial_state)
    visited = Visited()  ## will include frontier and explored states
    visited.addVisited(list(initial_state.config))

    while not frontier.isEmpty():

        ##Explore state
        state = frontier.pop()

        #### DEBUG:
        ##print('Popping: ')
        ##state.display()

        visited.addVisited(list(state.config))

        if test_goal(state):

            ##Stop Clock
            running_time = time.time() - starting_time

            ##Log Depth of Solution
            search_depth = state.level

            ##Calculate path to goal
            path_to_goal = []
            path_to_goal.append(state.action)
            cost_of_path = state.cost
            parent_state = state.parent

            while parent_state.parent != None:

                path_to_goal.append(parent_state.action)
                cost_of_path += parent_state.cost

                parent_state = parent_state.parent


            path_to_goal.reverse()

            ##Calculate max memory usage
            max_ram_usage = memory_usage_resource()

            ##Write File
            writeOutput(path_to_goal, cost_of_path , nodes_expanded, search_depth, max_search_depth, running_time, max_ram_usage)

            ##Exist program
            return 1

        ##Goal not achieved, expand state and increase number of expanded nodes
        state.expand_reverse()  ##Reverse UDLR expansion
        nodes_expanded +=  1

        #### DEBUG:
        ##print nodes_expanded

        for child_state in state.children:

            if not visited.isVisited(list(child_state.config)):

                ## Update output variables
                child_state.level = state.level + 1
                child_state.parent = state
                ##child_state.cost = 1

                ## Calculate Child A* cost
                child_state.cost = HeuristicCalc(child_state)

                #### DEBUG:
                ##print('Pushing: ')
                ##child_state.display()
                ##print "cost: " + str(child_state.cost)

                ## Put child in frontier
                frontier.push(child_state)
                visited.addVisited(list(child_state.config))

                ## Update max depth if needed
                if child_state.level > max_search_depth:
                    max_search_depth = child_state.level

    return 0


def calculate_total_cost(state):

    """calculate the total estimated cost of a state"""

    ### STUDENT CODE GOES HERE ###

def calculate_manhattan_dist(idx, value, n):

    """calculate the manhattan distance of a tile"""

    ### STUDENT CODE GOES HERE ###

def test_goal(puzzle_state):

    """test the state is the goal state or not"""

    ### STUDENT CODE GOES HERE ###
    goal_config_str = '0'

    for n in range(1,puzzle_state.dimension * puzzle_state.dimension):

        goal_config_str += ','
        goal_config_str += str(n)

    goal_config= goal_config_str.split(",")

    goal_config = tuple(map(int, goal_config))

    if puzzle_state.config == goal_config:

        return 1

    return 0

# Main Function that reads in Input and Runs corresponding Algorithm

def main():

    sm = sys.argv[1].lower()

    begin_state = sys.argv[2].split(",")

    begin_state = tuple(map(int, begin_state))

    size = int(math.sqrt(len(begin_state)))

    hard_state = PuzzleState(begin_state, size)

    if sm == "bfs":

        bfs_search(hard_state)

    elif sm == "dfs":

        dfs_search(hard_state)

    elif sm == "ast":

        A_star_search(hard_state)

    elif sm == "tst":

        HeuristicCalc(hard_state)

        return 1

    else:

        print("Enter valid command arguments !")

if __name__ == '__main__':

    main()
