#%%
import AstroMetricTemplate as tp
import numpy as np
import WLS as ls
#import matplotlib.pyplot as plt
import SampleClass as sc
from scipy.optimize import minimize

def radians_to_mas(radians):
    return radians/np.pi*180*3600*1000
def mas_to_radians(mas):
    return mas/1000/3600/180*np.pi

#initialize
DataList = tp.ReadData('hii_625.txt')
N = DataList.get_length()

alpha_epoch = DataList.get_node(0).get_longitude()
delta_epoch = DataList.get_node(0).get_latitude()
t_epoch = DataList.get_node(0).get_Year()

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
    t = Node_In.get_Year() #Julian Date

    #Earth Node
    Node_Earth = tp.CelestialCoordinate(np.pi+lambda_E,0.0,0.0,0.0,Node_In.get_JulianDate()).Ecliptic2Equator() #Earth Node in Equatorial Coordinate
    #Geometry in Cartesian Coordinate
    p = np.array([-np.sin(Node_In.get_longitude()), -np.cos(Node_In.get_longitude()), 0.0])
    q = np.array([-np.sin(Node_In.get_latitude())*np.cos(Node_In.get_longitude()), np.sin(Node_In.get_latitude())*np.sin(Node_In.get_longitude()), np.cos(Node_In.get_latitude())])
    r = Node_In.normal_vector()
    
    b = r_E* Node_Earth.normal_vector()
    #Consider Roemer Delay
    t_B = t + np.dot(r,b)/tp.c_AU_yr
    #Orbit Features
    OrbitFeature_1 = -np.dot(q,b)
    OrbitFeature_2 = -np.dot(p,b)

    #Features and Responses
    Features.add_node(sc.FeatureNode(1,'zero order'))
    Features.add_node(sc.FeatureNode(t_B-t_epoch,'time feature'))
    Features.add_node(sc.FeatureNode(OrbitFeature_1,'orbit feature for decl'))
    Features.add_node(sc.FeatureNode(OrbitFeature_2,'orbit feature for ra*'))

    ra_s = Node_In.get_longitude()*np.cos(Node_In.get_latitude()) - alpha_epoch*np.cos(Node_In.get_latitude())
    err_ra_s = np.sqrt( (Node_In.get_err_long() * np.cos(Node_In.get_latitude()))**2 + (Node_In.get_longitude()*np.sin(Node_In.get_latitude())*Node_In.get_err_lat())**2)
    Responses.add_node(sc.ResponseNode(Node_In.get_latitude()-delta_epoch ,Node_In.get_err_lat(),'latitude'))
    Responses.add_node(sc.ResponseNode(ra_s,err_ra_s,'ra_s')) #ra_*

    #link to SampleNode
    SampleNode.link_FeatureList(Features)
    SampleNode.link_ResponseList(Responses)
    #add to SampleList
    SampleList.add_node(SampleNode)

def main():
    print( ls.WLS(SampleList) )
    
if __name__ == '__main__':
    main()

# %%
