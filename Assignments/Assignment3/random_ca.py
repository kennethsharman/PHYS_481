# -*- coding: utf-8 -*-
"""
Name:
    random_ca.py
Description: 
    cellularAutomaton object instantiates a 1-dimensional cellular
    automaton. The first generation is randomly generated and other generations
    are initialized to zeros. Number of cells, number of steps, and integer rule
    number from 0-255 parameters are required to instantiate. Functional instance 
    methods include plot (which plots the CA) and steps (which advances the current
    state by a generation).  
@author: 
    Kenneth Sharman (Python 3.6)
"""

# import standard packages
import numpy as np
import matplotlib.pyplot as plt

class cellularAutomaton:
    '''
    cellularAutomaton object instantiates a 1-dimensional cellular automaton. 
    The first generation is randomly generated and other generations are 
    initialized to zeros.
    Parameters:
        ncells: Number of cells in the 1d grid which represents a generation
        nsteps: Numbers of generations to be included in plot
        rule_number: Integer rule number from 0-255
    '''
    
    def __init__(self, ncells, nsteps, rule_number):
        '''
        Constructor initializes instance variables, first generation of cells,
        and grid sequence.
        '''
        self.ncells = ncells # Number of cells in a grid
        self.nsteps = nsteps # Number of time steps in sequence
        self.rule_num = rule_number # Rule  numnber 0-255
        
        self.__init__cells(ncells) # Randomly generate 64-bit first generation
        self.__init__seq(ncells, nsteps) # Initialize grid sequence to include
        # the random first gen and set cells of other generations to zero
        
    def __init__cells(self, ncells):
        '''
        Initialize cells to a random 64-bit number
        '''
        self.cells = self.random_cells(ncells) # Call random_cell function
        
    def __init__seq(self, ncells, nsteps):
        '''
        Initialize sequence of grid generations to zero, and add random
        first generation
        '''
        # Sequence has nsteps for number of rows and ncells for num columns
        self.seq = np.ndarray( [nsteps, ncells], dtype=np.int8 )
        self.seq.fill(0) # Fill sequence "matrix" with zeros
        self.seq[np.size(self.seq,0)-1] = self.cells 
        # Set current generation to be the randomly generated 64-bit number
        
    
    def plot(self, axes=None, flush=True):
        '''
        Plots the current state of the sequence matrix. A title is included
        with the rule number
        '''
        plt.figure(figsize=(12,8)) # Customize rule number
        # Add rule number as title
        plt.title('Random Start with Rule '+str(self.rule_num), fontsize=25) 
        # Plot image using a neutral color scheme
        plt.imshow( self.seq, cmap="Greys" )
        return self     

    def random_cells(self, ncells):
        '''
        Randomly generates a 'ncell'-bit number. Note output is a numpy array.
        '''
        # 'ncells' consisting of either a 0 or a 1
        return np.random.choice([0,1], size=ncells )

    def steps(self, nsteps=1):
        '''
        Advances the current state of the CA by nsteps and updates the sequence
        matrix.
        '''
        for i in range(nsteps):
            
            for i in range( np.size(self.seq,0) - 1): # For all rows except last
                self.seq[i] = self.seq[i+1] # Shift all rows up
            
            self.cells = self.cellular_step() # Calculate new generation
            # Update the current generation with new state
            self.seq[np.size(self.seq,0)-1, :] = self.cells
        
        return self

    def cellular_step(self):
        '''
        Caculates a new generation state for the CA using the specified rule
        number. A temp array is used to avoid using updated cells to determine
        new state of cells that have not yet been calculated.
        '''
        # Array to hold new generation of state
        newcells = np.zeros(self.ncells, dtype=np.int8) 
    
        # For each cell in array: obtain state and states of neighbors, calculate 
        # new state using rules1 function and update cell state in newcells
        for i in range(1,self.ncells-1):
            left = self.cells[i-1]
            middle = self.cells[i]
            right = self.cells[i+1]
            newstate = self.rules1(left, middle, right)
            newcells[i] = newstate
            
        self.cells = newcells # Update cells to new generation and return
        return self.cells
        
    def rules1(self, a, b, c):
        '''
        Determines next generation state for cell b, with neighbors a and c 
        (left and right), based on the passed rule_number.
        Returns new state of cell b
        '''
        # Generate 8-bit binary number representing rule number
        ruleset = binaryRep(self.rule_num, 8, numpy_array=True)
         
        # Possible states - in same order as 'Nature of Code' docuement
        truple = [(1,1,1), (1,1,0), (1,0,1), (1,0,0), (0,1,1), (0,1,0), (0,0,1), (0,0,0)]
        
        # Make lookup dict, to associate each state with future state
        lookup_dict = {} # Initialize dictionary
        
        # Range is used to iterate through elements of ruleset (indices 0-7=range(8))
        for indx,lmr in zip(range(8),truple):
            lookup_dict[lmr] = ruleset[indx] 
            # Ex: 1st key:(1,1,1), 1st value: ruleset[0]= first digit of binary
            # representation of rule_number
        
        return lookup_dict[a,b,c]   
    
# binaryRep function was left outside the CA object since it is not really
# "part" of the object, but rather a tool that the object uses
    
def binaryRep(num, num_bits, numpy_array=False):
    '''
    Calculates the binary representation for a given number of bits.
    Function requires that the parameter num is a positive integer.
    Parameters:
        num: Number whose binary value we want
        num_bit: Number of bits used in binary representation
        numpy_array: If True, return binary number stored in numpy array 
    Returns
        Binary representation of number with specified number of bits
    '''
    # Only unsigned integers will be accepted
    assert num >= 0, 'Negative Values are not acceptable'
    assert num%1 == 0, 'Number must be an integer'
    
    # Verify the number fits into specificed number of bits
    assert num <= (2**num_bits - 1), 'Number too large for that many bits'
    
    # Remove prefix and pad on left with zeros
    result = bin(num)[2:].zfill(num_bits) 
    
    # Return type is by default a string but optionally can be in form of 
    # a numpy array
    if numpy_array == True:
        result = np.array( [ int(num) for num in result  ] )
    
    return result
