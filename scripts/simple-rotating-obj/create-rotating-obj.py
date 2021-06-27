from pxr import Usd, UsdGeom, Gf, Sdf

class AnimatedObject:
    objName = None
    objType = None
    availShapes = ['sphere', 'cube']

    def __init__(self) -> None:
        # get user input
        val = input("Enter your shape {}: ".format(self.availShapes))
        val.lower()
        if val not in self.availShapes:
            print("You enterd an invalid shape, goodbye")
            exit()
        # set object name      
        self.objName = val

        # set the object type to either sphere or cube 
        if val in 'cube':
            self.objType = UsdGeom.Cube
        else:
            self.objType = UsdGeom.Sphere


    '''
    Make the Base stage for every layer
    '''
    def MakeBaseStage(self, usdFileName):
        stage = Usd.Stage.CreateNew(usdFileName)
        UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)
        stage.SetStartTimeCode(0)
        stage.SetEndTimeCode(192)
        return stage

    def Step1(self):
        stage = self.MakeBaseStage('Step1.usda')
        stage.SetMetadata('comment', 'Step 1: Start and end time codes')
        stage.Save()

    def Step2(self):
        stage = self.MakeBaseStage('Step2.usda')
        stage.SetMetadata('comment', 'Step 2: Object Creation')
        form = UsdGeom.Xform.Define(stage, '/form')

        # create the shape based off of objType 
        shape = self.objType.Define(stage, '/form/shape')

        # set the default prim 
        stage.Export('Step2.usda')
        fPrim = stage.GetPrimAtPath('/form')
        stage.SetDefaultPrim(fPrim)

        # change color 
        # sphereSchema = UsdGeom.Cube(shape)
        # color = sphereSchema.GetDisplayColorAttr()
        # color.Set([(0,0,1)])

        stage.GetRootLayer().Save()

    def AddReferenceToShape(self, stage, path):
        geom = UsdGeom.Xform.Define(stage, path)
        geom.GetPrim().GetReferences().AddReference('./Step2.usda')
        return geom

    def AddSpin(self, shape):
        spin = shape.AddRotateZOp(opSuffix='spin')
        spin.Set(time=0, value=0)
        spin.Set(time=192, value=1440)


    def Step3(self):
        stage = self.MakeBaseStage('Step3.usda')
        stage.SetMetadata('comment', 'Step 3: Adding spin animation')
        shape = self.AddReferenceToShape(stage, '/form')
        self.AddSpin(shape)
        stage.Save()


animated = AnimatedObject()
animated.Step1() 
animated.Step2() 
animated.Step3() 