---
title: "open, update and save a file silently"
date: 2012-06-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - DWG
  - Database
description: "How to open a drawing and save it to another location without displaying it in the Acad window ?"
author: Autodesk
---
# open, update and save a file silently

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/open-update-and-save-a-file-silently-.html

## 文章内容

By Xiaodong Liang
Issue
How to open a drawing and save it to another location without displaying it in the Acad window ?
Solution
You can use AcDbDatabase::readDwgFile() and AcDbDatabase::saveAs() to accomplish this. When you do saveAs(), you can specify any local or mapped network drive and directory as you desire, given that you have write-access to the destination and the file is not opened by AutoCAD or any other application. If the file exists, saveAs() will overwrite it quietly without any warning if no one else is operating on it. Therefore, precaution must be taken so that data is not mistakenly lost.
The code snippet of an ARX below assumes a drawing "c:\temp\In.dwg" exists. It reads the dwg, adds one circle and save as to a new drawing silently.
 // save as silently
static void mySaveAs()
{
    AcDbDatabase* pDb = new AcDbDatabase(Adesk::kFalse);
    Acad::ErrorStatus es =
           pDb->readDwgFile(L"c:\\temp\\In.dwg");
    assert(es == Acad::eOk);
         // get the block table
         AcDbBlockTable *pBlockTable;
          es = pDb->getBlockTable(pBlockTable,
                                AcDb::kForRead);
         if (es != Acad::eOk)
         {
              return;
         }
         // get model space
         AcDbBlockTableRecord *pBlockTableRec;
         es = pBlockTable->
             getAt(ACDB_MODEL_SPACE, pBlockTableRec,
             AcDb::kForWrite);

         if (es != Acad::eOk)
         {
             pBlockTable->close();
              return;
         }

        pBlockTable->close();
        // create a new entity
        AcDbCircle *pCircle =
            new AcDbCircle(AcGePoint3d(0,0,0),
            AcGeVector3d(0,0,1),100);

        // add the new entity to the model space
        AcDbObjectId objId;
        pBlockTableRec->appendAcDbEntity(objId, pCircle);

        // close the entity
        pCircle->close();
        // close the model space block
        pBlockTableRec->close();
          // save as to the new drawing
        es = pDb->saveAs(L"c:\\temp\\Out.dwg");
        assert(es == Acad::eOk);
        delete pDb;
}

Notice if you use AcDbDatabase::saveAs() and the drawing exists and is currently open by AutoCAD, it will fail. The error code is eFileAccessErr. The ObjectARX documentation regarding this is incomplete. In addition, the document warns that if the database executing the saveAs() function is not the current database in the AutoCAD editor, then the thumbnail preview image is not saved to the file name you specified.
With the introduction of Accoreconsole , this becomes much easier. The following is a small demo to achieve the same effect as the above ARX does. It is just a script! And I found the thumbnail can also be saved with the drawing.
content of src file
;Command:
FILEDIA
;Enter new value for FILEDIA <1>:
0
;Command:
Circle
(100,100,0)
100
SaveAs
"C:\temp\Out.DWG"
;Command:
FILEDIA
;;;Enter new value for FILEDIA <1>:
1
It assumes a drawing "c:\temp\In.dwg" exists, the scr file is put to c:\temp and you have swtiched to the path of Accoreconsole, the command line of Windows could be:
C:\Program Files\Autodesk\AutoCAD 2013>accoreconsole /i "c:\temp\In.dwg"
/s "c:\temp\update.scr"
You can write a bat file to make it more flexible. Please refer to the DevTV on Accoreconsole

## 评论

**内容**: Vishnu Arunachalam said...
Awesome post. Found it extremely useful. A follow up question to your post. I am trying to store AutoCAD files into Azure Blob storage. Is there a way to store files to a cloud storage instead of a local or network drive?
Reply
12/07/2012 at 09:32 AM

---
**内容**: Le Manh Hung said in reply to Vishnu Arunachalam...
Can anyone help on this issue?
Reply
05/30/2016 at 07:52 PM

---
**内容**: draganst61@open.telekom.rs said...
Hello,
i try to create AcDbText object and change justify.
pstText->setAlignmentPoint(prPos);
pstText->setVerticalMode(AcDb::kTextVertMid);
pstText->setHorizontalMode(AcDb::kTextRight);
This don't work.
What is wrong.
thanks in advance.
Reply
10/02/2013 at 03:31 PM

---
**内容**: nizar akel said...
Hi
Can you help me with performing zoom extents before closing the file , exactly as you do in your example?
I need this to save as bmp file
Thanks
Reply
09/19/2014 at 12:04 AM

---
**内容**: gennady said...
Nice article.
I'm looking for file name from SaveAs dialog. Is it possible?
System variable DWGNAME still has original DWG name
Thank you,
GOK
Reply
01/10/2017 at 11:38 AM

---
