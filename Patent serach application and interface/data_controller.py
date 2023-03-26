import pandas as pd
from datetime import datetime as dt

class dataset:
    def __init__(self,df_name = 'Data/subset_different.csv'):
        self.df = pd.read_csv(df_name)
        self.df_column_names = self.df.columns
        self.df_labels = pd.Series('other',index = self.df.index)
        self.dfs = {df_name:self.df.copy(deep=False)}
        self.df_subset = self.df.copy(deep=False)
        self.df_len = len(self.df)
        self.df_subset_len = len(self.df_subset)
        self.name = 'Data/subset_different.csv'

        self.search_terms = []
        self.label_terms = []
        self.start_date = dt(2018, 1, 1)
        self.end_date = dt(2019, 12, 31)

        # Fyrir tsne gögn til að þurfa ekki að reikna upp á nýtt fyrir breytt labels
        self.plotable_df = None
        self.subset_hash = hash((hash(tuple(self.search_terms)),
                                 hash(tuple(self.label_terms)),
                                 hash(self.start_date),
                                 hash(self.end_date)))
        self.plotted = False

        self.selected_df = None

    def get_selected_df(self):
        return self.selected_df

    def json_to_df(self,json):
        tmp_df = pd.DataFrame([point for point in json['points']])
        return tmp_df

    # Velja allt sem var valið á grafi úr df_subset 
    def set_selected_df(self,json):
        if json is not None:
            tmp_df_selected = self.json_to_df(json)


            # --------------------Possible failure point-------------------- #
            # self.selected_df = self.df_subset.iloc[tmp_df_selected.pointNumber]

            # --------------------Attempt at fix-------------------- #
            tmp_index = self.df_subset.index #store
            self.df_subset.index = self.df_subset.id # Change

            self.selected_df = self.df_subset.loc[tmp_df_selected.customdata] # Use
            self.df_subset.index = tmp_index # Restore


    def get_col_names(self):
        return self.df_column_names 
    # start & end dates
    def get_start_date(self):
        return self.start_date

    def get_end_date(self):
        return self.end_date

    def set_start_date(self,date):
        self.start_date = date

    def set_end_date(self,date):
        self.end_date = date

    # Create a subset with given search terms
    # def mak

    # Name
    def get_name(self):
        return self.name

    def set_name(self,name):
        self.name = name

    # Search terms
    def get_search_terms(self):
        return self.search_terms

    def add_search_term(self,term):
        if term != None:
            if term not in self.search_terms:
                self.search_terms.append(term) 

    def clear_search_terms(self):
        self.search_terms = []

    # Search terms
    def get_label_terms(self):
        return self.label_terms

    def add_label_terms(self,term):
        if term != None:
            if term not in self.label_terms:
                self.label_terms.append(term) 

    def clear_label_terms(self):
        self.label_terms = []

    # df lengths
    def get_df_len(self):
        return self.df_len
    
    def get_df_subset_len(self):
        return self.df_subset_len
    
    # sets
    def get_subset(self):
        return self.df_subset

    def set_subset(self,subset):
        self.df_subset = subset
        self.df_subset_len = len(subset)
        self.update = True

    # Set file by inputtin name of dataset
    def set_df_filename(self,name):
        if name in self.dfs:
            self.df = self.dfs[name].copy(deep=False)
            self.df_columns_names = self.df.columns
        else:
            self.df = pd.read_csv(name)
            self.df_columns_names = self.df.columns
            self.dfs[name] = self.df.copy(deep=False)
        self.df_len = len(self.df)
        self.name = name

    def make_subset_date(self):
        tmp_df = self.df.copy(deep=False)

        # Þarf e-ð að laga (Gæti verið issue með datatype á df.date)
        # if 'date' in tmp_df.columns:
        #     tmp_df = tmp_df.iloc[[tmp_df.date >= self.start_date]]
        #     tmp_df = tmp_df.iloc[[tmp_df.date <= self.end_date]]
        self.set_subset(tmp_df)


    def make_subset_words(self):
        if self.search_terms == []:
            self.set_subset(self.df)
        else:
            tmp_df = self.df.copy(deep=False)
            tmp_dfs = []
            for term in self.search_terms:
                tmp_subset = tmp_df[[term in x for x in tmp_df.abstract]]
                tmp_dfs.append(tmp_subset)
            
            
            self.set_subset(pd.concat(tmp_dfs))

    def make_subset(self):
        self.make_subset_date()
        self.make_subset_words()
    
    def label_subset(self):
        self.df_labels = pd.Series('other',index=self.df_subset.index)

        for term in self.label_terms:
            self.df_labels[[term in x for x in self.df_subset.abstract]] = term
    
    def get_labels(self):
        return self.df_labels

    def set_plotable(self, plotable):
        self.plotable_df = plotable
        self.plotted = True

    def get_plotable(self):
        return self.plotable_df

    def is_plotted(self):
        return self.plotted

    # def is_changed(self):
    #     curr_hash = hash((  hash(tuple(self.search_terms)),
    #                         hash(tuple(self.label_terms)),
    #                         hash(self.start_date),
    #                         hash(self.end_date)))
    #     if curr_hash == self.subset_hash:
    #         return False
    #     else:
    #         return True


