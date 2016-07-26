# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 13:16:46 2016

@author: akshaybudhkar
"""
import control
import random
import matplotlib.pyplot as plt

# Evalutate fiteness of a solution
def fitnessFunction(Kp, Ti, Td):
    G = control.tf([Ti*Td, Ti, 1], [Ti, 0])
    
    F = control.tf(1,[1,6,11,6,0])
    
    sys = control.feedback(control.series(G, F), 1)
    
    y = control.step(sys)
    
    yout = y[0]
    t = y[-1]
    
    # Integrated Square Error
    error = 0
    
    for val in y[0]:
        error += (val - 1)*(val - 1)
       
    # Overshoot
    OS = (yout.max()/yout[-1]-1)*100
    
    Tr = 0
    Ts = 0
    
    # Rising Time
    for i in range(0, len(yout) - 1):
        if yout[i] > yout[-1]*.90:
            Tr = t[i] - t[0]
    
    # Settling Time            
    for i in range(2, len(yout) - 1):
        if abs(yout[-i]/yout[-1]) > 1.02:
            Ts = t[len(yout) - i] - t[0]
    
    return 1/(OS + Tr + Ts + error*error*10)*100000
    
# Generate initial population set
def generate_initial_set(size):
    final_set = []    
    refined_set = []
    count = 0
    while count < size:
        K = round(random.uniform(2, 18), 2)
        Ti = round(random.uniform(1.05, 9.42), 2)
        Td = round(random.uniform(0.26, 2.37), 2)
        
        if [K, Ti, Td] not in final_set:
            final_set.append([K, Ti, Td])
            
            fitness = fitnessFunction(K, Ti, Td)
            
            refined_set.append({"params": [K, Ti, Td],
                                "fit": round(fitness, 3)})
            count += 1
     
    return refined_set


def check_limits(K, Ti, Td):
    if K < 2:
        K = 2
    
    if K > 18:
        K = 18
    
    if Ti < 1.05:
        Ti = 1.05
        
    if Ti > 9.42:
        Ti = 9.42
        
    if Td < 0.26:
        Td = 0.26
        
    if Td > 2.37:
        Td = 2.37
        
    return [K, Ti, Td]
    
    
def crossover(lst):
    final = []
  
    for i in range(0, len(lst) - 1, 2):
        parent1 = lst[i]
        parent2 = lst[i+1]
        rand = random.random()
        
        # Do a crossover
        if rand < 0.6:
            # Whole arithmetic crossover used
            alpha = 0.9
            
            #child 1
            K1 = alpha*parent1['params'][0] + (1-alpha)*parent2['params'][0]
            Ti1 = alpha*parent1['params'][1] + (1-alpha)*parent2['params'][1]
            Td1 = alpha*parent1['params'][2] + (1-alpha)*parent2['params'][2]
            
            final.append({"params": check_limits(K1, Ti1, Td1),
                          "fit": round(fitnessFunction(K1, Ti1, Td1), 3)})
                          
            #child 2
            K2 = alpha*parent2['params'][0] + (1-alpha)*parent1['params'][0]
            Ti2 = alpha*parent2['params'][1] + (1-alpha)*parent1['params'][1]
            Td2 = alpha*parent2['params'][2] + (1-alpha)*parent1['params'][2]
            
            final.append({"params": check_limits(K2, Ti2, Td2),
                          "fit": round(fitnessFunction(K2, Ti2, Td2), 3)})
        else:
            final.append(parent1)
            final.append(parent2)
            
    
    return final


def mutate(lst):
    final = []
    
    for i in range(len(lst)):
        rand = random.random()
        
        # Mutate
        if rand < 0.25:
            # Uniform mutation is used
            mut_rand = random.random()
            K = 2 + mut_rand*(18 - 2)
            Ti = 1.05 + mut_rand*(9.42 - 1.05)
            Td = 0.26 + mut_rand*(2.37 - 0.26)
            
            final.append({"params": [K, Ti, Td],
                          "fit": round(fitnessFunction(K, Ti, Td), 3)})
                          
        else:
            final.append(lst[i])
            
    return final
    
    
def genetic_algorithm(initial_population, total_gen):
    
    current_gen = 0
    current_pop = sorted(initial_population, key= lambda k: k['fit'])
    
    fits = []
    while current_gen < total_gen:
        sum_fit = sum([x['fit'] for x in current_pop])
        avg_prob = (sum([x['fit']/sum_fit for x in current_pop]))/len(current_pop)    
        parent_pop = []
        
        for sol in current_pop:
            prob = sol['fit']/sum_fit
            expected_count = prob/avg_prob
            actual_count = int(round(expected_count))
            
            for i in range(actual_count):
                parent_pop.append(sol)
                    
        random.shuffle(parent_pop)
        cross_pop = crossover(parent_pop)
        
        random.shuffle(cross_pop)
        mutate_pop = sorted(mutate(cross_pop), key= lambda k: k['fit'])
        
        best = mutate_pop[-1]
        best_2 = mutate_pop[-2]
        
        current_pop[0] = best
        current_pop[1] = best_2
        
        current_pop = sorted(current_pop, key= lambda k: k['fit'])
        current_gen += 1
        
        print(current_pop[-1]["fit"])        
        fits.append(current_pop[-1]["fit"])
        
    
    plt.plot(fits)            
    return current_pop[-1]
        
size = 50
total_gen = 150
pc = 0.6
pm = 0.25

init = generate_initial_set(size)
print(genetic_algorithm(init, total_gen))





