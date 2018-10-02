# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 17:53:50 2016

@author: bjackel
"""


# example with animation
grid = np.random.rand(401,501) > 0.5
p = plt.matshow(grid)
grid = life_generation_stepper(grid,nsteps=10000,plot=p)


import numpy as np
import matplotlib.pyplot as plt


def life_generation_stepper(grid, nsteps=1, plot=None):
    
    # get most recently used plotting window
    fig = list(map(plt.figure, plt.get_fignums()))[-1]

    nx, ny = grid.shape
    x, y = np.meshgrid( np.arange(nx), np.arange(ny), indexing='ij' )
    xx = np.array([x+1, x-1, x+0, x+0, x+1, x-1, x+1, x-1]) % nx
    yy = np.array([y+0, y+0, y+1, y-1, y+1, y-1, y-1, y+1]) % ny

    for nstep in range(nsteps):
        nnear = np.sum( grid[xx,yy] , axis=0 )
        
        grid[(nnear < 2) | (nnear > 3)] = 0
        grid[nnear==3] = 1

        if plot is not None:
            plot.set_data(grid)
            plot.axes.set_title(str(nstep))
            fig.canvas.draw() ; fig.canvas.flush_events() #update plot window
   
    return grid

    
def stepper0(grid, nsteps=1, plot=None):
    """
    One step in Conway's game of life with wrap-around edges.
    
    Loop over all pixels in grid, and over all neighbors (very slow)
    """
    
    nx, ny = grid.shape
    xx, yy =  np.arange(nx), np.arange(ny) 
    newgrid = grid.copy()
    
    for x in xx:
        for y in yy:
            
            nnear = 0  # count number of neighbors
            
            for dx in [-1,0,1]:
                for dy in [-1,0,1]:
                    if (dx!=0 or dy!=0):  # don't include the cell itself
                        nnear += grid[ (x+dx)%nx, (y+dy)%ny ]

            # dead cells with three live neighbours become live cells
            if (grid[x,y] == 0):
                if nnear == 3:
                    newgrid[x,y]=1

            # live cells with fewer than two or more than 3 live neighbors die
            else:
                if nnear < 2:
                    newgrid[x,y]=0
                if nnear >3 :
                    newgrid[x,y]=0
                                                            
    return newgrid
    

def stepper1(grid, nsteps=1, plot=None):
    """
    One step in Conway's game of life with wrap-around edges.
    
    Loop over all pixels in grid, and then add all 8 neighbours (slow)
    """
    nx, ny = grid.shape
    xx, yy =  np.arange(nx), np.arange(ny) 
    newgrid = grid.copy()
    
    dx = np.array( [1, -1, 0, 0, 1, -1, 1, -1] )
    dy = np.array( [0, 0, 1, -1, 1, -1, -1, 1] )
               
    for x in xx:
        for y in yy:
            
            nnear = np.sum( grid[ (x+dx)%nx, (y+dy)%ny ] )
    
            if (nnear < 2) or (nnear > 3): 
                newgrid[x,y] = 0
            elif (nnear == 3):
                newgrid[x,y] = 1
                                            
    return newgrid    
    

def stepper2(grid, nsteps=1, plot=None):
    """
    One step in Conway's game of life with wrap-around edges.
    
    Loop over all neighbor shifts, adding an entire grid  (fast)
    """
    
    nx, ny = grid.shape
    xx, yy = np.meshgrid( np.arange(nx), np.arange(ny), indexing='ij' )

    nnear = 0
    newgrid = grid.copy()

    for dx in [-1,0,1]:
        for dy in [-1,0,1]:
            if (dx==0 and dy==0): continue
            nnear += grid[ (xx+dx)%nx,(yy+dy)%ny ]
    
    newgrid[(grid>0) & (nnear<2)] = 0
    newgrid[(grid>0) & (nnear>3)] = 0
    newgrid[(grid==0) & (nnear==3)] = 1
   
    return newgrid


def stepper3(grid, nsteps=1, plot=None):
    """
    One step in Conway's game of life with wrap-around edges.
    
    Try cleaning up the neighbour loops (faster?)
    """
    nx, ny = grid.shape
    xx, yy = np.meshgrid( np.arange(nx), np.arange(ny), indexing='ij' )
    dxy = [(1,0), (-1,0), (0,1), (0,-1), (1,1), (-1,-1), (1,-1), (-1,1) ]
    
    newgrid = grid.copy()           
    nnear = 0
    
    for dx,dy in dxy:
        nnear += grid[(xx+dx)%nx,(yy+dy)%ny] 
    
    newgrid[nnear < 2] = 0  
    newgrid[nnear > 3] = 0
    newgrid[nnear==3] = 1
   
    return newgrid


def stepper4(grid, nsteps=1, plot=None):
    """
    One step in Conway's game of life with wrap-around edges.
    
    -move more calculations outside loop (fastest?)
    -reuse input grid for output
    """
    nx, ny = grid.shape
    x, y = np.meshgrid( np.arange(nx), np.arange(ny), indexing='ij' )
    
    xx = np.array([x+1, x-1, x+0, x+0, x+1, x-1, x+1, x-1]) % nx
    yy = np.array([y+0, y+0, y+1, y-1, y+1, y-1, y-1, y+1]) % ny

    # grid[xx,yy].shape = 8,nx,ny  <= add up neighbours 
    # note: numpy will automatically convert boolean to integer before summing
    nnear = np.sum( grid[xx,yy] , axis=0 )
        
    grid[(nnear < 2) | (nnear > 3)] = 0
    grid[nnear==3] = 1

    return grid
    
    
      
# the code below will not run if this file is "included"
#
if __name__ == '__main__':

    print('Check agreement between different algorithms')
    grid = np.random.rand(31,21) >= 0.5  # don't use a square grid
    newgrid = stepper0(grid, nsteps=1)
    stepfunclist = [stepper0, stepper1, stepper2, stepper3, stepper4]
    
    for stepfunc in stepfunclist:
        test = stepfunc(grid)
        print( str(stepfunc), np.all(test == newgrid) )
        
    
    print('Compare speed of different algorithms (lower is better)')
    import timeit
    times = {}
    for stepfunc in stepfunclist:
        command = 'ng = {}(g)'.format(stepfunc.__name__)
        setup = 'from __main__ import {}; import numpy as np; g=(np.random.rand(31,21)>=0.5)'.format(stepfunc.__name__)
        times[stepfunc.__name__] = timeit.timeit(command,setup=setup, number=100)
    #t = timeit.timeit('ng = stepper0(grid)', setup='from __main__ import stepper0; import numpy as np; grid=np.random.rand(31,21)>=0.5', number=100)
    timeinfo = [ '{:9.5f} {}'.format(t,n) for (n,t) in times.items() ]
    print( '\n'.join( sorted(timeinfo) ) )
    
#newgrid = life_generation_stepper(grid, nsteps=1)
#p=plt.imshow(grid, interpolation='nearest')    
#p = plt.matshow(grid)
#newgrid = life_generation_stepper2(grid, nsteps=100, plot=p)
#p = plt.imshow(grid)
    