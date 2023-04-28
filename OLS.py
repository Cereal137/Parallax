import numpy as np
import SampleClass as sc
import AstroMetricTemplate as tp

def radians_to_mas(radians):
    return radians/np.pi*180*3600*1000

def OLS(SampleList:sc.NodeList):
    #initialize
    N = SampleList.get_length() #number of samples
    FeatureList = SampleList.get_node(0).get_FeatureList()
    p = FeatureList.get_length() #number of features

    y = np.zeros((N,1))
    X = np.zeros((N,p))
    B = np.zeros((N,N))
    for i in range(N):
        SampleNode = SampleList.get_node(i)
        ResponseList = SampleNode.get_ResponseList()
        FeatureList = SampleNode.get_FeatureList()
        y[i] = ResponseList.get_node(0).get_response()
        B[i][i] = 1/ResponseList.get_node(0).get_err()**2
        for j in range(p):
            X[i][j] = FeatureList.get_node(j).get_feature()
    
    beta_OLS = np.linalg.inv(X.T@B.T@X)@X.T@B.T@y
    return beta_OLS


    

def main():
    pass
    """DataList = tp.ReadData('hii_625.txt')
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
    print(radians_to_mas(OLS(SampleList)))
    params = OLS(SampleList).T
    sum = 0
    for i in range(SampleList.length):
        SNode = SampleList.get_node(i)
        FL = SNode.get_FeatureList()
        RL = SNode.get_ResponseList()
        sum += ((RL.get_node(0).get_response()-params[0][0]-params[0][1]*FL.get_node(1).get_feature()- params[0][2]*FL.get_node(2).get_feature() - params[0][3]*FL.get_node(3).get_feature() )/ RL.get_node(0).get_err() )**2
    print(sum)"""

if __name__ == '__main__':
    main()