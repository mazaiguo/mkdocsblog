---
title: "How To Retrieve Naviswork Model NWD Or BIM Underlay Information In AutoCAD Through Programming"
date: 2016-11-01
categories:
  - AutoCAD C++
tags:
  - API
  - AutoCAD
  - C++
  - DXF
  - ObjectARX
description: "I have received a query from an ADN partner, how to read the scale, rotation angle, insertion point and underlay reference path of  NWD model, thou..."
author: Autodesk
---
# How To Retrieve Naviswork Model NWD Or BIM Underlay Information In AutoCAD Through Programming

发布日期: 2016-11-01

原始链接: https://adndevblog.typepad.com/autocad/2016/11/how-to-retrieve-naviswork-model-nwd-or-bim-underlay-information-in-autocad-through-programming.html

## 文章内容

By Madhukar Moogala
I have received a query from an ADN partner, how to read the scale, rotation angle, insertion point and underlay reference path of  NWD model, though API to handle such information is not exposed to ObjectARX, but still not to loose hope we can retrieve the same through reading DXF.
When a Naviswork model is attached in AutoCAD through _COORDINATIONMODELATTACH user is invoked to enter insertion point,scale and other parameters and the model is attached a overlay in AutoCAD model space creating a ACDBNAVISWORKSMODELDEF symbol table and stored in the ACAD_BIM_DEFINITIONS dictionary. The corresponding reference entity in Model space is AcDbNavisworkModel.
AcDbNavisworkModel is not an AutoCAD native entity, it is created by a DBX application AcBIMUnderlay.dbx
Useful links to understand what each designated DXF group meant for AcDbNavisworkModel.
COORDINATION MODEL (DXF)
ACDBNAVISWORKSMODELDEF (DXF)
  /*Get  CoordinationModel*/
void test5()
{
 
 #pragma region Retrieve NWD Model from BlockTable
 AcDbObjectId entId;
 
 AcDbObjectIdArray blockEnts;

 AcDbBlockTable* blkTbl;
 AcDbDatabase* db = acdbHostApplicationServices()->workingDatabase();
 if (!eOkVerify(db->getSymbolTable(blkTbl, AcDb::kForRead))) return;


 // open named block and get NWD model
 AcDbBlockTableRecord* blkRec;
 AcDbBlockTableRecordIterator* iter;
 if (!eOkVerify(blkTbl->getAt(ACDB_MODEL_SPACE, blkRec, AcDb::kForRead))) return;

 if (!eOkVerify(blkRec->newIterator(iter, true, true)))
 {
  blkRec->close(); return;
 }

 for (; !iter->done(); iter->step(true, true)) {
  Acad::ErrorStatus es = iter->getEntityId(entId);
  if (es == Acad::eOk)
   blockEnts.append(entId);
 }

 blkRec->close();
 delete iter;
 blkTbl->close();

 #pragma endregion

 #pragma region Get entityname from ObjectId
 /*test drawing has only one NWD and it would be the first one*/
 ads_name ent_name;
 if(!eOkVerify(acdbGetAdsName(ent_name, blockEnts[0]))) return;
 #pragma endregion


 /*Get Resbuf struct of DXF Data of Selected  Model*/
 resbuf* args = acutNewRb(RTSTR);
 acutNewString(_T("*"), args->resval.rstring);
 resbuf* entdata = acdbEntGetX(ent_name, args);
 acutRelRb(args);
 LoopRbChain(entdata);
 acutRelRb(entdata);

 /*Get File Path*/
 acutPrintf(_T("NWD file path is %s"), nwdData.filePath);
 /*Create a transform Matrix to get Scale\Insertion\Rotation angle*/
 AcGeMatrix3d mat;
 int size = nwdData.rreals.length();
 for (int i = 0; i < 4; i++)
 {
  for (int j = 0; j < 4; j++)
  {
   mat(i,j) = nwdData.rreals.at(4*i + j);
  }
 }
 double scale = mat.scale();
 AcGeVector3d insertionV = mat.translation();
 AcGePoint3d insertionPt(insertionV.x, insertionV.y, insertionV.z);
 
 /*Some Math  to get rotation angle from  Matrix*/
 double acosVal = mat(0, 0) / scale;
 if (acosVal > 1.0)
  acosVal = 1.0;
 else if (acosVal < -1.0)
  acosVal = -1.0;

 double rotAngle = acos(acosVal);
 ASSERT(0.0 <= rotAngle && rotAngle <= M_PI);
 if (mat(0, 1) > 0.0)
  rotAngle = 2.0 * M_PI - rotAngle;



 acutPrintf(_T("\n Insertion Point [%.2f,%.2f,%.2f],\n Scale = %.2f \n Rotation = %.2f"),
  insertionV.x, insertionV.y, insertionV.z, scale, (rotAngle*180)/M_PI);

}
struct NWDData
{
 CString filePath;
 AcArray rreals;
};

/*Global Declration*/
NWDData nwdData;
/*Helper Methods*/
int dxfCodeToDataType(int resType)
{
 // which data type is this value
 if ((resType >= 0) && (resType <= 9))
  return RTSTR;
 else if ((resType >= 10) && (resType <= 17))
  return RT3DPOINT;
 else if ((resType >= 38) && (resType <= 59))
  return RTREAL;
 else if ((resType >= 60) && (resType <= 79))
  return RTSHORT;
 else if ((resType >= 90) && (resType <= 99))
  return RTLONG;
 else if ((resType == 100) || (resType == 101) || (resType == 102) || (resType == 105))
  return RTSTR;
 else if ((resType >= 110) && (resType <= 119))
  return RT3DPOINT;
 else if ((resType >= 140) && (resType <= 149))
  return RTREAL;
 else if ((resType >= 170) && (resType <= 179))
  return RTSHORT;
 else if ((resType >= 210) && (resType <= 219))
  return RT3DPOINT;
 else if ((resType >= 270) && (resType <= 299))
  return RTSHORT;
 else if ((resType >= 300) && (resType <= 309))
  return RTSTR;
 else if ((resType >= 310) && (resType <= 369))
  return RTENAME;
 else if ((resType >= 370) && (resType <= 379))
  return RTSHORT;
 else if ((resType >= 380) && (resType <= 389))
  return RTSHORT;
 else if ((resType >= 390) && (resType <= 399))
  return RTENAME;
 else if ((resType >= 400) && (resType <= 409))
  return RTSHORT;
 else if ((resType >= 410) && (resType <= 419))
  return RTSTR;
 else if (resType == 1004)
  return resType;        // binary chunk
 else if ((resType >= 999) && (resType <= 1009))
  return RTSTR;
 else if ((resType >= 1010) && (resType <= 1013))
  return RT3DPOINT;
 else if ((resType >= 1038) && (resType <= 1059))
  return RTREAL;
 else if ((resType >= 1060) && (resType <= 1070))
  return RTSHORT;
 else if ((resType == 1071))
  return RTLONG;
 else if ((resType < 0) || (resType > 4999))
  return resType;
 else
  return RTNONE;
}
void LoopRbChain(resbuf* entData)
{
 resbuf* tmp = entData;
 CString valueStr;
 //increase size of internal buffer from 128 to 512
 valueStr.GetBuffer(512);
 int count = 0; // To monitor Matrix filling
 while (tmp)
 {
  int dataType = dxfCodeToDataType(tmp->restype);
 
  switch (dataType)
  {
  case RTSTR:
   if (tmp->restype == 1) /*For NWD Model file path*/
   {
    if (tmp->resval.rstring == NULL)
     valueStr = _T("(NULL)");
    else
    {
     valueStr.Format(_T("\"%s\""), tmp->resval.rstring);
     nwdData.filePath = valueStr;
    }

   }
   break;
  case RTREAL:
   if (tmp->restype == 40)
   {
    if (nwdData.rreals.length() < 16/*Max size of 4 X 4 transformMatrix*/)
     nwdData.rreals.append(tmp->resval.rreal);   
   }
   break;
  case RTENAME:
   if (tmp->restype == 340)
   {
    resbuf* args = acutNewRb(RTSTR);
    acutNewString(_T("*"), args->resval.rstring);
    resbuf* entdata = acdbEntGetX(tmp->resval.rlname, args);
    LoopRbChain(entdata);
    acutRelRb(args);
    acutRelRb(entdata);
   }
   break;

  }
  tmp = tmp->rbnext;
 }
 return ;
}
Video Demonstration:

## 评论

**内容**: Sebastian Schoeller said...
Hello Madhukar,
thanks for your post.
Is it possible to retrieve/copy for example solid entities from an attached NWC coordination model in AutoCAD?
Best
Sebastian
Reply
10/24/2017 at 12:08 PM

---
**内容**: Madhukar Moogala said in reply to Sebastian Schoeller...

Typepad HTML Email

Hi Sebastian,
 
I’m sorry for delay, didn’t notice your comment.
 
NWC is just an underlay in AutoCAD unlike xref, reading the underlay database and extracting the solids is not possible at present.
 
-Madhukar
Reply
10/31/2017 at 01:34 AM

---
**内容**: gmail said...
thanks for this sharing, i am a newbie and this blog is really helpful for me!
Reply
09/19/2022 at 06:39 PM

---
**内容**: mapquest directions said...
With its turn-by-turn directions and real-time traffic updates, you can avoid getting lost or stuck in traffic.
Reply
04/25/2023 at 08:21 PM

---
