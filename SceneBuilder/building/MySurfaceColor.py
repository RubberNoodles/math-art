from Vector import *
from Surface import *
from Curve import *
#from PIL import Image
import os, sys, bpy, importlib
import csv
import MyCurve
import json
importlib.reload(MyCurve)

#im = Image.open("O:\\MB\\MB\peschke\\surfaces\\blender\\img\\world.200411.3x5400x2700.jpg")
#sys.path.append(os.path.dirname(bpy.context.blend_data.filepath+"/../../blender")+'/surf_data')
#im = Image.open(os.path.realpath(bpy.context.blend_data.filepath+"/../../blender")+'/Dissidia_012_World.jpg')
#pix = im.load()

def reshape(file_path):
    #TODO: tests that this reshape function works.
    with open(file_path) as f:
        array_reader = csv.reader(f, delimiter=',')

        list_dict={}
        uSteps=0
        vSteps=0
        vList=[] #The output array we want should be uSteps rows of vSteps triples
        for ind,line in enumerate(array_reader):
            if ind > 1:
                # Reshaping the lists
                line = [float(i) for i in line]
                if ind % vSteps == 1:
                    vList.append(line)
                    list_dict[lists[(ind-2)//arrlen]].append(vList)
                    vList=[]
                else:
                    vList.append(line)
            elif ind == 1:
                # All single value variables
                for i in range(int(len(line)/2)):
                    list_dict[line[2*i]]=line[2*i+1] if not line[2*i+1].isnumeric() else int(line[2*i+1])
                uSteps=list_dict['uSteps']
                vSteps=list_dict['vSteps']
                #The dimensions of each array
                arrlen=uSteps*vSteps
            else: #ind==0
                # The first line of the csv is a list of all the parameters
                # I want to set the second line to be all the possible changeable features.
                lists = []
                for val in line:
                    lists.append(val)
                    for list_data in lists:
                        list_dict[list_data] = []

        return list_dict

class MySurface(Surface):
    def __init__(self, file_path):
        Surface.__init__(self, self.value, self.du, self.dv,
                       0.0, 6.283185307179586, -1.570796326794896, 1.570796326794896,
                       uCyclic=False, vCyclic=True,
                       red=self.red, red0=0, red1=1,
                       green=self.green, green0=0, green1=1,
                       blue=self.blue, blue0=0, blue1=1)
        data=reshape(file_path)
        self.name=data['name']
        self.resu=data['uSteps']
        self.resv=data['vSteps']     
        self.valueList=data['valueList']
        self.uDeriv1List=data['uDeriv1List']
        self.vDeriv1List=data['vDeriv1List']
        self.redList=data['redList']
        self.greenList=data['greenList']
        self.blueList=data['blueList']
        self.col_name=data['col']
    
    def return_name(self):
        return self.name
    def value(self, u, v):
        (u,v) = (int(u),int(v))
        return (ScalMult(1.0,self.valueList[u][v]))
    def du(self, u, v):
        return (ScalMult(1.0,self.uDeriv1List[u][v]))
    def dv(self, u, v):
        return (ScalMult(1.0,self.vDeriv1List[u][v]))
    def cube_root(self, value):
        if value< 0:
            b=-(-value)**(1/3)
        else:
          b = (value)**(1/3)
        return b


    def red(self, u, v):
        return self.redList[u][v][0]
    def green(self, u, v):
        return self.greenList[u][v][0]
    def blue(self, u, v):
        return self.blueList[u][v][0]

def SurfaceToCoordinateLine(file_path, uv, name0, ind=10):
    data=reshape(file_path)
    #This is structured so that each row is a given value of u, iterated over all possible v.
    #i.e. values[0] "SHOULD" be a u coordinate line; it works
    # How densely you want coordinate lines.
    curveData={}
    if uv == 'U':
        if ind > data['uSteps']-1:
            ind = data['uSteps']-1
        name = data['name'] +'Ucoord'+name0
        curveData={'name':name, 'steps':data['vSteps'],
            'valueList': data['valueList'][ind], 'deriv1List': data['vDeriv1List'][ind],
            'deriv2List': data['vDeriv2List'][ind], 'col':data['col'],
            'redList':data['redList'][ind], 'greenList':data['greenList'][ind],
            'blueList':data['blueList'][ind]}
    elif uv == 'V':
        if ind > data['vSteps']-1:
            ind = data['vSteps']-1
        name = data['name'] +'Vcoord'+name0
        curveData={'name':name, 'steps':data['uSteps'], 'col':data['col']}

        lists = [('valueList','valueList'), ('deriv1List','uDeriv1List'), ('deriv2List','uDeriv2List'),
         ('redList','redList'), ('greenList','greenList'), ('blueList','blueList')]
        for l in lists:
            curveData[l[0]] = [row[ind] for row in data[l[1]]]
    else:
        return {'NONE'}
    return MyCurve.MyCurve(data=curveData)

