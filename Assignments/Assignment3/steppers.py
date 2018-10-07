# -*- coding: utf-8 -*-
"""
Name:
    steppers.py
Description:
    File contains 5 versions of a step function to be used in an implementation
    of Game of Life. Purpose of the file is simply to define functions, so that
    they can be compared.
@author:
    Kenneth Sharman, Adapted from code written by bjackel (Python 3.6)
"""

import numpy as np

def stepper0(grid, nsteps=1, plot=None):
    """
    One step in Conway's game of life with wrap-around edges.
    
    Loop over all pixels in grid, and over all neighbors (very slow)
    """
    
    nx, ny = grid.shape # width and height of grid
    xx, yy =  np.arange(nx), np.arange(ny) # Array with len matching grid dimension 
    newgrid = grid.copy() 
    # Copy grid to ensure that the new generation of a cell is calculated using
    # the states of its neighbors in previous generation. See game_of_life.py
    # step function for discussion
    
    for x in xx: # For every cell in every row
        for y in yy: # For every cell in every column
            
            nnear = 0  # count number of neighbors
            
            for dx in [-1,0,1]: # Inspect each of the 8 neighbors
                for dy in [-1,0,1]:
                    if (dx!=0 or dy!=0):  # don't include the cell itself
                        # Increment the count if neighbor is alive
                        # The modulus ensures that if on an edge, index will 
                        # wrap around to opposite side of the grid
                        nnear += grid[ (x+dx)%nx, (y+dy)%ny ]

            if (grid[x,y] == 0): # If cell is dead
                if nnear == 3: # Check the neighbor count. Dead cells with three 
                    newgrid[x,y]=1 # live neighbors become live cells

            else:
                if nnear < 2: # If there are fewer than 2 live neighbors
                    newgrid[x,y]=0 # the cell dies
                if nnear >3 : # If there are more than 3 live neighbors
                    newgrid[x,y]=0 # the cell dies
                                                            
    return newgrid # Update grid with new generation
    

def stepper1(grid, nsteps=1, plot=None):
    """
    One step in Conway's game of life with wrap-around edges.
    
    Loop over all pixels in grid, and then add all 8 neighbors (slow)
    """
    nx, ny = grid.shape # width and height of grid
    xx, yy =  np.arange(nx), np.arange(ny) # Array with len matching grid dimension
    newgrid = grid.copy()
    # Copy grid to ensure that the new generation of a cell is calculated using
    # the states of its neighbors in previous generation. See game_of_life.py
    # step function for discussion
    
    # x and y directions to each of the 8 neighbors of a cell
    dx = np.array( [1, -1, 0, 0, 1, -1, 1, -1] )
    dy = np.array( [0, 0, 1, -1, 1, -1, -1, 1] )
            
    # For every cell in the grid
    for x in xx:
        for y in yy:
            # Increment the count if neighbor is alive. The modulus ensures 
            # that if on an edge, index will wrap around to opposite side of 
            # the grid
            nnear = np.sum( grid[ (x+dx)%nx, (y+dy)%ny ] )
    
            # If there are fewer than 2 or more than 3 live neighbors:
            if (nnear < 2) or (nnear > 3): 
                newgrid[x,y] = 0 # then the cell dies
            elif (nnear == 3): # If there are 3 live neighbors then
                newgrid[x,y] = 1 # Then cell lives (or is revived)
                                            
    return newgrid # Update grid with new generation 
    

def stepper2(grid, nsteps=1, plot=None):
    """
    One step in Conway's game of life with wrap-around edges.
    
    Loop over all neighbor shifts, adding an entire grid  (fast)
    """
    
    nx, ny = grid.shape # width and height of grid
    # matrix representing the indices of each cell in the grid
    xx, yy = np.meshgrid( np.arange(nx), np.arange(ny), indexing='ij' )

    nnear = 0 # Initialize count to zero
    newgrid = grid.copy()
    # Copy grid to ensure that the new generation of a cell is calculated using
    # the states of its neighbors in previous generation. See game_of_life.py
    # step function for discussion

    # Similar method to Stepper0 except it replaces the control statements with
    # matrix operations when determining the next generation state. This is
    # much faster as a single operation is applied to all cells
    for dx in [-1,0,1]:
        for dy in [-1,0,1]:
            if (dx==0 and dy==0): continue
            nnear += grid[ (xx+dx)%nx,(yy+dy)%ny ]
    
    # Matrix operations that apply rules to determine new state of cell
    newgrid[(grid>0) & (nnear<2)] = 0
    newgrid[(grid>0) & (nnear>3)] = 0
    newgrid[(grid==0) & (nnear==3)] = 1
   
    return newgrid # Update grid


def stepper3(grid, nsteps=1, plot=None):
    """
    One step in Conway's game of life with wrap-around edges.
    
    Try cleaning up the neighbour loops (faster?)
    """
    nx, ny = grid.shape # width and height of grid
    # matrix representing the indices of each cell in the grid
    xx, yy = np.meshgrid( np.arange(nx), np.arange(ny), indexing='ij' )
    # Define a list of tuples that contain indices for eahc neighbor
    # The goal here is to replace a time consuming iterations done in Stepper2
    dxy = [(1,0), (-1,0), (0,1), (0,-1), (1,1), (-1,-1), (1,-1), (-1,1) ]
    
    newgrid = grid.copy()
    # Copy grid to ensure that the new generation of a cell is calculated using
    # the states of its neighbors in previous generation. See game_of_life.py
    # step function for discussion    
       
    nnear = 0
    
    # With the x/y index for each neighbor already calculated, a matrix operation
    # can be applied which should speed things up
    for dx,dy in dxy:
        nnear += grid[(xx+dx)%nx,(yy+dy)%ny] 
    
    # Same update method used in stepper2
    newgrid[nnear < 2] = 0  
    newgrid[nnear > 3] = 0
    newgrid[nnear==3] = 1
   
    return newgrid # Update grid


def stepper4(grid, nsteps=1, plot=None):
    """
    One step in Conway's game of life with wrap-around edges.
    
    -move more calculations outside loop (fastest?)
    -reuse input grid for output
    """
    nx, ny = grid.shape # width and height of grid
    # matrix representing the indices of each cell in the grid
    x, y = np.meshgrid( np.arange(nx), np.arange(ny), indexing='ij' )
    
    # Indices of each of the 8 neighbors of a cell
    # This makes one more improvement over the method used in Stepper3
    # When computing the neighboring indices, wrap around is considered.
    # After these 2 assignment statements, all that is left to calculate is
    # done using matrix operations, which should be the fastest method yet
    xx = np.array([x+1, x-1, x+0, x+0, x+1, x-1, x+1, x-1]) % nx
    yy = np.array([y+0, y+0, y+1, y-1, y+1, y-1, y-1, y+1]) % ny

    # grid[xx,yy].shape = 8,nx,ny  <= add up neighbours 
    # note: numpy will automatically convert Boolean to integer before summing
    nnear = np.sum( grid[xx,yy] , axis=0 )
        
    grid[(nnear < 2) | (nnear > 3)] = 0
    grid[nnear==3] = 1

    return grid # Update grid