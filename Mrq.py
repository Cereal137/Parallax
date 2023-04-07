import numpy as np
import time
import Template as tp
import SampleLinearFit as slf


##function
def f(X_sample,params):
    params = params.reshape(1,-1)
    return params[0][2] + params[0][0]*X_sample[0] + params[0][1]*X_sample[1]

##matrix operator
def dot(A,B):
    #A=A.reshape(1,-1)
    rA = A.shape[0]
    cA = B.shape[0]
    cB = B.shape[1]
    sum = np.zeros((rA,cB))
    for j in range(cA):
        for i in range(rA):
            for k in range(cB):
                sum[i][k] += A[i][j] * B[j][k]
    return sum
##solve linear equation for theta+
def solve(A,B):
    A_inv = np.linalg.inv(A)
    x = np.matmul(A_inv,B)
    return x
##gradient
def grad(theta,X):
    theta = theta.reshape(1,-1)
    grad_f = np.zeros((N,theta.shape[1]))
    for i in range(N):
        grad_f[i][0] = X[i][0]
        grad_f[i][1] = X[i][1]
        grad_f[i][2] = 1
    return grad_f
##Hessian
def hess(theta,X,error):
    theta = theta.reshape(1,-1)
    G = grad(theta,X)
    H = np.zeros((theta.shape[1],theta.shape[1]))
    for i in range(N):
        for j in range(theta.shape[1]):
            for k in range(theta.shape[1]):
                H[j][k] = G[i][j]*G[i][k] / np.square(error[i])
    return H
##first order derivative of chi_square
def chi_derivative(theta,X,y,error):
    diff = np.zeros((1,N))
    for i in range(N):
        diff[0][i] = (f(X[i],theta) - y[i]) / np.square(error[i])
    theta = theta.reshape(1,-1)
    grad_f = grad(theta,X)
    return np.matmul( diff , grad_f )
##chi_square
def chi_square(theta,X,y,error):
    chi_sqr = 0
    for i in range(N):
        chi_sqr += np.square( ( f(X[i],theta) - y[i] ) / error[i] )
    return chi_sqr
##Levenberg-Marquardt Method
def Mrq(theta,X,y,error):
    start=time.time()
    check=start
    chi_sqr0 = chi_square(theta,X,y,error)
    l = .01
    while (check-start<.2):  #pause criteria
        B = -chi_derivative(theta,X,y,error)
        A = hess(theta,X,error)
        for i in range(A.shape[0]):
            A[i][i] = A[i][i] * (1+l)
        theta_1 = theta + solve( A , B.T ).T
        chi_sqr1 = chi_square(theta_1,X,y,error)
        if (chi_sqr1 >= chi_sqr0):
            l = l * 10
        else:
            l = l / 10
            theta = theta_1 
            chi_sqr0 = chi_sqr1 
        check=time.time()
    return theta

def main():
    pass
if __name__ == 'main':
    main()