# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 01:02:40 2018

@author: Ken
"""

def scope_test():
    def do_local():
        spam = "local spam"
    
    def do_nonlocal():
        nonlocal spam
        spam = "nonlocal spam"
    
    def do_global():
        global spam
        spam = "global spam"
    
    spam = "test spam"
    do_local()
    print("After local assignment:", spam)

scope_test()