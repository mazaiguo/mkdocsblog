---
title: "Create a leader attached MText"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - API
  - Database
  - Unicode
description: "When we create a leader with attached MText, the main API is attachAnnotation , this function will only work if both the AcDbLeader and the AcDbMTe..."
author: Autodesk
---
# Create a leader attached MText

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/create-a-leader-attached-mtext.html

## 文章内容

By Virupaksha Aithal
When we create a leader with attached MText, the main API is attachAnnotation , this function will only work if both the AcDbLeader and the AcDbMText are database resident. So we first create a leader and post it to database, then open the leader object and invoke  attachAnnotation to attach the mtext. Below is an example that does this
void CreateLeaderAttachText(void)
{
    ads_point adspt1, adspt2, entpt;
      if(acedGetPoint(NULL,_T("\nSelect first point "),
                                            adspt1) != RTNORM)
        return;
      if(acedGetPoint(NULL,_T("\nSelect Second point "),
                                            adspt2) != RTNORM)
        return;
      AcGePoint3d point1, point2;
    point1.set(adspt1[0],adspt1[1],0.0);
    point2.set(adspt2[0],adspt2[1],0.0);
      AcDbDatabase *pDb =
      acdbHostApplicationServices()->workingDatabase();
      //get model psace id
    AcDbObjectId modelId;
    modelId = acdbSymUtil()->blockModelSpaceId(pDb);
      AcDbBlockTableRecord *pBlockTableRecord;
    acdbOpenAcDbObject((AcDbObject*&)pBlockTableRecord,
                                    modelId, AcDb::kForWrite);
      AcDbObjectId mtextId;
      AcDbMText *pMtext = new AcDbMText();
    pMtext->setDatabaseDefaults () ;
    pMtext->setContents(_T("TEXT STRING"));
    pMtext->setLocation (point2);
    pBlockTableRecord->appendAcDbEntity(mtextId, pMtext);
      pMtext->close();
    AcDbObjectId leaderId;
    AcDbLeader *pLeader = new AcDbLeader();
    pLeader->appendVertex(point1);
    pLeader->appendVertex(point2);
      pLeader->setDatabaseDefaults(pDb);
      pBlockTableRecord->appendAcDbEntity(leaderId, pLeader);
    pBlockTableRecord->close();
    pLeader->close();
      acdbOpenObject (pLeader, leaderId, AcDb::kForWrite) ;
      pLeader->attachAnnotation(mtextId);
    pLeader->evaluateLeader();
    pLeader->close();
}

## 评论

**内容**: Owen Wengerd said...
Your code is unnecessarily closing the leader object then immediately re-opening it again. Also, I thought that evaluateLeader() is not needed immediately after attachAnnotation().
Reply
07/27/2012 at 06:50 AM

---
