#%%
import numpy as np
import matplotlib.pyplot as plt
import AstroMetricTemplate as tp

def radians_to_mas(radians):
    return radians/np.pi*180*3600*1000

def mas_to_radians(mas):
    return mas/1000/3600/180*np.pi


#read in
DataList = tp.ReadData('hii_625.txt')
N = DataList.get_length()
alpha_epoch = DataList.get_node(0).get_longitude()
delta_epoch = DataList.get_node(0).get_latitude()
t_epoch = DataList.get_node(0).get_Year()
#params obtained
params = np.array([  1.65171967,5.19470275,-44.37645348,19.48086502,7.31131175])

#initialize
JulianDate_epoch = DataList.get_node(0).get_JulianDate()
JulianDate_plot = np.linspace(JulianDate_epoch-50,JulianDate_epoch+500,1000)

Node_In = tp.CelestialCoordinate(alpha_epoch,delta_epoch,0.0,0.0,JulianDate_plot)

r_E = Node_In.GetEarthDistance()
lambda_E = Node_In.GetEarthLambda()
t = Node_In.get_Year() #Julian Date

#Earth Node
Node_Earth = tp.CelestialCoordinate(np.pi+lambda_E,0.0,0.0,0.0,Node_In.get_JulianDate()).Ecliptic2Equator() #Earth Node in Equatorial Coordinate
#Geometry in Cartesian Coordinate
alpha = Node_In.get_longitude()
delta = Node_In.get_latitude()

p = np.array([-np.sin(alpha), -np.cos(alpha), 0.0])
#q = np.array([-np.sin(delta)*np.cos(alpha), -np.sin(delta)*np.sin(alpha), np.cos(delta)])
q = np.array([-np.sin(delta)*np.cos(alpha), np.sin(delta)*np.sin(alpha), np.cos(delta)])
r = Node_In.normal_vector()
    
b = r_E* Node_Earth.normal_vector()
print(b[2].max())
#Consider Roemer Delay
t_B = t + np.dot(r,b)/tp.c_AU_yr
#Orbit Feature
OrbitFeature_1 = -np.dot(q,b)
print('max1=',OrbitFeature_1.max())
OrbitFeature_2 = -np.dot(p,b)
print('max2=',OrbitFeature_2.max())

#plot section
plt.subplot(2,1,1)
for i in range(N):
    PNode = DataList.get_node(i)
    delta_p = PNode.get_latitude()
    t = PNode.get_Year()
    plt.scatter(t,radians_to_mas(delta_p-delta_epoch)-params[0]-params[2]*(t-t_epoch),c='g',s=5)
plt.plot(Node_In.get_Year(),OrbitFeature_1*params[4],'r',label='Orbit Feature 1')
plt.legend()
plt.xlabel('Time(years)')
plt.ylabel('North offset (mas)')
plt.title('$\delta$ vs Year')
plt.show()

plt.subplot(2,1,2)
for i in range(N):
    PNode = DataList.get_node(i)
    alpha_p = PNode.get_longitude()
    delta_p = PNode.get_latitude()
    t = PNode.get_Year()
    plt.scatter(t,radians_to_mas(alpha_p-alpha_epoch)*np.cos(delta_p)-params[1]-params[3]*(t-t_epoch),c='g',s=5)
plt.plot(Node_In.get_Year(),OrbitFeature_2*params[4],'r',label='Orbit Feature 2')
plt.legend()
plt.xlabel('Time(years)')
plt.ylabel('East offset (mas)')
plt.title('R.A.$\cos\delta$ vs Year')
plt.show()


# %%
