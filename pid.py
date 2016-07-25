# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 13:16:46 2016

@author: akshaybudhkar
"""
import control
import math

#def step_info(t,yout):
#    # [OS, Tr, Ts]
#    return [(yout.max()/yout[-1]-1)*100,
#    t[next(i for i in range(0,len(yout)-1) if yout[i]>yout[-1]*.90)]-t[0],
#    t[next(len(yout)-i for i in range(2,len(yout)-1) if abs(yout[-i]/yout[-1])>1.02)]-t[0]]

def performanceFunction(Kp, Ti, Td):
    G = control.tf([Ti*Td, Ti, 1], [Ti, 0])
    
    F = control.tf(1,[1,6,11,6,0])
    
    sys = control.feedback(control.series(G, F), 1)
    
    y = control.step(sys)
    
    error = 0
    
    for val in y[0]:
        error += (val - 1)*(val - 1)
        
    return error
    
print(performanceFunction(2, 18, 10))


