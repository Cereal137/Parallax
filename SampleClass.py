import numpy as np
import Template as tp
class FeatureNode():
    def __init__(self,feature):
        self.feature = feature
    def get_feature(self)->float:
        return self.feature
    
class SampleNode():
    def __init__(self, Node: tp.CelestialCoordinate):
        r = Node.GetEarthDistance()
        lambda_E = Node.GetEarthLambda()
        
        FeatureList = tp.NodeList()
        FeatureList.add_node(FeatureNode(lambda_E))
        FeatureList.add_node(FeatureNode(r*np.cos(lambda_E)))
        FeatureList.add_node(FeatureNode(r*np.sin(lambda_E)*np.cos(tp.epsilon)))
        t_now = lambda_E/(2*np.pi) #time feature in yrs
        FeatureList.add_node(FeatureNode(t_now)) #velocity feature
        #FeatureList.add_node(FeatureNode(t_now**2)) #acceleration feature
        self.features = FeatureList
        self.lat = Node.get_latitude()
        self.ra = Node.get_longitude()* np.cos(Node.get_latitude())
        self.err_latitude = Node.get_err_lat()
        self.err_ra = np.sqrt((Node.get_err_long() * np.cos(Node.get_latitude()))**2 + (np.sin(Node.get_err_lat()) * Node.get_longitude() * Node.get_err_lat())**2)

    def get_feature_i(self, index)->float:
        return self.features.get_node(index).get_feature()
    def get_lat(self)->float:
        return self.lat
    def get_ra(self)->float:
        return self.ra
    def get_err_latitude(self)->float:
        return self.err_latitude
    def get_err_ra(self)->float:
        return self.err_ra

class SampleSet():
    def __init__(self, DataList: tp.NodeList):
        self.length = DataList.get_length()
        self.node_list = []
        for i in range(self.length):
            NewNode = SampleNode(DataList.get_node(i))
            self.node_list.append(NewNode)
    def get_length(self)->int:
        return self.length
    def get_node(self, index)->SampleNode:
        return self.node_list[index]
    def get_node_list(self)->tp.NodeList:
        return self.node_list

def main():
    pass

if __name__ == "__main__":
    main()