import bpy, sys

argv=sys.argv

argv = argv[argv.index('--')+1:]
bpy.ops.object.select_all(action='DESELECT')
for i in argv:
    is_coord = False
    try:
        print(i)
        if i[-5:] == 'coord':
            is_coord = True
    except:
        pass
    try:
        if is_coord:
            count = 0
            while True:
                try:
                    bpy.data.objects[i+str(count)].select_set(True)
                    count+=1
                except:
                    break
        else:
            bpy.data.objects[i].select_set(True)
    except:
        pass
bpy.ops.object.delete()
bpy.ops.wm.save_as_mainfile()