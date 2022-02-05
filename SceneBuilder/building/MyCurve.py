from math import sqrt, cos, sin, pi,tan 
from Vector import *
from Curve import *
from VizParm import VizParms
import csv

def reshape(file_path):
    list_dict={}
    with open(file_path) as f:
        array_reader = csv.reader(f, delimiter=',')

        for ind,line in enumerate(array_reader):
            if ind > 1:
                #Getting the value/deriv lists
                list_dict[lists[(ind-2)//list_dict['steps']]].append([float(i) for i in line])
            elif ind == 1:
                # All single value variables
                for i in range(int(len(line)/2)):
                    list_dict[line[2*i]]=line[2*i+1] if not line[2*i+1].isnumeric() else int(line[2*i+1])
                
            else: #ind==0
                # The first line of the csv is a list of all the data lists
                # I want to set the second line to be all the possible changeable features.
                lists = []
                for val in line:
                    lists.append(val)
                    for list_data in lists:
                        list_dict[list_data] = []
        return list_dict

class MyCurve(Curve):
    def __init__(self, file_path = None, data = None):
        Curve.__init__(self, self.value, self.deriv1, self.deriv2,
                       self.deriv3, 0, 101,
                       cyclic=True,
                       unitSpeed=False,
                       planar=False,
                       linear=False)
        data = data or reshape(file_path)

        self.name = data['name']
        self.vizparm = VizParms()
        self.vizparm.Set(True,False, False, False, False, False, False, True, 1.0 , True)
        ###MAXIMA OUTPUT
        self.steps = data['steps']
        self.valueList= data['valueList']
        self.deriv1List=data['deriv1List']
        self.deriv2List=data['deriv2List']
        self.col_name=data['col']
        self.redList=data['redList']
        self.greenList=data['greenList']
        self.blueList=data['blueList']
    def viz(self):
        return self.vizparm
    def r_name(self):
        return self.name
    def value(self, t):
        x=self.valueList[t][0]
        y=self.valueList[t][1]
        z=self.valueList[t][2]
        return ([x,y,z])
    def deriv1(self, t):
        x=self.deriv1List[t][0]
        y=self.deriv1List[t][1]
        z=self.deriv1List[t][2]
        return ([x,y,z])
    def deriv2(self, t):
        x=self.deriv2List[t][0]
        y=self.deriv2List[t][1]
        z=self.deriv2List[t][2]
        return ([x,y,z])
    def deriv3(self, t):
        pass 
    def col(self, t):
        rgb_temp=[self.redList[t][0],self.greenList[t][0],self.blueList[t][0]]
        rgb=[]
        for i in range(3):
            col=rgb_temp[i]
            try:
                col = float(col)
            except:
                col = 0.0
            if col < 0.0:
                col = 0.0
            if col > 1.0:
                col = 1.0
            rgb.append(col)
        return rgb
