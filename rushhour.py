#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.

'''
rushhour STATESPACE
'''
#   You may add only standard python imports---i.e., ones that are automatically
#   available on CDF.
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

from search import *
from random import randint


##################################################
# The search space class 'rushhour'             #
# This class is a sub-class of 'StateSpace'      #
##################################################

class rushhour(StateSpace):

    def __init__(self, action, gval, board_size, goal_entrance, goal_direction, vehicle_list, board_space, parent):
        StateSpace.__init__(self, action, gval, parent)
        self.board_size = board_size #stored as y,x
        self.goal_entrance = goal_entrance
        self.goal_direction = goal_direction
        self.vehicle_list = vehicle_list
        self.board_space = board_space
        """Initialize a rushhour search state object."""

    def successors(self):
        successors = list()
        for v in self.vehicle_list:
            for s in self.canMove(v):
                successors.append(s)
        return successors            
        #For my successor function, I only return states that are different from the given state.
        #For example if there's an action to move a car that will result in the same configuration, it is not counted as a successor.
        '''Return list of rushhour objects that are the successors of the current object'''

    def hashable_state(self):
        hashlist = []
        for v in self.vehicle_list:
            hashlist.append(v[0])
            hashlist.append(v[1])
            hashlist.append(v[2])
            hashlist.append(v[3])
            hashlist.append(v[4])
        return (tuple(hashlist))
        '''Return a data item that can be used as a dictionary key to UNIQUELY represent the state.'''

    def print_state(self):
        #DO NOT CHANGE THIS FUNCTION---it will be used in auto marking
        #and in generating sample trace output.
        #Note that if you implement the "get" routines
        #(rushhour.get_vehicle_statuses() and rushhour.get_board_size())
        #properly, this function should work irrespective of how you represent
        #your state.

        if self.parent:
            print("Action= \"{}\", S{}, g-value = {}, (From S{})".format(self.action, self.index, self.gval, self.parent.index))
        else:
            print("Action= \"{}\", S{}, g-value = {}, (Initial State)".format(self.action, self.index, self.gval))

        print("Vehicle Statuses")
        for vs in sorted(self.get_vehicle_statuses()):
            print("    {} is at ({}, {})".format(vs[0], vs[1][0], vs[1][1]), end="")
        board = get_board(self.get_vehicle_statuses(), self.get_board_properties())
        print('\n')
        print('\n'.join([''.join(board[i]) for i in range(len(board))]))

#Data accessor routines.

    def get_vehicle_statuses(self):
        return self.vehicle_list
        
        '''Return list containing the status of each vehicle
           This list has to be in the format: [vs_1, vs_2, ..., vs_k]
           with one status list for each vehicle in the state.
           Each vehicle status item vs_i is itself a list in the format:
                 [<name>, <loc>, <length>, <is_horizontal>, <is_goal>]
           Where <name> is the name of the robot (a string)
                 <loc> is a location (a pair (x,y)) indicating the front of the vehicle,
                       i.e., its length is counted in the positive x- or y-direction
                       from this point
                 <length> is the length of that vehicle
                 <is_horizontal> is true iff the vehicle is oriented horizontally
                 <is_goal> is true iff the vehicle is a goal vehicle
        '''

    def get_board_properties(self):
        return (self.board_size, self.goal_entrance, self.goal_direction)
        '''Return (board_size, goal_entrance, goal_direction)
           where board_size = (m, n) is the dimensions of the board (m rows, n columns)
                 goal_entrance = (x, y) is the location of the goal
                 goal_direction is one of 'N', 'E', 'S' or 'W' indicating
                                the orientation of the goal
        '''

    def getGoalVehicle(self):
        goalVehicles = []
        for v in self.vehicle_list: #searches for goal vehicles
            if v[4]:
                goalVehicles.append(v)
        return goalVehicles
    
    def isHorizontal(self, v):
        return v[3]

    def getCarLength(self, v):
        return v[2]
    
    def getX(self, v):
        return v[1][0]

    def getY(self, v):
        return v[1][1]

    def convert(self, x, y):
        return x+y*self.board_size[1] #formula to convert a 2D array into a 1D array but using the 2D coordinates
    
    def canMove(self, v):
        canMove = []
        if (self.isHorizontal(v)):
            #CONSIDERS WRAP-AROUND WITH %
            if (not self.board_space[self.convert((self.getX(v) + self.getCarLength(v))%self.board_size[1],self.getY(v))]):
                canMove.append(self.newState(v, (self.getX(v)+1)%self.board_size[1], self.getY(v), 0))
            if (not self.board_space[self.convert((self.getX(v)-1)%self.board_size[1],self.getY(v))]):
                canMove.append(self.newState(v, (self.getX(v)-1)%self.board_size[1], self.getY(v), 1))
        else:
            if (not self.board_space[self.convert(self.getX(v),(self.getY(v)+self.getCarLength(v))%self.board_size[0])]):
                canMove.append(self.newState(v, self.getX(v), (self.getY(v)+1)%self.board_size[0], 2))
            if (not self.board_space[self.convert(self.getX(v),(self.getY(v)-1)%self.board_size[0])]):
                canMove.append(self.newState(v, self.getX(v), (self.getY(v)-1)%self.board_size[0], 3))
        return canMove
    
    def newState(self, v, x, y, move):
        newVL = []
        action = ""
        newBoardSpace = []
        for oldV in self.vehicle_list:
            if oldV == v:
                newV = ["", (0,0), 0, False, False]
                vloc = [0,0]
                newV[0] = oldV[0]
                newV[2] = oldV[2]
                newV[3] = oldV[3]
                newV[4] = oldV[4]
                vloc[0] = x
                vloc[1] = y
                newV[1] = tuple(vloc) 
                newVL.append(newV)
            else:
                newVL.append(oldV)

        for s in self.board_space:
            newBoardSpace.append(s)

        if move==0:
            action = "Move car " + v[0] + " 1 unit right"
            del newBoardSpace[self.convert((x-1)%self.board_size[1], y)]
            newBoardSpace.insert(self.convert((x-1)%self.board_size[1], y), False)
            del newBoardSpace[self.convert((x+self.getCarLength(v)-1)%self.board_size[1],y)]
            newBoardSpace.insert(self.convert((x+self.getCarLength(v)-1)%self.board_size[1],y), True)
        elif move==1:
            action = "Move car " + v[0] + " 1 unit left"
            del newBoardSpace[self.convert(x, y)]
            newBoardSpace.insert(self.convert(x, y), True)
            del newBoardSpace[self.convert((x+self.getCarLength(v))%self.board_size[1],y)]
            newBoardSpace.insert(self.convert((x+self.getCarLength(v))%self.board_size[1],y), False)
        elif move==2:
            action = "Move car " + v[0] + " 1 unit down"
            del newBoardSpace[self.convert(x, (y-1)%self.board_size[0])]
            newBoardSpace.insert(self.convert(x, (y-1)%self.board_size[0]), False)
            del newBoardSpace[self.convert(x,(y+self.getCarLength(v)-1)%self.board_size[0])]
            newBoardSpace.insert(self.convert(x, (y+self.getCarLength(v)-1)%self.board_size[0]), True)            
        else:
            action = "Move car " + v[0] + " 1 unit up"           
            del newBoardSpace[self.convert(x, y)]
            newBoardSpace.insert(self.convert(x, y), True)
            del newBoardSpace[self.convert(x,(y+self.getCarLength(v))%self.board_size[0])]
            newBoardSpace.insert(self.convert(x,(y+self.getCarLength(v))%self.board_size[0]), False)  
        
        newR = rushhour(action, self.gval+1, self.board_size, self.goal_entrance, self.goal_direction, newVL, newBoardSpace, self)
        return newR

#############################################
# heuristics                                #
#############################################


def heur_zero(state):
    '''Zero Heuristic use to make A* search perform uniform cost search'''
    return 0


def heur_min_moves(state):
    gvList = state.getGoalVehicle()
    minHeur = []
    if rushhour_goal_fn(state):
        return 0
    for gv in gvList:
        if state.isHorizontal(gv):
            if state.goal_direction=='W' and state.getY(gv)==state.goal_entrance[1]:
                i = abs(state.getX(gv) - state.goal_entrance[0])
                j = state.board_size[1] - i
                minHeur.append(min(i,j))
            if state.goal_direction=='E' and state.getY(gv)==state.goal_entrance[1]:
                i = abs((state.getX(gv)+state.getCarLength(gv)-1)%state.board_size[1] - state.goal_entrance[0])
                j = state.board_size[1] - i
                minHeur.append(min(i,j))
        else:
            if state.goal_direction=='N' and state.getX(gv)==state.goal_entrance[0]:
                i = abs(state.getY(gv) - state.goal_entrance[1])
                j = state.board_size[0] - i
                minHeur.append(min(i,j))
            if state.goal_direction=='S' and state.getX(gv)==state.goal_entrance[0]:
                i = abs((state.getY(gv)+state.getCarLength(gv)-1)%state.board_size[0] - state.goal_entrance[1])
                j = state.board_size[0] - i
                minHeur.append(min(i,j))
    if len(minHeur) == 0: #if no feasible solution exists
        return float("inf")
    else:
        return min(minHeur)            
    '''rushhour heuristic'''
    #We want an admissible heuristic. Getting to the goal requires
    #one move for each tile of distance.5
    #Since the board wraps around, there are two different
    #directions that lead to the goal.
    #NOTE that we want an estimate of the number of ADDITIONAL
    #     moves required from our current state
    #1. Proceeding in the first direction, let MOVES1 =
    #   number of moves required to get to the goal if it were unobstructed
    #2. Proceeding in the second direction, let MOVES2 =
    #   number of moves required to get to the goal if it were unobstructed
    #
    #Our heuristic value is the minimum of MOVES1 and MOVES2 over all goal vehicles.
    #You should implement this heuristic function exactly, even if it is
    #tempting to improve it.


def rushhour_goal_fn(state):
    gvList = state.getGoalVehicle()
    for gv in gvList:
        if state.goal_direction == 'N' and state.getX(gv)==state.goal_entrance[0]:
            if not state.isHorizontal(gv): #head
                if state.getY(gv) == state.goal_entrance[1] and state.getX(gv) == state.goal_entrance[0]:
                    return True
        elif state.goal_direction == 'S': #tail
            if not state.isHorizontal(gv) and state.getX(gv)==state.goal_entrance[0]:
                if (state.getY(gv)+state.getCarLength(gv) - 1)%state.board_size[0] == state.goal_entrance[1] and state.getX(gv) == state.goal_entrance[0]:
                    return True
        elif state.goal_direction == 'W': #head
            if state.isHorizontal(gv) and state.getY(gv)==state.goal_entrance[1]:
                if state.getX(gv) == state.goal_entrance[0] and state.getY(gv) == state.goal_entrance[1]:
                    return True
        else: #tail
            if state.isHorizontal(gv) and state.getY(gv)==state.goal_entrance[1]:
                if (state.getX(gv)+state.getCarLength(gv)-1)%state.board_size[1] == state.goal_entrance[0] and state.getY(gv) == state.goal_entrance[1]:
                    return True
    return False            
    '''Have we reached a goal state'''


def make_init_state(board_size, vehicle_list, goal_entrance, goal_direction):
    rboard_space = []
    for i in range(board_size[1]):
        for j in range(board_size[0]):
            rboard_space.append(False)

    r = rushhour("START", 0, board_size, goal_entrance, goal_direction, vehicle_list, rboard_space, None)
    r.goal_entrance = goal_entrance
    r.goal_direction = goal_direction

    for v in vehicle_list:
        for l in range(r.getCarLength(v)):
            if (r.isHorizontal(v)):
                index = r.convert((r.getX(v)+l)%r.board_size[1],r.getY(v))
                del rboard_space[index]
                rboard_space.insert(index, True)
            else:
                index = r.convert(r.getX(v),(r.getY(v)+l)%r.board_size[0])
                del rboard_space[index]
                rboard_space.insert(index, True)                
    
    return r
    '''Input the following items which specify a state and return a rushhour object
       representing this initial state.
         The state's its g-value is zero
         The state's parent is None
         The state's action is the dummy action "START"
       board_size = (m, n)
          m is the number of rows in the board
          n is the number of columns in the board
       vehicle_list = [v1, v2, ..., vk]
          a list of vehicles. Each vehicle vi is itself a list
          vi = [vehicle_name, (x, y), length, is_horizontal, is_goal] where
              vehicle_name is the name of the vehicle (string)
              (x,y) is the location of that vehicle (int, int)
              length is the length of that vehicle (int)
              is_horizontal is whether the vehicle is horizontal (Boolean)
              is_goal is whether the vehicle is a goal vehicle (Boolean)
      goal_entrance is the coordinates of the entrance tile to the goal and
      goal_direction is the orientation of the goal ('N', 'E', 'S', 'W')

   NOTE: for simplicity you may assume that
         (a) no vehicle name is repeated
         (b) all locations are integer pairs (x,y) where 0<=x<=n-1 and 0<=y<=m-1
         (c) vehicle lengths are positive integers
    '''
########################################################
#   Functions provided so that you can more easily     #
#   Test your implementation                           #
########################################################


def get_board(vehicle_statuses, board_properties):
    #DO NOT CHANGE THIS FUNCTION---it will be used in auto marking
    #and in generating sample trace output.
    #Note that if you implement the "get" routines
    #(rushhour.get_vehicle_statuses() and rushhour.get_board_size())
    #properly, this function should work irrespective of how you represent
    #your state.
    (m, n) = board_properties[0]
    board = [list(['.'] * n) for i in range(m)]
    for vs in vehicle_statuses:
        for i in range(vs[2]):  # vehicle length
            if vs[3]:
                # vehicle is horizontal
                board[vs[1][1]][(vs[1][0] + i) % n] = vs[0][0]
                # represent vehicle as first character of its name
            else:
                # vehicle is vertical
                board[(vs[1][1] + i) % m][vs[1][0]] = vs[0][0]
                # represent vehicle as first character of its name
    # print goal
    board[board_properties[1][1]][board_properties[1][0]] = board_properties[2]
    return board


def make_rand_init_state(nvehicles, board_size):
    '''Generate a random initial state containing
       nvehicles = number of vehicles
       board_size = (m,n) size of board
       Warning: may take a long time if the vehicles nearly
       fill the entire board. May run forever if finding
       a configuration is infeasible. Also will not work any
       vehicle name starts with a period.

       You may want to expand this function to create test cases.
    '''

    (m, n) = board_size
    vehicle_list = []
    board_properties = [board_size, None, None]
    for i in range(nvehicles):
        if i == 0:
            # make the goal vehicle and goal
            x = randint(0, n - 1)
            y = randint(0, m - 1)
            is_horizontal = True if randint(0, 1) else False
            vehicle_list.append(['gv', (x, y), 2, is_horizontal, True])
            if is_horizontal:
                board_properties[1] = ((x + n // 2 + 1) % n, y)
                board_properties[2] = 'W' if randint(0, 1) else 'E'
            else:
                board_properties[1] = (x, (y + m // 2 + 1) % m)
                board_properties[2] = 'N' if randint(0, 1) else 'S'
        else:
            board = get_board(vehicle_list, board_properties)
            conflict = True
            while conflict:
                x = randint(0, n - 1)
                y = randint(0, m - 1)
                is_horizontal = True if randint(0, 1) else False
                length = randint(2, 3)
                conflict = False
                for j in range(length):  # vehicle length
                    if is_horizontal:
                        if board[y][(x + j) % n] != '.':
                            conflict = True
                            break
                    else:
                        if board[(y + j) % m][x] != '.':
                            conflict = True
                            break
            vehicle_list.append([str(i), (x, y), length, is_horizontal, False])

    return make_init_state(board_size, vehicle_list, board_properties[1], board_properties[2])


def test(nvehicles, board_size):   
    s0 = make_rand_init_state(nvehicles, board_size)
    s = make_init_state((7, 7), [['gv', (5, 1), 3, True, True],
              ['1', (3, 1), 2, False, False],
              ['3', (4, 4), 5, False, False]], (4, 1), 'E')
    s.print_state()
    se = SearchEngine('astar', 'full')
    #se.trace_on(2)
    final = se.search(s, rushhour_goal_fn, heur_min_moves)
