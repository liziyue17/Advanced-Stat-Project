import numpy as np 
import pandas as pd 
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
from sklearn.preprocessing import scale
import matplotlib.pyplot as plt
from data_prep import prepare_input


class Clustering(object):
    '''
        Cluster the scholars in the data set
    '''
    def __init__(self, file_path="./data/full_features.csv", encoding="onehot", std=True):
        self.raw_data = pd.read_csv(file_path, index_col=0)
        self.data = prepare_input(file_path=file_path, encoding=encoding, std=std)
        self.x, self.y = self.data.drop(["h_index"], axis=1), self.data["h_index"]
        
    
    def kmeans_clustering(self, data, n, save_data=False):
        model = KMeans(n_clusters=n).fit(data)
        mean_dist = sum(np.min(cdist(data, model.cluster_centers_, "euclidean"), axis=1))/data.shape[0]
        self.labels = model.labels_
        self.result = self.raw_data
        self.result["labels"] = self.labels
        print(self.result)
        if save_data:
            self.result.to_csv("./data/full_features_cluster.csv")
            print("data saved.")
        
        return mean_dist

    def select_opt_k(self, data, max_range=10):
        mean_dist = []
        for k in range(1, max_range):
            temp = self.kmeans_clustering(data=data, n=k)
            mean_dist.append(temp)

        figure, ax = plt.subplots(1, 1)
        ax.plot(range(1, max_range), mean_dist, "o-")
        ax.set_xticks(range(1, max_range))
        ax.set_xlabel("k")
        ax.set_ylabel("SSE")
        plt.savefig("./results/elb.png", dpi=600)
        plt.show()

    def draw_scatter_plots(self):
        data = self.result.loc[:, ["Documents", "Cited By", "Topics", "Coauthor", "academic_age", "Category", "h_index", "labels"]]

        type0_cs, type0_econ = data.query('labels==0 & Category=="Computer Science"'), data.query('labels==0 & Category=="Economics and Business"')
        type1_cs, type1_econ = data.query('labels==1 & Category=="Computer Science"'), data.query('labels==1 & Category=="Economics and Business"')
        type2_cs, type2_econ = data.query('labels==2 & Category=="Computer Science"'), data.query('labels==2 & Category=="Economics and Business"')
        type3_cs, type3_econ = data.query('labels==3 & Category=="Computer Science"'), data.query('labels==3 & Category=="Economics and Business"')
        
        figure, ax = plt.subplots(2, 2, figsize=(10, 8))
        
        def add_scatter(i0, i1, col_name, xy_names):
            ax[i0, i1].scatter(type0_cs[col_name[0]], type0_cs[col_name[1]], c="red", label="type0_cs", marker="o", s=(type0_cs["h_index"]/13.0)**2)
            ax[i0, i1].scatter(type0_econ[col_name[0]], type0_econ[col_name[1]], c="red", label="type0_econ", marker="*", s=(type0_econ["h_index"]/13.0)**2)
            ax[i0, i1].scatter(type1_cs[col_name[0]], type1_cs[col_name[1]], c="blue", label="type1_cs", marker="o", s=(type1_cs["h_index"]/13.0)**2)
            ax[i0, i1].scatter(type1_econ[col_name[0]], type1_econ[col_name[1]], c="blue", label="type1_econ", marker="*", s=(type1_econ["h_index"]/13.0)**2)
            ax[i0, i1].scatter(type2_cs[col_name[0]], type2_cs[col_name[1]], c="green", label="type2_cs", marker="o", s=(type2_cs["h_index"]/13.0)**2)
            ax[i0, i1].scatter(type2_econ[col_name[0]], type2_econ[col_name[1]], c="green", label="type2_econ", marker="*", s=(type2_econ["h_index"]/13.0)**2)
            ax[i0, i1].scatter(type3_cs[col_name[0]], type3_cs[col_name[1]], c="orange", label="type3_cs", marker="o", s=(type3_cs["h_index"]/13.0)**2)
            ax[i0, i1].scatter(type3_econ[col_name[0]], type3_econ[col_name[1]], c="orange", label="type3_econ", marker="*", s=(type3_econ["h_index"]/13.0)**2)
            
            ax[i0, i1].set_xlabel(xy_names[0])
            ax[i0, i1].set_ylabel(xy_names[1])

        add_scatter(0, 0, col_name=["Documents", "Cited By"], xy_names=["# of Paper", "# of Citations"])
        add_scatter(0, 1, col_name=["Coauthor", "Cited By"], xy_names=["# of Coauthors", "# of Citations"])
        add_scatter(1, 0, col_name=["Topics", "Cited By"], xy_names=["# of Topics", "# of Citations"])
        add_scatter(1, 1, col_name=["academic_age", "Documents"], xy_names=["Academic Age", "# of Paper"])

        plt.legend(loc="upper left")
        plt.subplots_adjust(wspace=0.4, hspace=0.4)

        plt.savefig("./results/cluster_figure.png", dpi=800)
        plt.show()

        





if __name__ == "__main__":
    C = Clustering(encoding="onehot", std=True)
    data = C.x
    #C.select_opt_k(data, max_range=10)
    C.kmeans_clustering(data=data, n=4, save_data=True)
    C.draw_scatter_plots()