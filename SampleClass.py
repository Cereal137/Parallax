class NodeList():
    def __init__(self):
        self.length = 0
        self.node_list = []

    def add_node(self, node):
        self.node_list.append(node)
        self.length += 1

    def delate_node(self, index):
        self.node_list.pop(index)
        self.length -= 1

    def get_node(self, index):
        return self.node_list[index]
    
    def get_length(self)->int:
        return self.length

class FeatureNode():
    def __init__(self,feature,attributeName:str):
        self.feature = feature
        self.attribute = attributeName
    def get_feature(self)->float:
        return self.feature
    def get_attribute(self)->str:
        return self.attribute
    
class ResponseNode():
    def __init__(self,response,err,attributeName:str):
        self.response = response
        self.err = err
        self.attribute = attributeName
    def get_response(self)->float:
        return self.response
    def get_attribute(self)->str:
        return self.attribute
    def get_err(self)->float:
        return self.err
    
class SampleNode():
    def __init__(self):
        self.FeatureList = NodeList()
        self.ResponseList = NodeList()
    def get_FeatureList(self)->NodeList:
        return self.FeatureList
    def get_ResponseList(self)->NodeList:
        return self.ResponseList
    def link_FeatureList(self,featurelist:NodeList):
        self.FeatureList = featurelist
    def link_ResponseList(self,responselist:NodeList):
        self.ResponseList = responselist

def main():
    pass

if __name__ == "__main__":
    main()