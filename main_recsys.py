import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math as math
import json
import time 
import os.path
from os import path
plt.style.use('seaborn')
plt.rcParams['figure.figsize'] = [14,14]

df = pd.read_csv('./database/anime_titles_cleaned.csv')
df['synopsis'].fillna("no synopsis", inplace=True)
df['score'].fillna("0.0", inplace=True)


df['categories'] = df['genre'].apply(lambda l: [] if pd.isna(l) else [i.strip() for i in l.split(",")])
df['Score'] = df['score'].astype(str)
df['Popularity'] = df['popularity'].astype(str)

dtst = df.head()

# print(dtst)


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.cluster import MiniBatchKMeans

# Build the tfidf matrix with the synopsiss
start_time = time.time()
text_content = df['synopsis']
vector = TfidfVectorizer(max_df=0.4,         
                             min_df=1,      
                             stop_words='english', 
                             lowercase=True,  
                             use_idf=True,   
                             norm=u'l2',     
                             smooth_idf=True 
                            )
tfidf = vector.fit_transform(text_content)

# Clustering  Kmeans
k = 200
kmeans = MiniBatchKMeans(n_clusters = k)
kmeans.fit(tfidf)
centers = kmeans.cluster_centers_.argsort()[:,::-1]
terms = vector.get_feature_names()

    
request_transform = vector.transform(df['synopsis'])

df['cluster'] = kmeans.predict(request_transform) 

def find_similar(tfidf_matrix, index, top_n = 5):
    cosine_similarities = linear_kernel(tfidf_matrix[index:index+1], tfidf_matrix).flatten()
    related_docs_indices = [i for i in cosine_similarities.argsort()[::-1] if i != index]
    return [index for index in related_docs_indices][0:top_n]  


#function to make graph    
def make_graph():
    G = nx.Graph(label="MOVIE")
    start_time = time.time()
    for i, rowi in df.iterrows():
        if (i%1000==0):
            print(" iter {} -- {} seconds --".format(i,time.time() - start_time))
        G.add_node(rowi['title'],key=rowi['uid'],label="MOVIE",score=rowi['score'],linkToMAL=rowi['link'])

        for element in rowi['Popularity']:
            G.add_node(element,label="POPULARITY")
            G.add_edge(rowi['title'], element, label="POP")
        for element in rowi['categories']:
            G.add_node(element,label="CAT")
            G.add_edge(rowi['title'], element, label="CAT_IN")

        
        indices = find_similar(tfidf, i, top_n = 5)
        snode="Sim("+rowi['title'][:15].strip()+")"        
        G.add_node(snode,label="SIMILAR")
        G.add_edge(rowi['title'], snode, label="SIMILARITY")
        for element in indices:
            G.add_edge(snode, df['title'].loc[element], label="SIMILARITY")
    print(" finish -- {} seconds --".format(time.time() - start_time))
    nx.write_gpickle(G, "./database/complied/data4.pickle")
    return G
#to check if pickle exists to save time
check_pickle = path.exists("./database/complied/data4.pickle")

if (check_pickle):
    G = nx.read_gpickle("./database/complied/data4.pickle")
else:
    G = make_graph()


def get_all_adj_nodes(list_in):
    sub_graph=set()
    for m in list_in:
        sub_graph.add(m)
        for e in G.neighbors(m):        
                sub_graph.add(e)
    return list(sub_graph)
def draw_sub_graph(sub_graph):
    subgraph = G.subgraph(sub_graph)
    colors=[]
    for e in subgraph.nodes():
        if G.nodes[e]['label']=="MOVIE":
            colors.append('blue')
        elif G.nodes[e]['label']=="POPULARITY":
            colors.append('red')
        elif G.nodes[e]['label']=="CAT":
            colors.append('green')
        elif G.nodes[e]['label']=="COU":
            colors.append('yellow')
        elif G.nodes[e]['label']=="SIMILAR":
            colors.append('orange')    
        elif G.nodes[e]['label']=="CLUSTER":
            colors.append('orange')

    nx.draw(subgraph, with_labels=True, font_weight='bold',node_color=colors)
    plt.show()



def get_recommendation(root):
    aN = root.lower()
    commons_dict = {}
    if G.has_node(root):
        for e in G.neighbors(root):
            for e2 in G.neighbors(e):
                if e2 == root:
                    continue
                if G.nodes[e2]['label']=="MOVIE":
                    commons = commons_dict.get(e2)
                    if commons==None:
                        commons_dict.update({e2 : [e]})
                    else:
                        commons.append(e)
                        commons_dict.update({e2 : commons})
        movies=[]
        weight=[]
        for key, values in commons_dict.items():
            w=0.0
            for e in values:
                w=w+1/math.log(G.degree(e))
            movies.append(key) 
            weight.append(w)
    
        result = pd.Series(data=np.array(weight),index=movies)
        result.sort_values(inplace=True,ascending=False)        
        result.to_json(r'./results.json')
        # return result
        a = ""
        return a
    else:
        a = "Not Found"
        return a




