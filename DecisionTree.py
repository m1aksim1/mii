class DecisionTree:
    def __init__(self, data, target):
        self.data = data
        self.target = target
        self.tree = self.build_tree(data, target)

    def build_tree(self, data, target):
        # реализация алгоритма построения дерева решений
        # ...
        return

    def predict(self, new_data):
        # реализация алгоритма предсказания с помощью дерева решений
        # ...
        return