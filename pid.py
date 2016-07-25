# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 13:16:46 2016

@author: akshaybudhkar
"""
import control
import random

# Evalutate fiteness of a solution
def fitnessFunction(Kp, Ti, Td):
    G = control.tf([Ti*Td, Ti, 1], [Ti, 0])
    
    F = control.tf(1,[1,6,11,6,0])
    
    sys = control.feedback(control.series(G, F), 1)
    
    y = control.step(sys)
    
    yout = y[0]
    t = y[-1]
    
    error = 0
    
    for val in y[0]:
        error += (val - 1)*(val - 1)
        
    OS = (yout.max()/yout[-1]-1)*100
    Tr = t[next(i for i in range(0,len(yout)-1) if yout[i]>yout[-1]*.90)]-t[0]
    Ts = t[next(len(yout)-i for i in range(2,len(yout)-1) if abs(yout[-i]/yout[-1])>1.02)]-t[0]
    
    return 1/(OS + Tr + Ts + error*error)*1000
    
# Generate initial population set
def generate_initial_set(size):
    final_set = []
    count = 0
    while count < size:
        K = round(random.uniform(2, 18), 2)
        Ti = round(random.uniform(1.05, 9.42), 2)
        Td = round(random.uniform(0.26, 2.37), 2)
        
        if [K, Ti, Td] not in final_set:
            final_set.append([K, Ti, Td])
            count += 1
            
    return final_set

size = 50
total_gen = 150

print(generate_initial_set(size))





