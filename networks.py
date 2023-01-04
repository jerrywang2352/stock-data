import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from scipy.sparse.csgraph import laplacian


class Fiedler:
    '''
    Generates networks and correlation matrices for data sets 
    using the fiedler partition of eigenvectors 
    '''
    def __init__(self):
        '''
        correlation -> numpy correlation matrix for a given data set
        '''
        self.correlation = None
        self.inList = []
        self.outList = []
    def build_matrix(self,filePath):
        '''
        Requires: a valid filePath 
        Effects: builds a correlation matrix, input/output list of node connections
        '''
        try:
            self.correlation = pd.read_csv(filePath)
        except:
            print("Invalid file path")
            return

        l = list(self.correlation.columns)[1:]
        tickD = {}
        for i in range(len(l)):
            tickD[l[i]] = i+1
            
        self.correlation = self.correlation.set_index('Unnamed: 0')
        for col in l:
            for row in l:
                d = self.correlation[col]
                if col != row and d.loc[row]:
                    d = self.correlation[col]
                    self.inList.append(str(tickD[row]) + ": " + row)
                    self.outList.append(str(tickD[col]) + ": " + col)

    def laplace_matrix(self):
        '''
        Return: Laplacian matrix based on the current correlation matrix
        '''
        laplace = laplacian(self.correlation.to_numpy())
        return laplace

    def build_graph(self):
        '''
        Precondition: build_matrix is called already
        Effects: Plots a Fiedler network of nodes based on the given laplacian matrix
        Return: None
        '''
        df = pd.DataFrame({ 'from':self.inList, 'to':self.outList})

        # Build your graph
        G=nx.from_pandas_edgelist(df, 'from', 'to')
        nx.draw(G, with_labels=True,node_size=2000,font_size=10, node_color="skyblue")
        plt.show()

f = Fiedler()

f.build_matrix('asset_correlation.csv')
print(f.laplace_matrix())
f.build_graph()