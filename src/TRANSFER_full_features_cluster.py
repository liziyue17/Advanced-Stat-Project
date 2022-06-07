# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 01:46:22 2022

@author: liziy

This file is created to transfer data to linear_regression-friendly version.
"""

import pandas as pd
from data_prep import *
from sklearn import preprocessing


data = pd.read_csv("../data/full_features_cluster.csv",  index_col=0) #Note: Run python XXX.py in this folder
data["Country"] = data["Primary Affiliation"].apply(lambda x: x.split(",")[-1].replace(" ", ""))
data = data.drop(["First Name", "Last Name", "ID", "Primary Affiliation", "Secondary Affiliations"], axis=1)
encoding_list = ["Category", "Country"]
enc = preprocessing.OrdinalEncoder().fit(data[encoding_list])
data[encoding_list] = enc.transform(data[encoding_list])
numeric_list = ["Documents", "Cited By", "Preprints", "Coauthor", "Topics", "Awarded Grants", "max_cite", "pub_div", "recent_3", "academic_age"]
print(data)
data.to_csv("../data/full_features_linearregFRIENDLY.csv", encoding="utf_8")
