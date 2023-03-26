import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize
from sklearn.manifold import TSNE
from scipy import sparse
from sklearn.decomposition import PCA
from nltk.stem import PorterStemmer
import Stemmer

english_stemmer = Stemmer.Stemmer('en')
class StemmedTfidfVectorizer(TfidfVectorizer):
    def build_analyzer(self):
        analyzer = super(TfidfVectorizer, self).build_analyzer()
        return lambda doc: english_stemmer.stemWords(analyzer(doc))
    

def docs_to_vecs(sub_df,additioinal_stop_words = []):
    new_stop_words = [x for x in ENGLISH_STOP_WORDS] 
    [new_stop_words.append(x) for x in additioinal_stop_words]
    vectorizer = StemmedTfidfVectorizer(max_df=0.95,min_df=2, stop_words=new_stop_words)
    X = vectorizer.fit_transform(sub_df.abstract)
    
    return X

def Vecs_to_Sim_matrix(X):
    # Create similarity matrix
    # Erum með sparse matrix, viljum optimizea fyrir það. 
    Sim_matrix = cosine_similarity(X)
    # Diagonal = 0
    
    np.fill_diagonal(Sim_matrix,0)
    # Normalize to sum = 1
    Sim_matrix = normalize(Sim_matrix)
    
    return Sim_matrix

def get_coords(sub_df,X_emb):
    sub_df.loc[:,'x'] = X_emb[:,0]
    sub_df.loc[:,'y'] = X_emb[:,1]
    return sub_df

def without_PCA(df,max_values = 8_000):

    # If dataframe is > 8 000, then shrink to 8 000
    len_df = len(df)
    if len_df > max_values:
        df = df.iloc[::len_df//max_values]

    X = docs_to_vecs(df)
    Sim_matrix = Vecs_to_Sim_matrix(X)
    tsne = TSNE(n_components=2,n_jobs=-1,verbose=2,metric='cosine',angle=1,random_state=42)
    X_embedded = tsne.fit_transform(Sim_matrix)
    df_return = get_coords(df,X_embedded)
    return df_return

def with_PCA(df,max_values = 10_000,pca_n_comp = 100):

    # If dataframe is > 8 000, then shrink to 8 000
    len_df = len(df)
    if len_df > max_values:
        df = df.iloc[::(len_df//max_values)]

    X = docs_to_vecs(df)
    Sim_matrix = Vecs_to_Sim_matrix(X)
    
    new_input = PCA(n_components=pca_n_comp).fit_transform(Sim_matrix)
    tsne = TSNE(n_components=2,n_jobs=-1,verbose=2,metric='cosine',angle=1,random_state=42)
    X_embedded = tsne.fit_transform(new_input)
    df_return = get_coords(df,X_embedded)
    return df_return

