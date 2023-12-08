import math

import pandas as pd
import numpy as np
import treelib



class DecisionTree:
    def __init__(self, data, target):
        self.data = data
        self.target = target
        self.tree = self.build_tree(data, target)
    def build_tree(self, data, target):
        entropy = pd.Series(index=data.columns)
        #сначала находи энтропию
        for col in data.columns:
            group = data.groupby(col).count()
            group = group/group.sum()
            group = group.applymap(lambda x: x*np.log2(x))
            entropy[col] = -1 * group.sum().tolist()[0]

        entropy = entropy.sort_values(ascending=True)
        tree = treelib.Tree()

        tree.create_node(entropy.index[0], entropy.index[0])
        data['price'] = target
        grouped_df = data.groupby(['cut', 'clarity'])['price'].mean()


        for i in data[entropy.index[0]].unique():
            id = entropy.index[0] + str(i)
            tree.create_node(i, id, parent=entropy.index[0])
            iid = entropy.index[1]+str(i)
            tree.create_node(entropy.index[1], iid, parent=id)

            for j in data[entropy.index[1]].unique():
                idj = entropy.index[1] + str(j)+str(i)
                tree.create_node(j, idj, parent=iid)
                value = grouped_df.loc[(i, j)]
                tree.create_node(value, str(i)+str(j), parent=idj)
        print(tree)
        self.btree = tree

        return

    def predict(self, new_data):
        predict = list()
        for i,row in new_data.iterrows():
            _id = str(row['cut'])+str(row['clarity'])
            predict.append(self.btree.get_node(_id).tag)
        return predict