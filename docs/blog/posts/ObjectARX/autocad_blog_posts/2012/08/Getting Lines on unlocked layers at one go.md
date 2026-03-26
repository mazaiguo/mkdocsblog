---
title: "Getting Lines on unlocked layers at one go"
date: 2012-08-01
categories:
  - AutoCAD
tags:
  - Layer
  - Selection
description: "Recently a developer asked this question and here is the code snippet. The code snippet can be modified to fetch entities based on any such criteri..."
author: Autodesk
---
# Getting Lines on unlocked layers at one go

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/getting-lines-on-unlocked-layers-at-one-go.html

## 文章内容

By Balaji Ramamoorthy
Recently a developer asked this question and here is the code snippet. The code snippet can be modified to fetch entities based on any such criteria. The "acedssget" method can take filter in the form a result buffer. It can be formed using the "acutBuildList" method, but I havent used it in this code snippet since the layers that are unlocked are not known until we iterate the Layer table. Instead, the result buffer is created node by node based on the number of unlocked layer that we find.
resbuf* pLineResbuf;
resbuf* pIter = 0;
  wchar_t szLineBuff[] = L"LINE";
pLineResbuf = acutNewRb(0);
pIter = pLineResbuf;
pIter->resval.rstring = new wchar_t[wcslen(szLineBuff) + 1];
wcscpy(pIter->resval.rstring, szLineBuff);
  wchar_t szConditionBuff1[] = L"<OR";
pIter->rbnext = acutNewRb(-4);
pIter = pIter->rbnext;
pIter->resval.rstring = new wchar_t[wcslen(szConditionBuff1) + 1];
wcscpy(pIter->resval.rstring, szConditionBuff1);
  AcDbObjectId layerId = AcDbObjectId::kNull;
AcDbLayerTable* pLayerTable;
  AcApDocument *pActiveDoc = acDocManager->mdiActiveDocument();
AcDbDatabase *pActiveDB = pActiveDoc->database();
pActiveDB->getSymbolTable(pLayerTable, AcDb::kForRead);
  AcDbLayerTableIterator *pLayerTableIter = NULL;
pLayerTable->newIterator(pLayerTableIter);
pLayerTableIter->setSkipHidden(true);
for (; !pLayerTableIter->done(); pLayerTableIter->step())
{
    AcDbLayerTableRecord *pLTR = NULL;
    pLayerTableIter->getRecord(pLTR, AcDb::kForRead);
    TCHAR *lname;
    pLTR->getName(lname);
      if(pLTR->isLocked() == false)
    {
        pIter->rbnext = acutNewRb(8);
        pIter = pIter->rbnext;
        pIter->resval.rstring = new wchar_t[wcslen(lname) + 1];
        wcscpy(pIter->resval.rstring, lname);
    }
    pLTR->close();
}
delete pLayerTableIter;
pLayerTable->close();
  wchar_t szConditionBuff2[] = L"OR>";
pIter->rbnext = acutNewRb(-4);
pIter = pIter->rbnext;
pIter->resval.rstring = new wchar_t[wcslen(szConditionBuff2) + 1];
wcscpy(pIter->resval.rstring, szConditionBuff2);
  ads_name selectset;
acedSSGet(L"_X", NULL, NULL, pLineResbuf, selectset);
  long length=0;
acedSSLength (selectset, &length);
  acutPrintf(L"\nNumber of Entities: %d", length);
  for (int idx=0; idx<length; ++idx)
{
    ads_name entres;
    if(acedSSName(selectset, idx, entres) != RTNORM)
    {
          acedSSFree(selectset);
          return;
    }
      AcDbObjectId id;
    acdbGetObjectId(id, entres);
      AcDbObjectPointer<AcDbEntity> pEntity(id, AcDb::kForRead);
    acutPrintf(L"\nEntity: %s", pEntity->isA()->name());
}
  acedSSFree(selectset);
acutRelRb(pLineResbuf);

## 评论

**内容**: Anonymoose said...
Why go through all of that, when the acedSSGet() function supports the :L option which rejects objects on locked layers?
Are you kidding us or what?

Command: (ssget ":L")
Select objects: ALL
25012 found
2033 were on a locked layer.
Reply
08/26/2012 at 12:02 PM

---
**内容**: Balaji said...
Hello,
"Are you kidding us or what?"
No, I wouldnt dare to. :)
I did try the ":L" option which is undocumented but I could only get it to work when used along with the filter only select "_X" option. So decided to include all that info into the filter resbuf instead.
Yes, it is indeed lenghthier, but in my opinion it will help developers to modify that code to suit to their specific filtering criteria.
Reply
08/28/2012 at 05:04 AM

---
**内容**: Tony Tanzillo said...
Hi. The :L option seems to work for me regardless of whether using "_X" all filter or not, but it may have something to do with the local language you're using.
While this method is undocumented,I think that is only because no one has been asked to document it, and it is in very extensive use out here in the real world.
Not only that, but the managed PromptSelectionOptions class's ExcludeObjectsOnLockedLayers property is the public API for the :L option in the AutoCAD .NET api, which is documented.
Reply
08/30/2012 at 12:54 AM

---
