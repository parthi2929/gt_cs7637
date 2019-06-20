"""
These are helper functions to visualize, and comprehend the many coin flips problem
Author: Parthiban Rajendran
Email: parthi292929@gmail.com
Date: 19th Jul 2018
Github: https://github.com/parthi2929
License: Kindly credit if used/shared
"""
from graphviz import Digraph
import pandas as pd 
import matplotlib.pyplot as plt
# from sympy import binomial
import numpy as np
from random import choice, seed

# statistical flip functions.. 
seed(0)  # just for consistent result every time..   

def draw_graph(g, n_flips=2, probs = ['p','q']):
    """
    Given no of flips, this function creates a corresponding probability tree
    """
    #g.attr(rankdir='LR', ranksep='0.5')
    g.attr('node', shape='circle', fontsize='10')
    g.attr('edge', fontsize='10')
    g.node('Root','R',style='filled', fillcolor='#DCDCDC')    # first node
    
    i_outcome = 1
    parent_list = []
    
    for each_flip in range(1, n_flips+1):
        n_outcomes = 2**each_flip
        
        temp_list = []
        p_index = 0 # parent index for each node
        for each_outcome in range(0, int(n_outcomes/2)):  
            
            # draw nodes, record parents
            new_H = 'H{}'.format(i_outcome) 
            new_T = 'T{}'.format(i_outcome)             
            g.node(new_H, 'H', style='filled', fillcolor='#FFFAAE')
            g.node(new_T, 'T', style='filled', fillcolor='#D2FFFF')                     
            i_outcome += 1
            parents = parent_list[-1] if len(parent_list) > 0 else []
            parent = parents[p_index] if len(parents) > 0 else None
            
            # debug
            #print('Flip:{} New H:{} New T:{} Parents:{} Parent Index:{}'.format(each_flip, new_H, new_T,list(parents), p_index))
            #print('Flip:{} New H:{} New T:{} Parent:{}'.format(each_flip, new_H, new_T,parent))
            
            # draw edges
            if parent is not None:
                g.edge(parent, new_H,'<<b>{}</b>>'.format(probs[0]),fontcolor='red')
                g.edge(parent, new_T,'<<b>{}</b>>'.format(probs[1]),fontcolor='blue')
            else: 
                g.edge('Root', new_H,'<<b>{}</b>>'.format(probs[0]),fontcolor='red')
                g.edge('Root', new_T,'<<b>{}</b>>'.format(probs[1]),fontcolor='blue')
                
            
            # for next set of H and T
            p_index += 1
            temp_list.append(new_H)
            temp_list.append(new_T)
            
            
            
        parent_list.append(temp_list)
        print()
    return g

def tosses(N):
    
    L = [''] 
    dicty = { 'sequence' : [], 'x' : []}  # x is no of heads in a sequence
    for i in range(0,N):
        L=[l+'H' for l in L]+[l+'T' for l in L]
               
    index = 0
    for each_L in L:
        county = each_L.count('H')        
        #dicty[index] = {'sequence': each_L, 'x': county}
        dicty['sequence'].append(each_L)
        dicty['x'].append(county)
        index +=1
        
    #return L
    return dicty

def get_combinations(n_flips=2):
    """
    Given the no of flips, this function will provide the final sequence combinations as a panda dataframe
    """
    # setup data frame with necessary cols
    columns = ['sequence', 'x']
    df = pd.DataFrame(columns=columns)
    
    # get the combinations
    # from itertools import product
    # for i in product(['H','T'], repeat=n_flips):     
    #     combi = ''.join(i)
    #     n_H = combi.count('H') # no of heads
    #     df = df.append({'sequence': combi, 'x': n_H }, ignore_index=True)

    # trying alternate faster method
    temp_dict = tosses(n_flips)
    df = pd.DataFrame.from_dict(temp_dict)
        
    # get no of heads in the combinations
    #print('Given no of flips:', n_flips)
    #print('\nx = no of heads in respective sequence')
        
    return df

def get_combinations_consolidated(n_flips=2):
    """
    Given the raw dataframe of combinations, this will provide n(x) and p(x)
    """
    # setup data frame with necessary cols
    columns = ['x', 'n(x)', 'p(x)']
    df = pd.DataFrame(columns=columns)
    
    # get raw data
    combi_df = get_combinations(n_flips=n_flips)
    x_list = combi_df['x'].tolist()
    
    # extract frequency
    #ref: https://stackoverflow.com/questions/2161752/how-to-count-the-frequency-of-the-elements-in-a-list/2162045
    x_list.sort()
    from itertools import groupby 
    freq_tuple = [ (key, len(list(group))) for key, group in groupby(x_list)]
    #print(freq_tuple)
    
    for each_freq_tuple in freq_tuple:
        x = each_freq_tuple[0]
        n_x = each_freq_tuple[1]
        p_x = n_x/(2**n_flips)  # its a conditional probability, thats y divided by total outcomes
        df = df.append({'x': x, 'n(x)': n_x, 'p(x)': p_x }, ignore_index=True)
        
    # convert cols to integer (except p(x))
    df[['x','n(x)']] = df[['x','n(x)']].astype(int) #ref: https://stackoverflow.com/questions/21291259/convert-floats-to-ints-in-pandas/21291622

    #print('n(x) = total no of possible x type sequences')
    #print('for eg, if x = 2, n(x) = 3, then there are 3 possible sequence types, in each of which, no of heads is 2')    
    
    #print('\np(x) = conditional probability that n(x) could occur out of all outcomes')
    
    return df

def autoformat(ax, xlabel, ylabel, fontsize): 
    """
    Few tweaks for better graph
    """
    ax.set_xlabel(xlabel, fontsize=fontsize)
    ax.set_ylabel(ylabel, fontsize=fontsize)
    
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(fontsize) # Size here overrides font_prop
        
    ymin = ax.get_ylim()[0]
    ymax = ax.get_ylim()[1]*1.1  # increase space to insert bar value
    ax.set_ylim([ymin,ymax])    

    # x values should be integers as its no of heads
    xmin = -1
    xmax = ax.get_xlim()[1]
    from math import ceil
    xmaxint = ceil(xmax)+1
    xint = range(xmin, xmaxint)
    ax.set_xticks(xint)

def autolabel(ax, rects, fontsize):
    """
    Attach a text label above each bar displaying its height
    ref: https://matplotlib.org/2.0.2/examples/api/barchart_demo.html
    """    
    for rect in rects:
        height = rect.get_height()
        #text = '%.4f' % height
        text = '{0: <{width}}'.format(height, width=1) 
        ax.text(rect.get_x() + rect.get_width()/2., 1.005*height,text, ha='center', va='bottom', fontsize=fontsize+3, color='red')

def plot_combinations_consolidated(df, fontsize=10, label=True):
    """
    Given the dataframe with x, n(x), p(x) this provides two plots:
    x vs n(x)
    x vs p(x)
    """
    fig, (ax1, ax2) = plt.subplots(1,2, figsize=(12,5))
    
    X = df['x'].tolist()
    N = df['n(x)'].tolist()
    P = df['p(x)'].tolist()
    
    rects = ax1.bar(X, N)
    if label == True:
        autolabel(ax1, rects, fontsize)
    
    xlabel = 'No of Heads'
    ylabel = 'No of Sequences\nhaving those no of Heads'   
    autoformat(ax1, xlabel, ylabel, fontsize)
    

    rects = ax2.bar(X, P)
    if label == True:
        autolabel(ax2, rects, fontsize)
    
    ylabel = 'Probability of ANY of Sequences\nhaving those no of Heads'   
    autoformat(ax2, xlabel, ylabel, fontsize)

    ax1.title.set_text('Fig A: Frequency Distribution')
    ax2.title.set_text('Fig B: Probability Mass Function')
    
    plt.tight_layout()
    plt.subplots_adjust(wspace=0.45)    
    plt.show()

# def get_combinations_consolidated_turbo(N=2, p=0.5):
#     """
#     Given the  no of flips, this will provide dataframe: x, n(x) and p(x)
#     WITHOUT CALCULATING INDIVIDUAL COMBINATIONS
#     """
#     q = 1-p
#     k = np.linspace(0,N,N+1)
#     X = [ binomial(N, i) for i in range(N+1)]
#     P = [ X[i]*(p**i)*(q**(N-i)) for i in range(0,len(X)) ]
#     df = pd.DataFrame({'x': k, 'n(x)': X, 'p(x)': P})
#     return df

def flip(n_flips, p_H):
    """
    Flip N times and return no of heads in the outcome
    """

    final_sequence = []
    for i in range(n_flips):  # 0 to (N-1) times..
        flip_result = np.random.choice([1,0],p=[p_H,1-p_H]) # you could change probs here and observe outcome
        flip_result = 'H' if flip_result == 1 else 'T'
        final_sequence.append(flip_result)
    return final_sequence.count('H')

def sample(n_experiments, n_flips, p_H=0.5):
    """
    Conduct experiment given no of times
    In each experiemnt, flip given no of times, and update n_X
    """
    from collections import defaultdict
    samples = defaultdict(lambda: 0)
    for each_experiment in range(0, n_experiments):
        X = flip(n_flips,p_H)  # X is no of heads in the outcome sequence of n_flips        
        samples[X] += 1
        #print(each_experiment, dict(samples))
        
    # convert to pandas
    df = pd.DataFrame([[key,value] for key,value in samples.items()],columns=['x','n(x)'])
    df.sort_values('x', inplace=True)
    total_outcomes = df['n(x)'].sum()
    df['p(x)'] = df['n(x)']/total_outcomes
    return df