---
title: "Exploding all entities in a selection set"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - Database
  - Selection
description: "Here is a sample code to explode all the entities in a selection set. Here we use the explode method of AcDbEntity class and the result of explode(..."
author: Autodesk
---
# Exploding all entities in a selection set

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/exploding-all-entities-in-a-selection-set.html

## 文章内容

By Balaji Ramamoorthy
Here is a sample code to explode all the entities in a selection set. Here we use the explode method of AcDbEntity class and the result of explode() is stored in a AcDbVoidPtrArray type. All the entities in AcDbVoidPtrArray are posted to a database and the original entity is erased.
static void AdskProject_EXPENT(void)
{
    ads_name ss;
    ads_name eName;
    AcDbObjectId objId;
    AcDbEntity* pEnt;
      if (acedSSGet(NULL, NULL,NULL,NULL,ss) != RTNORM)
        return;
      long i=0;
    acedSSLength(ss,&i);
      //explode all enities in the selection set
    for (int j=0;j<i;j++)
    {
        if(acedSSName(ss,j,eName) != RTNORM)
        {
            acedSSFree(ss);
            return;
        }
        acdbGetObjectId(objId,eName) ;
        acdbOpenAcDbEntity(pEnt,objId,AcDb::kForWrite);
          AcDbVoidPtrArray eSet;
        Acad::ErrorStatus es=pEnt->explode(eSet);
        if (es == Acad::eOk)
        {   
            pEnt->close();
              //delete the original entity
            acdbEntDel(eName);
              // Add the new entities to the db
            es=postToDatabase(eSet);
            if (es != Acad::eOk)
            {
                acutPrintf(L"\nFailed to append entites to database");
                acedSSFree(ss);
                return;
            }
        }
        else //self
            pEnt->close();
    }   
    acedSSFree(ss);
}
  static Acad::ErrorStatus postToDatabase(AcDbVoidPtrArray eSet)
{
    Acad::ErrorStatus es;
    AcDbBlockTable *pBtbl;
    AcDbBlockTableRecord *pBtblr;
    es =acdbHostApplicationServices()->workingDatabase()
                        ->getSymbolTable(pBtbl, AcDb::kForRead);
    if (es != Acad::eOk)
    {
        acutPrintf(L"\nFailed to open block table");
        return es;
    }
    es=pBtbl->getAt(ACDB_MODEL_SPACE, pBtblr,AcDb::kForWrite);
    if (es != Acad::eOk)
    {
        acutPrintf(L"\nFailed to open block table record");
        es =pBtbl->close();
        if (es != Acad::eOk)
        {
            acutPrintf(L"\nFailed to close block table");
        }
        return es;
    }
      es =pBtbl->close();
    if (es != Acad::eOk)
    {
        acutPrintf(L"\nFailed to close block table");
        return es;
    }
      for(int i=0; i < eSet.length(); i++)
    {
        AcDbObjectId ObjId;
        AcDbEntity *pNewEnt=AcDbEntity::cast((AcRxObject*)eSet[i]);
        es=pBtblr->appendAcDbEntity(ObjId, pNewEnt);
        if (es != Acad::eOk)
        {
            acutPrintf(L"\nFailed to append entity");
        }
          es=pNewEnt->close();
        if (es != Acad::eOk)
        {
            acutPrintf(L"\nFailed to close entity");
        }
    }
      es=pBtblr->close();
    if (es != Acad::eOk)
    {
        acutPrintf(L"\nFailed to close block table record");
    }
    return es;
}

## 评论

**内容**: petcon said...
必须要说这个印度孩子老是不上心
use _T("") or ACRX_T("")
DO NOT USE L
Reply
06/06/2012 at 10:08 PM

---
**内容**: Madhukar Moogala said in reply to petcon...
Hi petcon,
There is nothing wrong with using 'L' in the above code.
We migrated AutoCAD to Unicode in the 2007 release. At that time, _T (or similar) was recommended to allow developers to support MBCS and Unicode from the same codebase. But the last MBCS version of AutoCAD (AutoCAD 2006) has long since retired (and is now sitting on a beach sipping pina coladas :-).
If you really want to support very old AutoCAD versions, then by all means continue using _T. That is a decision based on the needs of your customers and the effort it takes you to maintain that support. But if you don't want to support those old MBCS versions then using L is fine.
The ADN DevTech team support the previous three product releases - and focus the majority of our effort on the latest release - so we're not going to be generally considering backward support beyond that in code we post here.
You are, of course, very welcome to comment on legacy support issues for the benefit of other readers. But we won't be updating code in our blogs posts as a result of such comments.
And thank you for contributing your comments to this blog.
Cheers,
Stephen
Reply
06/07/2012 at 11:05 AM

---
**内容**: Owen Wengerd said in reply to Madhukar Moogala...
There's also an argument for using _T to make code easier to migrate forward to future versions of AutoCAD that use UTF-32 or some such future string format.
Reply
06/07/2012 at 11:32 PM

---
**内容**: petcon said...
ok i just want to say my way is better
i can not ask u to do any thing
Reply
06/07/2012 at 10:22 PM

---
**内容**: Qu Chang said...
Hello:
I use your code and release an arx file runing on AutoCAD2012,when enter this explode command,It breaked down and poped up a massagebox:Unhandled Access Violation Reading......
Please tell me why is that?(I'm sure that I set up my arx project correctly.....)
Or this API
ACDB_PORT ADESK_SEALED_VIRTUAL Acad::ErrorStatus explode(
AcDbVoidPtrArray& entitySet
) const;
is not compatible with AutoCAD2012？
Reply
03/26/2016 at 03:16 AM

---
