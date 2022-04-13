import community as community_louvain
import networkx as nx

#read file
graph_file = 'abide4132_au_el2.txt'
label_file='4132_regions.txt'

with open(graph_file) as f:
    graph = f.readlines()
graph = [x.strip() for x in graph] 

with open(label_file) as f:
    label = f.readlines()

# offset  for one based indexing and removing new line 
label = ['$'] + [x.strip() for x in label ]


#input the label count
num_label=90 #here



#graph partitioning: graph list is split into  a sub_graph list of list
sub_graphs = [[] for i in range(num_label)]
for edge in graph:
    u,v=edge.split("\t")
    u,v=int(u),int(v)
   # print(u,v,"#")
    if label[u]==label[v]:
        #print(u,v,label[u],label[v])
        sub_graphs[int(label[u])-1].append(edge)
  
#louvain algorithm      
community_set=set()
vertex_comm_map=dict()
for sub_graph in sub_graphs:
    G = nx.parse_edgelist(sub_graph, delimiter="\t", nodetype=int)
    partition = community_louvain.best_partition(G)
    #print(partition)
    offset=len(community_set)
    for v in partition:
        partition[v]=partition[v]+offset
        community_set.add(partition[v])
    vertex_comm_map.update(partition)

#graph coarsening
coarsened_graph=set() 
new_label=dict()  
for edge in graph:
    uv=[]
    for vertex in edge.split("\t"):
        vertex=int(vertex)
        #checking if vertex is isolated after the label wise partition and assigning new community
        if vertex not in vertex_comm_map:
            vertex_comm_map[vertex]=len(community_set)
            community_set.add(vertex_comm_map[vertex])
        uv.append(vertex_comm_map[vertex])
        new_label[vertex_comm_map[vertex]]=label[vertex]
    u,v=uv
    #remove self loops u!=v     
    if u>v:
        u,v=v,u
    if u !=v:
        coarsened_graph.add(str(u)+" "+ str(v))

#write the result
coarsened_graph_file=open("coarsened_graph.txt","w")
new_label_file=open("new_label2.txt","w")
for edge in coarsened_graph:
    coarsened_graph_file.write(edge+'\n')
coarsened_graph_file.close()

for c in sorted(new_label):
    new_label_file.write(new_label[c]+'\n')
new_label_file.close()    
    
#print(coarsened_graph) 
