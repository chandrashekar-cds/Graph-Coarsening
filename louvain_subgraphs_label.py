import community as community_louvain
import networkx as nx

#read file
graph_file = 'abide_au_2_4132_sparse.txt'
#label_file='4132_regions.txt'

with open(graph_file) as f:
    graph = f.readlines()
graph = [x.strip() for x in graph] 

G = nx.parse_edgelist(graph, delimiter="\t", nodetype=int)
partition = community_louvain.best_partition(G)
#print(partition)

comm_file=open("vertex_community_au_sparse2_run2.txt","w")

for comm in sorted(partition):
    comm_file.write(str(comm)+'\t'+str(partition[comm])+'\n')
comm_file.close()


num_comm = max(partition.values())+1

vertex_subsets = [set() for i in range(num_comm)]
subgraphs = [set() for i in range(num_comm)]
cut_edges = set()
for key in partition:
    vertex_subsets[partition[key]].add(key)

for edge in graph:
    u,v=edge.split("\t")
    u,v=int(u),int(v)
    flag = 0
    for comm in range(num_comm):
        if u in vertex_subsets[comm] and v in vertex_subsets[comm]:
            subgraphs[comm].add(edge)
            flag = 1
            break
    if flag == 0:
            cut_edges.add(edge)
	
#print(cut_edges)
for i in range(num_comm):
    print("subgraph ",i," contains ",len(subgraphs[i])," number of edges")
print("Cut edges are - ",len(cut_edges))


subgraph_file=open("subgraphs_au_sparse2_run2.txt","w")

for comm in range(num_comm):
    subgraph_file.write(str(comm)+'\n')
    subgraph_file.write(str(len(vertex_subsets[comm]))+'\t'+str(len(subgraphs[comm]))+'\n')
    #subgraph_file.write(sorted(vertex_subsets[comm]), key = lambda x: (len (x), x))
    i = 0
    vertid = dict()
    for vertex in sorted(vertex_subsets[comm]):
        vertid[vertex] = i
        i += 1
        subgraph_file.write(str(vertex)+'\n')
    #subgraph_file.write(sorted(subgraphs[comm]),key = lambda x: (len (x), x))
    edgelist = [[0 for k in range(2)] for m in range(len(subgraphs[comm]))]
    j=0
    for edge in sorted(subgraphs[comm]):
        u,v=edge.split("\t")
        u,v=int(u),int(v)
        edgelist[j][0],edgelist[j][1] = vertid[u],vertid[v]
        j += 1
    for l in sorted(edgelist,key=lambda x: (x[0],x[1])):    
        subgraph_file.write(str(l[0])+'\t'+str(l[1])+'\t'+str(1)+'\n')

subgraph_file.close()

