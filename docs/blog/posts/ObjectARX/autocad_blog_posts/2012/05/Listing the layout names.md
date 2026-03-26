---
title: "Listing the layout names"
date: 2012-05-01
categories:
  - AutoCAD C++
tags:
  - AutoLISP
  - C++
  - ObjectARX
description: "The layouts are stored in the dictionary "ACADLAYOUT". To find the available layouts in a drawing one has to iterate the dictionary "ACADLAYOUT" av..."
author: Autodesk
---
# Listing the layout names

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/listing-the-layout-names.html

## 文章内容

By Balaji Ramamoorthy
The layouts are stored in the dictionary "ACAD_LAYOUT". To find the available layouts in a drawing one has to iterate the dictionary "ACAD_LAYOUT" available in Root dictionary.
To manage and access the layouts, like making them active etc. AcApLayoutManager class should be used. To add and delete the layouts you can use AcDbLayoutManager class. The sample code below lists the number & names of all layouts in the drawing and also the active layout.
From Lisp you may list all the layouts in a drawing by calling (LayoutList) function.
Here is the ObjectARX sample code :
static void ADSProjectListLayouts(void)
{
    // A project created using the ObjectARX wizard
    // will already have this included.
    //#include "acaplmgr.h"
    //#include "dblayout.h"
      Acad::ErrorStatus es;
    AcDbDatabase *pDb
        = acdbHostApplicationServices()->workingDatabase();
      AcApLayoutManager *pLayoutMngr =
        dynamic_cast<AcApLayoutManager *>
            (
                acdbHostApplicationServices()->layoutManager()
            );
      //print the active layout
    acutPrintf(
                ACRX_T("\nActive Layout is : %s"),
                pLayoutMngr->findActiveLayout(Adesk::kTrue)
              );
      acutPrintf(
                ACRX_T("\nNumber of Layouts: %i\nList of Layouts:"),
                pLayoutMngr->countLayouts()
              );
      //print rest of the layouts. First get the layout dictionary
    AcDbDictionary *pDict = NULL;
    if (Acad::eOk
                == pDb->getLayoutDictionary(pDict,AcDb::kForRead))
    {          
        AcDbObject *pObj;
        ACHAR *pLayName;
        AcDbDictionaryIterator *pIter = pDict->newIterator();
          //Iterate through all the items in the dictionary
        for(;!pIter->done();pIter->next())
        {
            pIter->getObject(pObj,AcDb::kForRead);
            AcDbLayout *pLayout = AcDbLayout::cast(pObj);
              //The caller should not free the returned string.
            // Refer to ObjectARX documentation for getLayoutName
            es = pLayout->getLayoutName(pLayName);
              acutPrintf(ACRX_T("\n --> %s"),pLayName);
              pLayout->close();
        }
        //clean up
        delete pIter;
        pDict->close();
    }
}
Here is the .Net sample code :
[CommandMethod("ListLayouts")]
public static void ListLayoutsMethod()
{
    Document doc
        = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      LayoutManager layoutMgr = LayoutManager.Current;
      ed.WriteMessage
    (
        String.Format
        (
            "{0}Active Layout is : {1}",
            Environment.NewLine,
            layoutMgr.CurrentLayout
        )
    );
      ed.WriteMessage
    (
        String.Format
        (
            "{0}Number of Layouts: {1}{0}List of all Layouts:",
            Environment.NewLine,
            layoutMgr.LayoutCount
        )
    );
      using (Transaction tr
        = db.TransactionManager.StartTransaction())
    {
        DBDictionary layoutDic
            = tr.GetObject(
                            db.LayoutDictionaryId,
                            OpenMode.ForRead,
                            false
                          ) as DBDictionary;
          foreach (DBDictionaryEntry entry in layoutDic)
        {
            ObjectId layoutId = entry.Value;
              Layout layout
                = tr.GetObject(
                                layoutId,
                                OpenMode.ForRead
                              ) as Layout;
              ed.WriteMessage(
                String.Format(
                                "{0}--> {1}",
                                Environment.NewLine,
                                layout.LayoutName
                             )
                           );
        }
        tr.Commit();
    }
}

## 评论

**内容**: dba said...
hello, for the .net part of listing the names... iterating throught the layoutDictionary the DBDictionaryentry.Key already holds the Name of the Layout. Is there a particular reason to open the Layout object itself for this purpose? Just wondering...
(ACA 2014 - might be different in 2012)
BR,
Daniel
Reply
06/30/2015 at 05:49 AM

---
**内容**: Balaji said in reply to dba...
Hi Daniel,
Yes, the key should do if you are only after the names.
Thanks
Balaji
Reply
06/30/2015 at 10:50 PM

---
**内容**: dba said...
Hi Balaji,
thanks for the feedback, just wanted to be sure, there are no backdrafts :) I only need the names in my current situation.
BR,
Daniel
Reply
07/01/2015 at 12:23 AM

---
**内容**: Chris said...
Balaji,
Do you know of any way to get the list of layouts in the order the tabs are shown on-screen?
(eg) Layout1, Layout2, Layout10, Layout11
Autocad appears to return them in this order from this code:
Layout1, Layout10, Layout11, Layout2
Thanks!
Chris.
Reply
10/21/2015 at 04:51 AM

---
**内容**: Balaji said in reply to Chris...
Hi Chris,
Sorry for the delay in getting back to you.
The layout's tab order property should let you know that info.
Regards,
Balaji
Reply
10/24/2015 at 04:44 AM

---
