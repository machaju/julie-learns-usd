'''
Following https://graphics.pixar.com/usd/docs/Simple-Shading-in-USD.html 

tutorial for shading, but using a different object 

'''

from pxr import Gf, Kind, Sdf, Usd, UsdGeom, UsdShade

# create a container for geometery and prims 
stage = Usd.Stage.CreateNew("simpleShading.usd")
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)

modelRoot = UsdGeom.Xform.Define(stage, "/TexModel")
Usd.ModelAPI(modelRoot).SetKind(Kind.Tokens.component)

# we already have the house mesh, so just grab it from here 
modelRoot.GetPrim().GetReferences().AddReference('./house.usd')

# make a material, this is a container for our shaders 
material = UsdShade.Material.Define(stage, '/TexModel/houseMat')


# create a surface shader, this is a child of material 
#make a preview surface
pbrShader = UsdShade.Shader.Define(stage, '/TexModel/houseMat/PBRShader')
pbrShader.CreateIdAttr("UsdPreviewSurface")
pbrShader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.4)
pbrShader.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(0.0)

# add this shader to teh preview surface 
material.CreateSurfaceOutput().ConnectToSource(pbrShader.ConnectableAPI(), "surface")

# adding texture 
# create a node to read and map the texture
stReader = UsdShade.Shader.Define(stage, '/TexModel/houseMat/stReader')
stReader.CreateIdAttr('UsdPrimvarReader_float2')

# create a node to fetch a texture coordinate from each piece of geometry 
# bound to the material, to inform the texture node how to map surface coordinates 
# to texture coordinates
diffuseTextureSampler = UsdShade.Shader.Define(stage,'/TexModel/houseMat/diffuseTexture')
diffuseTextureSampler.CreateIdAttr('UsdUVTexture')
diffuseTextureSampler.CreateInput('file', Sdf.ValueTypeNames.Asset).Set("house_diffuse.jpg")
diffuseTextureSampler.CreateInput("st", Sdf.ValueTypeNames.Float2).ConnectToSource(stReader.ConnectableAPI(), 'result')
diffuseTextureSampler.CreateOutput('rgb', Sdf.ValueTypeNames.Float3)
pbrShader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).ConnectToSource(diffuseTextureSampler.ConnectableAPI(), 'rgb')

stInput = material.CreateInput('frame:stPrimvarName', Sdf.ValueTypeNames.Token)
stInput.Set('st')

stReader.CreateInput('varname',Sdf.ValueTypeNames.Token).ConnectToSource(stInput)

# bind mest to materials 
house = stage.GetPrimAtPath('/TexModel/Mesh')
UsdShade.MaterialBindingAPI(house).Bind(material)

stage.Save()