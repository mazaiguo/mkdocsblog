---
title: "Decomposing Material Mapper Transform Matrix"
date: 2014-08-01
categories:
  - AutoCAD C++
tags:
  - C++
  - Selection
description: "Question: Is it possible to return origin, rotation, the x-y- scale factors and offset values from the Matrix3d of  MaterialMapper.Transform ?"
author: Autodesk
---
# Decomposing Material Mapper Transform Matrix

发布日期: 2014-08-01

原始链接: https://adndevblog.typepad.com/autocad/2014/08/decomposing-material-mapper-transform-matrix.html

## 文章内容

By Madhukar Moogala
Question: Is it possible to return origin, rotation, the x-y- scale factors and offset values from the Matrix3d of  MaterialMapper.Transform ?
Answer: Yes ,it is possible to retrieve details from  transform matrix of an Entity's material mapper , I have demonstrate below assuming user has selected a 3DFace entity on which Material is applied using MaterialMap command iteractively and adjusted rotation ,offset and scale as per user needs.
Somethink like this as shown in below screenshot.
Note : If AcGiMapper::autoTransform() is set to kObject or kModel, then you will not be able to recover the scale/translation/rotation, as the GS will dynamically compute it based on whatever entity/selection the mapper is applied to.
C++ Code :
static void ASDKMyGroupTestMapper()
{
Acad::ErrorStatus es;
ads_name entres;
ads_point ptres;
AcGeVector3d scale;
AcGeVector3d rotation;
AcGeVector3d translate;
AcGeMatrix3d mat;
/*Select Entity*/
if(RTNORM != acedEntSel(_T("Select 3DFace entity"),entres,ptres))
return;
AcDbObjectId objId = AcDbObjectId::kNull;
if((es = acdbGetObjectId(objId,entres) ) != Acad::eOk)
return;
AcDbEntity* pFaceEntity = NULL;
if ((es = acdbOpenAcDbEntity(pFaceEntity,objId,AcDb::kForRead) )
!= Acad::eOk) return;
  if(pFaceEntity->isA() == AcDbFace::desc())
{
AcDbFace* pFace =  AcDbFace::cast(pFaceEntity);
AcGiMapper mapper;
AcDbMaterial* material = NULL;
AcGiMaterialMap materialMap;
if((es = acdbOpenObject((AcDbObject*&)material,pFace->materialId(),
AcDb::kForRead))!= Acad::eOk)
{
pFaceEntity->close();
return;
}
double strength=0.0;
AcGiMaterialColor color;
/*Get diffuse gives details about Texture in general,
and what component to be used to retrieve materialmap
can be found from AcDbMaterial::channelFlags*/           
material->diffuse(color,materialMap);
  mat = materialMap.mapper().transform();
if(materialMap.mapper().autoTransform() < 2)
{
decomposeMatrix(mat,scale,rotation,translate);
}
  pFaceEntity->close();
material->close();
      }
acutPrintf(_T("\n Rotation Angle : %2f \n"),rotation.z*(180/M_PI));
acutPrintf(_T("\n Scale X : %2f , Scale Y : %2f \n"),scale.x,scale.y);
/*You may have to negate offset values of Translate vector for correct sign*/
acutPrintf(_T("\n Translation Vector: %2f,%2f \n"),-translate.x,-translate.y);
    }
  static void decomposeMatrix (const AcGeMatrix3d &mat,
AcGeVector3d &scale,
AcGeVector3d &rotate,
AcGeVector3d &translate)
{
// Scale - assume always positive, and must be non-zero
scale.x = 1.0/AcGeVector3d(mat(0,0), mat(0,1), mat(0,2)).length();
scale.y = 1.0/AcGeVector3d(mat(1,0), mat(1,1), mat(1,2)).length();
scale.z = 1.0/AcGeVector3d(mat(2,0), mat(2,1), mat(2,2)).length();
if (scale.x == 0.0)
scale.x = 1.0;
if (scale.y == 0.0)
scale.y = 1.0;
if (scale.z == 0.0)
scale.z = 1.0;
  // Translation
translate =  mat.translation();
translate.x *= scale.x;
translate.y *= scale.y;
translate.z *= scale.z;
  // Rotation – assume only rotation about the Z axis
double acosVal = mat(0,0) / scale.x;
if (acosVal > 1.0)
acosVal = 1.0;
else if (acosVal < -1.0)
acosVal = -1.0;
  double zAngle = acos(acosVal);
assert(0.0 <= zAngle && zAngle <= M_PI);
if (mat(0, 1) > 0.0)
zAngle = 2.0 * M_PI - zAngle;
  rotate.x = 0.0;
rotate.y = 0.0;
rotate.z = zAngle;
}
C# .NET code :
[CommandMethod("TestMapper")]
public void Mappertest()
{
Document activeDoc = Application.DocumentManager.MdiActiveDocument;
Database db = activeDoc.Database;
Editor ed = activeDoc.Editor;
PromptEntityResult oRes = ed.GetEntity("Select 3dFace");
if (oRes.Status != PromptStatus.OK) return;
Vector3d scale = default(Vector3d);
Vector3d rotate = default(Vector3d);
Vector3d translate = default(Vector3d);
  using (Transaction oTrans = db.TransactionManager.StartTransaction())
{
Face oFace = oTrans.GetObject(oRes.ObjectId, OpenMode.ForRead) as Face;
  if (oFace != null)
{
string strMat = oFace.Material;
ObjectId nMat = oFace.MaterialId;
Material material = oTrans.GetObject(nMat,OpenMode.ForRead) as Material;
ChannelFlags cFlasg = material.ChannelFlags;
MaterialDiffuseComponent mDC = material.Diffuse;                                 
MaterialMap materialMap = mDC.Map;                            
Matrix3d tranform = materialMap.Mapper.Transform;
double scaleD = tranform.GetScale();               
if (materialMap.Mapper.AutoTransform == AutoTransform.InheritAutoTransform ||
    materialMap.Mapper.AutoTransform == AutoTransform.None)
DecomposeMatrix(tranform , ref scale, ref rotate, ref translate);
/*You have negate offset value to reflect correct sign*/
ed.WriteMessage("Rotation Angle : " + rotate.Z * (180 / Math.PI) + "\n"
                + "Scale X :" + Math.Round(scale.X) + " Scale Y : " + Math.Round(scale.Y) + "\n" +
                "Translation Vector offset Values :" + -translate.X + "," + -translate.Y);
    }
oTrans.Commit();
}
    }
  public void DecomposeMatrix( Matrix3d mat, ref Vector3d scale, ref Vector3d rotate, ref Vector3d translate)
{
// Scale - assume always positive, and must be non-zero
Vector3d v3dOne= new Vector3d(mat[0, 0], mat[0, 1], mat[0, 2]);
Vector3d v3dTwo = new Vector3d(mat[1, 0], mat[1, 1], mat[1, 2]);
Vector3d v3dThree = new Vector3d(mat[2, 0], mat[2, 1], mat[2, 2]);
  //    scale = new Vector3d(v3dOne.Length, v3dTwo.Length, v3dThree.Length);
scale = new Vector3d(1/v3dOne.Length, 1/v3dTwo.Length, 1/v3dThree.Length);
if (scale.X == 0)
scale = new Vector3d(1.0, scale.Y, scale.Z);
if (scale.Y == 0)
scale = new Vector3d(scale.X, 1.0, scale.Z);
if (scale.Z == 0)
scale = new Vector3d(scale.X, scale.Y, 1.0);
// Translation
translate = mat.Translation;
translate = new Vector3d(translate.X * Math.Round(scale.X), translate.Y*Math.Round(scale.Y), translate.Z*Math.Round(scale.Z));
// Rotation – assume only rotation about the Z axis
double acosValue = mat[0, 0] / scale.X;
if (acosValue > 1.0)
acosValue = 1.0;
else if (acosValue < -1.0)
acosValue = -1.0;
double zAngle = Math.Acos(acosValue);
Debug.Assert(0.0 <= zAngle && zAngle <= Math.PI);
if(mat[0,1] > 0.0)
zAngle = 2.0 * Math.PI - zAngle;
rotate = new Vector3d(0.0, 0.0, zAngle);
  }
Output :
Rotation Angle : 60.0000016696521
Scale X :1 Scale Y : 2
Translation Vector offset Values :12,15

