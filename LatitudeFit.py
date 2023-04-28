#%%
import AstroMetricTemplate as tp
import numpy as np
import OLS as ls
#import matplotlib.pyplot as plt
import SampleClass as sc

def radians_to_mas(radians):
    return radians/np.pi*180*3600*1000
def mas_to_radians(mas):
    return mas/1000/3600/180*np.pi

#initialize
DataList = tp.ReadData('hii_625.txt')
N = DataList.get_length()
SampleList = sc.NodeList()
for i in range(N):
    #initialize
    SampleNode = sc.SampleNode()
    Features = sc.NodeList()
    Responses = sc.NodeList()
    #get data
    Node_In:tp.CelestialCoordinate = DataList.get_node(i)
    r_E = Node_In.GetEarthDistance()
    lambda_E = Node_In.GetEarthLambda()
    t = lambda_E/(2*np.pi) #time feature in years

    #Features and Responses
    Features.add_node(sc.FeatureNode(1,'zero order'))
    Features.add_node(sc.FeatureNode(r_E*np.cos(lambda_E),'cosine term'))
    Features.add_node(sc.FeatureNode(r_E*np.sin(lambda_E)*np.cos(tp.epsilon),'sin term'))
    Features.add_node(sc.FeatureNode(t,'time feature'))

    #choose which response to fit
    Responses.add_node(sc.ResponseNode(Node_In.get_latitude(),Node_In.get_err_lat(),'latitude'))
    #Responses.add_node(sc.ResponseNode(Node_In.get_ra(),Node_In.get_err_ra(),'ra'))

    #link to SampleNode
    SampleNode.link_FeatureList(Features)
    SampleNode.link_ResponseList(Responses)
    #add to SampleList
    SampleList.add_node(SampleNode)

def main():
    params = ls.OLS(SampleList)
    print( radians_to_mas(params) )
    
if __name__ == '__main__':
    main()

# %%
