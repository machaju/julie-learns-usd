from pxr import Usd, UsdGeom, Gf, Sdf

'''
Make the Base stage for every layer
'''
def MakeBaseStage(usdFileName):
    stage = Usd.Stage.CreateNew(usdFileName)
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
    stage.SetStartTimeCode(0)
    stage.SetEndTimeCode(192)
    return stage

def Step1():
    stage = MakeBaseStage('Step1.usda')
    stage.SetMetadata('comment', 'Step 1: Start and end time codes')
    stage.Save()

def AddReferenceToGeometry(stage, path):

    geom = stage.GetPrimAtPath(path)
    geom = UsdGeom.Xform.Define(stage, path)
    geom.GetPrim().GetReferences().AddReference('./house.usd')
    return geom

def Step2():
    stage = MakeBaseStage('Step2.usda')
    stage.SetMetadata('comment', 'Step 2: Object Creation')

    house = AddReferenceToGeometry(stage, '/house')
    stage.Save()


def AddSpin(shape):
    spin = shape.AddRotateYOp(opSuffix='spin')
    spin.Set(time=0, value=0)
    spin.Set(time=192, value=1440)


def Step3():
    stage = MakeBaseStage('animated-house.usda')
    stage.SetMetadata('comment', 'Step 3: Adding spin animation')
    house = AddReferenceToGeometry(stage, '/house')
    AddSpin(house)
    stage.Save()


Step1()
Step2()
Step3()
