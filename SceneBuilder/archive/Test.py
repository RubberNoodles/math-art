import bpy
import bmesh

def dump(mesh):
    ob1 = bpy.data.objects["TestRiemannSurface"]
    ob2 = bpy.data.objects["RiemannSurfaceSurface"]
    me1 = ob1.data
    me2 = ob2.data
    
    sk1b = ob1.shape_key_add("Basis")
    sk1 = ob1.shape_key_add("Key1")
    
    
    #sl = bm1.verts.layers.shape.get("Key1")
    #print(sl)

    for vert in ob2.data.vertices:
        sk1.data[vert.index].co = vert.co

dump(bpy.context.active_object.data)