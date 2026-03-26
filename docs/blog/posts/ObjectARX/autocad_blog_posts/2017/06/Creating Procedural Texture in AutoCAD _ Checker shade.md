---
title: "Creating Procedural Texture in AutoCAD : Checker shade"
date: 2017-06-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Unicode
description: "Procedural textures are algorithmic texture unlike textures based on images these textures are created using logic, we can created patterned textur..."
author: Autodesk
---
# Creating Procedural Texture in AutoCAD : Checker shade

发布日期: 2017-06-01

原始链接: https://adndevblog.typepad.com/autocad/2017/06/creating-procedural-texture-in-autocad-checker-shade.html

## 文章内容

By Madhukar Moogala
Procedural textures are algorithmic texture unlike textures based on images these textures are created using logic, we can created patterned textures using Checker shade.
Programmatically we can create Checker,Speckle, Wave and Tile type generic textures.
In this post I will discuss how we can create a Checker procedural texture.

void applyProceduralTextureToVase()
 {
 //Select Vase
 ads_point s_pt;
 ads_name s_ent;
 if (RTNORM != acedEntSel(_T("Select Vase"), s_ent, s_pt)) 
        return;
 AcDbObjectId vaseId = AcDbObjectId::kNull;
 if (!eOkVerify(acdbGetObjectId(vaseId, s_ent))) 
        return;
 AcDbObjectPointer<AcDbEntity> pVase(vaseId, AcDb::kForWrite);
 if (!eOkVerify(pVase.openStatus())) return;
 const ACHAR* materialName = _T("TestGeneric");
 //create Generic Procedural texture and apply to Material
 createGenericTexture(materialName);
 //Appy Material to Vase entity
 pVase->setMaterial(materialName);
 //Compute Mapper and apply to vase entity
 AcGiMapper mapper;
 mapper.setProjection(AcGiMapper::kSphere);
 mapper.setAutoTransform(AcGiMapper::kNone);
 mapper.setUTiling(AcGiMapper::kTile);
 mapper.setVTiling(AcGiMapper::kTile);
 double uScale = 1;
 double vScale = 1;
 double uOffset = 0;
 double vOffset = 0;
 AcGeMatrix3d mx;
 mx(0, 0) = uScale;
 mx(0, 1) = 0.000;
 mx(0, 2) = 0.000;
 mx(0, 3) = uScale*uOffset;
 mx(1, 0) = 0.000;
 mx(1, 1) = vScale;
 mx(1, 2) = 0.000;
 mx(1, 3) = vScale*vOffset;
 mx(2, 0) = 0.000;
 mx(2, 1) = 0.000;
 mx(2, 2) = 1.000;
 mx(2, 3) = 0.000;
 mx(3, 0) = 0.000;
 mx(3, 1) = 0.000;
 mx(3, 2) = 0.000;
 mx(3, 3) = 1.000;

 mapper.setTransform(mx);
 //Apply Mapper to Vase 
 pVase->setMaterialMapper(mapper);

 }
Util Methods:
AcDbObjectId createMaterial(const ACHAR*& name)
{
    // Open the material dictionary for writing
    AcDbDictionary *pMaterialDict;
    Acad::ErrorStatus dbStatus;
    AcDbObjectId mtlId;
 #define cwDB acdbHostApplicationServices()->workingDatabase()
    if (cwDB->getMaterialDictionary(pMaterialDict,
      AcDb::kForWrite) == Acad::eOk)
    {
        // Create and initialize the material
        AcDbMaterial *pMaterialObj = new AcDbMaterial();
  // Name
        pMaterialObj->setName(name);
   // Diffuse color
        AcCmEntityColor acClr;
  acClr.setRGB(153, 153, 153);
  AcGiMaterialColor color;
        color.setMethod(AcGiMaterialColor::kOverride);
        color.setFactor(1.0);
        color.setColor(acClr);
  // Diffuse texture
        pMaterialObj->setDiffuse(color, AcGiMaterialMap());
    // Ambient and specular color
        AcGiMaterialColor inheritColor;
        color.setFactor(0.5);
        pMaterialObj->setAmbient(color);
        pMaterialObj->setSpecular(color, AcGiMaterialMap(), 0.5);
   // Add material to dictionary
        dbStatus = pMaterialDict->setAt(name, pMaterialObj, mtlId);
        assert(dbStatus == Acad::eOk);
  // Close the material and dictionary
        pMaterialObj->close();
        pMaterialDict->close();
    }
    return mtlId;

 }

void createGenericTexture(const ACHAR*& materialName)
 {
 // This example is a simple procedural texture
 
 //Create a Material "Test"
 AcDbObjectId mtlId = createMaterial(materialName);
 AcDbObjectPointer<AcDbMaterial> mtl(mtlId, AcDb::kForWrite);
 if (Acad::eOk != mtl.openStatus())
  return;
 mtl->setMode(AcGiMaterialTraits::kRealistic);
 AcCmColor clr1, clr2;
 clr1.setRGB(0, 127, 255);
 clr2.setRGB(191, 255, 0);
 
 AcGiVariant varData;
 // the Shader element
 varData.setElem(_T("Shader"), AcGiVariant(_T("Checker"))); 
 //the soften element
 varData.setElem(_T("Soften"), AcGiVariant(0.0)); 
 AcGiVariant clr1Data,clr2Data;
  clr1Data.setElem(_T("Color"), AcGiVariant(clr1));
 varData.setElem(_T("Map1"), clr1Data);
  clr2Data.setElem(_T("Color"), AcGiVariant(clr2));
 varData.setElem(_T("Map2"), clr2Data);
 //Set Variant Data to Texture
 AcGiGenericTexture texture;
 texture.setDefinition(varData);
 //Set Texture to Material Map
 AcGiMaterialMap map;
 map.setTexture(&texture);
 //Apply Texture Material Map to Material
 mtl->setDiffuse(AcGiMaterialColor(), map);

 }
ScreenCast Demo

## 评论

**内容**: James Maeding said...
while on the subject of textures, I have some tools where I need to show an image on a subdmesh. I use them for terrain surfaces so want to "drape" an aerial image on them.
I also have 3d solids that I want to do the same thing for. I also want to "wrap" an image around some 3d solids like swept circle, which I use for pipes. Just some fuel for your posts, thx!
Reply
07/18/2017 at 08:35 AM

---
**内容**: Madhukar Moogala said in reply to James Maeding...
Hi James,
Thanks for dropping by, this post only discussed about creating algorithmic textures, following code wraps the material using mapper

 AcGiMapper mapper;
 mapper.setProjection(AcGiMapper::kSphere);
 mapper.setAutoTransform(AcGiMapper::kNone);
 mapper.setUTiling(AcGiMapper::kTile);
 mapper.setVTiling(AcGiMapper::kTile);
 double uScale = 1;
 double vScale = 1;
 double uOffset = 0;
 double vOffset = 0;
 AcGeMatrix3d mx;
 mx(0, 0) = uScale;
 mx(0, 1) = 0.000;
 mx(0, 2) = 0.000;
 mx(0, 3) = uScale*uOffset;
 mx(1, 0) = 0.000;
 mx(1, 1) = vScale;
 mx(1, 2) = 0.000;
 mx(1, 3) = vScale*vOffset;
 mx(2, 0) = 0.000;
 mx(2, 1) = 0.000;
 mx(2, 2) = 1.000;
 mx(2, 3) = 0.000;
 mx(3, 0) = 0.000;
 mx(3, 1) = 0.000;
 mx(3, 2) = 0.000;
 mx(3, 3) = 1.000;
 mapper.setTransform(mx);
 //Apply Mapper to Vase 
 pVase->setMaterialMapper(mapper);

for image based textures you may visit
http://adndevblog.typepad.com/autocad/2015/12/mapping-a-material-texture-on-a-subdmesh.html

Wrapping material to a 3dsolid based on image on disk
http://adndevblog.typepad.com/autocad/2013/07/applying-material-to-a-cylinder.html
Reply
07/18/2017 at 09:35 PM

---
**内容**: James Maeding said...
I should have asked, how do you do the draping and wrapping?...thx
Reply
07/18/2017 at 08:36 AM

---
**内容**: James Maeding said...
Thanks Madhukar!
Reply
07/24/2017 at 08:58 AM

---
**内容**: snow rider said...
We appreciate your visit, but this page mainly covered how to create algorithmic textures. The following code covers the material using a mapper.
Reply
09/19/2022 at 06:38 PM

---
**内容**: dordle said...
Thank you for providing this information. I am delighted to come on this fantastic article.
Reply
02/13/2023 at 02:20 AM

---
