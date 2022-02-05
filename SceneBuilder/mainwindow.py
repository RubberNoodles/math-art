import sys, os
import subprocess

import PyQt6.QtWidgets as Qw
import PyQt6.QtCore as Qc
import PyQt6.QtGui as Qg

from GUI.form import Ui_MainWindow
import PathConfig

# Of course, these need to be dynamic to the user, but right now 
# the file path of this entire folder is not in the right place
origWD = "/Users/seesea/Documents/Coding-Projects/AlphaOmega/peschke/SceneBuilder"
LD_dir = os.path.realpath(origWD+'/building/surf_data')
CD_dir = os.path.realpath(origWD+'/building/curve_data')

if not os.path.isdir(LD_dir):
    os.mkdir(LD_dir)
if not os.path.isdir(CD_dir):
    os.mkdir(CD_dir)

class MainWindow(Qw.QMainWindow, Ui_MainWindow):
    def __init__(self,*args, obj = None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.ui = Ui_MainWindow() 
        self.ui.setupUi(self)
        self.blenderPath, self.maximaPath = PathConfig.find_app_paths()
        self.bFile = os.path.realpath(origWD + "/building/MySurfaceTest.blend")
        
        # TODO: Figure out what these coord u/v actually do lmao
        self.coordUVal = 0
        self.coordVVal = 0

        self.connectButtons()
        self.addImg(renderFrame = self.ui.labelSurfaceRender)
        self.addImg(renderFrame = self.ui.labelCurveRender)

    def debugOnClick(self):
        print("a")
        return None

    def eventLoopRefreshGUI(self):
        # TODO: essentially something that I can run to make sure that
        # variables on screen (i.e. option menus for mat list etc.) are always
        # the same as the variables that Python is storing.
        raise NotImplementedError

    def blendCommunicate(self, files):
        fileStr=""
        for file in files:
            fileStr+= "--python " + file + " "
        fileStr= fileStr[:-1]
        sub = subprocess.Popen(f"\"{self.blenderPath}\" {self.bFile} --python-use-system-env -b {fileStr}",
            shell=True, stdout = subprocess.PIPE)
        stdout_lis = sub.communicate()[0].decode('utf-8').split('\n')[0:len(files)]
        return stdout_lis
    
    def connectButtons(self):
        self.ui.btnSurfaceRender.clicked.connect(self.renderOnClick)
        self.ui.btnCurveRender.clicked.connect(self.renderOnClick)
        self.ui.btnFillSurfaceInput.clicked.connect(self.fillSurfaceInputOnClick)
        self.ui.btnFillCurveInput.clicked.connect(self.fillCurveInputOnClick)
        self.ui.btnFillSurfaceColorInput.clicked.connect(self.fillSurfaceColorInputOnClick)
        for btnQuit in [self.ui.btnQuit,self.ui.btnQuit2,self.ui.btnQuit3,self.ui.btnQuit4]:
            btnQuit.clicked.connect(self.quitOnClick)
        self.ui.btnDebug.clicked.connect(self.debugOnClick)
    
    def renderOnClick(self):
        #Create Parameters
        if self.ui.ObjectTabWidget.currentIndex() == 0: # Surface
            x=self.ui.surfacex.text()
            y=self.ui.surfacey.text()
            z=self.ui.surfacez.text()
            id=self.ui.surfaceId.text()
            func_data = (x,y,z, id)

            r=self.ui.surfaceRed.text()
            g=self.ui.surfaceGreen.text()
            b=self.ui.surfaceBlue.text()
            col_id=self.ui.surfaceColorId.text()
            col_data = (r,g,b,col_id)

            u0=self.ui.u0.text()
            u1=self.ui.u1.text()
            v0=self.ui.v0.text()
            v1=self.ui.v1.text()
            domain = (u0,u1,v0,v1,"0","1")

            self.createParams(func_data,col_data, domain)
            print(f"Surface Parameters created at {origWD}/building/params.mac")
            self.drawSurface()
            self.assignMat(id, col_id)
            self.render()
            self.addImg(renderFrame = self.ui.labelSurfaceRender, file = "img0000.png") # TODO: make the file name dynamic.
        
        elif self.ui.ObjectTabWidget.currentIndex() == 1: # Curves
            x=self.ui.curvex.text()
            y=self.ui.curvey.text()
            z=self.ui.curvez.text()
            id=self.ui.curveId.text()
            func_data = (x,y,z, id)

            r=self.ui.curveRed.text()
            g=self.ui.curveGreen.text()
            b=self.ui.curveBlue.text()
            col_id=self.ui.curveColorId.text()
            col_data = (r,g,b,col_id)

            t0=self.ui.t0.text()
            t1=self.ui.t1.text()
            domain = ("0","0","0","0",t0,t1)

            self.createParams(func_data,col_data, domain)
            print(f"Curve Parameters created at {origWD}/building/params.mac")
            self.drawCurve()
            self.assignMat(id, col_id)
            self.render()
            self.addImg(renderFrame = self.ui.labelCurveRender, file = "img0000.png")

        elif self.ui.ObjectTabWidget.currentIndex() == 2: # Animation
            pass
    
        return None


    def createParams(self,func_data: tuple[str],col_data: tuple[str], domain: tuple[str], data_file="\"surf0.txt\""):
        #try: I'm going to implement fail safes later.
        
        if not self.paramsValid(self):
            return # TODO: what do i want to happen?
        
        x,y,z,name = func_data
        red,green,blue,col_id = col_data
        u0,u1,v0,v1,t0,t1 = domain

        with open(f"{origWD}/building/params.mac",'w') as paramFile:
            #Surfaces
            paramFile.write('x(u,v):='+x+';\n'+'y(u,v):='+y+';\n'+ 'z(u,v):='+z
            + ';\n')
            paramFile.write('red_func(u,v):=' + red + ';\ngreen_func(u,v):=' + green + ';\nblue_func(u,v):=' + blue +';\n')
            
            #Curves
            paramFile.write('x0(t):='+x+';\n'+'y0(t):='+y+';\n'+ 'z0(t):='+z
            + ';\n')
            paramFile.write('red_func0(t):=' + red + ';\ngreen_func0(t):=' + green + ';\nblue_func0(t):=' + blue +';\n')
            
            #Domain

            paramFile.write('id:'+name +';\n' + 'file:'+data_file+';\n')
            paramFile.write('col_id:'+col_id+';\n')

            paramFile.write("u0:"+u0 + ';\n'+"u1:" + u1 + ';\n' +"v0:" + v0 + ';\n' +"v1:" +v1 + ';\n'
                "t0:" + t0 + ';\n' + "t1:" + t1 + ';\n')


        self.temp_obj = {'name':name, 'xyz':(x,y,z),'rgb':(red,green,blue), 'parent':None}


    def drawSurface(self):
        if os.path.isfile(f'{origWD}/building/params.mac'):
            pass
        else:
            raise Exception
            self.params_label['text'] = "Data has not been created. Hint: write parameters and Create Data"
            return None
        subprocess.run(f"\"{self.maximaPath}\" -b {origWD}/building/MySurfaceColorFile.mac",
            shell=True) #Ok this failsafe doesn't work
        print("List Data Written")

        # atm I need to call different files if I want different functions.
        print("Drawing Objects ...")
        # Make coordU bool into an integer from 0-10
        subprocess.run(f"\"{self.blenderPath}\" {self.bFile} -b --python {origWD}/features/DrawSurface.py -- {self.coordUVal} {self.coordVVal}",
                    shell=True)
        print("Objects Drawn")
        '''
        if self.coordU_val:
            self.add_obj(self.temp_objU)
        if self.coordV_val:
            self.add_obj(self.temp_objV)
        self.temp_obj['type'] = 'SURFACE'
        self.add_obj(self.temp_obj)
        self.mat_list['menu'].add_command(label=self.temp_col,
             command=lambda:self.mat_var.set(self.temp_col))
        '''
        #os.unlink("./building/params.mac")
        return {"FINISHED"}

    def drawCurve(self):
        if os.path.isfile('./building/params.mac'):
            pass
        else:
            self.params_label['text'] = "Data has not been created. Hint: write parameters and Create Data"
            return None
        subprocess.run(f"\"{self.maximaPath}\" -b building/MyCurveListData.mac",
            shell=True) #Ok this failsafe doesn't work
        print("List Data Written")

        # atm I need to call different files if I want different functions.
        print("Drawing Objects")
        subprocess.run(f"\"{self.blenderPath}\" {self.bFile} -b --python features/DrawCurve.py",
                    shell=True)
        print("Objects Drawn")
        '''
        self.temp_obj['type'] = 'CURVE'
        self.add_obj(self.temp_obj)
        self.mat_list['menu'].add_command(label=self.temp_col,
             command=lambda:self.mat_var.set(self.temp_col))
        '''

        os.unlink("./building/params.mac")

    def assignMat(self, obj, mat):
        # WIP: Assign all coordinate lines to be the same material.
        obmat= mat + ' ' + obj
        subprocess.run(f"\"{self.blenderPath}\" {self.bFile} -b --python features/AssignMat.py -- {obmat}",shell=True)
   
    def render(self):
        subprocess.run(f"\"{self.blenderPath}\" {self.bFile} -b -f 0", shell=True)
        

        '''
        img=PhotoImage(file="img0000.png")
        img=img.subsample(5,5)
        self.img_label['image']=img
        self.img_label.image=img
        '''
    
    def addImg(self, renderFrame, file = "img0000.png"):
        if os.path.isfile(file):
            renderLabel = Qg.QPixmap(file)
            renderFrame.setPixmap(renderLabel)
            renderFrame.setScaledContents(True)

    def strListToList(self,strList):
        '''turning the lists that have been modified to strings by
        bash back into a list. Supports str and list of str inputs.'''
        if isinstance(strList, str):
            outTemp=strList.split(",")
            outList=[]
            for index, ele in enumerate(outTemp):
                if index==0:
                    outList.append(ele[2:-1])
                elif index==len(outTemp)-1:
                    outList.append(ele[2:-2])
                else:
                    outList.append(ele[2:-1])
            return outList # There are no parameters to these obj's
        if isinstance(strList, list):
            totalOutList = []
            for sl in strList:
                outTemp=sl.split(",")
                outList=[]
                for index, ele in enumerate(outTemp):
                    if index==0:
                        outList.append(ele[2:-1])
                    elif index==len(outTemp)-1:
                        outList.append(ele[2:-2])
                    else:
                        outList.append(ele[2:-1])
                totalOutList.append(outList)
            return totalOutList

    def paramsValid(self, type = None):
        ''' 
        Check whether the input parameters are correctly formatted 
        
        Type:
        0 => Surface
        1 => Curve
        2 => Animation
        '''
        if not type:
            type = self.ui.ObjectTabWidget.currentIndex()

        _, f_err = self.functionsValid()
        _, c_err= self.colorsValid()
        _, d_err = self.domainValid()

        errors = f_err + c_err + d_err

        # TODO: print into some label all the errors that were found.

        return bool(errors), errors
    
    def functionsValid(self):
        #TODO: need to check all of these, but in order to do this,
        # I need to communicate with Maxima/mathematica quickly in order to check
        # if these are valid expressions in the CAS
        valid = True
        errors = []
        return valid, errors

    def colorsValid(self):
        valid = True
        errors = []
        return valid, errors
    
    def domainValid(self):
        valid = True
        errors = []
        return valid, errors



    def fillSurfaceInputOnClick(self):
        self.ui.surfacex.setText("sin(u)*sin(v)")
        self.ui.surfacey.setText("sin(u)*cos(v)")
        self.ui.surfacez.setText("cos(u)")
        self.ui.surfaceId.setText("idSurfaceTest")
        self.ui.u0.setText("-%pi")
        self.ui.u1.setText("%pi")
        self.ui.v0.setText("0")
        self.ui.v1.setText("%pi")

    def fillCurveInputOnClick(self):
        self.ui.curvex.setText("sin(3*t)")
        self.ui.curvey.setText("cos(3*t)")
        self.ui.curvez.setText("0.2*t")
        self.ui.curveId.setText("idCurveTest")
        self.ui.t0.setText("-%pi")
        self.ui.t1.setText("%pi")

    def fillSurfaceColorInputOnClick(self):
        # TODO change this in the UI and link it up.
        self.ui.surfaceRed.setText("0.3")
        self.ui.surfaceGreen.setText("0.3")
        self.ui.surfaceBlue.setText("0.3")
        self.ui.surfaceColorId.setText("idColorTest")
    
    def quitOnClick(self):
        Qc.QCoreApplication.quit()


app = Qw.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()