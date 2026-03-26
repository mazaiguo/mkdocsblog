---
title: "How to store an object ID into an Xrecord in an extension dictionary of another object?"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "The appended code does this exactly. Please note that we have to convert object ID to ads name when we set the result buffer to the xrecord, and vi..."
author: Autodesk
---
# How to store an object ID into an Xrecord in an extension dictionary of another object?

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/how-to-store-an-object-id-into-an-xrecord-in-an-extension-dictionary-of-another-object.html

## 文章内容

By Gopinath Taget
The appended code does this exactly. Please note that we have to convert object ID to ads name when we set the result buffer to the xrecord, and vise versa when we retrieve the result buffer. Please also make sure that we pass a reference to the first resbuf in the linked list to the setFromRbChain() function instead of the resbuf pointer.
int AddSoftpointerIntoXdict(AcDbObjectId id1,AcDbObjectId id2)
{
Acad::ErrorStatus retStat;
AcDbXrecord * pXrec=new AcDbXrecord;
AcDbDictionary *pDict﻿﻿=NULL;
AcDbObjectId dictid,xrecid;
AcDbSoftPointerId ﻿﻿SP(id2);
AcDbObject * pobj;
 struct resbuf * head=NULL;
ads_name adsName;
   if((retStat=acdbOpenObject(pobj,id1,AcDb::kForWrite))!=
  Acad::eOk)
  return 0;
  pobj->createExtensionDictionary();
dictid=pobj->extensionDictionary();
pobj->close();
  acdbOpenObject(pDict﻿﻿,dictid,AcDb::kForWrite);
  pDict﻿﻿->setAt(_T("TEST"),pXrec,xrecid);
pDict﻿﻿->close();
  acdbGetAdsName(adsName, id2);
head=acutBuildList(AcDb::kDxfSoftPointerId, adsName, 0);
  pXrec->setFromRbChain(* head);
pXrec->close();
acutRelRb(head);
   return 1;
}
    void AddInfo()
{
 int rt;
ads_name en1,en2;
ads_point pickpt;
AcDbObjectId id1, id2;
Acad::ErrorStatus retStat;
  rt=acedEntSel(
  _T("\nSelect an entity to reference the following entity: "),
  en1,pickpt);
 if(rt!=RTNORM)
  return;
retStat=acdbGetObjectId(id1,en1);
assert(retStat==Acad::eOk);
  rt=acedEntSel(_T("\nSelect an entity to be referenced: "),
  en2,pickpt);
 if(rt!=RTNORM)
  return;
retStat=acdbGetObjectId(id2,en2);
assert(retStat==Acad::eOk);
  acutPrintf(_T("\nid2=%ld"),id2);
rt=AddSoftpointerIntoXdict(id1,id2);
 if(rt==0)
  return;
}
    void GetInfo()
{
 int rt;
ads_name en1;
ads_point pickpt;
AcDbObjectId id1;
Acad::ErrorStatus retStat;
AcDbXrecord * pXrec=NULL;
AcDbDictionary * pDict;
AcDbObjectId dictid,xrecid;
 struct resbuf * rb;
AcDbObjectId tmpId=NULL;
  rt=acedEntSel(
  _T("\nSelect an entity attached extension dictionary:"),
  en1,pickpt);
 if(rt!=RTNORM)
  return;
  retStat=acdbGetObjectId(id1,en1);
assert(retStat==Acad::eOk);
AcDbObject * pobj;
retStat=acdbOpenObject(pobj,id1,AcDb::kForRead);
assert(retStat==Acad::eOk);
  dictid=pobj->extensionDictionary();
 if(dictid==AcDbObjectId::kNull)
{
  acutPrintf(_T("\nId is NULL."));
  pobj->close();
  return;
}
pobj->close();
  acdbOpenObject(pDict,dictid,AcDb::kForRead);
pDict->getAt(_T("TEST"),(AcDbObject * &)pXrec,AcDb::kForRead);
pDict->close();
pXrec->rbChain(&rb);
pXrec->close();
 if(rb==NULL)
  acutPrintf(_T("\nNull result buffer."));
 if (rb->restype == AcDb::kDxfSoftPointerId)
{
  acdbGetObjectId(tmpId, rb->resval.rlname);
  acutPrintf(_T("\nReferenced Id=%ld"),tmpId);
}
acutRelRb(rb);
}

