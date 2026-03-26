---
title: "When to Lock the Document"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - C++
  - COM
  - Database
description: "If your code is executed in the so-called document context, you do not have to lock the document. Therefore, when you execute a command that has be..."
author: Autodesk
---
# When to Lock the Document

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/when-to-lock-the-document.html

## 文章内容

By Xiaodong Liang
If your code is executed in the so-called document context, you do not have to lock the document. Therefore, when you execute a command that has been registered via acedDefun(),or when it has been registered via acedRegCmds->addCommand() without the ACRX_CMD_SESSION flag ( CommandFlags.Session in .NET), your code executes in document context. In this context, AutoCAD locks the current document for you and unlocks it when your function ends. If you have to access other documents in the document context, you have to lock the other documents 'manually'. You should register your command for the application context by using the ACRX_CMD_SESSION command flag ( CommandFlags.Session in .NET).
In any other context you have to lock the document you want to modify. This means you have to lock a document if your command is registered for the application context. This is by using the ACRX_CMD_SESSION flag on addCommand(), or in a message handler of a modeless dialog box where you have to modify database objects. If your application defines a COM interface and if you provide methods or properties where you have to change a document or objects, you have to lock a document, as well.
Following are small demos of ARX and .NET when you want to lock document in the command.
  ObjectARX:
//  define your command with ACRX_CMD_SESSION
acedRegCmds->addCommand(L"ADSK",L"MyTest",L"MyTest",ACRX_CMD_MODAL | ACRX_CMD_SESSION , MyTestARX);
//  add one circle to an non-active document
static void MyTestARX()
{
     AcApDocument* pActiveDoc = acDocManager-
                         >mdiActiveDocument(); 
      AcApDocumentIterator *pIter =
           acDocManager->newAcApDocumentIterator();
        // just select one non-active document   
     AcApDocument *pDocToDo = NULL; 
      for (;!pIter->done() ;
          pIter->step() )          
      {             
         if(pIter->document() != pActiveDoc)
         {
             pDocToDo = pIter->document() ;
             break;
         }
      }
        delete pIter;
       // lock the document
     // in default, the DocLockMode
     // is write enable.
     Acad::ErrorStatus es =
         acDocManager->lockDocument(
         pDocToDo
         /* AcAp::DocLockMode = AcAp::kWrite */ );
           if (es != Acad::eOk)        
         {    
            // fail to lock     
             return;
         }
           // return status:
         //  1. Acad::eOk if the lock change
         //     was successful.
         //  2. Acad::eLockChangeInProgress
         //    if an attempt to lock a document
         //    is made from the document lock
         //    change reactor  callback.
         //    You cannot "nest" locking requests.
         // 3. Acad::eVetoed
         //    if the lock change is vetoed by
         //    another application
         // 4. Acad::eNoDocument
         //      if pDoc is NULL.  
            AcDbDatabase* pDb = pDocToDo->database();
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
          // unlock the document
        es = acDocManager->unlockDocument(pDocToDo);
          if(es == Acad::eOk)
        {    
            // handle one document
            // successfully        
        }    
}
.NET
using AcadApp = Autodesk.AutoCAD.ApplicationServices.Application;
// modify value of 'TILEMODE ' of one document
[CommandMethod("MyTest", CommandFlags.Session)]
public void MyTestNet()
{
    foreach (Document doc in
        AcadApp.DocumentManager)
    {
        if (doc != AcadApp.DocumentManager.MdiActiveDocument)
        {
            // switch the active document
            AcadApp.DocumentManager.MdiActiveDocument = doc;
              // If you do not lock the document
            // then the below code just simply has no effect
            // whereas "doc.Database.TileMode =
            // !doc.Database.TileMode;" 
            // would even crash AutoCAD      
              // If you lock the document then both should
                work fine
            using (doc.LockDocument())
            {
                short tm =
                (short)AcadApp.GetSystemVariable("TILEMODE");
                AcadApp.SetSystemVariable("TILEMODE",
                                       (tm + 1) % 2);
            }
            break;
        }
    }
}

## 评论

**内容**: Toby.Rosenberg@CreativeCADSolutions.co.nz said...
Hi Xiadong
Would you mind sharing a bit of further insight into above?
I'm coming from the VB.NET corner and I have to admit that I never ever really understood when a document needs to be locked.
By trial and error I figured out that my functions in VB.NET were always working correctly when DOCUMENTLOCK was applied at the top level (i.e. the command calling them) but this seems to have been changed within AutoCAD 2013 because I get plenty of these lovely 'eViolation' messages all over the place but can't figure out why.
IOW: do I need to apply DOCUMENTLOCK at the lowest level (i.e. the actual functions doing changes to the document) or shall I apply it at the top level functions calling all these low level functions.
Would really appreciate some feedback from you, even if my question is plain stupid.
Cheers
Reply
07/02/2012 at 12:12 AM

---
**内容**: Xiaodong Liang said in reply to Toby.Rosenberg@CreativeCADSolutions.co.nz...
Hi Toby,
Sorry I was in a meeting and a vacation in the past days.
I converted the C# demo above to a VB.NET project and tested with AutoCAD 2013. All works well. I did not get such errors you described. Is there any more info that may help to recreate the issue? My environment is: Win7 64bits, VS2010, AutoCAD 2013 RTM. What I did is:
create a VB.NET class lib dll
add the references: acCoreMdg, acdbMgd, acMgd
create a command as below
_
Public Sub mytest()

Dim doc As Document
For Each doc In App.DocumentManager
If doc <> App.DocumentManager.MdiActiveDocument Then
App.DocumentManager.MdiActiveDocument = doc
myfun(doc)
Exit For
End If
Next
End Sub
Sub myfun(ByVal doc As Document)
Dim docLock As DocumentLock = doc.LockDocument()
Dim tm As Integer = App.GetSystemVariable("TILEMODE")
App.SetSystemVariable("TILEMODE", (tm + 1) Mod 2)
docLock.Dispose()
End Sub

And I think the code has answered your question: when you want to modify a document in the context of multi-documents, you need to lock it before modification. If you do not need to deal with it, you can unlock it.
Regards,
Xiaodong
Reply
07/14/2012 at 08:30 PM

---
**内容**: John Yan said...
Hi Xiaodong,
I work for a company that need help developing an ActiveX plugin for Navisworks 2011 through 2013.
Please let me know whether you are able to help.
thanks,
John
Reply
08/17/2012 at 03:35 PM

---
**内容**: Xiaodong Liang said in reply to John Yan...
Hi John,
I am not sure what you want to consult with, but I would suggest you raise the question on Autodesk forum:
http://forums.autodesk.com/t5/Autodesk-Navisworks-API/bd-p/600
probably the answers have existed, or other gurus could help. Our team also often offer a hand there.
In addition, the blogs for Navisworks are posted at:
http://adndevblog.typepad.com/aec/

Regards,
Xiaodong
Reply
08/19/2012 at 06:44 PM

---
**内容**: john keays said...
I am writing xrecords to an entity and found that I had to lock the drawing to get access to the xrecords through the object getobject function. Now should I then look at the return of the lock to see if it fails and then wait till it clears or just give up.
The simplest code is to lock for each xrecord read and unlock so that 1000 records will require 1000 lock/unlock sequences. How much resources would that take. I want to open up a list of entities in a table and then pan to each element by clicking on the line with the entity.
This would be best done with a modeless dialog. I am current using modal dialogs for each entity as it is selected from the database. Each xrecord has about 2 pages of information in custom dialog boxes done as modal dialog boxes.
What is current practice in this situation....?
Cheers john Keays
Reply
07/02/2015 at 12:11 AM

---
**内容**: Jason Huffine said...
In a program I'm working on, the command starts a service managed by a singleton object. It's using AutoCAD events (document and application level) to trigger different processes and stays active throughout the life of the AutoCAD session. It's in .NET. In situations like these where the command is no longer active and a Transactional process is triggerred through an event, is it safer to just lock the document?
Reply
03/15/2017 at 09:57 AM

---
**内容**: Ben said...
Hi there thank you for the article.
Reply
07/23/2017 at 08:01 PM

---
**内容**: Felix said...
能不能具体解释下为什么需要锁？
Reply
03/28/2018 at 03:35 PM

---
**内容**: new said...
is there any way use acedcommand in application context？ some api makes code execute in document context
Reply
04/02/2019 at 12:22 AM

---
