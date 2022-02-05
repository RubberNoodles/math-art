from tkinter import *
import os, shutil, platform
import subprocess
from tkinter.filedialog import askopenfilename
import sys, importlib
import PathConfig as pathc

sys.path.append("")
sys.path.append(os.getcwd()+"/../common")

origWD = os.getcwd() # remember our original working directory
#os.chdir(os.path.join(os.path.abspath(sys.path[0]), relPathToLaunch))
LD_dir = os.path.realpath(origWD+'/building/surf_data') #directory for all the list data

#Reset the folder with all data points
#folders = ['building/surf_data','building/curve_data']
folders = ['building/surf_data']
for folder in folders:
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except:
            pass

#Create the GUI
class App:

    def __init__(self, master):
        self.obj = {}
        frame = Frame(master,bg="gray90")
        frame.grid(row=0, column=0)

        self.quit = Button(frame, text="QUIT", fg="red", command=lambda: self.exit(master))
        self.quit.grid(row=7, column=0)

        #Initialize Entry variables
        self.x,self.y,self.z,self.id, self.x0,self.y0, self.z0, self.r, self.g,\
             self.b, self.col_id, self.bfile, self.blender_path, self.maxima_path,\
             self.u0,self.u1,self.v0,self.v1,self.t0,self.t1 = [StringVar(master) for i in range(20)]
        self.coordU_val, self.t_key, self.coordV_val = [IntVar(master) for j in range(3)]
        #Entering Parameters
        self.x_param = Entry(frame, textvariable=self.x)
        self.x_param.grid(row=0, column=2)
        self.x_label=Label(frame, text="x(u,v)/x(t) :=")
        self.x_label.grid(row=0, column=1)
        self.y_param = Entry(frame, textvariable=self.y)
        self.y_param.grid(row=1, column=2)
        self.y_label=Label(frame, text="y(u,v)/y(t) :=")
        self.y_label.grid(row=1, column=1)
        self.z_param = Entry(frame, textvariable=self.z)
        self.z_param.grid(row=2, column=2)
        self.z_label=Label(frame, text="z(u,v)/z(t) :=")
        self.z_label.grid(row=2, column=1)

        self.name = Entry(frame, textvariable=self.id)
        self.name.grid(row=3, column=2)
        self.name_label = Label(frame, text="id:")
        self.name_label.grid(row=3, column=1)

        self.animate_label = Label(frame, text="t steps: ")
        self.animate_label.grid(row=3,column=3)
        self.animate_steps = Entry(frame, textvariable=self.t_key)
        self.animate_steps.grid(row=3,column=4)
        self.x0_param = Entry(frame, textvariable=self.x0)
        self.x0_param.grid(row=0, column=4)
        self.x0_label=Label(frame, text="x(u,v)/x(t) :=")
        self.x0_label.grid(row=0, column=3)
        self.y0_param = Entry(frame, textvariable=self.y0)
        self.y0_param.grid(row=1, column=4)
        self.y0_label=Label(frame, text="y(u,v)/y(t) :=")
        self.y0_label.grid(row=1, column=3)
        self.z0_param = Entry(frame, textvariable=self.z0)
        self.z0_param.grid(row=2, column=4)
        self.z0_label=Label(frame, text="z(u,v)/z(t) :=")
        self.z0_label.grid(row=2, column=3)

        #Domain
        self.u0_label=Label(frame, text = "u min: ")
        self.u0_label.grid(row=0, column=7)
        self.u1_label=Label(frame, text = "u max: ")
        self.u1_label.grid(row=1, column=7)
        self.v0_label=Label(frame, text = "v min: ")
        self.v0_label.grid(row=2, column=7)
        self.v1_label=Label(frame, text = "v max: ")
        self.v1_label.grid(row=3, column=7)
        self.t0_label=Label(frame, text = "t min: ")
        self.t0_label.grid(row=4, column=7)
        self.t1_label=Label(frame, text = "t max: ")
        self.t1_label.grid(row=5, column=7)

        self.u0_param=Entry(frame, textvariable=self.u0)
        self.u0_param.grid(row=0, column=8)
        self.u1_param=Entry(frame, textvariable=self.u1)
        self.u1_param.grid(row=1, column=8)
        self.v0_param=Entry(frame, textvariable=self.v0)
        self.v0_param.grid(row=2, column=8)
        self.v1_param=Entry(frame, textvariable=self.v1)
        self.v1_param.grid(row=3, column=8)
        self.t0_param=Entry(frame, textvariable=self.t0)
        self.t0_param.grid(row=4, column=8)
        self.t1_param=Entry(frame, textvariable=self.t1)
        self.t1_param.grid(row=5, column=8)

        self.red_param = Entry(frame, textvariable=self.r)
        self.red_param.grid(row=0, column=6)
        self.red_label=Label(frame, text="red(u,v):=")
        self.red_label.grid(row=0, column=5)
        self.green_param = Entry(frame, textvariable=self.g)
        self.green_param.grid(row=1, column=6)
        self.green_label=Label(frame, text="green(u,v):=")
        self.green_label.grid(row=1, column=5)
        self.blue_param = Entry(frame, textvariable=self.b)
        self.blue_param.grid(row=2, column=6)
        self.blue_label=Label(frame, text="blue(u,v):=")
        self.blue_label.grid(row=2, column=5)
        self.col_label=Label(frame,text="col_id:")
        self.col_label.grid(row=3, column=5)
        self.col_param=Entry(frame, textvariable=self.col_id)
        self.col_param.grid(row=3, column=6)

                        #Coordinate Lines
        self.coordU = Label(frame, text = "U Coordinate Line")
        self.coordU_param = Entry(frame, textvariable = self.coordU_val)
        self.coordU_param.grid(row=0, column=10)
        self.coordU.grid(row = 0, column = 9)
        self.coordV = Label(frame, text = "V Coordinate Line")
        self.coordV_param = Entry(frame, textvariable = self.coordV_val)
        self.coordV_param.grid(row=1, column = 10)
        self.coordV.grid(row = 1, column = 9)

        self.params_label = Label(frame)
        self.params_label.grid(row=5, column=4)

        self.set_param = Button(frame,text="Test", command = self.set_entry)
        self.set_param.grid(row=4, column=6)

        # Drawing Features
        self.surface = Button(frame, text="Surface", command=self.draw_Surface)
        self.surface.grid(row=4, column=1)
        self.curve = Button(frame, text="Curve", command=self.draw_Curve)
        self.curve.grid(row=4, column=2)
        self.mkparam = Button(
                frame, text = "Create_Data",
                command=lambda: self.create_params(self.x.get(), self.y.get(),
                self.z.get(), self.id.get(),
                self.r.get(),self.g.get(),self.b.get(),
                self.col_id.get(),
                [self.u0.get(),self.u1.get(),self.v0.get(),self.v1.get(),self.t0.get(),self.t1.get()],
                )
                )
        self.mkparam.grid(row=4, column=3)
        self.animate_button = Button(frame,text="Animate Surface",
                command = lambda: self.animate_Surface(self.x.get(), self.y.get(),
                self.z.get(),
                self.x0.get(), self.y0.get(), self.z0.get(),
                self.id.get(), self.col_id.get(),
                domain = [self.u0.get(),self.u1.get(),self.v0.get(),self.v1.get(),self.t0.get(),self.t1.get()],
                )
                )
        self.animate_button.grid(row=4, column=4)

        self.bfile.set(f"{origWD}/building/MySurfaceTest.blend")
        self.blend_file=Label(frame, textvariable=self.bfile, wraplength=80)
        self.blend_file.grid(row=5, column=0)
        self.blend_button=Button(frame, text = "Open File",
                command = lambda: self.get_file(self.blend_file))
        self.blend_button.grid(row=4, column=0)

        self.render_button=Button(frame, text="Render", command = self.render)
        self.render_button.grid(row=4,column=5)

        #Finding Location of Blender and Maxima

        blender, maxima = pathc.find_app_paths()
        # Store temporary location for blender/maxima paths.
        self.maxima_path.set(maxima)
        '''
        try:
            sub = subprocess.Popen("which maxima", shell=True, stdout=subprocess.PIPE)
            bpath = sub.communicate()[0]
            spath = bpath.decode('utf-8')
            if spath.rstrip().split('/')[-1] == 'maxima':
                self.maxima_path.set(spath.rstrip())
            else:
                self.params_label['text'] = "Maxima not found on system"

        except:
            # MacOS default
            self.maxima_path.set('/opt/homebrew/bin/maxima')
        '''

        self.maxima = Label(frame, textvariable = self.maxima_path, wraplength=80)
        self.maxima.grid(row=6,column=1)
        self.maxima_button = Button(frame, text="Maxima Location:", command=lambda
            :self.get_file(self.maxima))
        self.maxima_button.grid(row=5,column=1)

        self.blender_path.set(blender)
        '''
        if platform.system() == 'Linux':
            try:
                sub = subprocess.Popen("which blender", shell=True, stdout=subprocess.PIPE)
                bpath = sub.communicate()[0]
                spath = bpath.decode('utf-8')
                if spath.rstrip().split('/')[-1] == 'blender':
                    self.blender_path.set(spath.rstrip())
                else:
                    self.params_label['text'] = "Blender not found on system"

            except:
                self.blender_path.set('/Applications/Blender.app/Contents/MacOS/Blender')
        elif platform.system() == 'Darwin':
            #At least, this is where blender is for Oliver
            self.blender_path.set('/Applications/Blender.app/Contents/MacOS/Blender')
        elif platform.system() == 'Windows':
            self.blender_path.set("\"%USERPROFILE%/AppData/Roaming/Blender Foundation/Blender/2.83/blender \"")
            #WIP I don't know where blender installs on windows.
        else:
            pass
            #WIP
        '''

        self.blender = Label(frame, textvariable = self.blender_path, wraplength=80)
        self.blender.grid(row=6,column=2)
        self.blender_button = Button(frame, text="Blender Location:", command=lambda
            :self.get_file(self.blender))
        self.blender_button.grid(row=5,column=2)

        subprocess.run(f"\"{self.blender_path.get()}\" {self.bfile.get()} -b --python features/initBlend.py", shell=True)

        #Modifing Objects in Scene

        self.obj_canvas = Canvas(master, width=300, height=200, bg='gray70')
        self.obj_canvas.grid(row=1,column=0)

        self.renew_button = Button(self.obj_canvas, text="Renew",command = self.renew)
        self.renew_button.pack(side=LEFT)
        self.scroll=Scrollbar(self.obj_canvas)
        self.obj_list=Listbox(self.obj_canvas, yscrollcommand = self.scroll.set)
        self.obj_list.pack(side=LEFT)
        self.scroll.pack(side=LEFT,fill=Y)
        self.scroll.config(command=self.obj_list.yview)
        self.modify = Button(self.obj_canvas, text="Modify",
           command=lambda : self.modify_obj(self.obj[self.obj_list.get(
               self.obj_list.curselection()[0])]))
        self.modify.pack(side=LEFT)

        #Maybe eventually some ideas of deleting multiple objects
        #Also some concepts of running multiple scripts with a
        #single opening of blender so we don't have to
        #continually open and close the application (1-2s delay~)

        #At some point I will need to figure out how to actually parse all this content
        #And turn these null obj back in obj with parameters
        self.modify_frame = Frame(self.obj_canvas,bg='gray90')
        self.modify_frame.pack(side=LEFT)
        self.obj_label = Label(self.modify_frame, text = "")
        self.obj_label.pack(side=LEFT)

        self.obj_delete = Button(self.modify_frame, text = "Delete", state="disabled",
             command=lambda: self.delete_obj(self.obj[self.obj_label['text']]))
        self.obj_delete.pack(side=TOP)

        self.warning=Label(self.modify_frame, text = "Please don't delete Camera or Light",wraplength=100)
        self.warning.pack(side=TOP)

        self.mat = ['']
        self.mat_var = StringVar(self.modify_frame)
        self.mat_var.set(self.mat[0])
        self.mat_list = OptionMenu(self.modify_frame, self.mat_var, *self.mat)
        self.mat_list.pack(side=TOP)

        self.mat_assign = Button(self.modify_frame, text = "Assign Material",
            command = lambda:self.assign_mat(self.obj_label['text'], self.mat_var.get()),
            state="disabled")
        self.mat_assign.pack(side=TOP,fill=X)

        self.img_label = Label(self.obj_canvas,text="")
        self.img_label.pack(side=LEFT)
        #self.renew()
        #extract saved path from temp file.


    def blend_communicate(self, files):
        file_str=""
        for file in files:
            file_str+= "--python " + file + " "
        file_str= file_str[:-1]
        sub = subprocess.Popen(f"\"{self.blender_path.get()}\" {self.bfile.get()} -b {file_str}",
            shell=True, stdout = subprocess.PIPE)
        stdout_lis = sub.communicate()[0].decode('utf-8').split('\n')[0:len(files)]
        return stdout_lis

    def create_params(self,x,y,z,name,red,green,blue,col_id, domain, data_file="\"surf0.txt\""):
        #try: I'm going to implement fail safes later.
        u0,u1,v0,v1,t0,t1 = domain
        '''
        if (u0==u1 and u0 and u1) or (v0 == v1 \
            and u0 and u1) or (t0==t1 and u0 and u1):
            self.params_label['text'] = "Domain has zero size"
            raise Exception
        else:
            domain=[str(i) for i in domain]
            u0,u1,v0,v1,t0,t1 = domain
        '''
        if ' ' in name or ' ' in col_id:
            self.params_label['text'] = "No spaces in id/col_id"
            raise Exception

        if not red:
            red = '0.5'
        if not green:
            green = '0.7'
        if not blue:
            blue = '0.5'
        if not col_id:
            col_id = 'Default'
        if not name:
            name = 'Default'
        if 'coord' in name:
            self.params_label['text'] = "No \'coord\' in id"
            raise Exception
        #if x[-1] != ';' or y[-1] != ';' or z[-1] != ';' or name[-1] != ';':
        #    self.params_label['text'] = "Syntax error with maxima hint: ';' is required at the end"

        with open(f"{origWD}/building/params.mac",'w') as param_file:
            #Surfaces
            param_file.write('x(u,v):='+x+';\n'+'y(u,v):='+y+';\n'+ 'z(u,v):='+z
            + ';\n')
            param_file.write('red_func(u,v):=' + red + ';\ngreen_func(u,v):=' + green + ';\nblue_func(u,v):=' + blue +';\n')
            #Curves
            param_file.write('x0(t):='+x+';\n'+'y0(t):='+y+';\n'+ 'z0(t):='+z
            + ';\n')
            param_file.write('red_func0(t):=' + red + ';\ngreen_func0(t):=' + green + ';\nblue_func0(t):=' + blue +';\n')
            #Domain

            #Other Parameters
            param_file.write('id:'+name +';\n' + 'file:'+data_file+';\n')
            param_file.write('col_id:'+col_id+';\n')

            param_file.write("u0:"+u0 + ';\n'+"u1:" + u1 + ';\n' +"v0:" + v0 + ';\n' +"v1:" +v1 + ';\n'
                "t0:" + t0 + ';\n' + "t1:" + t1 + ';\n')


            self.params_label['text'] = "Data written"
        self.temp_obj = {'name':name, 'xyz':(x,y,z),'rgb':(red,green,blue), 'parent':None}

        if self.coordU_val.get():
            self.temp_objU = {'name':name+'Ucoord', 'parent':self.temp_obj['name'], 'rgb':(red,green,blue), 'type':'COORD_CURVE'}
        if self.coordV_val.get():
            self.temp_objV = {'name':name+'Vcoord', 'parent':self.temp_obj['name'], 'rgb':(red,green,blue), 'type':'COORD_CURVE'}
        self.temp_col = col_id

    def draw_Curve(self):
        if os.path.isfile('./building/params.mac'):
            pass
        else:
            self.params_label['text'] = "Data has not been created. Hint: write parameters and Create Data"
            return None
        subprocess.run(f"\"{self.maxima_path.get()}\" -b building/MyCurveListData.mac",
            shell=True) #Ok this failsafe doesn't work
        print("List Data Written")

        # atm I need to call different files if I want different functions.
        print("Drawing Objects")
        subprocess.run(f"\"{self.blender_path.get()}\" {self.bfile.get()} -b --python features/DrawCurve.py",
                    shell=True)
        print("Objects Drawn")
        self.temp_obj['type'] = 'CURVE'
        self.add_obj(self.temp_obj)
        self.mat_list['menu'].add_command(label=self.temp_col,
             command=lambda:self.mat_var.set(self.temp_col))
        os.unlink("params.mac")

    def draw_Surface(self):
        if os.path.isfile('./building/params.mac'):
            pass
        else:
            self.params_label['text'] = "Data has not been created. Hint: write parameters and Create Data"
            return None
        subprocess.run(f"\"{self.maxima_path.get()}\" -b ./building/MySurfaceColorFile.mac",
            shell=True) #Ok this failsafe doesn't work
        print("List Data Written")

        # atm I need to call different files if I want different functions.
        print("Drawing Objects ...")
        # Make coordU bool into an integer from 0-10
        subprocess.run(f"\"{self.blender_path.get()}\" {self.bfile.get()} -b --python features/DrawSurface.py -- {self.coordU_val.get()} {self.coordV_val.get()}",
                    shell=True)
        print("Objects Drawn")
        if self.coordU_val.get():
            self.add_obj(self.temp_objU)
        if self.coordV_val.get():
            self.add_obj(self.temp_objV)
        self.temp_obj['type'] = 'SURFACE'
        self.add_obj(self.temp_obj)
        self.mat_list['menu'].add_command(label=self.temp_col,
             command=lambda:self.mat_var.set(self.temp_col))

        os.unlink("./building/params.mac")
        return {"FINISHED"}

    def animate_Surface(self,x,y,z,x0,y0,z0, name, col_id, domain):
        #WIP, Todo: I have to automate a way for animations to be outputted? Or idk.

        steps = self.t_key.get()
        if steps <= 0:
            self.params_label['text'] = "In order to animate a surface, please have a positive number of t steps."
            return
        for i in range(steps):
            # Create all the data for each keyframe
            ratio = i/steps
            func_x = str(1-ratio) + '*' + x +'+'+ str((ratio)) + '*' + x0
            func_y = str(1-ratio) + '*' + y +'+'+ str((ratio)) + '*' + y0
            func_z = str(1-ratio) + '*' + z +'+'+ str((ratio)) + '*' + z0
            self.create_params(
                func_x, func_y, func_z, name,
                self.r.get(),self.g.get(),self.b.get(),
                self.col_id.get(), domain,
                data_file = f"\"surf{i}.txt\"",
                )
            subprocess.run(f"\"{self.maxima_path.get()}\" -b building/MySurfaceColorFile.mac",
                shell=True)
            print(f"surf{i}.txt Written")
        print(" -----------------------------------------")
        print("List Data Written")
        print("Creating Animation")

        subprocess.run(f"\"{self.blender_path.get()}\" {self.bfile.get()} -b --addons animation_animall --python features/AnimateSurface.py",
                    shell=True)

    def modify_obj(self, obj):
        self.obj_label['text'] = str(obj['name'])
        if obj['type'] == 'NULL':
            #only allow delete buttons
            self.obj_delete['state'] = 'normal'

        elif obj['type'] == 'SURFACE' or obj['type'] == 'CURVE':
            self.obj_delete['state'] = 'normal'
            #idk, figure out all the potential options?
        elif obj['type'] == 'COORD_CURVE':
            self.obj_delete['state'] = 'normal'
        self.mat_assign['state'] = 'normal'

    def delete_obj(self, obj):
        obj_del = [obj]

        #Deleting corresponding coordinate lines
        for obj_name in self.obj:
            obj_child = self.obj[obj_name]
            if obj_child['parent'] == obj['name']:
                obj_del.append(obj_child)
        obj_str = ""
        for a in obj_del:
            obj_str += a['name'] + ' '
        obj_str = obj_str[:-1]
        subprocess.run(f"\"{self.blender_path.get()}\" {self.bfile.get()} -b --python features/DeleteObj.py -- {obj_str}",shell=True)
        for ob in obj_del:
            self.obdesgj.pop(ob['name'])
            obj = self.obj_list.get(0,END).index(ob['name'])
            self.obj_list.delete(obj)
        self.obj_label['text']=""
        self.obj_delete['state']="disabled"
        self.mat_assign['state']="disabled"

    def assign_mat(self, obj, mat):
        # WIP: Assign all coordinate lines to be the same material.
        obmat= mat + ' ' + obj
        self.obj[obj]['col_id'] = mat
        subprocess.run(f"\"{self.blender_path.get()}\" {self.bfile.get()} -b --python features/AssignMat.py -- {obmat}",shell=True)

    def get_file(self,app_entry):
        file = askopenfilename()
        if app_entry['textvariable']:
            # WIP find how to find which variable is assosciated to the text
            if app_entry == self.maxima:
                self.maxima_path.set(file)
            elif app_entry == self.blender:
                self.blender_path.set(file)
            elif app_entry == self.blend_file:
                self.bfile.set(file)
            else:
                pass
        else:
            app_entry['text'] = file

    def add_obj(self,obj):

        try:
            if obj['name'][-6:-1] == 'coord':
                name = obj['name'][:-1]
                obj['name']=name
            else:
                name = obj['name']
        except:
            name = obj['name']
        self.obj[name] = obj
        if name in self.obj_list.get(0,END):
            pass
        else:
            self.obj_list.insert(END,name)

    def renew(self):
        strlist = self.blend_communicate(['features/CheckObj.py','features/CheckMat.py'])
        obj_null = self.strlist_to_list(strlist[0])
        self.mat = self.strlist_to_list(strlist[1])
        null_dict={}
        for i in obj_null:
            null_dict[i] = {'name':i,'type':'NULL','parent':None, 'col_id':None}
        self.obj_list.delete(0,END)
        for key in null_dict.keys():
            self.add_obj(null_dict[key])
        self.mat_list['menu'].delete(0, END)
        for i in self.mat:

            self.mat_list['menu'].add_command(label=i,
            command=lambda val=i:self.mat_var.set(val))

    def render(self):
        subprocess.run(f"\"{self.blender_path.get()}\" {self.bfile.get()} -b -f 0", shell=True)
        img=PhotoImage(file="img0000.png")
        img=img.subsample(5,5)
        self.img_label['image']=img
        self.img_label.image=img

    def strlist_to_list(self,str_lis):
        '''turning the weird string to list'''
        out_temp=str_lis.split(",")
        out_list=[]
        for index, ele in enumerate(out_temp):
            if index==0:
                out_list.append(ele[2:-1])
            elif index==len(out_temp)-1:
                out_list.append(ele[2:-2])
            else:
                out_list.append(ele[2:-1])
        return out_list # There are no parameters to these obj's

    def save_GUI(self):
        with open("tempSettings.txt",'w') as txt:
                txt.write(self.blender_path.get()+'@@@'+self.maxima_path.get()
                    + '@@@' + self.bfile.get())

    def exit(self, master):
        self.save_GUI()
        master.quit()

    def set_entry(self):
        self.x.set("sin(u)*sin(v)")
        self.y.set("sin(u)*cos(v)")
        self.z.set("cos(u)")
        self.id.set("idtest")
        self.col_id.set("colidtest")
        self.t_key.set("3")
        self.u0.set("0")
        self.u1.set("%pi")
        self.v0.set("-%pi")
        self.v1.set("%pi")
        self.t0.set("0")
        self.t1.set("0")
        self.x0.set("sin(u)*sin(v)")
        self.y0.set("sin(u)*cos(v)")
        self.z0.set("cos(v)")
root = Tk()

app = App(root)

root.mainloop()
root.destroy() # optional; see description below
