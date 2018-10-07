# -*- coding: utf-8 -*-
"""
Name:
    game_of_life.py
Description:
    Implements Conway's Game of Life. Initial grid can be passed to object or
    a random grid can be generated. Instance methods include step, advance by
    a time step, and plot.
@author:
    Kenneth Sharman, Adapted from code written by bjackel (Python 3.6)
"""
# Import standard packages
import numpy as np
import matplotlib.pyplot as plt

# Main object
class GameOfLife:
    
    def __init__(self, nx=10, ny=10, grid=None):
        '''
        Default constructor initializes grid to optional parameter or a grid
        full of zeros.
        Parameters:
            nx, ny: Optional Width and Height of grid. Default values are set
                    to 10
            grid:   Optional parameter, used to initialize grid.
        '''
        self.nx = nx # Width of grid
        self.ny = ny # Height of grid
        
        if grid is None: # If optional parameter is blank
            self.grid = np.zeros( [nx,ny] ) # Initialize grid to zeros
        else: # If grid is passed in
            self.grid = grid # Initialize using parameter
            self.nx, self.ny = self.grid.shape 
            # Set width and height to size of the grid parameter
            
        self.__init__step() # Call next initialization function
        
    def __init__step(self):
        '''
        Purpose of constructor is to perform step calculations which would
        otherwise be repeated every time step function is called.
        '''
        self.step_num = 0 # Initialize step number to zero
        
        # Create row/ column indices
        x,y = np.meshgrid( np.arange(self.nx), np.arange(self.ny), indexing='ij' )
        # Determine indices of each neighbor when a step is taken in one of
        # the 8 possible directions (8 neighboring cells in a 2D grid)
        # modulo is used to wrap around when index reaches edge of grid
        xx = np.array([x+1, x-1, x+0, x+0, x+1, x-1, x+1, x-1]) % self.nx
        yy = np.array([y+0, y+0, y+1, y-1, y+1, y-1, y-1, y+1]) % self.ny
        
        self.step_x = xx # Define instance variables that hold the indices
        self.step_y = yy # for the neighbors of a particular cell
        
    def get_grid(self):
        '''
        Returns the grid variable
        '''
        return self.grid
            
    def step(self, nsteps=1):
        ''' 
        Apply rules to evolve the grid by one step
        '''
        
        self.step_num += 1 # Increment step counter
        grid = self.grid.copy()
        # A copy of the grid is used to ensure that updated cells are not
        # being considered when determining the next generation of a cell.
        # This method is costly because it copies the value of every cell,
        # regardless of if it will change or not. A more efficient method
        # would be to check to see if the cell will change, and if it will, then
        # copy its value. This algorithm would most likely be implemented in the
        # updating process, rather than before any changes have occurred.
        
        for indx in range(nsteps):            
            # Variable declaration could be defined in __init__step
            nnear = np.sum( grid[self.step_x,self.step_y] , axis=0 )
            # Cell with fewer than two live neighbors, or more than three live 
            # neighbors dies
            grid[(nnear < 2) | (nnear > 3)] = 0
            # Any dead cell with three neighbors will come to life
            grid[nnear==3] = 1
            
        self.grid = grid # Update grid with new generation
        return self
    
    def randomize(self, p):
        '''
        rand function creates ndarray of shape nx x ny and randomly assigns each 
        element with a number in uniform distribution [0,1). Comparing if greater 
        than probability will generate ndarray of Booleans, where True means the 
        random number was greater than p
        Parameters:
            nx. ny: Number of rows and columns
            p: probability between 0 and 1
        Returns
            nx * ny matrix will Boolean elements 
        '''
        self.grid = random_grid(self.nx, self.ny, p)
        return self

    def plot(self, axes=None):
        '''
        Plots the current state of the grid using matplotlib's imshow function
        Parameters:
            axes:   Optional parameter allows axes object to be passed in. This
                    This allows for plot customization
        '''
        if axes is None:
            fig, axes = plt.subplots()
            # plts.subplots return figure and axes object
            # fig can be used to change figure attributes and/ or save
            # axes allows for plot customization and/ or subplot features
            
        axes.imshow( self.grid, cmap="Greys" ) # Plot with neutral color scheme
        return self    
    
# Note this function is more or less useless. A better option would be to 
# include an additional parameter to the GameOfLife object, which could be used
# to call the randomize instance method.
def random_grid(nx, ny, p):
    '''
    Same function as the randomize instance method, however it is offered in a
    static context to allow for a GameOfLife object to be instantiated with
    a random grid.
    
    rand function creates ndarray of shape nx x ny and randomly assigns each 
    element with a number in uniform distribution [0,1). Comparing if greater 
    than probability will generate ndarray of Booleans, where True means the 
    random number was greater than p
    Parameters:
        nx. ny: Number of rows and columns
        p: probability between 0 and 1
    Returns
        nx x ny matrix will Boolean elements
    '''
    return np.random.rand(nx, ny) > p            