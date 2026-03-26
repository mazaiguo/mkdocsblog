---
title: "Setting Color to Each Face of Solid"
date: 2016-03-01
categories:
  - AutoCAD
tags:
  - Solid
description: "The below is self explanatory, we ‘ll look at it how we can traverse to each face and paint with different colours."
author: Autodesk
---
# Setting Color to Each Face of Solid

发布日期: 2016-03-01

原始链接: https://adndevblog.typepad.com/autocad/2016/03/setting-color-to-each-face-of-solid.html

## 文章内容

By Madhukar Moogala
The below is self explanatory, we ‘ll look at it how we can traverse to each face and paint with different colours.
void TestBrep(void)
{
    Adesk::Int32 len;
    ads_name  ssname0;
  struct resbuf *buffer;
    buffer = acutBuildList(-4, _T("<AND"),
              RTDXF0, _T("3DSOLID"),
              -4, _T("AND>"), RTNONE);
    acutPrintf(_T("\nSelect a box:"));
    acedSSGet(NULL, NULL, NULL, buffer, ssname0);
    acutRelRb(buffer);
  if (RTNORM == acedSSLength(ssname0, &len))
    {
        ads_name  ent;
        AcDbObjectId entId;
    for(long k = 0; k < len; k++)
        {
            acedSSName(ssname0, k, ent);
            acdbGetObjectId(entId, ent);
        settingDifferentColorToEachFace(entId);
        }
        acedSSFree(ssname0);
    }
}
  void settingDifferentColorToEachFace(AcDbObjectId solidId)
{
  AcCmColor specialColor;
  AcDb3dSolid* pSolid;
    if (Acad::eOk == acdbOpenObject(pSolid, solidId, AcDb::kForRead))
    {
        AcDbFullSubentPath path(solidId, AcDbSubentId());
    AcBrBrep brep;
        AcBr::ErrorStatus bs = brep.setSubentPath(path);
        if (bs != AcBr::eOk)
            return;
   //Initialize the BrepFace traverser
        AcBrBrepFaceTraverser bft;
        bs = bft.setBrep(brep);
        if (bs != AcBr::eOk)
            return;
          AcArray<AcDbSubentId> arrSubentId;
        // Traverse all faces
        for (;!bft.done();bft.next())
        {
            AcBrFace face;
            bs = bft.getFace(face);    
            if (bs != Acad::eOk)
            {
                acutPrintf(L"\ngetFace failed");
                break;
            }
            AcDbFullSubentPath    Path(kNullSubent);
            AcDbSubentId          subentId;
            AcBr::ErrorStatus bss = face.getSubentPath(Path);
            subentId = Path.subentId();
              arrSubentId.append(subentId);
        }
          pSolid->upgradeOpen();
        for (int i = 0; i < arrSubentId.length(); i++)
        {
      specialColor.setColorIndex(i);
            pSolid->setSubentColor(arrSubentId[i],specialColor);
        }
        pSolid->downgradeOpen();
    }
      pSolid->close();
}

