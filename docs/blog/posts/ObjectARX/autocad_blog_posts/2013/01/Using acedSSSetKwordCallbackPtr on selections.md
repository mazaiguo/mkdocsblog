---
title: "Using acedSSSetKwordCallbackPtr on selections"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - Selection
description: "This method allow a custom code to be executed when the user selects a keyword, which allow us include some additional keywords."
author: Autodesk
---
# Using acedSSSetKwordCallbackPtr on selections

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/using-acedsssetkwordcallbackptr-on-selections.html

## 文章内容

By Augusto Goncalves
This method allow a custom code to be executed when the user selects a keyword, which allow us include some additional keywords.
On the sample below, when acedSSGet() is called in a custom command, the user is able to use two new keywords: LInes to select all lines in the current drawing and CIRcles to select all circles. The callback function uses all possible return values.
First, check below the custom command, that register for the call back.
void MyCustomCommand()
{
  // save the old callback function
  resbuf* (*oldFunc) (const ACHAR*);
  acedSSGetKwordCallbackPtr(&oldFunc);
    // set own callback function
  acedSSSetKwordCallbackPtr(ssCallback);
  // let the user make a selection
  ads_name ss;
  // this is the keyword list
  // to use local and global keywords:
  ACHAR kwordlist[] = { _T("LInes CIRcles _ LInes CIRcles") };
    if (RTNORM != acedSSGet(_T("_:K"), NULL, kwordlist, NULL, ss)) {
    // cancel
  } else {
    acutPrintf(_T("\nDone."));
    acedSSFree(ss);
  }
  // restore old callback function
  acedSSSetKwordCallbackPtr(*oldFunc);
}
Now the callback that is executed when the keyword is selected:
// Callback function for acedSSGet()
resbuf* ssCallback(const TCHAR* kword)
{
  // kword contains the global keyword
  acutPrintf(_T("\nCallback: '%s'"), kword);
    // result to return
  // NULL: no changes on selection set
  resbuf *result = NULL;
    if (!wcscmp(kword, _T("LInes"))) {
    // select all lines (just for testing)
    AcDbObjectIdArray objIds;
    getLines(objIds);
    // create resbuf containing single
    // enames from object id array
    result = getResbuf(objIds);
  } else if (!wcscmp(kword, _T("CIRcles"))) {
    // select all circles (just for testing)
    AcDbObjectIdArray objIds;
    getCircles(objIds);
    // create resbuf containing a selection set
    ads_name ss;
    acedSSGet(_T("X"), NULL, NULL,
      acutBuildList(RTDXF0, _T("CIRCLE"), RTNONE),
      ss);
    result = acutBuildList(RTPICKS, ss, RTNONE);
  } else {
    // return an error message
    result = acutBuildList(RTSTR, _T("\nUnknown error"), RTNONE);
  }
  return result;
}
And finally some additional methods for this specific sample:
resbuf* getResbuf(AcDbObjectIdArray ids)
{
  resbuf *result = NULL, *temp1, *temp2;
  ads_name ename;
  int length = ids.length();
    for (int i = 0; i < length; ++i) {
    acdbGetAdsName(ename, ids[i]);
    temp2 = acutBuildList(RTENAME, ename, RTNONE);
    if (result == NULL) {
      result = temp2;
    } else {
      temp1->rbnext = temp2;
    }
    temp1 = temp2;
  }
    return result;
}
  void getLines(AcDbObjectIdArray& ids)
{
  // select all lines from model space
  // (without any error checking)
  AcDbBlockTable *pTable;
  AcDbBlockTableRecord *pModelSpace;
  AcDbBlockTableRecordIterator *pIter;
  AcDbEntity* pEnt;
    acdbHostApplicationServices()->workingDatabase()->
    getBlockTable(pTable, AcDb::kForRead);
  pTable->getAt(ACDB_MODEL_SPACE, pModelSpace, AcDb::kForRead);
  pTable->close();
  pModelSpace->newIterator(pIter);
  pModelSpace->close();
    for (; !pIter->done(); pIter->step()) {
    pIter->getEntity(pEnt, AcDb::kForRead);
    if (pEnt->isKindOf(AcDbLine::desc()))
      ids.append(pEnt->objectId());
    pEnt->close();
  }
    delete pIter;
}
  void getCircles(AcDbObjectIdArray& ids)
{
  // select all circles from model space
  // (without any error checking)
  AcDbBlockTable *pTable;
  AcDbBlockTableRecord *pModelSpace;
  AcDbBlockTableRecordIterator *pIter;
  AcDbEntity* pEnt;
    acdbHostApplicationServices()->workingDatabase()->
    getBlockTable(pTable, AcDb::kForRead);
  pTable->getAt(ACDB_MODEL_SPACE, pModelSpace, AcDb::kForRead);
  pTable->close();
  pModelSpace->newIterator(pIter);
  pModelSpace->close();
    for (; !pIter->done(); pIter->step()) {
    pIter->getEntity(pEnt, AcDb::kForRead);
    if (pEnt->isKindOf(AcDbCircle::desc()))
      ids.append(pEnt->objectId());
    pEnt->close();
  }
    delete pIter;
}

## 评论

**内容**: Robophy said...
hello, if the keyword is "Add" or "Remove",how to do it??
Reply
11/07/2014 at 05:40 AM

---
**内容**: Augusto Goncalves said in reply to Robophy...
You'll probably need to use ADd and REmove (with 2 letters on uppercase) for the keywords
Reply
11/07/2014 at 06:41 AM

---
**内容**: Robophy said...
tks for your idea, my problem is i want to remove sub entities form a existing entities use acedSSSet :$ +:k mode, i do this:
1,create a empey selection;
2,add existing entities to selection;
3,run acedSSGet(":$:K"......);
code:
int res;
ACHAR* promptPtrs[2];
ACHAR KeyW[16]="Add Remove _A R";
promptPtrs[0]="Select Entity(Add)Or(Remove))A" ;
promptPtrs[1]="Select Entity(Remove)Or(Add))R" ;
acedSSSetFirst(NULL,NULL);//clear the pickfirst selection,
resbuf* (*oldFunc) (const ACHAR*);
acedSSGetKwordCallbackPtr(&oldFunc);
res=acedSSSetKwordCallbackPtr(keywordCallback);
res=acedSSAdd(NULL,NULL,ssname);//create a empty selection
for (.....)//add to selection and hlight
{
res=acedSSAdd(entname,ssname,ssname);
acedRedraw(entname,3);
}
res=acedSSGet(":$:K",promptPtrs,KeyW,NULL,ssname);//if i sel "R" keyword ret -5001,it looks like none entity in the selection,why?
i had added to the selection(ssname). pls help me.tks
Reply
11/07/2014 at 11:21 PM

---
**内容**: Augusto Goncalves said in reply to Robophy...
Hi,
Can you please place your question on our forum? That will be the best way to help you: http://forums.autodesk.com/t5/objectarx/bd-p/34
In this case, it seems that you are using the built-in keywords, A and R... have you tried with different one?
Regards,
Augusto Goncalves
Reply
11/10/2014 at 08:16 AM

---
