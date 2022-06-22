import seaborn as sb
import matplotlib.pyplot as plt 
import numpy as np
import colors as cs
import random as rd
from scipy.cluster.hierarchy import dendrogram
from itertools import chain, combinations
import networkx as nx



__all__  = ['graphnx']

class graphplot:
    '''
    Plot different distributions
     -  Conectivity Diagram of diferent networks
     -  Logarithmic distribution degree for diferent networks.
            * Shortest Path Lenth
            * Degree
            * Clustering 
     -  Betwenness Centrality graph.
     -  Network Efficiency.
     - Calculate and plot louvain partitions

     - Dendogram using Girvan - Newman algorithm**

    **Warning: For a bigger network is not possible Girvan - Newman dendogram. 

    Every graph will save with main method + random number on your directory.

    Example:
    Dendogram_45.png

    Parameters.
    ----------
    incoming_graph_data : input graph (G)

    Example.
    graphnetworkx = gc.graphplot(G)
    
    #For distributions
    graphnetworkx.Diagrama_connectivity()
    '''
    def __init__(self,G):
        self.graphix = G
        self.distribution = []
        self.random = rd.randint(0,1000)
    def Diagram_conectivity(self):
        self.graphix = self.graphix
        degree_dict = dict(nx.degree(self.graphix))
        sequence = sorted(degree_dict.values(),reverse=True)
        fig = plt.figure(figsize=(12,8))
        ax_1 = fig.add_subplot(221)
        hist = plt.hist(sequence,bins=50)
        plt.xlabel("$K$")
        plt.ylabel("$P(K)$")
        plt.title("Diagram distribution.")
        ax_2 = fig.add_subplot(222)
        for i in range(len(hist[1])-1):self.distribution.append(hist[1][i])
        plt.loglog(self.distribution,hist[0],"y.")
        plt.title("Logarithmic distribution degree")
        plt.xlabel("$\log{(P(k))}$")
        plt.ylabel("$\log{(k)}$")
        plt.xscale('log')
        plt.yscale('log')
        plt.savefig("Diagram_log_{}".format(self.random))
    def ssdc(self):#Shortes Path - Degreee - Clustering
        self.graphix = self.graphix
        mat = nx.to_numpy_array(self.graphix)
        p_t = np.logspace(0.0,1.0,np.shape(mat)[1])
        f = [len(c) for c in sorted(nx.shortest_path_length(self.graphix), key=len, reverse=True)]
        d = dict(nx.degree(self.graphix))
        seq = sorted(d.values(),reverse=True)
        u = dict(nx.clustering(self.graphix))
        wq = sorted(u.values(),reverse=True)
        fig = plt.figure(figsize=(12,8))
        sb.scatterplot(x=p_t,y=f,label='Shortest Path Length .')
        sb.scatterplot(x=p_t,y=seq,label = 'Degree.')
        sb.scatterplot(x=p_t,y=wq,label ='Clustering.')
        plt.grid(True) 
        plt.xscale("log")
        plt.savefig("Diagram_three_distributions_{}".format(self.random))
    #Network Efficiency.
    def NetEfficiency_Betenness(self):
        self.graphix = self.graphix
        values = []
        for x,y in nx.betweenness_centrality(self.graphix).items():
            if y!=0:
                values.append((x,y))
            else:
                pass #Not values with 0
        """
        We changed to dictinary to list to be able  to get the keys.
        In this case, the most important nodes from the network.
        And finally, they'll plot the networkx.
        """
        r = rd.randint(0,len(cs.hexcol()))
        dict_network = dict((t,y) for t,y in values)
        fig =  plt.figure(figsize=(12,8))
        ax_1 = fig.add_subplot(221)
        nx.draw_spring(self.graphix,nodelist=sorted(dict_network.keys()),
        node_size = 50,
        node_color = cs.hexcol()[r])
        Betwennessg = dict_network
        '''
        Calculate Efficienty and Betenness of the networks.
        Parameters:
        ----------
        NetEfficiency_Betenness(G)
        Return a graph
        '''
        self.graphix = self.graphix
        ef = []
        fm = []
        for j in Betwennessg.keys():
            try:
                print("Nodo {} y Nodo {}. Eficiencia: {}".format(self.graphix,j,j+1))
                ef.append(nx.efficiency(self.graphix,j,j+1))
                fm.append({j,j+1})
            except:
                break
        seq_ef = sorted(ef,reverse=True)
        ax_2 = fig.add_subplot(222)
        hist = plt.hist(seq_ef,bins=len(ef))
        plt.title("Efficiency Distribution Diagram.png")
        plt.xlabel("$\epsilon _{i}$")
        plt.ylabel("$K$")
        plt.savefig("Efficiency Distribution Diagram.png")
        plt.savefig('Efficiency and Betenness distribution diagram_{}.png'.format(self.random))
    def plot_louvain_graph(self):
        self.graphix = self.graphix
        aux = []
        lis_col = cs.hexcol()
        val_n = 0
        louvain_p = nx.community.louvain_communities(self.graphix)
        g = globals()
        k = len(louvain_p)
        try:
            while val_n <len(louvain_p):
                r = rd.randint(0,len(lis_col))
                aux.append(lis_col[r])
                val_n +=1
        except IndexError:
            while val_n <len(louvain_p):
                r = rd.randint(0,len(lis_col))
                aux.append(lis_col[r])
                val_n +=1
        else:
            while k>0:
                for i in range(0,len(louvain_p)):
                    g['part{0}'.format(i)] = [y for y in louvain_p[i]] #Genera las variables dinamicas
                k-=1
            else:
                ax = plt.figure(figsize=(12,8))
                pos = nx.spring_layout(self.graphix)
                nx.draw(self.graphix,pos,edge_color='k',with_labels=False,
                font_weight = 'light',node_size = 50, width=0.9)
                for x in range(0,len(louvain_p)):
                    nx.draw_networkx_nodes(self.graphix,pos,nodelist=g['part{0}'.format(x)],node_color=aux[x])
                    plt.scatter([],[],c = aux[x],label = 'Group {}'.format(x))
                plt.legend()
                plt.savefig("fig_{}.png".format(r))
                plt.plot()
    def Dendogram_gn(self):
        self.graphix = self.graphix
        dn = nx.community.girvan_newman(self.graphix)
        data = list(dn)
        communities = data

        # building initial dict of node_id to each possible subset:
        node_id = 0
        init_node2community_dict = {node_id: communities[0][0].union(communities[0][1])}
        for comm in communities:
            for subset in list(comm):
                if subset not in init_node2community_dict.values():
                    node_id += 1
                    init_node2community_dict[node_id] = subset
        # turning this dictionary to the desired format in @mdml's answer
        node_id_to_children = {e: [] for e in init_node2community_dict.keys()}
        for node_id1, node_id2 in combinations(init_node2community_dict.keys(), 2):
            for node_id_parent, group in init_node2community_dict.items():
                if len(init_node2community_dict[node_id1].intersection(init_node2community_dict[node_id2])) == 0 and group == init_node2community_dict[node_id1].union(init_node2community_dict[node_id2]):
                    node_id_to_children[node_id_parent].append(node_id1)
                    node_id_to_children[node_id_parent].append(node_id2)
        # also recording node_labels dict for the correct label for dendrogram leaves
        node_labels = dict()
        for node_id, group in init_node2community_dict.items():
            if len(group) == 1:
                node_labels[node_id] = list(group)[0]
            else:
                node_labels[node_id] = ''
        # also needing a subset to rank dict to later know within all k-length merges which came first
        subset_rank_dict = dict()
        rank = 0
        for e in communities[::-1]:
            for p in list(e):
                if tuple(p) not in subset_rank_dict:
                    subset_rank_dict[tuple(sorted(p))] = rank
                    rank += 1
        subset_rank_dict[tuple(sorted(chain.from_iterable(communities[-1])))] = rank
        # my function to get a merge height so that it is unique (probably not that efficient)
        def get_merge_height(sub):
            sub_tuple = tuple(sorted([node_labels[i] for i in sub]))
            n = len(sub_tuple)
            other_same_len_merges = {k: v for k, v in subset_rank_dict.items() if len(k) == n}
            min_rank, max_rank = min(other_same_len_merges.values()), max(other_same_len_merges.values())
            range = (max_rank-min_rank) if max_rank > min_rank else 1
            return float(len(sub)) + 0.8 * (subset_rank_dict[sub_tuple] - min_rank) / range
        # finally using @mdml's magic, slightly modified:
        G           = nx.DiGraph(node_id_to_children)
        nodes       = G.nodes()
        leaves      = set( n for n in nodes if G.out_degree(n) == 0 )
        inner_nodes = [ n for n in nodes if G.out_degree(n) > 0 ]
        # Compute the size of each subtree
        subtree = dict( (n, [n]) for n in leaves )
        for u in inner_nodes:
            children = set()
            node_list = list(node_id_to_children[u])
            while len(node_list) > 0:
                v = node_list.pop(0)
                children.add( v )
                node_list += node_id_to_children[v]
            subtree[u] = sorted(children & leaves)
        inner_nodes.sort(key=lambda n: len(subtree[n])) # <-- order inner nodes ascending by subtree size, root is last
        # Construct the linkage matrix
        leaves = sorted(leaves)
        index  = dict( (tuple([n]), i) for i, n in enumerate(leaves) )
        Z = []
        k = len(leaves)
        for i, n in enumerate(inner_nodes):
            children = node_id_to_children[n]
            x = children[0]
            for y in children[1:]:
                z = tuple(sorted(subtree[x] + subtree[y]))
                i, j = index[tuple(sorted(subtree[x]))], index[tuple(sorted(subtree[y]))]
                Z.append([i, j, get_merge_height(subtree[n]), len(z)]) # <-- float is required by the dendrogram function
                index[z] = k
                subtree[z] = list(z)
                x = z
                k += 1
        # dendrogram
        plt.figure(figsize=(12,8))
        plt.savefig('Dendogram_{}'.format(self.random))
        dendrogram(Z, labels=[node_labels[node_id] for node_id in leaves])
if '__name__'  == '__main__':
    try:
        graphplot = graphplot()
    except:
        pass
graphplot.__doc__

