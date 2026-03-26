---
title: "acedSSGet - multi select in :N mode"
date: 2012-08-01
categories:
  - AutoCAD
tags:
  - Selection
description: "We have known acedSSGet can select nested entities with the argument :N. But in default, it supports single selection. If you select by window, no ..."
author: Autodesk
---
# acedSSGet - multi select in :N mode

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/acedssget-multi-select-in-n-mode.html

## 文章内容

By Xiaodong Liang
We have known acedSSGet can select nested entities with the argument :N. But in default, it supports single selection. If you select by window, no any nested entity is returned. If you select by cross, only one nested entity will be returned.
The following code is a solution:
static void multi-select_nested_entity()
{
// switch on the multi selection of nested entities
setAllowDuplicateSelection(curDoc(), true);   
curDoc()->inputPointManager()->turnOnSubentityWindowSelection();
  ads_name sset, eName;
AcDbObjectId id;
   // in the mode "_:n" 
 //
 if (RTNORM == acedSSGet(L"_:n", NULL, NULL, NULL, sset))
{
      acutPrintf(L"\n");
      long len = 0;
      acedSSLength(sset, &len);
      for (long i = 0; i < len; i++)
      {             
           resbuf *rb = NULL;
           //  ssnamex() returns all selected nested entities
           //  
           if (RTNORM == acedSSNameX(&rb, sset, i))
           {
                resbuf *rbWalk = rb;
                while (NULL != rbWalk)
                {
                     if (RTENAME ==
                         rbWalk->restype)
                     {
                          eName[0] =
                              rbWalk->resval.rlname[0];
                          eName[1] =
                              rbWalk->resval.rlname[1];
      if(Acad::eOk == acdbGetObjectId(id, eName))
                          {
                               acutPrintf(L"Entity %d: %x",
                                   i,
                                   id.asOldId());
                               AcDbEntity *pEnt;
                               if (Acad::eOk ==
                                   acdbOpenObject(pEnt,
                                   id,
                                   AcDb::kForRead))
                               {
                                 acutPrintf(L"(%s)\n",
                                pEnt->isA()->name());                           
                               pEnt->close();
                               }
                               else
                               {
                     acutPrintf(L"\nCouldn't open object");
                               }
                          }
                          //rbWalk = NULL; 
                     }
                     //else
                     {
                          rbWalk = rbWalk->rbnext;
                     }
                }
                acutRelRb(rb);
           }
      }
      acedSSFree(sset);
  } 
   // swtich off
  setAllowDuplicateSelection(curDoc(), false);
  curDoc()->inputPointManager()->turnOffSubentityWindowSelection();
}

## 评论

**内容**: Jeff Suffet said...
Is it possible to select multiple nested entities in VB.NET or C# Managed? Selecting 1 Nested Entity at a time is not really a good option...
Reply
01/08/2014 at 08:28 PM

---
**内容**: Kirill Zakharov said in reply to Jeff Suffet...
Yes. You can find the solution on .NET there: http://adn-cis.org/forum/index.php?topic=7683.msg25135#msg25135 made by Alexander Rivilis.
Reply
03/15/2017 at 01:42 AM

---
**内容**: Robophy said...
Mr.Liang
How to use the :$+:K mode?
there are have some entities,and want to remove sub entities from it by acedSSGet.
ACHAR* promptPtrs[2];
ACHAR KeyW[16]="Add Remove _A R";
promptPtrs[0]="Select Entity(Add)Or(Remove)):";
promptPtrs[1]="Select Entity(Remove)Or(Add)):";
acedSSSetFirst(NULL,NULL);//clear the pickfirst selection,
resbuf* (*oldFunc) (const ACHAR*);
acedSSGetKwordCallbackPtr(&oldFunc);
res=acedSSSetKwordCallbackPtr(keywordCallback);
res=acedSSAdd(NULL,NULL,ssname);//create a empty selection
res=acedSSAdd(NULL,NULL,ssname);//create a empty selection
for (.....)//add to selection and hlight
{
res=acedSSAdd(entname,ssname,ssname);
acedRedraw(entname,3);
}
res=acedSSGet(":$:K",promptPtrs,KeyW,NULL,ssname);//if i sel "R" keyword,ret -5001
Reply
11/07/2014 at 10:54 PM

---
