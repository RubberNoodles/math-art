

class VizParms():
    def __init__(self): #constructor
        self.showFrenet=True
        self.showInset=True
        self.showOsculating=True
        self.showRectifying=False
        self.showNormalPlane=False
        self.showFrameNo=True
        self.showCurvatureTorsion=True
        self.showParticle = False
        self.scale=6.0
        self.curveRes=2000
        self.radius=0.1
        self.radRes=100
        self.endFrame=1000
        self.timeRes=100
        self.cameraDelay=-5
        self.cameraRotate=False
        self.binormalUp=True

    def Set \
        (
            self,
            showFrenet=True,
            showInset=True,
            showOsculating=False,
            showRectifying=False,
            showNormalPlane=False,
            showFrameNo=False,
            showCurvatureTorsion=True,
            showParticle=False,
            scale=6.0,
            curveRes=2000,
            radius=0.1,
            radRes=100,
            endFrame=1000,
            timeRes=100,
            cameraDelay=-5,
            cameraRotate=False,
            binormalUp=True
        ):
        self.showFrenet=showFrenet
        self.showInset=showInset
        self.showOsculating=showOsculating
        self.showRectifying=showRectifying
        self.showNormalPlane=showNormalPlane
        self.showFrameNo=showFrameNo
        self.showCurvatureTorsion=showCurvatureTorsion
        self.showParticle = showParticle
        self.scale=scale
        self.curveRes=curveRes
        self.radius = radius
        self.radRes=radRes
        self.endFrame=endFrame
        self.timeRes=timeRes
        self.cameraDelay=cameraDelay
        self.cameraRotate=cameraRotate
        self.binormalUp=binormalUp



#a = VizParms()
#a.SshowFrenet(False)
#print(a.showFrenet)

#print("done")