import pandas as pd 
import numpy as np 
import os 


class SingleScholar(object):
    def __init__(self, file_path="./data/raw/Paper_Econ_Detail/6508196211.csv"):
        self.raw_data = pd.read_csv(file_path)
        self.raw_data.index = range(len(self.raw_data))

        self.data = self.raw_data.loc[:, ["标题", "年份", "来源出版物名称", "施引文献", "文献类型"]]
        self.data.columns = ["title", "year", "pub_name", "cite_num", "type"]
        self.data["cite_num"] = self.data["cite_num"].fillna(0)
        #print(self.data)

    def get_h_index(self):
        cite_num_list = self.data["cite_num"].values.tolist()
        cite_num_list.sort(reverse=True)

        h_index = len(cite_num_list)
        for i in range(len(cite_num_list)):
            if i + 1 > cite_num_list[i]:
                h_index = i
                break
        
        return h_index

    def get_features(self):
        max_cite = max(self.data["cite_num"].values.tolist())
        pub_diversity = len(self.data["pub_name"].drop_duplicates())
        recent_3_num = len(self.data[self.data["year"] >= 2020])

        return max_cite, pub_diversity, recent_3_num


def get_extra_features(file_path="./data/raw/Paper_Econ_Detail/"):
    file_list = os.listdir(file_path)

    feature_list = []
    for file_name in file_list:
        scholar = SingleScholar(file_path=os.path.join(file_path, file_name))
        max_cite, pub_div, recent_3 = scholar.get_features()
        h_index = scholar.get_h_index()
        feature_list.append([file_name[:-4], max_cite, pub_div, recent_3, h_index])
    
    feature_df = pd.DataFrame(feature_list, columns=["ID", "max_cite", "pub_div", "recent_3", "h_index"])
    feature_df["ID"] = feature_df["ID"].astype(np.int64)
    print(feature_df)

    return feature_df

def merge_full_data():
    econ_df = pd.read_csv("./data/raw/author_econ.csv")
    econ_df.index = range(len(econ_df))
    econ_df = pd.merge(econ_df, get_extra_features(file_path="./data/raw/Paper_Econ_Detail/"), how="left", on="ID")

    cs_df = pd.read_csv("./data/raw/author_cs.csv")
    cs_df.index = range(len(cs_df))
    cs_df = pd.merge(cs_df, get_extra_features(file_path="./data/raw/Paper_CS_Detail/"), how="left", on="ID")

    full_df = pd.concat([econ_df, cs_df])
    full_df.index = range(len(full_df))
    print(full_df)

    full_df.to_csv("./data/full_features.csv", encoding="utf_8_sig")
    print("csv saved. ")



if __name__ == "__main__":
    #s = SingleScholar(file_path="./data/raw/Paper_Econ_Detail/6508196211.csv")
    #s.get_h_index()
    #s.get_features()
    #get_extra_features()
    merge_full_data()
