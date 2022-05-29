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
        self.data = prepare_input(file_path=file_path, encoding=encoding, std=std)
        self.x, self.y = self.data.drop(["h_index"], axis=1), self.data["h_index"]
        
        

    def kmeans_clustering(self, data, n, save_data=False):
        model = KMeans(n_clusters=n).fit(data)
        mean_dist = sum(np.min(cdist(data, model.cluster_centers_, "euclidean"), axis=1))/data.shape[0]
        self.labels = model.labels_
        self.result = self.data
        self.result["labels"] = self.labels
        print(self.result)
        if save_data:
            self.result.to_csv("./results/cluster_orders.csv")
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
        #plt.savefig("./results/figures/elb.png", dpi=800)
        plt.show()

    def try_plots(self):
        data = self.result.loc[:, ["Documents", "Coauthor", "labels"]]
        type0 = data[data["labels"]==0]
        type1 = data[data["labels"]==1]
        type2 = data[data["labels"]==2]
        type3 = data[data["labels"]==3]

        figure, ax = plt.subplots(1, 1)
        ax.scatter(type0.iloc[:,0], type0.iloc[:, 1], c="red", label="type0")
        ax.scatter(type1.iloc[:,0], type1.iloc[:, 1], c="blue", label="type1")
        ax.scatter(type2.iloc[:,0], type2.iloc[:, 1], c="green", label="type2")
        ax.scatter(type3.iloc[:,0], type3.iloc[:, 1], c="orange", label="type3")

        ax.legend()
        plt.show()


    def draw_scatter_plots(self):
        data = self.result.iloc[:, [1,2,3,4,5,6]]
        type0 = data[data["labels"]==0]
        type1 = data[data["labels"]==1]
        type2 = data[data["labels"]==2]
        type3 = data[data["labels"]==3]
        
        figure, ax = plt.subplots(2, 2)
        ax[0,0].scatter(type0.iloc[:,0], type0.iloc[:, 4], s=(type0.iloc[:, 1]/20.0)**2, c="red", label="type0")
        ax[0,0].scatter(type1.iloc[:,0], type1.iloc[:, 4], s=(type1.iloc[:, 1]/20.0)**2, c="blue", label="type1")
        ax[0,0].scatter(type2.iloc[:,0], type2.iloc[:, 4], s=(type2.iloc[:, 1]/20.0)**2, c="green", label="type2")
        ax[0,0].scatter(type3.iloc[:,0], type3.iloc[:, 4], s=(type3.iloc[:, 1]/20.0)**2, c="orange", label="type3")
        ax[0,0].set_xlabel("Academic age")
        ax[0,0].set_ylabel("Number of citation")

        ax[0,1].scatter(type0.iloc[:,0], type0.iloc[:, 3], s=(type0.iloc[:, 1]/20.0)**2, c="red", label="type0")
        ax[0,1].scatter(type1.iloc[:,0], type1.iloc[:, 3], s=(type1.iloc[:, 1]/20.0)**2, c="blue", label="type1")
        ax[0,1].scatter(type2.iloc[:,0], type2.iloc[:, 3], s=(type2.iloc[:, 1]/20.0)**2, c="green", label="type2")
        ax[0,1].scatter(type3.iloc[:,0], type3.iloc[:, 3], s=(type3.iloc[:, 1]/20.0)**2, c="orange", label="type3")
        ax[0,1].set_xlabel("Academic age")
        ax[0,1].set_ylabel("Number of paper")

        ax[1,0].scatter(type0.iloc[:,0], type0.iloc[:, 1], s=(type0.iloc[:, 1]/20.0)**2, c="red", label="type0")
        ax[1,0].scatter(type1.iloc[:,0], type1.iloc[:, 1], s=(type1.iloc[:, 1]/20.0)**2, c="blue", label="type1")
        ax[1,0].scatter(type2.iloc[:,0], type2.iloc[:, 1], s=(type2.iloc[:, 1]/20.0)**2, c="green", label="type2")
        ax[1,0].scatter(type3.iloc[:,0], type3.iloc[:, 1], s=(type3.iloc[:, 1]/20.0)**2, c="orange", label="type3")
        ax[1,0].set_ylabel("H-index")
        ax[1,0].set_xlabel("Academic age")

        ax[1,1].scatter(type0.iloc[:,4], type0.iloc[:, 3], s=(type0.iloc[:, 1]/20.0)**2, c="red", label="type0")
        ax[1,1].scatter(type1.iloc[:,4], type1.iloc[:, 3], s=(type1.iloc[:, 1]/20.0)**2, c="blue", label="type1")
        ax[1,1].scatter(type2.iloc[:,4], type2.iloc[:, 3], s=(type2.iloc[:, 1]/20.0)**2, c="green", label="type2")
        ax[1,1].scatter(type3.iloc[:,4], type3.iloc[:, 3], s=(type3.iloc[:, 1]/20.0)**2, c="orange", label="type3")
        ax[1,1].set_ylabel("Number of paper")
        ax[1,1].set_xlabel("Number of citation")

        plt.subplots_adjust(wspace=0.45, hspace=0.45)

        ax[0,0].legend()
        ax[0,1].legend()
        ax[1,0].legend()
        ax[1,1].legend()
        #plt.savefig("./results/figures/cluster_figure.png", dpi=800)
        plt.show()
        





if __name__ == "__main__":
    C = Clustering(encoding="onehot", std=True)
    data = C.x
    #C.select_opt_k(data, max_range=10)
    C.kmeans_clustering(data=data, n=4, save_data=False)
    C.try_plots()
    #C.draw_scatter_plots()