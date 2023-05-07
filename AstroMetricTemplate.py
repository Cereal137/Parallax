import numpy as np

epsilon=23.44 /180*np.pi #Earth Obliquity in radians
eccentricity=0.0167 #Earth orbit Eccentricity
Period=365.25 #Earth Period in days
semi_major_axis=1.00000011 #Earth Semi-Major Axis in AU
JD_VernalEquinox=2451623.815972 #Julian Date of Vernal Equinox in 2000
JD_Perihelion=2451546.708333 #Julian Date of Perihelion in 2000
c_AU_yr= 63239.7263 #speed of light in AU/yr

class CartesianCoordinate():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def DotProduct(self, v):
        return self.x*v.x + self.y*v.y + self.z*v.z
    
class CelestialCoordinate():
    def __init__(self, longitude, latitude, err_long, err_lat, JulianDate):
        self.longitude = longitude
        self.latitude = latitude
        self.err_long = err_long
        self.err_lat = err_lat
        self.JulianDate = JulianDate

    def Equator2Ecliptic(self): 
        """Converts from Equatorial Coordinate System to Ecliptic Coordinate System
        Datum_fun: Data point in Equatorial Coordinate System
        returns: Data point in Ecliptic Coordinate System"""
        alpha = self.longitude
        delta = self.latitude
        beta = np.arcsin(np.sin(delta)*np.cos(epsilon) - np.cos(delta)*np.sin(epsilon)*np.sin(alpha))
        lambda_b = np.arccos((np.cos(delta)*np.cos(alpha))/(np.cos(beta)))
        self.latitude = beta
        self.longitude = lambda_b
        return self

    def Ecliptic2Equator(self):
        """Converts from Ecliptic Coordinate System to Equatorial Coordinate System
        Datum_fun: Data point in Ecliptic Coordinate System
        returns: Data point in Equatorial Coordinate System"""
        lambda_b = self.longitude
        beta = self.latitude
        delta = np.arcsin(np.sin(beta)*np.cos(epsilon) + np.cos(beta)*np.sin(epsilon)*np.sin(lambda_b))
        sign = (-np.sin(epsilon)*np.sin(beta) +np.cos(beta)*np.cos(epsilon)*np.sin(lambda_b) )/np.abs((-np.sin(epsilon)*np.sin(beta) +np.cos(beta)*np.cos(epsilon)*np.sin(lambda_b) ))
        alpha = -sign*np.arccos((np.cos(beta)*np.cos(lambda_b))/np.cos(delta))
        self.latitude = delta
        self.longitude = alpha
        return self
       
    def get_longitude(self)->float:
        return self.longitude
    
    def get_latitude(self)->float:
        return self.latitude
    
    def get_err_long(self)->float:
        return self.err_long
    
    def get_err_lat(self)->float:
        return self.err_lat
    
    def get_JulianDate(self)->float:
        return self.JulianDate
    
    def get_Year(self)->float:
        return self.JulianDate/Period-4712
    
    def GetEarthDistance(self)->float:
        #Finds the distance of the Earth from the Sun
        Phase = 2*np.pi*(-JD_Perihelion+self.JulianDate)/Period
        p = semi_major_axis*(1-eccentricity**2)
        return p/(1+eccentricity*np.cos(Phase))
    
    def GetEarthLambda(self)->float:
        return 2*np.pi*(self.JulianDate- JD_VernalEquinox)/Period
    
    def normal_vector(self)->np.ndarray:
        return np.array([np.cos(self.longitude)*np.cos(self.latitude), np.sin(self.longitude)*np.cos(self.latitude), np.sin(self.latitude)])
    
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

    def get_node(self, index)->CelestialCoordinate:
        return self.node_list[index]
    
    def get_length(self)->int:
        return self.length

txtIn = np.dtype({
    'names':['JD', 'hh_RA', 'mm_RA', 'ss_RA', 'err_RA', 'deg', 'min', 'sec', 'err_Dec'],
    'formats':['f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f']
}) #Data type for the data

def ReadData(s:str)->NodeList:
    ## Data Input from txt file
    DataIn_txt = np.loadtxt(s, dtype=txtIn) #Load data from file
    N = len(DataIn_txt) #Number of data points

    ## transform data into a list of nodes
    DataList = NodeList()
    for i in range(N):
        alpha = DataIn_txt[i][1]*np.pi/12 + DataIn_txt[i][2]*np.pi/12/60 + DataIn_txt[i][3]*np.pi/12/3600
        delta = DataIn_txt[i][5]*np.pi/180 + DataIn_txt[i][6]*np.pi/180/60 + DataIn_txt[i][7]*np.pi/180/3600
        err_alpha = DataIn_txt[i][4]*np.pi/12/3600
        err_delta = DataIn_txt[i][8]*np.pi/180/3600
        JD = DataIn_txt[i][0]
        DataList.add_node(CelestialCoordinate(alpha, delta, err_alpha, err_delta, JD))
    return DataList


def main():
    pass

if __name__ == '__main__':
    main()