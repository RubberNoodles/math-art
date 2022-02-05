import bpy, sys
#Figure this out for coordinate lines.

argv=sys.argv

argv = argv[argv.index('--')+1:]

mat, obj = argv
obj_list=[]
try:
    # This is for coordinate lines
    if obj[-5:]=='coord':
        count=0
        while True:
            obj_temp=bpy.data.objects.get(obj+str(count))
            if not obj_temp:
                break
            else:
                obj_list.append(obj_temp)
                count+=1
    else:
        obj_list = [bpy.data.objects[obj]]
except:
    obj_list = [bpy.data.objects[obj]]



mat = bpy.data.materials[mat]
for ob in obj_list:
    if ob.data.materials:
        # assign to 1st material slot
        ob.data.materials[0] = mat
    else:
        # no slots
        ob.data.materials.append(mat)

bpy.ops.wm.save_as_mainfile()