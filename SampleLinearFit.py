#%%
import Template as tp
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import SampleClass as sc


def radians_to_mas(radians):
    return radians/np.pi*180*3600*1000
def mas_to_radians(mas):
    return mas/1000/3600/180*np.pi

DataList = tp.ReadData()
SampleList = sc.SampleSet(DataList)

def loss(params):
    sum = 0
    for i in range(SampleList.length):
        SNode = SampleList.get_node(i)
        #sum += ((SNode.get_result()-params[0]-params[1]*SNode.get_feature_i(1)- params[2]*SNode.get_feature_i(2) - params[3]*SNode.get_feature_i(3) -params[4]*SNode.get_feature_i(4))/ SNode.get_err())**2
        sum += ((SNode.get_lat()-params[0]-params[1]*SNode.get_feature_i(1)- params[2]*SNode.get_feature_i(2) - params[3]*SNode.get_feature_i(3) )/ SNode.get_err_latitude())**2
        sum += ((SNode.get_ra()-params[4]-params[5]*SNode.get_feature_i(1)- params[6]*SNode.get_feature_i(2) - params[7]*SNode.get_feature_i(3) )/ SNode.get_err_ra())**2
    return sum

def plot(params):
    ##plot the result
    for i in range(SampleList.get_length()):
        SNode = SampleList.get_node(i)
        #result = SNode.get_result()- params[3]*SNode.get_feature_i(3) -params[4]*SNode.get_feature_i(4) - params[0]
        result = SNode.get_lat()- params[3]*SNode.get_feature_i(3) - params[0]
        plt.errorbar(2000.219 +SNode.get_feature_i(0)/(2*np.pi), radians_to_mas(result), yerr=radians_to_mas(SNode.get_err_latitude()), fmt='o')
    JulianDate_show = np.linspace(2456000,2456460,200)
    Node_show = tp.CelestialCoordinate(0, 0, 0 ,0,JulianDate_show)
    r_show = Node_show.GetEarthDistance()
    lambda_E_show = Node_show.GetEarthLambda()
    x_show = 2000.219 + lambda_E_show/(2*np.pi)
    y_show = params[1]*np.cos(lambda_E_show) + params[2]*r_show*np.sin(lambda_E_show)*np.cos(tp.epsilon)
    plt.plot(x_show, radians_to_mas(y_show))
    plt.xlim(2011.7,2014)
    plt.ylim(-10,10)
    plt.show()

    for i in range(SampleList.get_length()):
        SNode = SampleList.get_node(i)
        #result = SNode.get_result()- params[3]*SNode.get_feature_i(3) -params[4]*SNode.get_feature_i(4) - params[0]
        result = SNode.get_ra()- params[7]*SNode.get_feature_i(3) - params[4]
        plt.errorbar(2000.219+SNode.get_feature_i(0)/(2*np.pi), radians_to_mas(result), yerr=radians_to_mas(SNode.get_err_ra()), fmt='o')
    JulianDate_show = np.linspace(2456000,2456460,200)
    Node_show = tp.CelestialCoordinate(0, 0, 0 ,0, JulianDate_show)
    r_show = Node_show.GetEarthDistance()
    lambda_E_show = Node_show.GetEarthLambda()
    x_show = 2000.219 + lambda_E_show/(2*np.pi)
    y_show = params[5]*np.cos(lambda_E_show) + params[6]*r_show*np.sin(lambda_E_show)*np.cos(tp.epsilon)
    plt.plot(x_show, radians_to_mas(y_show))
    plt.xlim(2011.7,2014)
    plt.ylim(-10,10)
    plt.show()

def main():
    #initial guess
    params = np.array([ 8.54188744e+07 ,-1.85190047e+00  ,5.01776374e-01 ,-4.42293242e+01, 1.85673575e+08 ,-5.35628563e+00  ,3.28595949e+00  ,3.70327367e+01])
    #Powell method
    results = minimize(loss, params, method='Powell', tol=1e-10)
    params = results.x #get the result
    print(radians_to_mas(params)) #print the result in mas
    print(loss(params)) #print the loss
    plot(params) #plot the result

    """for i in range(SampleList.get_length()):
        SNode = SampleList.get_node(i)
        #result = SNode.get_result()- params[3]*SNode.get_feature_i(3) -params[4]*SNode.get_feature_i(4) - params[0]
        result = SNode.get_ra()- 0*params[7]*SNode.get_feature_i(3) - params[4]
        #plt.scatter(2000.219+SNode.get_feature_i(0)/(2*np.pi), radians_to_mas(SNode.get_ra()))
        plt.errorbar(2000.219+SNode.get_feature_i(0)/(2*np.pi), radians_to_mas(result), yerr=radians_to_mas(SNode.get_err_ra()), fmt='o')
    JulianDate_show = np.linspace(2456000,2456460,200)
    Node_show = tp.CelestialCoordinate(0, 0, 0 ,0, JulianDate_show)
    r_show = Node_show.GetEarthDistance()
    lambda_E_show = Node_show.GetEarthLambda()
    x_show = 2000.219 + lambda_E_show/(2*np.pi)
    y_show = params[7]* lambda_E_show/(2*np.pi)
    plt.plot(x_show, radians_to_mas(y_show))
    plt.show()"""
    

if __name__ == '__main__':
    main()

# %%
