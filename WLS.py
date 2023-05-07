import numpy as np
import SampleClass as sc
import AstroMetricTemplate as tp

def radians_to_mas(radians):
    return radians/np.pi*180*3600*1000

def WLS(SampleList:sc.NodeList):
    #initialize
    N = SampleList.get_length() #number of samples
    FeatureList = SampleList.get_node(0).get_FeatureList()
    p = 5 #number of parameters
    DoF = 2*N-p

    X_decl = np.zeros((N,p))
    X_ra = np.zeros((N,p))
    y_decl = np.zeros((N,1))
    y_ra = np.zeros((N,1))
    B_decl = np.zeros((N,N))
    B_ra = np.zeros((N,N))

    chi_square = 0
    l = 0
    r = 1e-5
    while(l<r):
        m = (l+r)/2
        sigma_sys = m #radians

        for i in range(N):
            SampleNode = SampleList.get_node(i)
            ResponseList = SampleNode.get_ResponseList()
            FeatureList = SampleNode.get_FeatureList()
            y_decl[i] = ResponseList.get_node(0).get_response()
            y_ra[i] = ResponseList.get_node(1).get_response()
            B_decl[i][i] = 1 / ( (ResponseList.get_node(0).get_err())**2+ sigma_sys**2 )
            B_ra[i][i] = 1 / ( (ResponseList.get_node(1).get_err())**2+ sigma_sys**2 )

            X_decl[i][0] = FeatureList.get_node(0).get_feature()
            X_decl[i][1] = 0
            X_decl[i][2] = FeatureList.get_node(1).get_feature()
            X_decl[i][3] = 0
            X_decl[i][4] = FeatureList.get_node(2).get_feature()

            X_ra[i][0] = 0
            X_ra[i][1] = FeatureList.get_node(0).get_feature()
            X_ra[i][2] = 0
            X_ra[i][3] = FeatureList.get_node(1).get_feature()
            X_ra[i][4] = FeatureList.get_node(3).get_feature()

        beta_WLS = np.linalg.inv( X_decl.T@B_decl@X_decl +X_ra.T@B_ra@X_ra )@(X_decl.T@B_decl@y_decl+X_ra.T@B_ra@y_ra)
        
        chi_square = ((y_decl-X_decl@beta_WLS).T@B_decl@(y_decl-X_decl@beta_WLS) + (y_ra-X_ra@beta_WLS).T@B_ra@(y_ra-X_ra@beta_WLS))/DoF
        if (chi_square > 1.003):   
            l = m
        else:
            if (chi_square < 1.002):  
                r = m
            else:
                break
        var_beta_WLS = np.linalg.inv( X_decl.T@B_decl@X_decl +X_ra.T@B_ra@X_ra )
    return radians_to_mas(beta_WLS), radians_to_mas(np.sqrt(var_beta_WLS)), chi_square , sigma_sys

def main():
    pass
   
if __name__ == '__main__':
    main()
