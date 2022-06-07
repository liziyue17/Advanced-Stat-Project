import pandas as pd 
from sklearn import tree
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt



class TreeModels(object):
    def __init__(self, with_cluster=False):
        if with_cluster:
            self.Data = pd.read_csv("./data/full_features_cluster_onehot.csv", index_col=0)
        else:
            self.Data = pd.read_csv("./data/full_features_onehot.csv", index_col=0)

        self.Data = self.Data.drop(["Category_Computer Science", "Country_Australia"], axis=1)
        print(self.Data)
        self.X, self.y = self.Data.drop(["h_index"], axis=1), self.Data["h_index"]
        
        self.split_train_test()
        print("data prepared")

    def split_train_test(self):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.3, random_state=41)

    def score_fn(self, y_pred, y_true): 
        #return accuracy_score(y_pred, y_true)
        return mean_squared_error(y_pred, y_true)

    def plot_importance(self, imp_list, name_list, topn=10, title="Decision Tree"):
        imp_dict = dict(zip(name_list, imp_list))
        imp_df = pd.DataFrame(imp_dict, index=["importance"]).T
        imp_df = imp_df.sort_values("importance", ascending=False)
        #print(imp_df)
        figure, ax = plt.subplots(1, 1, figsize=(10, 5))
        ax.barh(imp_df.head(topn).index, imp_df.head(topn)["importance"])
        ax.set_xlabel("Importance")
        ax.set_title(title)

        #plt.savefig("./results/feature_importance_" + title + ".png", dpi=600)
        #plt.show()

    def run_DT(self):
        '''
        # CV + GridSearch
        model = tree.DecisionTreeRegressor(random_state=42)
        params = {
            "min_samples_leaf": [0.01, 0.03, 0.05],
            "max_features": ["auto", "sqrt", "log2"],
            "max_depth": [5, 8, 10, 15]
        }

        opt_model = GridSearchCV(model, param_grid=params, cv=5, scoring="neg_mean_squared_error")
        
        opt_model.fit(self.X_train, self.y_train)
        print("best score: " + str(opt_model.best_score_))
        print("best params: " + str(opt_model.best_params_))
        '''
        model = tree.DecisionTreeRegressor(max_depth=8, max_features="auto", min_samples_leaf=0.03, random_state=42)
        model.fit(self.X_train, self.y_train)
        y_pred = model.predict(self.X_test)
        print("Decision Tree: ")
        print("train MSE: ", self.score_fn(model.predict(self.X_train), self.y_train))
        print("test MSE: ", self.score_fn(y_pred, self.y_test))

        self.plot_importance(model.feature_importances_, model.feature_names_in_, 
                                topn=10, title="Decision Tree")
        

    def run_RF(self):
        '''
        # CV + GridSearch
        model = RandomForestRegressor(random_state=42)
        params = {
            "n_estimators": [50, 100, 200],
            "max_features": [0.5, 0.75, 1],
            "max_depth": [3, 5, 8, 10]
        }

        opt_model = GridSearchCV(model, param_grid=params, cv=5, scoring="neg_mean_squared_error")
        
        opt_model.fit(self.X_train, self.y_train)
        print("best score: " + str(opt_model.best_score_))
        print("best params: " + str(opt_model.best_params_))
        
        '''

        model = RandomForestRegressor(n_estimators=200, max_depth=10, max_features=0.75, random_state=42)
        model.fit(self.X_train, self.y_train)
        y_pred = model.predict(self.X_test)
        print("Random Forest")
        print("train MSE: ", self.score_fn(model.predict(self.X_train), self.y_train))
        print("test MSE: ", self.score_fn(y_pred, self.y_test))

        self.plot_importance(model.feature_importances_, model.feature_names_in_, 
                                topn=10, title="Random Forest")
        

    def run_GBDT(self):
        '''
        # CV + GridSearch
        model = GradientBoostingRegressor(random_state=42)
        params = {
            "n_estimators": [50, 100, 200],
            "learning_rate": [0.6, 0.8, 1.0],
            "max_depth": [1, 3, 5, 7]
        }

        opt_model = GridSearchCV(model, param_grid=params, cv=5, scoring="neg_mean_squared_error")
        
        opt_model.fit(self.X_train, self.y_train)
        print("best score: " + str(opt_model.best_score_))
        print("best params: " + str(opt_model.best_params_))
        '''
        
        model = GradientBoostingRegressor(n_estimators=50, learning_rate=0.6, max_depth=3, random_state=42)
        model.fit(self.X_train, self.y_train)
        y_pred = model.predict(self.X_test)
        print("Gradient Boosting:")
        print("train MSE: ", self.score_fn(model.predict(self.X_train), self.y_train))
        print("test MSE: ", self.score_fn(y_pred, self.y_test))

        self.plot_importance(model.feature_importances_, model.feature_names_in_, 
                                topn=10, title="Gradient Boosting")
        
        


if __name__ == "__main__":
    Models = TreeModels(with_cluster=True)
    
    Models.run_DT()
    Models.run_RF()
    
    Models.run_GBDT()


