---
title: "Use the normal to correct the text when mirroring a dimension with transformBy"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - Dimension
  - Unicode
description: "While applying the transformBy() method on a dimension entity, the dimension text also gets mirrored and does not respect the MIRRTEXT system varia..."
author: Autodesk
---
# Use the normal to correct the text when mirroring a dimension with transformBy

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/use-the-normal-to-correct-the-text-when-mirroring-a-dimension-with-transformby.html

## 文章内容

By Gopinath Taget
While applying the transformBy() method on a dimension entity, the dimension text also gets mirrored and does not respect the MIRRTEXT system variable. To avoid this behavior, store the normal of the dimension entity before mirroring and then apply it to the mirrored entity as shown in the sample code below:
NOTE: Error handling has been kept short for clarity.
void ASDKtest()
{
ads_name ent;
ads_point ptres;
acedEntSel( L"\nSelect a dimension entity: ", ent, ptres );
  AcDbObjectId objId;
acdbGetObjectId(objId, ent);
  AcDbEntity * pEnt = NULL;
acdbOpenObject(pEnt, objId, AcDb::kForWrite);
  AcDbDimension * pDim = NULL;
pDim = AcDbDimension::cast(pEnt);
 if(!pDim)
{   
  acutPrintf(L"\nPlease select a Dimension");
  pEnt->close();
  return;
}
  AcGeVector3d norm;
norm = pDim->normal();
  AcGeMatrix3d mat;
mat.setToIdentity();
AcGeLine3d line(AcGePoint3d(7,7,0), AcGePoint3d(7,0,0));
mat.setToMirroring(line);
  pDim->transformBy(mat);
pDim->setNormal(norm);
pDim->close();
}

