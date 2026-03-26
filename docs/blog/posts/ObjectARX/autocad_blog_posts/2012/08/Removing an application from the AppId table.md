---
title: "Removing an application from the AppId table"
date: 2012-08-01
categories:
  - AutoCAD
tags:
  - Database
description: "To remove your application from the APPID table, you first have to obtain the table from the database (AcDbDatabase::getRegAppTable()). In order to..."
author: Autodesk
---
# Removing an application from the AppId table

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/removing-an-application-from-the-appid-table-1.html

## 文章内容

By Balaji Ramamoorthy
To remove your application from the APPID table, you first have to obtain the table from the database (AcDbDatabase::getRegAppTable()). In order to get the table entries (records) you have to initialize an table iterator and traverse through its records (AcDbRegAppTable::newIterator). From the iterator, obtain the records itself. Finally open it for write and use the erase() function to remove the record.
IMPORTANT: Use the following with care. Be sure to not unregister others' applications.
Here is the sample code :
// - AdskTest_DelRegApp command (do not rename)
static void AdskTest_DelRegApp(void)
{
    const ACHAR* name;
    Acad::ErrorStatus es;
      // Get the RegAppTable
    AcDbRegAppTable *pRegAppTable = NULL;
      AcDbDatabase* pDb = acdbHostApplicationServices()->workingDatabase();
    pDb->getRegAppTable(pRegAppTable, AcDb::kForRead);
      // Create an iterator of the RegAppTable
    AcDbRegAppTableIterator *it;
    es = pRegAppTable->newIterator(
                                    it,
                                    Adesk::kTrue,
                                    Adesk::kTrue
                                   );
    if(es == Acad::eOk)
    {
        pRegAppTable->close();
          // iterate through the RegAppTable
        while(!it->done() )
        {
            // get a RegAppRecord
            AcDbRegAppTableRecord *rec = NULL;
            if((es = it->getRecord(rec, AcDb::kForRead)) != Acad::eOk)
            {
                acutPrintf(acadErrorStatusText(es));
                delete it;
                return;
            }
              // print out some data
            rec->getName(name);
            acutPrintf(ACRX_T("\nAcDbRegAppTable : %s"), name);
            // ask user whether app should be unregistered
            if(getYesOrNo(ACRX_T("\nUnregister App ? ")))
            {
                // put the record in write status
                rec->upgradeOpen();
                rec->erase();   
            }
            rec->close();
            it->step();
        }
        delete it;   
          acutPrintf(ACRX_T("\nDone."));
    }
}
  static Adesk::Boolean getYesOrNo(const ACHAR* prompt)
{
    acedInitGet(RSG_OTHER, ACRX_T("Yes No"));
      ACHAR kword[255]; ACHAR pr[255];
    wsprintf(pr, ACRX_T("%s Yes/<No>"), prompt);
      if(acedGetKword(pr, kword) != RTNORM)
        return Adesk::kFalse;
      if(!_tcscmp(kword,L"Yes"))
        return Adesk::kTrue;
      return Adesk::kFalse;
}

## 评论

**内容**: Account Deleted said...
Double post:
http://adndevblog.typepad.com/autocad/2012/08/removing-an-application-from-the-appid-table-1.html
http://adndevblog.typepad.com/autocad/2012/08/removing-an-application-from-the-appid-table.html
?
Reply
08/10/2012 at 12:31 AM

---
**内容**: Balaji said in reply to Account Deleted...
Thank you :)
I removed the duplicate post.
Reply
08/10/2012 at 05:31 AM

---
