---
title: "How to export specific layers to a dxf file using ObjectARX?"
date: 2012-08-01
categories:
  - AutoCAD C++
tags:
  - C++
  - DXF
  - Layer
  - ObjectARX
description: "I want to export some specific layers to a .DXF file. AcDbDatabase::dxfOut() can export a drawing, but I only want to export specific layers. How c..."
author: Autodesk
---
# How to export specific layers to a dxf file using ObjectARX?

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/how-to-export-specific-layers-to-a-dxf-file-using-objectarx.html

## 文章内容

By Philippe Leefsma
Q:
I want to export some specific layers to a .DXF file. AcDbDatabase::dxfOut() can export a drawing, but I only want to export specific layers. How can I do this using ObjectARX?
A:
To make a DXF file that contains entities from specified layers, use acedSSGet() with a filter to select the entities on the required layers. Then wblock these entities to a new database and call dxfOut() to create the dxf file. Below is one of the functions from the attached example. The function named FilterObjects (not shown here) fills a selectionSet with the entities on layer 0 and a layer named "Layer1".
- 
int FilterObjects(ads_name ss)
{
        int resVal;
        char *chLayerName[] = {"0", "Layer1"};
        struct resbuf * resBufLayerFilter = NULL;
        struct resbuf **resBufTemp;
          resBufTemp = &resBufLayerFilter;
        *resBufTemp = acutBuildList(-4, "<OR", 0);
        resBufTemp = &(*resBufTemp)->rbnext;
          for (int nIndex = 0 ; nIndex<2;nIndex++)
        {
                *resBufTemp = acutBuildList (8, chLayerName[nIndex], 0);
                resBufTemp = &(*resBufTemp)->rbnext;
        }       
          *resBufTemp = acutBuildList(-4, "OR>", 0);
        resBufTemp = &(*resBufTemp)->rbnext;
          while(true)
        {
                //select all objects only on layer '0, Layer1'
                resVal = acedSSGet(L"_X", NULL, NULL, resBufLayerFilter, ss);
                  if (resVal == RTCAN || resVal == RTERROR)
                {
                        //user selected zero objects
                        if (resVal == RTERROR)
                            acutPrintf (L"\nZero objects are selected.\n");
                        acutRelRb(resBufLayerFilter);
                        return resVal;
                }
                else
                        break;
        }
          acutRelRb(resBufLayerFilter);
        return resVal;
}
  void ADSKDEX()
{
        Acad::ErrorStatus es;
        AcGePoint3d  pt (0.,0.,0.) ;
        AcGeVector3d    ex(1., 0., 0.), ey(0., 1., 0.), ez(0., 0., 1.) ;
          ads_name SourceSS;
        long  sslen = -1;
        AcDbObjectIdArray ObjIDArray;
        ads_name ename;
        long  sscur;
        CString ClasseObj, Result;
        AcDbObjectId       eId;
          FilterObjects(SourceSS); //filter the objects based on the layers
          int nRet = acedSSLength(SourceSS, &sslen);
          if (nRet == RTNORM)
        {
                acutPrintf(L"%d objects selected for export\n",sslen);
        }
          if( acedSSLength( SourceSS, &sslen) != RTNORM)
        {
                acutPrintf(L"No Objects are selected for export");
                return;
        }
          for (sscur = 0; sscur < sslen; sscur++)
        {
                acedSSName(SourceSS, sscur, ename);   
                acdbGetObjectId(eId, ename);
                ObjIDArray.append(eId);
        }
          AcDbDatabase *pDB = NULL;
          if( ( es = acdbHostApplicationServices()->workingDatabase()->wblock(
                pDB, ObjIDArray, pt ))!=Acad::eOk)
        {
                AfxMessageBox(L"wblock failed", MB_ICONEXCLAMATION | MB_OK);
                return;
        }
          es = pDB->dxfOut(L"c:\\test.dxf");
          if(pDB)
        {
                delete pDB; // delete the database.
                pDB = NULL;
        }
          acedSSFree(SourceSS);
        acedSSFree(ename);
}

