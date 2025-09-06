import pandas as pd
from unidecode import unidecode

class TitleDictionary:

    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)
        self.df['primaryTitle'] = self.df['primaryTitle'].apply(unidecode)
        self.title_dict = self._create_title_dict()
        self.profession_dict = self._create_profession_dict()

    def _create_title_dict(self):
        title_dict = dict()
        for _, row in self.df.iterrows():
            nconst, primaryTitle = row['nconst'], row['primaryTitle']
            if nconst in title_dict:
                title_dict[nconst].append(primaryTitle)
            else:
                title_dict[nconst] = [primaryTitle]
        return title_dict

    def _create_profession_dict(self):
        profession_dict = dict()
        for _, row in self.df.iterrows():
            nconst, name = row['nconst'], row['primaryName'] + "_" + row['primaryProfession'][:1]
            if nconst in profession_dict:
                profession_dict[nconst].append(name)
            else:
                profession_dict[nconst] = [name]
        return profession_dict


#Graph Network Creation
class MovieNetwork:
    def __init__(self, name_movie_dict, nconst_ar_dr):
        self.graph = dict()
        self.name_movie_dict = name_movie_dict
        self.nconst_ar_dr = nconst_ar_dr


    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = dict()

    def add_edge(self, node1, node2, nconst_ar_dr, weight=1):
        weight = len(set(self.name_movie_dict[node1]) & set(self.name_movie_dict[node2]))
        if weight <= 2:
            return
        self.add_node(node1)
        self.add_node(node2)
        if nconst_ar_dr[node1][0][-1] == "a" and nconst_ar_dr[node2][0][-1] == "d":
            node1, node2 = node2, node1
        self.graph[node1][node2] = weight
        if nconst_ar_dr[node1][0][-1] == nconst_ar_dr[node2][0][-1]:
            self.graph[node2][node1] = weight

    def create_graph(self):
        for x in self.nconst_ar_dr:
            for y in self.nconst_ar_dr:
                if x == y:
                    continue
                self.add_edge(x, y, self.nconst_ar_dr)
        return self.graph
