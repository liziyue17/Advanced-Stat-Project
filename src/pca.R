data_raw = read.csv("../data/full_features_linearregFRIENDLY.csv", header = TRUE)
data_raw$X = NULL
data = data.frame(Documents = data_raw$Documents, Cited.By = data_raw$Cited.By, Preprints = data_raw$Preprints, 
                  Coauthor = data_raw$Coauthor, Topics = data_raw$Topics, Awarded.Grants = data_raw$Awarded.Grants, 
                  Category = data_raw$Category, max_cite = data_raw$max_cite, pub_div = data_raw$pub_div,
                  recent_3 = data_raw$recent_3, academic_age = data_raw$academic_age, Cited = data_raw$Cited)
matrix=cor(data)
pc<-eigen(matrix)
pc

