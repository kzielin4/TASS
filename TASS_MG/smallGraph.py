import networkx as nx
import pylab as plt
import scipy.cluster.hierarchy as hierarchy
import time


def drawGraph(graph,filename):
    nx.draw(graph)
    nx.draw_random(graph)
    nx.draw_circular(graph)
    nx.draw_spectral(graph)
    plt.savefig(filename)
    print "Draw graph to file ",filename

def readGraphPajek(graph_filename):
    g = nx.read_pajek(graph_filename)
    # print information about graph
    print nx.info(g)
    print "Directed: ", g.is_directed()

    return g

def readGraphGml(graph_filename):
    g = nx.read_gml(graph_filename)
    # print information about graph
    print nx.info(g)
    print "Directed: ", g.is_directed()
    return g

#Funkcja przyjmuje jako argument liste i zwraca 5 najwiekszych elementow
def getTop5VertexValue(inList):
    sortedList = sorted(inList.iteritems(),
                        key=lambda n: -n[1] ) #klucz sortowania "-" bo desc
    return sortedList[:5]

#Funkcja zwraca mape klikow z iloscia wystapien danego rzedu
def getCliquesSizeList(cliques):
    cliqueAmmountSizeValues = {}
    for clique in cliques:
        sizeOfClique = len(clique)
        if sizeOfClique in cliqueAmmountSizeValues:
            preValue = cliqueAmmountSizeValues[sizeOfClique]
            cliqueAmmountSizeValues[sizeOfClique] = preValue +1
        else:
            preValue = 0
            cliqueAmmountSizeValues[sizeOfClique] = preValue + 1
    return cliqueAmmountSizeValues

#Funkcja grupujaca aglomeracyjne, identyfikator grupowania - single linkage
#Funkcja rysuje tez dendrogram
def saveDendogramSingleLinkage(graph):
    matrix = nx.to_scipy_sparse_matrix(graph)
    matrixDense = matrix.todense()
    clusters = hierarchy.linkage(matrixDense, method='single')
    hierarchy.dendrogram(clusters, show_leaf_counts=True)
    plt.title("dendrogram")
    plt.savefig('dendrogram.png')
    print 'Save dendrogram.png'

if __name__ == "__main__":
    #Wczytanie grafu i konwersja
    graphMulti = readGraphPajek("netscience.net")
    #nx.write_gml(graphMulti, 'netsciencePajek.gml')
    print "\nConvert graph from gml to net\n"
    graph = nx.Graph(graphMulti)
    print nx.info(graph)
    print "Directed: ", graph.is_directed(), "\n"

############################################################################

    # Wczytanie grafu i konwersja
    # graphDi = readGraphGml("netscience.gml")
    # #nx.write_gml(graphMulti, 'netsciencePajek.gml')
    # #print "\nConvert graph from gml to net\n"
    # graph = nx.Graph(graphDi)
    # print nx.info(graph)
    # print "Directed: ", graph.is_directed(), "\n"

############################################################################

    #Rysowanie grafu
    drawGraph(graph, "grafJPG.jpg")

############################################################################

    #Skladowe spojne
    print "Number of components: ", nx.number_connected_components(graph)
    start = time.time()
    conectedComponent = max(nx.connected_component_subgraphs(graph), key=len)
    end = time.time()
    print "Duration: ",end - start,"\n"
    print "Largest connected component range: ", conectedComponent.number_of_nodes()
    print "Largest connected components size: ", conectedComponent.number_of_edges()

############################################################################

    #Najwieksze wartosci
    top5Betweenness = getTop5VertexValue(nx.betweenness_centrality(conectedComponent))
    top5Closeness = getTop5VertexValue(nx.closeness_centrality(conectedComponent))
    top5Rang = getTop5VertexValue(nx.pagerank(conectedComponent))
    print "Top 5 - Betweenness","\n",top5Betweenness
    print "Top 5 - Closeness","\n",top5Closeness
    print "Top 5 - Rang","\n",top5Rang

############################################################################

    #Klika
    cliques = list(nx.find_cliques(conectedComponent))
    print "Number of cliques in graph: ",cliques.__len__()
    cliquesLenList = getCliquesSizeList(cliques)
    for size, number in cliquesLenList.items():
        print'Number of clique with size', size , ': ', number
############################################################################

    #Single linkage
    max_cliques = list(nx.find_cliques(conectedComponent))
    saveDendogramSingleLinkage(conectedComponent)
    i=2
############################################################################
############################################################################
############################################################################

