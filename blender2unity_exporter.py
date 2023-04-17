from io import TextIOWrapper
import bpy
import random
import os
from shutil import Error, copyfile
from shutil import rmtree
import tarfile

#  bl_info = {
        #  "name" : "Blender2Unity Exporter",
        #  "author" : "q8f13",
        #  "version" : (0, 0, 1),
        #  "blender" : (3, 3, 5),
        #  "location" : "View 3D > Edit Mode > Tool Shelf",
        #  "description" :
            #  "Exporting tools for Unity",
        #  "warning" : "",
        #  "wiki_url" : "",
        #  "tracker_url" : "",
        #  "category" : "Material",
    #  }

CHANNELS = ['R','G','B','A']
#  rough_from_channel = 0
#  metal_from_channel = 0
#  mapnames=['Base Color','Subsurface','Subsurface_Radius','Subsurface_Color','Subsurface_IOR','Subsurface_Anisotropy','Metallic','Specular','Speular_Tint','Rooughness','Anisotropic','Anisotropic_Rotation','Sheen','Sheen_Tint','Clearcoat','Clearcoat_Roughness','IOR','Transmission','Transmission_Roughness','Emission','Emission_Strength','Alpha','Normal','Clearcoat_Normal','Tangent']

def randomguid(length):
    chars=['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
    return ''.join(random.choice(chars) for i in range(length))



def allexport(context):
    if not os.path.exists(context.scene.my_string_prop):
        os.makedirs(context.scene.my_string_prop)
    assetname=bpy.context.selected_objects[0].name
    path=context.scene.my_string_prop+assetname+"\\"
    if not os.path.exists(path):
        os.makedirs(path)
    prefabguid=randomguid(32)
    scriptguid=randomguid(32)
    fbxguid=randomguid(32)
    matguid=randomguid(32)
    norguid=randomguid(32)
    metguid=randomguid(32)
    alguid=randomguid(32)
    fol1guid=randomguid(32)
    fol2guid=randomguid(32)
    #print(fbxguid)
    #export fbx
    if not os.path.exists(path+fbxguid):
        os.makedirs(path+fbxguid)
    mainexp(context, path+fbxguid+"\\asset")
    file=open(path+fbxguid+"\\asset.meta","w")
    fbxmeta="""fileFormatVersion: 2
guid: """+fbxguid+"""
ModelImporter:
  serializedVersion: 20300
  internalIDToNameTable: []
  externalObjects: {}
  materials:
    materialImportMode: 2
    materialName: 0
    materialSearch: 1
    materialLocation: 1
  animations:
    legacyGenerateAnimations: 4
    bakeSimulation: 0
    resampleCurves: 1
    optimizeGameObjects: 0
    motionNodeName: 
    rigImportErrors: 
    rigImportWarnings: 
    animationImportErrors: 
    animationImportWarnings: 
    animationRetargetingWarnings: 
    animationDoRetargetingWarnings: 0
    animationCompression: 1
    animationRotationError: 0.5
    animationPositionError: 0.5
    animationScaleError: 0.5
    animationWrapMode: 0
    extraExposedTransformPaths: []
    extraUserProperties: []
    clipAnimations: []
    isReadable: 0
  meshes:
    lODScreenPercentages: []
    globalScale: 1
    meshCompression: 0
    addColliders: 0
    importVisibility: 1
    importBlendShapes: 1
    importCameras: 1
    importLights: 1
    fileIdsGeneration: 2
    swapUVChannels: 0
    generateSecondaryUV: 0
    useFileUnits: 1
    optimizeMeshForGPU: 1
    keepQuads: 0
    weldVertices: 1
    secondaryUVAngleDistortion: 8
    secondaryUVAreaDistortion: 15.000001
    secondaryUVHardAngle: 88
    secondaryUVPackMargin: 4
    useFileScale: 1
  tangentSpace:
    normalSmoothAngle: 60
    normalImportMode: 0
    tangentImportMode: 3
    normalCalculationMode: 4
  importAnimation: 1
  copyAvatar: 0
  humanDescription:
    serializedVersion: 2
    human: []
    skeleton: []
    armTwist: 0.5
    foreArmTwist: 0.5
    upperLegTwist: 0.5
    legTwist: 0.5
    armStretch: 0.05
    legStretch: 0.05
    feetSpacing: 0
    rootMotionBoneName: 
    rootMotionBoneRotation: {x: 0, y: 0, z: 0, w: 1}
    hasTranslationDoF: 0
    hasExtraRoot: 0
    skeletonHasParents: 1
  lastHumanDescriptionAvatarSource: {instanceID: 0}
  animationType: 0
  humanoidOversampling: 1
  additionalBone: 0
  userData: 
  assetBundleName: 
  assetBundleVariant: """
    file.write(fbxmeta)
  
    file=open(path+fbxguid+"\\pathname","w")
    file.write("Assets/"+assetname+"/"+assetname+".fbx")


    cfgs = {\
            "path_met":path+metguid+"\\asset",\
            "path_al":path+alguid+"\\asset",\
            "path_nor":path+norguid+"\\asset",\
            "guid_prefab":prefabguid,\
            "guid_script":scriptguid,\
            "guid_fbx":fbxguid,\
            "guid_mat":matguid,\
            "path_root":path,\
            }
    
    bpy.data.objects[assetname].select_set(True)
    cfgs = mainPBRConvert(context, cfgs)

    #export normalmap
    normalnode=True
    #bpy.data.objects[assetname].select = True
    bpy.data.objects[assetname].select_set(True)
    #  ob = bpy.data.objects[assetname]
    #  imagename=""
    #  if ob.type=='MESH':
        #  me=ob.data
        #  #  for slot in me.materials:
        #  # TODO: multiple materials
        #  slot = me.materials[0]
        #  #  dif=slot.node_tree.nodes['Principled BSDF']
        #  result = retrieve_image('Normal', slot, None)
        #  if result == None:
            #  normalnode=None
        #  else:
            #  image = result
            #  imagename = image.name

    if normalnode:
        #  if not os.path.exists(path+norguid):
            #  os.makedirs(path+norguid)

        #  image = bpy.data.images[imagename]
        height=cfgs['h_normal']
        #  height=image.size[1]
        #  width=image.size[0]
        #  imgpath=bpy.path.abspath(image.filepath_raw)
        #  print(imgpath)
        #  copyfile(imgpath,path+norguid+"\\asset")

        normeta="""fileFormatVersion: 2
guid: """+norguid+"""
timeCreated: 1505499899
licenseType: Free
TextureImporter:
  fileIDToRecycleName: {}
  serializedVersion: 4
  mipmaps:
    mipMapMode: 0
    enableMipMap: 1
    sRGBTexture: 0
    linearTexture: 0
    fadeOut: 0
    borderMipMap: 0
    mipMapsPreserveCoverage: 0
    alphaTestReferenceValue: 0.5
    mipMapFadeDistanceStart: 1
    mipMapFadeDistanceEnd: 3
  bumpmap:
    convertToNormalMap: 0
    externalNormalMap: 0
    heightScale: 0.25
    normalMapFilter: 0
  isReadable: 0
  grayScaleToAlpha: 0
  generateCubemap: 6
  cubemapConvolution: 0
  seamlessCubemap: 0
  textureFormat: 1
  maxTextureSize: """+str(height)+"""
  textureSettings:
    serializedVersion: 2
    filterMode: -1
    aniso: -1
    mipBias: -1
    wrapU: -1
    wrapV: -1
    wrapW: -1
  nPOTScale: 1
  lightmap: 0
  compressionQuality: 50
  spriteMode: 0
  spriteExtrude: 1
  spriteMeshType: 1
  alignment: 0
  spritePivot: {x: 0.5, y: 0.5}
  spriteBorder: {x: 0, y: 0, z: 0, w: 0}
  spritePixelsToUnits: 100
  alphaUsage: 1
  alphaIsTransparency: 0
  spriteTessellationDetail: -1
  textureType: 1
  textureShape: 1
  maxTextureSizeSet: 0
  compressionQualitySet: 0
  textureFormatSet: 0
  platformSettings:
  - buildTarget: DefaultTexturePlatform
    maxTextureSize: """+str(height)+"""
    textureFormat: -1
    textureCompression: 1
    compressionQuality: 50
    crunchedCompression: 0
    allowsAlphaSplitting: 0
    overridden: 0
  - buildTarget: Standalone
    maxTextureSize: """+str(height)+"""
    textureFormat: -1
    textureCompression: 1
    compressionQuality: 50
    crunchedCompression: 0
    allowsAlphaSplitting: 0
    overridden: 0
  spriteSheet:
    serializedVersion: 2
    sprites: []
    outline: []
    physicsShape: []
  spritePackingTag:
  userData:
  assetBundleName:
  assetBundleVariant:
    """
        #  file=open(path+norguid+"\\asset.meta","w")
        #  file.write(normeta)

        #  file=open(path+norguid+"\\pathname","w")
        #  file.write("Assets/"+assetname+"/"+assetname+"_Normal."+context.scene.my_enum2)

        prepare_upack_asset(path, norguid,  assetname, assetname+"_Normal."+context.scene.my_enum2, None, normeta)
    
    
    
    
    #export metallic
    
        
       
    #  ob = bpy.data.objects[assetname]
    #  imagename=""
    metalnode=True
    #  if ob.type=='MESH':
        #  me=ob.data
        #  for slot in me.materials:
            #  result = extract_map(slot, 6)
            #  if result[0] == None:
                #  metalnode=None
            #  else:
                #  image = result[0]
                #  imagename = image.name
                #  newname = slot.name
            #  dif=slot.node_tree.nodes['Principled BSDF']
            #  socket=dif.inputs[4]
            #  print(socket.name)
            #  try:
                #  link=next(link for link in slot.node_tree.links if link.to_node==dif and link.to_socket == socket)
                #  imageNode = link.from_node #The node this link is coming from
                #  print(imageNode.name)

                #  if imageNode.type == 'TEX_IMAGE': #Check if it is an image texture node

                    #  image = imageNode.image #Get the image
                    #  imagename=image.name
                    #  print( "result", image.name, image.filepath )
                    #  newname=slot.name
                #  else:
                    #  link=next(link for link in slot.node_tree.links if link.to_node==imageNode)
                    #  imageNode = link.from_node #The node this link is coming from
                    #  print(imageNode.name)

                    #  if imageNode.type == 'TEX_IMAGE': #Check if it is an image texture node

                        #  image = imageNode.image #Get the image
                        #  imagename=image.name
                        #  print( "result", image.name, image.filepath )
                        #  newname=slot.name


            #  except:
                #  print( "no link for metallic" )
                #  metalnode=None

    # submesh hash is hash from a 'MeshName_MeshPartX', X is the index of mesh
    if metalnode:                
        if not os.path.exists(path+metguid):
            os.makedirs(path+metguid)                
                        
        if context.scene.my_enum=="SECOND":
            bpy.data.objects[assetname].select_set(True)
            bpy.context.view_layer.objects.active=bpy.data.objects[assetname]


        height = cfgs.get('h_metal')
        if height == None:
            height = cfgs.get('h_albedo')
        
        #  print(imagename)


        #  image = bpy.data.images[imagename]
        #  height=image.size[1]
        #  width=image.size[0]
        #  imgpath=bpy.path.abspath(image.filepath_raw)
        #  print(imgpath)
        #  if context.scene.my_enum=="FIRST":
            #  copyfile(imgpath,path+metguid+"\\asset")
            
            
            
            
            
         
        metmeta="""fileFormatVersion: 2
guid: """+metguid+"""
timeCreated: 1505499900
licenseType: Free
TextureImporter:
  fileIDToRecycleName: {}
  serializedVersion: 4
  mipmaps:
    mipMapMode: 0
    enableMipMap: 1
    sRGBTexture: 0
    linearTexture: 1
    fadeOut: 0
    borderMipMap: 0
    mipMapsPreserveCoverage: 0
    alphaTestReferenceValue: 0.5
    mipMapFadeDistanceStart: 1
    mipMapFadeDistanceEnd: 3
  bumpmap:
    convertToNormalMap: 0
    externalNormalMap: 0
    heightScale: 0.25
    normalMapFilter: 0
  isReadable: 0
  grayScaleToAlpha: 0
  generateCubemap: 6
  cubemapConvolution: 0
  seamlessCubemap: 0
  textureFormat: 1
  maxTextureSize: """+str(height)+"""
  textureSettings:
    serializedVersion: 2
    filterMode: -1
    aniso: -1
    mipBias: -1
    wrapU: -1
    wrapV: -1
    wrapW: -1
  nPOTScale: 1
  lightmap: 0
  compressionQuality: 50
  spriteMode: 0
  spriteExtrude: 1
  spriteMeshType: 1
  alignment: 0
  spritePivot: {x: 0.5, y: 0.5}
  spriteBorder: {x: 0, y: 0, z: 0, w: 0}
  spritePixelsToUnits: 100
  alphaUsage: 1
  alphaIsTransparency: 0
  spriteTessellationDetail: -1
  textureType: 0
  textureShape: 1
  maxTextureSizeSet: 0
  compressionQualitySet: 0
  textureFormatSet: 0
  platformSettings:
  - buildTarget: DefaultTexturePlatform
    maxTextureSize: """+str(height)+"""
    textureFormat: -1
    textureCompression: 1
    compressionQuality: 50
    crunchedCompression: 0
    allowsAlphaSplitting: 0
    overridden: 0
  spriteSheet:
    serializedVersion: 2
    sprites: []
    outline: []
    physicsShape: []
  spritePackingTag: 
  userData: 
  assetBundleName: 
  assetBundleVariant: 
    """   
            
        #  file=open(path+metguid+"\\asset.meta","w")
        #  file.write(metmeta)

        #  file=open(path+metguid+"\\pathname","w")
        #  file.write("Assets/"+assetname+"/"+assetname+"_Metallic."+context.scene.my_enum2)
    
        prepare_upack_asset(path, metguid, assetname, assetname+"_Metallic."+context.scene.my_enum2, None, metmeta)
    
    
    
    #export albedo
    
        
       
    #  ob = bpy.data.objects[assetname]
    #  imagename=""
    alnode=True
    #  if ob.type=='MESH':
        #  me=ob.data
        #  for slot in me.materials:
            #  result = extract_map(slot, 0)
            #  if result[0] == None:
                #  alnode=None
            #  else:
                #  image = result[0]
                #  imagename = image.name
                #  newname=slot.name
            #  dif=slot.node_tree.nodes['Principled BSDF']
            #  socket=dif.inputs[0]
            #  print(socket.name)
            #  try:
                #  link=next(link for link in slot.node_tree.links if link.to_node==dif and link.to_socket == socket)
                #  imageNode = link.from_node #The node this link is coming from
                #  print(imageNode.name)

                #  if imageNode.type == 'TEX_IMAGE': #Check if it is an image texture node

                    #  image = imageNode.image #Get the image
                    #  imagename=image.name
                    #  print( "result", image.name, image.filepath )
                    #  newname=slot.name
                #  else:
                    #  link=next(link for link in slot.node_tree.links if link.to_node==imageNode)
                    #  imageNode = link.from_node #The node this link is coming from
                    #  print(imageNode.name)

                    #  if imageNode.type == 'TEX_IMAGE': #Check if it is an image texture node

                        #  image = imageNode.image #Get the image
                        #  imagename=image.name
                        #  print( "result", image.name, image.filepath )
                        #  newname=slot.name
                        
                                        
            #  except:
                #  print( "no link for albedo" )
                #  alnode=None
    if alnode:             
        #  if not os.path.exists(path+alguid):
            #  os.makedirs(path+alguid)
        #  if context.scene.my_enum=="FIRST":
            #  bpy.data.objects[assetname].select_set(True)
            #  bpy.context.view_layer.objects.active=bpy.data.objects[assetname]
            #  mainPBRConvert(context, path+alguid+"\\asset")
        
        #  print(imagename)
        height = cfgs.get('h_albedo')
        if height == None:
            height = cfgs.get('h_metal')

                  
        #  image = bpy.data.images[imagename]
        #  height=image.size[1]
        #  width=image.size[0]
        #  imgpath=bpy.path.abspath(image.filepath_raw)
        #  print(imgpath)
        #  if context.scene.my_enum=="SECOND":
            #  copyfile(imgpath,path+alguid+"\\asset")
            
        almeta="""fileFormatVersion: 2
guid: """+alguid+"""
timeCreated: 1505499902
licenseType: Free
TextureImporter:
  fileIDToRecycleName: {}
  serializedVersion: 4
  mipmaps:
    mipMapMode: 0
    enableMipMap: 1
    sRGBTexture: 1
    linearTexture: 0
    fadeOut: 0
    borderMipMap: 0
    mipMapsPreserveCoverage: 0
    alphaTestReferenceValue: 0.5
    mipMapFadeDistanceStart: 1
    mipMapFadeDistanceEnd: 3
  bumpmap:
    convertToNormalMap: 0
    externalNormalMap: 0
    heightScale: 0.25
    normalMapFilter: 0
  isReadable: 0
  grayScaleToAlpha: 0
  generateCubemap: 6
  cubemapConvolution: 0
  seamlessCubemap: 0
  textureFormat: 1
  maxTextureSize: """+str(height)+"""
  textureSettings:
    serializedVersion: 2
    filterMode: -1
    aniso: -1
    mipBias: -1
    wrapU: -1
    wrapV: -1
    wrapW: -1
  nPOTScale: 1
  lightmap: 0
  compressionQuality: 50
  spriteMode: 0
  spriteExtrude: 1
  spriteMeshType: 1
  alignment: 0
  spritePivot: {x: 0.5, y: 0.5}
  spriteBorder: {x: 0, y: 0, z: 0, w: 0}
  spritePixelsToUnits: 100
  alphaUsage: 1
  alphaIsTransparency: 0
  spriteTessellationDetail: -1
  textureType: 0
  textureShape: 1
  maxTextureSizeSet: 0
  compressionQualitySet: 0
  textureFormatSet: 0
  platformSettings:
  - buildTarget: DefaultTexturePlatform
    maxTextureSize: """+str(height)+"""
    textureFormat: -1
    textureCompression: 1
    compressionQuality: 50
    crunchedCompression: 0
    allowsAlphaSplitting: 0
    overridden: 0
  spriteSheet:
    serializedVersion: 2
    sprites: []
    outline: []
    physicsShape: []
  spritePackingTag: 
  userData: 
  assetBundleName: 
  assetBundleVariant: 
     
    """        
        
        #  file=open(path+alguid+"\\asset.meta","w")
        #  file.write(almeta)

        #  file=open(path+alguid+"\\pathname","w")
        #  file.write("Assets/"+assetname+"/"+assetname+"_Albedo."+context.scene.my_enum2)
        
        prepare_upack_asset(path, alguid, assetname, assetname+"_Albedo."+context.scene.my_enum2, None, almeta)

    #export material
    #  if not os.path.exists(path+matguid):
        #  os.makedirs(path+matguid)
    #  file=open(path+matguid+"\\pathname","w")
    #  file.write("Assets/"+assetname+"/Materials/Material.mat")
    #  file.write("Assets/"+assetname+"/"+assetname+"_Metallic."+context.scene.my_enum2)
        
    matmeta="""fileFormatVersion: 2
guid: """+matguid+"""
timeCreated: 1505559282
licenseType: Free
NativeFormatImporter:
  mainObjectFileID: 2100000
  userData: 
  assetBundleName: 
  assetBundleVariant: 
"""    

    #  file=open(path+matguid+"\\asset.meta","w")
    #  file.write(matmeta)
    
    sm=1
    
    
    smoothness=""
    if context.scene.my_enum=="FIRST":
        smoothness="""SMOOTHNESS_TEXTURE_METALLIC_CHANNEL_A _METALLICGLOSSMAP _NORMALMAP
    _SMOOTHNESS_TEXTURE_ALBEDO_CHANNEL_A"""
    if context.scene.my_enum=="SECOND":
        sm=0
        smoothness="""SMOOTHNESS_TEXTURE_METALLIC_CHANNEL_A _METALLICGLOSSMAP _NORMALMAP"""    
    
    normalstr="{x: 1, y: 1}"
    metalstr="{x: 1, y: 1}"
    alstr="{x: 1, y: 1}"
    
    #  if normalnode:
    normalstr="{fileID: 2800000, guid: "+norguid+", type: 3}"
    if metalnode:
        metalstr="{fileID: 2800000, guid: "+metguid+", type: 3}"
    if alnode:
        alstr="{fileID: 2800000, guid: "+alguid+", type: 3}"    
    
    matasset="""%YAML 1.1
%TAG !u! tag:unity3d.com,2011:
--- !u!21 &2100000
Material:
  serializedVersion: 6
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {fileID: 0}
  m_PrefabParentObject: {fileID: 0}
  m_PrefabInternal: {fileID: 0}
  m_Name: Material
  m_Shader: {fileID: 46, guid: 0000000000000000f000000000000000, type: 0}
  m_ShaderKeywords: """+smoothness+"""
  m_LightmapFlags: 4
  m_EnableInstancingVariants: 0
  m_DoubleSidedGI: 0
  m_CustomRenderQueue: 2000
  stringTagMap:
    RenderType: Opaque
  disabledShaderPasses: []
  m_SavedProperties:
    serializedVersion: 3
    m_TexEnvs:
    - _BaseMap:
        m_Texture: """+alstr+"""
        m_Scale: {x: 1, y: 1}
        m_Offset: {x: 0, y: 0}
    - _BumpMap:
        m_Texture: """+normalstr+"""
        m_Scale: {x: 1, y: 1}
        m_Offset: {x: 0, y: 0}
    - _DetailAlbedoMap:
        m_Texture: {fileID: 0}
        m_Scale: {x: 1, y: 1}
        m_Offset: {x: 0, y: 0}
    - _DetailMask:
        m_Texture: {fileID: 0}
        m_Scale: {x: 1, y: 1}
        m_Offset: {x: 0, y: 0}
    - _DetailNormalMap:
        m_Texture: {fileID: 0}
        m_Scale: {x: 1, y: 1}
        m_Offset: {x: 0, y: 0}
    - _EmissionMap:
        m_Texture: {fileID: 0}
        m_Scale: {x: 1, y: 1}
        m_Offset: {x: 0, y: 0}
    - _MainTex:
        m_Texture: """+alstr+"""
        m_Scale: {x: 1, y: 1}
        m_Offset: {x: 0, y: 0}
    - _MetallicGlossMap:
        m_Texture: """+metalstr+"""
        m_Scale: {x: 1, y: 1}
        m_Offset: {x: 0, y: 0}
    - _OcclusionMap:
        m_Texture: {fileID: 0}
        m_Scale: {x: 1, y: 1}
        m_Offset: {x: 0, y: 0}
    - _ParallaxMap:
        m_Texture: {fileID: 0}
        m_Scale: {x: 1, y: 1}
        m_Offset: {x: 0, y: 0}
    m_Floats:
    - _AlphaClip: 0
    - _Blend: 0
    - _BumpScale: 1
    - _Cull: 2
    - _Cutoff: 0.5
    - _DetailNormalMapScale: 1
    - _DstBlend: 0
    - _GlossMapScale: 1
    - _Glossiness: 0
    - _GlossyReflections: 1
    - _Metallic: 0
    - _Mode: 0
    - _OcclusionStrength: 1
    - _Parallax: 0.02
    - _SmoothnessTextureChannel: """+str(sm)+"""
    - _SpecularHighlights: 1
    - _SrcBlend: 1
    - _Surface: 0
    - _UVSec: 0
    - _WorkflowMode: 1
    - _ZWrite: 1
    m_Colors:
    - _BaseColor: {r: 1, g: 1, b: 1, a: 1}
    - _Color: {r: 1, g: 1, b: 1, a: 1}
    - _EmissionColor: {r: 0, g: 0, b: 0, a: 1}
    - _SpecColor: {r: 0.19999996, g: 0.19999996, b: 0.19999996, a: 1}
"""
    
    #  file=open(path+matguid+"\\asset","w")
    #  file.write(matasset)

    #  file.write("Assets/"+assetname+"/Materials/Material.mat")
    prepare_upack_asset(path, matguid, assetname, "Material.mat", matasset, matmeta)
    
    #folder1
    
    #  if not os.path.exists(path+fol1guid):
        #  os.makedirs(path+fol1guid)
    #  file=open(path+fol1guid+"\\pathname","w")
    #  file.write("Assets/"+assetname)
    
    fol1asset="""fileFormatVersion: 2
guid: """+fol1guid+"""
folderAsset: yes
timeCreated: 1505557484
licenseType: Free
DefaultImporter:
  userData: 
  assetBundleName: 
  assetBundleVariant: 
"""
    #  file=open(path+fol1guid+"\\asset.meta","w")
    #  file.write(fol1asset)

    prepare_upack_asset(path, fol1guid, "", assetname, None, fol1asset)
    
     #folder2
    
    #  if not os.path.exists(path+fol2guid):
        #  os.makedirs(path+fol2guid)
    #  file=open(path+fol2guid+"\\pathname","w")
    #  file.write("Assets/"+assetname+"/Materials")

    #  fol2asset="""fileFormatVersion: 2
#  guid: """+fol2guid+"""
#  folderAsset: yes
#  timeCreated: 1505557484
#  licenseType: Free
#  DefaultImporter:
  #  userData:
  #  assetBundleName:
  #  assetBundleVariant:
#  """
    #  file=open(path+fol2guid+"\\asset.meta","w")
    #  file.write(fol2asset)
    file.close()
    
    # pack
    output=context.scene.my_string_prop+assetname+".unitypackage"
    dir=path     
    make_tarfile(output, dir)       

    
    # clear tmp files
    try:
        rmtree(path)
    except:
        print("WARNING: fail to rm tmp folder, check if folder is used by other process")



# create asset for unitypackage
def prepare_upack_asset(path, guid, folder_name, asset_name, content, meta):
    if not os.path.exists(path+guid):
        os.makedirs(path+guid)
              
    #  image = bpy.data.images[imagename]
    #  height=image.size[1]
    #  width=image.size[0]
    #  asset_path=bpy.path.abspath(content.filepath_raw)
    #  print(imgpath)
    if content:
        file=open(path+guid+"\\asset","w")
        file.write(content)

    file=open(path+guid+"\\asset.meta","w")
    file.write(meta)
    
    file=open(path+guid+"\\pathname","w")
    file.write("Assets/"+folder_name+"/"+asset_name)
    pass


# retrieve image using socket name and target material
# try to find TEX_IMAGE type node recursively from the given input socket from princpled BSDF node
# only support principled BSDF
def retrieve_image(socket_name, material, cfg, failsafe = 5):
    dif = material.node_tree.nodes['Principled BSDF']
    socket = dif.inputs[socket_name]
    img = None
    try:
        link = next(link for link in material.node_tree.links if link.to_node == dif and link.to_socket == socket)
        img_node = link.from_node
        skt = link.from_socket
        while img_node.type != 'TEX_IMAGE' and failsafe > 0:
            # try find color channel for data
            # use match case in python3.10 or higher version
            if img_node.type == 'SEPARATE_COLOR' and cfg != None:
                if socket_name == 'Roughness':
                    cfg['rough_from_channel'] = img_node.outputs.find(skt.name)
                    print("roughness data is from channel " + skt.name) 
                elif socket_name == 'Metallic':
                    cfg['metal_from_channel'] = img_node.outputs.find(skt.name)
                    print("metallic data is from channel " + skt.name) 
            img_node = next(ipt for ipt in img_node.inputs if ipt.links).links[0].from_node
            failsafe-=1;
        if img_node.type == 'TEX_IMAGE':
            img = img_node.image
    except:
        print( "fail to retrieve image from material {}, using socket {}".format(material.name, socket) )
    return img

def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:bz2") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

def checknode(index):
    ob = bpy.context.object
    if ob.type=='MESH':
        me=ob.data
        #  mat_offset=len(me.materials)
        for slot in me.materials:
            dif = slot.node_tree.nodes['Principled BSDF']
            socket2=dif.inputs[index]


def mainPBRConvert(context, cfgs, mapsonly = False):
    cfgs['rough_from_channel'] = 0
    cfgs['metal_from_channel'] = 0
    if not os.path.exists(context.scene.my_string_prop):
        os.makedirs(context.scene.my_string_prop)
    
    #  if path_metal=="thisisnotunityexport" or path_albedo=="thisisnotunityexport":
        #  mapsonly=True
        
        
    path_albedo = cfgs['path_al']
    path_normal = cfgs['path_nor']
    path_metal = cfgs['path_met']
    if mapsonly:    
        print("============ START =============== maps only")
    else:
        print("============ START =============== unitypackage export")    
    #  path=path
    #  mapnames=['Albedo','Subsurface','Subsurface_Radius','Subsurface_Color','Metallic','Specular','Speular_Tint','Rooughness','Anisotropic','Anisotropic_Rotation','Sheen','Sheen_Tint','Clearcoat','Clearcoat_Roughness','IOR','Transmission','Unknown','Normal','Clearcoat_Normal','Tangent']
        
    mapstoexpo=[]


    # albedo always needed anyhow
    mapstoexpo.append('Base Color')
    if context.scene.my_boolme:
        mapstoexpo.append('Metallic')  # blender 3.x metallic idx from 4->6
    if context.scene.my_boolno:
        mapstoexpo.append('Normal') # blender 3.x normal idx from 17->22
    
    #  if context.scene.my_enum=="SECOND" and context.scene.my_boolal:
        #  mapstoexpo.append('Base Color')
    #  #  if context.scene.my_enum=="FIRST" and context.scene.my_boolme:
    #  if context.scene.my_boolme:
        #  mapstoexpo.append('Metallic')  # blender 3.x metallic idx from 4->6
    #  if context.scene.my_boolno:
        #  mapstoexpo.append('Normal') # blender 3.x normal idx from 17->22
        #  mapstoexpo.append(22) # blender 3.x normal idx from 17->22
    
    roughnode=True
    resultname=""
    newname=""
    imagename=""

    roughimagename=""
    #  def mean(numbers):
        #  return float(sum(numbers)) / max(len(numbers), 1)
    ob = bpy.context.object
    nodes = 0

    # flags
    bake_rough_to_albedo_a = context.scene.my_enum=="FIRST" and context.scene.my_boolal
    bake_rough_to_metallic_a = context.scene.my_enum=="SECOND" and context.scene.my_boolme

    # find albedo / metallic map due to user choice
    # find roughness map and bake it into albedo / metallic map
    if ob.type=='MESH':
        me=ob.data
        #  mat_offset=len(me.materials)
        # TODO: multiple materials
        slot = me.materials[0]
        #  for slot in me.materials:
            
        dif = slot.node_tree.nodes['Principled BSDF']
        #  socket2=dif.inputs[9] # roughness idx

        # flag for confirming the roughness baking is viable
        nodes=0
        
        socket_name=None
        if bake_rough_to_albedo_a:
            #  socket = dif.inputs[0]
            print("Converting Roughness to Albedo alpha")
            socket_name="Base Color"
        elif bake_rough_to_metallic_a:
            #  socket=dif.inputs[6]
            print("Converting Roughness to Metallic alpha")
            socket_name="Metallic"        

        # find albedo / metallic map and waiting for fill roughness(smoothness) to alpha channel
        image = retrieve_image(socket_name, slot, cfgs)
        if image != None:
            imagename = image.name
            newname = slot.name
            print( "albedo or metallic map for alpha channel injection found" )
        else:
            print( "no link for base color / metallic" )
            nodes=nodes+1

        #  try:
            #  link=next(link for link in slot.node_tree.links if link.to_node==dif and link.to_socket == socket)
            #  imageNode = link.from_node #The node this link is coming from

            #  failsafe = 5
            #  while imageNode.type != 'TEX_IMAGE' and failsafe > 0:
                #  imageNode = next(ipt for ipt in imageNode.inputs if ipt.links).links[0].from_node
                #  failsafe-=1;
            #  if imageNode.type == 'TEX_IMAGE': #Check if it is an image texture node
                #  image = imageNode.image #Get the image
                #  imagename=image.name
                #  print( "result", image.name, image.filepath )
                #  newname=slot.name
            #  print( "albedo or metallic map for alpha channel injection found" )
        #  except:
            #  print( "no link for base color" )
            #  nodes=nodes+1
        #  find roughtness map
        img_rough = retrieve_image('Roughness', slot, cfgs)
        if img_rough != None:
            roughimagename = img_rough.name
            print( "roughness map found" )
        else:
            print( "no link for roughness" )
            nodes=nodes+1
            roughnode=None

        #  try:
            #  link=next(link for link in slot.node_tree.links if link.to_node==dif and link.to_socket == socket2)
            #  imageNode = link.from_node #The node this link is coming from
            #  #  print("imageNode name is " + imageNode.name)
            #  failsafe = 5
            #  skt=link.from_socket
            #  while imageNode.type != 'TEX_IMAGE' and failsafe > 0:
                #  #  print(imageNode.label + "->" + nextnode)
                #  if imageNode.type == 'SEPARATE_COLOR':
                    #  rough_from_channel = imageNode.outputs.find(skt.name)
                    #  print("roughness data is from channel " + skt.name)
                #  imageNode = next(ipt for ipt in imageNode.inputs if ipt.links).links[0].from_node
                #  # check if color data is been seperated for roughness
                #  failsafe-=1;
            #  if imageNode.type == 'TEX_IMAGE': #Check if it is an image texture node
                #  image = imageNode.image #Get the image
                #  roughimagename=image.name
                #  print( "result", roughimagename, image.filepath )
            #  print( "roughness map found" )
        #  except:
            #  print( "no link for roughness" )
            #  nodes=nodes+1
            #  roughnode=None

    # only works when both target map and roughtness map are valid
    if nodes<2 and roughnode:
        imageold = bpy.data.images[imagename]  
        print("name of image which to inject: " + imagename)
        rough_img=bpy.data.images[roughimagename]
        width = imageold.size[0]
        height = imageold.size[1]
        print("size of image whitch to inject: " + str(height))
        bpy.ops.image.new(name="PBR_Diff", width=width, height=height)
        image = bpy.data.images['PBR_Diff']  
        index=0
        Alpha_list=list(rough_img.pixels)
        #  Alpha_list_new=[]
        RGBA_list = list(imageold.pixels)
        RGBA_list_new=[]
        for i in RGBA_list:    
            RGBA_list_new.append(i)
        index=0    
        rough_from_channel = cfgs['rough_from_channel']
        print("copying pixels from " + CHANNELS[rough_from_channel] + " to alpha channel of target texture...")
        for i in RGBA_list_new:
            if index%4==0:
                # find specific channel
                clr = abs(Alpha_list[index+rough_from_channel]-1)
                #  r=abs(Alpha_list[index]-1)
                #  g=abs(Alpha_list[index+1]-1)
                #  b=abs(Alpha_list[index+2]-1)
                #  al=mean([r,g,b])
                al=clr
                RGBA_list_new[index+3]=al
                #  print(str(RGBA_list_new[index+3]))
            index=index+1
        image.pixels=RGBA_list_new
        
        filetp=""
        if context.scene.my_enum2=="PNG":
            filetp='png'
        else:
            filetp='tga'
        if mapsonly:
            if bake_rough_to_albedo_a:
                path_albedo=context.scene.my_string_prop+newname+"_"+resultname+"."+filetp    
            elif bake_rough_to_metallic_a:
                path_metal=context.scene.my_string_prop+newname+"_"+resultname+"."+filetp    
        path=""
        if bake_rough_to_albedo_a:
            path = path_albedo
        elif bake_rough_to_metallic_a:
            path = path_metal
        image.filepath_raw = path
        image.file_format = context.scene.my_enum2            
        image.save()
        print("save injected albedo/metallic map to " + path)
        # do not clear bpy.data.images['PBR_Diff'] yet for possible usage later
        #  image.user_clear()
        #  bpy.data.images.remove(image)
            
        
        #  else:
            #  imageold = bpy.data.images[imagename]
            #  width = imageold.size[0]
            #  height = imageold.size[1]
            #  bpy.ops.image.new(name="PBR_Diff", width=width, height=height)
            #  RGBA_list = list(imageold.pixels)
            #  image = bpy.data.images['PBR_Diff']
            #  image.pixels=RGBA_list
            #  filetp=""
            #  if context.scene.my_enum2=="PNG":
                #  filetp='png'
            #  else:
                #  filetp='tga'
            #  if mapsonly:
                #  if context.scene.my_enum=="FIRST" and context.scene.my_boolal:
                    #  path_albedo=context.scene.my_string_prop+newname+"_"+resultname+"."+filetp
                #  if context.scene.my_enum=="SECOND" and context.scene.my_boolme:
                    #  path_metal=context.scene.my_string_prop+newname+"_"+resultname+"."+filetp
            #  if context.scene.my_enum=="FIRST" and context.scene.my_boolal:
                #  image.filepath_raw = path_albedo
            #  if context.scene.my_enum=="SECOND" and context.scene.my_boolme:
                #  image.filepath_raw = path_metal
            #  image.file_format = context.scene.my_enum2
            #  image.save()

            #  path=""
            #  if context.scene.my_enum=="FIRST" and context.scene.my_boolal:
                #  path = path_albedo
            #  if context.scene.my_enum=="SECOND" and context.scene.my_boolme:
                #  path = path_metal
            #  print("(no rough map) save injected into albedo/metallic map as " + path)
            #  image.user_clear()
            #  bpy.data.images.remove(image)
            
    ob = bpy.context.object
    if ob.type=='MESH':
        me=ob.data
        #  mat_offset=len(me.materials)
        # TODO: multiple materials
        slot = me.materials[0]
        #  olddif = slot.node_tree.nodes['Principled BSDF']
        dif = slot.node_tree.nodes['Principled BSDF']        
        for m in mapstoexpo:
            istex=None
            print("Try fetching: "+ m + "...")
            #  if len(dif.inputs) < 26:
                #  print("dif name is " + dif.name)
            socket=dif.inputs[m]

            #  link=next(link for link in slot.node_tree.links if link.to_node==dif and link.to_socket == socket)
            #  imageNode = link.from_node
            if len(socket.links) == 0:
                print("no map for socket " + m)
                continue
            
            img = retrieve_image(m, slot, cfgs)
            if img != None:
                imagename = img.name
                newname = slot.name
                istex = True
            #  imageNode = socket.links[0].from_node
            #  skt = socket.links[0].from_socket
            #  failsafe = 15
            #  while failsafe > 0 and imageNode.type != 'TEX_IMAGE':
                #  # try check which channel did the color data comes from
                #  if m==6 and imageNode.type == 'SEPARATE_COLOR':
                    #  metal_from_channel = imageNode.outputs.find(skt.name)
                    #  print("metallic data is from channel " + skt.name)
                #  imageNode = next(ipt.links[0] for ipt in imageNode.inputs if ipt.links).from_node
                #  failsafe-=1

            #  if imageNode.type == 'TEX_IMAGE': #Check if it is an image texture node
                #  image = imageNode.image #Get the image
                #  imagename=image.name
                #  print( "result", image.name, image.filepath )
                #  newname=slot.name
                #  istex=True

            if istex:
                imageold = bpy.data.images[imagename]
                # if user choosed baking roughtness into A channel of metallic map
                # retrieve image from 'PBR_Diff'
                if (m == 'Metallic' and bake_rough_to_metallic_a) or (m == 'Base Color' and bake_rough_to_albedo_a):
                    imageold = bpy.data.images['PBR_Diff']
                    print("get incomplete map where roughtness baked")
                width = imageold.size[0]
                height = imageold.size[1]
                bpy.ops.image.new(name="Temporary_map_to_export", width=width, height=height)
                RGBA_list = list(imageold.pixels)            
                image = bpy.data.images['Temporary_map_to_export']
                # if user choosed baking roughtness into A channel of metallic map
                # then here we should make sure metallic R is valid
                # TODO: make mask map for HDRP
                metal_from_channel = cfgs['metal_from_channel']
                if m == 'Metallic' and metal_from_channel != 0 and context.scene.my_boolme:
                    RGBA_list_new=[]
                    for i in RGBA_list:    
                        RGBA_list_new.append(i)
                    index=0
                    print("copying pixels from channel " + CHANNELS[metal_from_channel] + " to R channel in metallic map...")
                    for i in RGBA_list:
                        if index%4==0:
                            # fill metallic data
                            RGBA_list_new[index+0]=RGBA_list[index+metal_from_channel]  # Metallic map for unity use r channel
                            RGBA_list_new[index+1]=RGBA_list[index+metal_from_channel]
                            RGBA_list_new[index+2]=RGBA_list[index+metal_from_channel]
                            # do not touch alpha channel for preventing overwrite smoothness
                            #  RGBA_list_new[index+3]=1.0  # alpha
                        index=index+1
                    image.pixels=RGBA_list_new
                else:
                    image.pixels=RGBA_list
                filetp=""
                if context.scene.my_enum2=="PNG":
                    filetp='png'
                else:
                    filetp='tga'
                   
                if mapsonly:
                    path=context.scene.my_string_prop+newname+"_"+m+"."+filetp
                else:
                    if m == 'Metallic':
                        path=path_metal
                        cfgs['h_metal'] = image.size[1]
                        cfgs['w_metal'] = image.size[0]
                        print("metal map size is " + str(image.size[1]))
                    elif m == 'Base Color':
                        cfgs['h_albedo'] = image.size[1]
                        cfgs['w_albedo'] = image.size[0]
                        print("albedo map size is " + str(image.size[1]))
                        path=path_albedo
                    elif m == 'Normal':
                        cfgs['h_normal'] = image.size[1]
                        cfgs['w_normal'] = image.size[0]
                        print("normal map size is " + str(image.size[1]))
                        path=path_normal
                    else:
                        path = ""
                        pass
                print("Exporting "+m + " as " + path)
                image.filepath_raw = path
                image.file_format = context.scene.my_enum2
                image.save()
                image.user_clear()
                bpy.data.images.remove(image)                         
                if bpy.data.images.get('PBR_Diff') != None and imageold == bpy.data.images['PBR_Diff']:
                    bpy.data.images.remove(imageold)                         
                    

    # prefabs
    prefabguid = cfgs['guid_prefab']
    scriptguid = cfgs['guid_script']
    path=cfgs['path_root']
    fbxguid=cfgs['guid_fbx']
    matguid=cfgs['guid_mat']
    assetname=bpy.context.selected_objects[0].name

    #  if not os.path.exists(path+prefabguid):
        #  os.makedirs(path+prefabguid)
    #  file=open(path+prefabguid+"\\pathname","w")
    #  file.write("Assets/"+assetname+"/" +assetname+ ".prefab")
        
    prefabmeta="""fileFormatVersion: 2
guid: """+prefabguid+"""
PrefabImporter:
  externalObjects: {}
  userData: 
  assetBundleName: 
  assetBundleVariant: 
"""    

    #  file=open(path+prefabguid+"\\asset.meta","w")
    #  file.write(prefabmeta)

    prefabasset="""%YAML 1.1
%TAG !u! tag:unity3d.com,2011:
--- !u!1 &6530883066055556866
GameObject:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {fileID: 0}
  m_PrefabInstance: {fileID: 0}
  m_PrefabAsset: {fileID: 0}
  serializedVersion: 6
  m_Component:
  - component: {fileID: 6530883066055713570}
  - component: {fileID: 6530883066056483586}
  - component: {fileID: 6530883066057482690}
  m_Layer: 0
  m_Name: """+assetname+"""
  m_TagString: Untagged
  m_Icon: {fileID: 0}
  m_NavMeshLayer: 0
  m_StaticEditorFlags: 0
  m_IsActive: 1
--- !u!4 &6530883066055713570
Transform:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {fileID: 0}
  m_PrefabInstance: {fileID: 0}
  m_PrefabAsset: {fileID: 0}
  m_GameObject: {fileID: 6530883066055556866}
  m_LocalRotation: {x: 0, y: 0, z: 0, w: 1}
  m_LocalPosition: {x: -0, y: 0, z: -0}
  m_LocalScale: {x: 1, y: 1.0000001, z: 1.0000001}
  m_Children: []
  m_Father: {fileID: 0}
  m_RootOrder: 0
  m_LocalEulerAnglesHint: {x: 0, y: 0, z: 0}
--- !u!33 &6530883066056483586
MeshFilter:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {fileID: 0}
  m_PrefabInstance: {fileID: 0}
  m_PrefabAsset: {fileID: 0}
  m_GameObject: {fileID: 6530883066055556866}
  m_Mesh: {fileID: 0, guid: """+fbxguid+""", type: 3}
--- !u!23 &6530883066057482690
MeshRenderer:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {fileID: 0}
  m_PrefabInstance: {fileID: 0}
  m_PrefabAsset: {fileID: 0}
  m_GameObject: {fileID: 6530883066055556866}
  m_Enabled: 1
  m_CastShadows: 1
  m_ReceiveShadows: 1
  m_DynamicOccludee: 1
  m_MotionVectors: 1
  m_LightProbeUsage: 1
  m_ReflectionProbeUsage: 1
  m_RayTracingMode: 2
  m_RayTraceProcedural: 0
  m_RenderingLayerMask: 1
  m_RendererPriority: 0
  m_Materials:
  - {fileID: 2100000, guid: """+ matguid +""", type: 2}
  m_StaticBatchInfo:
    firstSubMesh: 0
    subMeshCount: 0
  m_StaticBatchRoot: {fileID: 0}
  m_ProbeAnchor: {fileID: 0}
  m_LightProbeVolumeOverride: {fileID: 0}
  m_ScaleInLightmap: 1
  m_ReceiveGI: 1
  m_PreserveUVs: 0
  m_IgnoreNormalsForChartDetection: 0
  m_ImportantGI: 0
  m_StitchLightmapSeams: 1
  m_SelectedEditorRenderState: 3
  m_MinimumChartSize: 4
  m_AutoUVMaxDistance: 0.5
  m_AutoUVMaxAngle: 89
  m_LightmapParameters: {fileID: 0}
  m_SortingLayerID: 0
  m_SortingLayer: 0
  m_SortingOrder: 0
  m_AdditionalVertexStreams: {fileID: 0}
"""

    #  file=open(path+prefabguid+"\\asset","w")
    #  file.write(prefabasset)

    prepare_upack_asset(path, prefabguid, assetname, assetname+".prefab", prefabasset, prefabmeta)
    print("write prefab done") 

    #  if not os.path.exists(path+scriptguid):
        #  os.makedirs(path+scriptguid)
    #  file=open(path+scriptguid+"\\pathname","w")
    #  file.write("Assets/"+assetname+"/PrefabPostProcess.cs")

    # AssetPostprocessor script for prefab
    ppscript="""using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Rendering;
using UnityEditor;

public class PrefabPostProcess : AssetPostprocessor
{
    void OnPostprocessPrefab(GameObject g)
    {
        string fbx_path = assetPath.Replace(".prefab", ".fbx");
        GameObject fbxGo = AssetDatabase.LoadAssetAtPath<GameObject>(fbx_path);
        Mesh msh = fbxGo.GetComponentInChildren<MeshFilter>().sharedMesh;
        g.GetComponent<MeshFilter>().sharedMesh = msh;

        MeshRenderer mr = g.GetComponentInChildren<MeshRenderer>();
        Material m = mr.sharedMaterial;
        if(GraphicsSettings.currentRenderPipeline != null)
            mr.sharedMaterial.shader = GraphicsSettings.currentRenderPipeline.defaultShader;

        // clean up
        string scriptPath = this.assetPath.Substring(0, this.assetPath.LastIndexOf("/") + 1) + "/PrefabPostProcess.cs";
        AssetDatabase.DeleteAsset(scriptPath);
        AssetDatabase.ImportAsset(this.assetPath);
        AssetDatabase.Refresh(ImportAssetOptions.Default);
    }
}
    """
    #  file=open(path+scriptguid+"\\asset","w")
    #  file.write(ppscript)
    #  file.close()

    ppscriptmeta="""
fileFormatVersion: 2
guid: """+scriptguid+"""
MonoImporter:
  externalObjects: {}
  serializedVersion: 2
  defaultReferences: []
  executionOrder: 0
  icon: {instanceID: 0}
  userData: 
  assetBundleName: 
  assetBundleVariant: 
    """
    #  file=open(path+scriptguid+"\\asset.meta","w")
    #  file.write(ppscriptmeta)
    #  file.close()

    prepare_upack_asset(path, scriptguid, assetname, "/PrefabPostProcess.cs", ppscript, ppscriptmeta)

    print("write postprocess script done") 
    return cfgs


def mainmatuni(context):
    scene = bpy.context.scene

    def isclose(a, b, rel_tol=1e-09, abs_tol=context.scene.my_string_prop2):
        return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

    def replace_material(object,old_material,new_material):
        """
        replace a material in blender.
        params:
            object - object for which we are replacing the material
            old_material - The old material name as a string
            new_material - The new material name as a string
        """
        ob = object
        om = bpy.data.materials[old_material]
        nm = bpy.data.materials[new_material]
        # Iterate over the material slots and replace the material
        for s in ob.material_slots:
            if s.material.name == old_material:
                s.material = nm

    materialsmerged=0

    selected = bpy.context.selected_objects

    for obj in selected:
        #print(obj.name)
        if obj.type=='MESH':
            for slot in obj.data.materials:
                color_base=slot.diffuse_color
                for obj_match in selected:
                    if obj_match.type=='MESH':
                        for slot_match in obj_match.data.materials:
                            color_match=slot_match.diffuse_color
                            if isclose(color_base[0],color_match[0]):
                                if isclose(color_base[1],color_match[1]):
                                    if isclose(color_base[2],color_match[2]):
                                        if slot!=slot_match:
                                            print("match "+slot.name+" i simmilar to "+slot_match.name)
                                            replace_material(obj,slot.name,slot_match.name)
                                            materialsmerged+=1                                       

                                        
    print("merged "+str(materialsmerged)+" materials")

def mainexp(context, name):
    if not os.path.exists(context.scene.my_string_prop):
        os.makedirs(context.scene.my_string_prop)    
    selected = bpy.context.selected_objects
    lst = []
    for obj in selected:
        lst.append(obj.name)
        me = obj.data
        me.use_auto_smooth=True
        me.auto_smooth_angle=180
        me.name=obj.name

    if context.scene.my_bool:
        for str in lst:
            bpy.ops.object.select_all(action='DESELECT')
            bpy.data.objects[str].select_set(True)
            # bpy.data.objects[str].select = True            
            bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "constraint_axis":(False, False, False), "orient_matrix_type":'GLOBAL', "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
            
            if context.scene.my_bool2:
                
                bpy.ops.object.transform_apply(location = True, scale = True, rotation = True)
                bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')
                
                obj  = bpy.context.selected_objects[0]
                mesh = obj.data
                lowestv=mesh.vertices[0].co[2]
                #print(lowestv)
            
                for v in mesh.vertices:
                    #print(v.co[2])
                    if v.co[2]<lowestv:
                        lowestv=v.co[2]
                    
                print(lowestv)
            
                for v in mesh.vertices:
                    v.co[2]-=lowestv
            
            if name=="thisisnotunitypackage":
                bpy.ops.export_scene.fbx(filepath=context.scene.my_string_prop+str+".fbx", check_existing=True, filter_glob="*.fbx", use_selection=True, use_space_transform=False, bake_space_transform=True, global_scale=1.0, axis_forward='Z', axis_up='Y', object_types={'MESH'}, use_mesh_modifiers=False, mesh_smooth_type='EDGE', use_mesh_edges=False, use_armature_deform_only=False, bake_anim=True, bake_anim_use_all_actions=True, bake_anim_simplify_factor=1, path_mode='AUTO', batch_mode='OFF', use_batch_own_dir=True, use_metadata=True)
                #  bpy.ops.export_scene.fbx(filepath=context.scene.my_string_prop+str+".fbx", check_existing=True, filter_glob="*.fbx", use_selection=True, bake_space_transform=True, global_scale=1.0, axis_forward='-Z', axis_up='Y', object_types={'MESH'}, use_mesh_modifiers=False, mesh_smooth_type='EDGE', use_mesh_edges=False, use_armature_deform_only=False, bake_anim=True, bake_anim_use_all_action=True, use_default_take=True, use_anim_optimize=True, anim_optimize_precision=6.0, path_mode='AUTO', batch_mode='OFF', use_batch_own_dir=True, use_metadata=True)
            else:
                bpy.ops.export_scene.fbx(filepath=name, check_existing=True, filter_glob="*.fbx", use_selection=True, use_space_transform=False, bake_space_transform=True, global_scale=1.0, axis_forward='Z', axis_up='Y', object_types={'MESH'}, use_mesh_modifiers=False, mesh_smooth_type='EDGE', use_mesh_edges=False, use_armature_deform_only=False, bake_anim=True, bake_anim_use_all_actions=True, bake_anim_simplify_factor=1, path_mode='AUTO', batch_mode='OFF', use_batch_own_dir=True, use_metadata=True)
                #  bpy.ops.export_scene.fbx(filepath=name, check_existing=True, filter_glob="*.fbx", use_selection=True, bake_space_transform=True, global_scale=1.0, axis_forward='Z', axis_up='Y', object_types={'MESH'}, use_mesh_modifiers=False, mesh_smooth_type='EDGE', use_mesh_edges=False, use_armature_deform_only=False, use_anim=True, use_anim_action_all=True, use_default_take=True, use_anim_optimize=True, anim_optimize_precision=6.0, path_mode='AUTO', batch_mode='OFF', use_batch_own_dir=True, use_metadata=True)
            bpy.ops.object.delete(use_global=False)
    else:
        #str=bpy.context.selected_objects[0].name
        lst2=[]
        for str in lst:
            bpy.ops.object.select_all(action='DESELECT')
            bpy.data.objects[str].select_set(True)
            
            bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "constraint_axis":(False, False, False), "orient_matrix_type":'GLOBAL', "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
            if context.scene.my_bool2:
                bpy.ops.object.transform_apply(location = True, scale = True, rotation = True)
                bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')
                
                obj  = bpy.context.selected_objects[0]
                lst2.append(obj.name)
                mesh = obj.data
                lowestv=mesh.vertices[0].co[2]
                #print(lowestv)
            
                for v in mesh.vertices:
                    #print(v.co[2])
                    if v.co[2]<lowestv:
                        lowestv=v.co[2]
                    
                print(lowestv)
            
                for v in mesh.vertices:
                    v.co[2]-=lowestv
                
        for str in lst2:
            #print(str)        
            bpy.data.objects[str].select_set(True)
        
        nm=bpy.path.basename(bpy.context.blend_data.filepath)
        nm=nm[:nm.index(".blend")]
        print(nm)        
        bpy.ops.export_scene.fbx(filepath=name, check_existing=True, filter_glob="*.fbx", use_selection=True,use_space_transform=False, bake_space_transform=True, global_scale=1.0, axis_forward='Z', axis_up='Y', object_types={'MESH'}, use_mesh_modifiers=False, mesh_smooth_type='EDGE', use_mesh_edges=False, use_armature_deform_only=False, bake_anim=True, bake_anim_use_all_actions=True, bake_anim_step=1, bake_anim_simplify_factor=1, path_mode='AUTO', batch_mode='OFF', use_batch_own_dir=True, use_metadata=True)
        #  bpy.ops.export_scene.fbx(filepath=context.scene.my_string_prop+nm+".fbx", check_existing=True, filter_glob="*.fbx", use_selection=True, bake_space_transform=True, global_scale=1.0, axis_forward='-Z', axis_up='Y', object_types={'MESH'}, use_mesh_modifiers=False, mesh_smooth_type='EDGE', use_mesh_edges=False, use_armature_deform_only=False, bake_anim=True, bake_anim_use_all_actions=True, bake_anim_step=1, bake_anim_simplify_factor=1, path_mode='AUTO', batch_mode='OFF', use_batch_own_dir=True, use_metadata=True)
        bpy.ops.object.delete(use_global=False)

def mainconv(context):
    selected = bpy.context.selected_objects
    lst = []
    for obj in selected:
        lst.append(obj.name)
        me = obj.data
        me.use_auto_smooth=True
        me.auto_smooth_angle=180
        me.name=obj.name
    
    for str in lst:
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects[str].select = True  
        ob = bpy.context.object
        if ob.type=='MESH':
            me = ob.data
            mat_offset = len(me.materials)
            for slot in me.materials:
                slot.specular_intensity=0.05
                slot.diffuse_intensity=1
                slot.specular_hardness=10
                slot.use_nodes=False
                slot.diffuse_color=slot.node_tree.nodes["Diffuse BSDF"].inputs[0].default_value[0],slot.node_tree.nodes["Diffuse BSDF"].inputs[0].default_value[1],slot.node_tree.nodes["Diffuse BSDF"].inputs[0].default_value[2]

def maintrans(context):
    selected = bpy.context.selected_objects
    lst = []

    for obj in selected:
        lst.append(obj.name)
        me = obj.data    
        me.name=obj.name
        
        
    for str in lst:
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects[str].select = True
        bpy.ops.object.transform_apply(location = True, scale = True, rotation = True)
        bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')
        obj  = bpy.data.objects[str]
        mesh = obj.data
        lowestv=mesh.vertices[0].co[2]
        #print(lowestv)
        
        for v in mesh.vertices:
            #print(v.co[2])
            if v.co[2]<lowestv:
                lowestv=v.co[2]
                
        print(lowestv)
        
        for v in mesh.vertices:
            v.co[2]-=lowestv
    
class UnityTransform(bpy.types.Operator):
    """Correct object transformation. Apply location, rotation, scale an center pivot on lowest vertex"""
    bl_idname="cusops.unitytransform"
    bl_label="Correct transform"
    
    def execute(self,context):
        maintrans(context)
        return{'FINISHED'}
    
class UnityMatConv(bpy.types.Operator):
    """Convert Cycles materials to Internal materials (required when using the same materials in Unity)"""
    bl_idname="cusops.unitymatconv"
    bl_label="Convert materials"
    
    def execute(self,context):
        mainconv(context)
        return{'FINISHED'}
    
class UnityExport(bpy.types.Operator):
    """Export selected objects to FBX file/files"""
    bl_idname="cusops.unityexport"
    bl_label="Export to FBX"
    
    def execute(self,context):
        mainexp(context, "thisisnotunitypackage")
        return{'FINISHED'}
    
class AllExport(bpy.types.Operator):
    """Export as unitypackage"""
    bl_idname="cusops.allexport"
    bl_label="Export unitypackage"
    
    def execute(self,context):
        allexport(context)
        return{'FINISHED'}

class PBRConvert(bpy.types.Operator):
    """Convert PBR Roughness to Unity PBR Albedo_Smoothness. Required texture inputs in Roughness and Base Color or Metallic channels of Principled BSDF node"""
    bl_idname="cusops.pbrconvert"
    bl_label="Export texture set"
    
    def execute(self,context):
        mainPBRConvert(context, "thisisnotunityexport")
        return{'FINISHED'}               
    
class UnityMatMerge(bpy.types.Operator):
    """Merge similar materials. Use threshold to control similarity comparision"""
    bl_idname="cusops.unitymatmerge"
    bl_label="Unify materials"
    
    def execute(self,context):
        mainmatuni(context)
        return{'FINISHED'}            


    
class OpenBrowser(bpy.types.Operator):
        bl_idname = "open.browser"
        bl_label = "Choose export directory"

        filepath: bpy.props.StringProperty(name='filepath', subtype="FILE_PATH")
        #  filepath = ""
        #somewhere to remember the address of the file

        def execute(self, context):
            folpath=self.filepath
            index=folpath.rfind('\\')
            folpath=folpath[:index]
            display = "filepath= "+folpath
            print(display) #Prints to console  
            context.scene.my_string_prop=folpath+"\\"
            #Window>>>Toggle systen console

            return {'FINISHED'}

        def invoke(self, context, event): # See comments at end  [1]
            context.window_manager.fileselect_add(self) 
            #Open browser, take reference to 'self' 
            #read the path to selected file, 
            #put path in declared string type data structure self.filepath

            return {'RUNNING_MODAL'}
        
class OpenBrowser2(bpy.types.Operator):
        bl_idname = "open.browser2"
        bl_label = "Choose directory"

        filepath: bpy.props.StringProperty(subtype="FILE_PATH")
        #somewhere to remember the address of the file
        #  filepath = ""

        def execute(self, context):
            folpath=self.filepath
            index=folpath.rfind('\\')
            folpath=folpath[:index]
            display = "filepath= "+folpath
            print(display) #Prints to console  
            context.scene.my_string_prop3=folpath+"\\"
            #Window>>>Toggle systen console

            return {'FINISHED'}

        def invoke(self, context, event): # See comments at end  [1]

            context.window_manager.fileselect_add(self) 
            #Open browser, take reference to 'self' 
            #read the path to selected file, 
            #put path in declared string type data structure self.filepath

            return {'RUNNING_MODAL'}                
    
def register():
    bpy.utils.register_class(AllExport)
    #  bpy.utils.register_class(PBRConvert)
    bpy.utils.register_class(OpenBrowser)
    bpy.utils.register_class(OpenBrowser2)
    bpy.utils.register_class(UnityTransform)
    #  bpy.utils.register_class(UnityMatConv)
    bpy.utils.register_class(UnityExport)
    #  bpy.utils.register_class(UnityMatMerge)
    bpy.types.Scene.my_string_prop = bpy.props.StringProperty \
    (
     name = "Path",
     description = "Path to export",
     default = "D:\\Export\\"
    )
    bpy.types.Scene.my_string_prop2 = bpy.props.FloatProperty \
    (
     name = "Threshold",
     description = "Marging threshold",
     default = 0.1
    )
    bpy.types.Scene.my_string_prop3 = bpy.props.StringProperty \
    (
     name = "Path",
     description = "Choose where to save your texture",
     default = "D:\\Export\\"
    )
    # UNDONE:
    #  bpy.types.Scene.my_bool = bpy.props.BoolProperty(
    #  name="Separate files",
    #  description="Choose whehter to export objects in separate fbx file or in one",
    #  default = True)
    bpy.types.Scene.my_bool = True

    # UNDONE:
    #  bpy.types.Scene.my_bool2 = bpy.props.BoolProperty(
    #  name="Auto transform correction",
    #  description="Automatically correct transform while exporting",
    #  default = True)
    bpy.types.Scene.my_bool2 = False

    bpy.types.Scene.my_boolal = bpy.props.BoolProperty(
    name="Albedo",
    description="Check to export Albedo map",
    default = True) 
    bpy.types.Scene.my_boolme = bpy.props.BoolProperty(
    name="Metallic",
    description="Check to export Metallic Map",
    default = True)
    bpy.types.Scene.my_boolro = bpy.props.BoolProperty(
    name="Roughness",
    description="Check to export Roughness Map",
    default = True)  
    bpy.types.Scene.my_boolno = bpy.props.BoolProperty(
    name="Normal Map",
    description="Check to export Normal Map",
    default = True)  
    bpy.types.Scene.my_enum = bpy.props.EnumProperty(
        name = "Smoothness",
        description = "Choose whether to save smoothness alpha channel on albedo or metallic",
        items = [
            ("FIRST" , "Albedo Alpha" , "Cast roughness as alpha to albedo map"),
            ("SECOND", "Metallic Alpha", "Cast roughness as alpha to metallic map")
        ]
    )
    bpy.types.Scene.my_enum2 = bpy.props.EnumProperty(
        name = "Filetype",
        description = "Choose type of image",
        items = [
            ("PNG" , "PNG" , "Cast roughness as alpha to albedo map"),
            ("TARGA", "TGA", "Cast roughness as alpha to metallic map")
        ]
    )
    
def unregister():
    bpy.utils.unregister_class(AllExport)
    #  bpy.utils.unregister_class(PBRConvert)
    bpy.utils.unregister_class(OpenBrowser)
    bpy.utils.unregister_class(OpenBrowser2)
    bpy.utils.unregister_class(UnityTransform)
    #  bpy.utils.unregister_class(UnityMatConv)
    bpy.utils.unregister_class(UnityExport)
    #  bpy.utils.unregister_class(UnityMatMerge)
    del bpy.types.Scene.my_string_prop
    del bpy.types.Scene.my_bool
    del bpy.types.Scene.my_string_prop2
    del bpy.types.Scene.my_string_prop3
    del bpy.types.Scene.my_bool2
    del bpy.types.Scene.my_enum
    del bpy.types.Scene.my_enum2

register()

class UnityExporterPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Unity Exporter"
    bl_idname = "OBJECT_PT_UExporter"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    # bl_category = "Unity Export Tools"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        #row = layout.row()
        #row.label(text="Material tools")

        #row = layout.row()
        #row.operator("cusops.unitytransform")
        
        #row = layout.row()
        #row.operator("cusops.unitymatconv")
        
        #row = layout.row()
        #row.operator("cusops.unitymatmerge")
        
        #row = layout.row()
        #row.prop(context.scene, "my_string_prop2")
        
        #  row = layout.row()
        #  row = layout.row()
        #  row = layout.row()
        #  row = layout.row()
        #row.label(text="FBX Export")
        
        
		
        row = layout.row()
        row.prop(context.scene, "my_string_prop")
        row.operator("open.browser", icon="FILE_FOLDER", text="")
        row = layout.row()
        row = layout.row()
        row = layout.row()
        row.operator("cusops.unityexport")
        
        row = layout.row()
        #  row.prop(context.scene, "my_bool")

        row = layout.row()
        #  row.prop(context.scene, "my_bool2")
        
        #  row = layout.row()
        #  row = layout.row()
        row = layout.row()
        row = layout.row()
        row.label(text="Unity PBR textures")
        row = layout.row()
        row.prop(context.scene, "my_boolal")
        row = layout.row()
        row.prop(context.scene, "my_boolme")
        row = layout.row()
        row.prop(context.scene, "my_boolno")
        
        row = layout.row()
        row.label(text="Roughness>Smoothness")
        
        
        
        #row = layout.row()
        #row.prop(context.scene, "my_string_prop3")
        #row.operator("open.browser2", icon="FILE_FOLDER", text="")
        
        row = layout.row()
        row.prop(context.scene, "my_enum")
        
        row = layout.row()
        row.prop(context.scene, "my_enum2")
        
        #  row = layout.row()
        #  row.operator("cusops.pbrconvert")
        
        row = layout.row()
        row.operator("cusops.allexport")

def register():
    bpy.utils.register_class(UnityExporterPanel)


def unregister():
    bpy.utils.unregister_class(UnityExporterPanel)


if __name__ == "__main__":
    register()

