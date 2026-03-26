---
title: "Using ReadDwgFile with .NET AttachXRef or ObjectARX acdbAttachXRef"
date: 2012-07-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - C++
  - DWG
  - ObjectARX
  - XREF
description: "Some tips when using Database.ReadDwgFile() or AcDbDatabase::readDwgFile() in order to add an XRef to a side Database/AcDbDatabase…"
author: Autodesk
---
# Using ReadDwgFile with .NET AttachXRef or ObjectARX acdbAttachXRef

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/using-readdwgfile-with-net-attachxref-or-objectarx-acdbattachxref.html

## 文章内容

by Fenton Webb
Some tips when using Database.ReadDwgFile() or AcDbDatabase::readDwgFile() in order to add an XRef to a side Database/AcDbDatabase…
1) Whenever you use Database.ReadDwgFile() with AttachXref, never set the Database constructor with (buildDefaultDWG=True, noDocument=False) Database(True, False)
For a start, building a default DWG file when the next thing you do is read one that already exists is of course very inefficient, but when using AttachXref, you will probably get an ePermanentlyErased error (due to the incorrect use of the Database constructor) stopping the the AttachXref from working.
The noDocument parameter is intended to indicate that the Database DWG file has no associated Document window (like it would in AutoCAD) – so when reading a side database with ReadDwgFile it’s a good idea to set this to True so that the document handlers know to exclude this DWG Database, making it very quick to process. The downside to setting noDocument=True is that it bypasses the setup internal document functionality, like document locking and UNDO filing – this means that Transactions won’t work, so you will have to use Open/Close or StartOpenCloseTransaction instead of StartTransaction.
2) Always call Database.CloseInput() after a call to ReadDwgFile(). Calling CloseInput() ensures that the whole DWG file is read, and that no caching happens. It also releases the input file so that you can SaveAs() over the existing file.
3) When dealing with side databases, you may receive a eWrongDatabase error or AutoCAD may crash when disposing/freeing your Database/AcDbDatabase. This happens when AutoCAD is not expecting to be dealing with a database that is not associated with its current database list, or when AutoCAD wrongly decides that your side database is actually associated with its database list thus keeping a reference to the database. If this happens, you can set the working database yourself, but be *very careful* – make sure you set and reset the working database only where you need to do it, keep the redirection short and sweet and never forget to set it back.
Here’s a VB.NET example which shows what I am talking about
' test code to show how to use AttachXref with Database.ReadDwgFile
<Autodesk.AutoCAD.Runtime.CommandMethod("testXref")> _
Public Sub testXref()
    ' save old database
  Dim oldDb As Database = HostApplicationServices.WorkingDatabase
    ' when using ReadDwgFile, never specify True to buildDefaultDwg
  ' also, set noDocument=True because this drawing has no
  ' AutoCAD Document associated with it
  Using db As New Database(False, True) 
    db.ReadDwgFile("c:\temp\fenton.dwt",
                   FileOpenMode.OpenForReadAndWriteNoShare, True, "")
    ' closing the input makes sure the whole dwg is read from disk
    ' it also closes the file so you can SaveAs the same name
    db.CloseInput(True)
      ' now attach my xref
    Dim XrefObject As ObjectId = db.AttachXref("c:\temp\test.dwg", "test")
      ' ok time to set the working database
    HostApplicationServices.WorkingDatabase = db
    Using br As New BlockReference(New Point3d(0, 0, 0), XrefObject)
      br.SetDatabaseDefaults()
      br.Layer = "0"
      Using bt As BlockTable = db.BlockTableId.Open(OpenMode.ForRead)
        Using ModelSpace As BlockTableRecord =
          bt(BlockTableRecord.ModelSpace).Open(OpenMode.ForWrite)
          ModelSpace.AppendEntity(br)
        End Using
      End Using
    End Using
    ' reset it back ASAP
    HostApplicationServices.WorkingDatabase = oldDb 
    db.SaveAs("c:\temp\dwgs\XrefTest.dwg", DwgVersion.Current)
  End Using
  End Sub

## 评论

**内容**: Josh Dalton said...
Thankfully this was posted and indicated that closeInput() was necessary. The documentation with the 2014 ObjectARX says of closeInput:
"This function is intended for AutoCAD internal use. If used in ObjectARX applications, it may have undesirable results."
I chased a weird crash in our 2014 beta build, that happened somewhere in MDIGetActive during the activation of the next window we opened then closed, and could not find why it was crashing. I added the closeInput as you indicated here (previously not necessary in older acad versions), and now the code works again.
Reply
07/22/2013 at 08:24 PM

---
**内容**: Fenton Webb said...
Hey Josh!
there is some confusion I feel, basically it depends on the context... The above code is reading an external DWG file (which AutoCAD does not know about) - it's using the ObjectDBX layer (or RealDWG if using this code outside of acad.exe) - Closeinput() is fine to use. However, if the DWG file was loaded into AutoCAD you should never call CloseInput() as per the documentation because AutoCAD has control of the DWG file and is not expecting it.
Reply
07/23/2013 at 08:29 AM

---
**内容**: Josh Dalton said...
This was during our rename operation, where it downloads, updates the file in the background, but never truly opens it, and then closes it. Basically the sequence was:
setactivedrawing(newdwg)
readdwgfile(newdwg, filename)
do some work...
acdbsaveas2000()
delete newdwg
setactivedrawing(olddwg)
Which worked in acad 2008 without crashing, but fails in 2014. The new sequence in 2014 is:
setactivedrawing(newdwg)
readdwgfile(newdwg, filename)
newdwg->closeInput(true) //new code
setactivedrawing(OLDdwg); //new code
do some work...
acdbsaveas2000()
delete newdwg
Thank you for the clarification. I'm wondering if previously the deletion of newdwg took care of closing the input, and the new one does not, or if some events now require it to be closed earlier, but the key thing for me is obviously that it is working now. Thanks again!
Reply
07/24/2013 at 09:29 AM

---
**内容**: Rasmus Bugge said...
I also had crashes in 2014 when trying to export/wblockclone objects from working db to a side db. CloseInput and an OpenCloseTransaction did the trick (thanks!), although the ObjectARX doc says that such a transaction relies on the Transaction Manager's TopTransaction - however, there is no TopTransaction? (Also, I am having issues with the behaviour of the right click (!) after the export/wblockclone completes - it suddenly repeats the last command, instead of display the right click menu (although according to the right-click customization settings in OPTIONS, Acad is supposed to show the short cut menu in all "modes").
Reply
10/15/2013 at 07:27 AM

---
**内容**: James Morris said...
Thanks Fenton. Tip 3 helped with one of my problems. However I haven't been able to figure out another problem with using ReadDwgFile with .net. I posted the problem here http://forums.autodesk.com/t5/net/side-loading-a-dwg-with-readdwgfile-then-plotting/m-p/5840816#M46121. Basically I am plotting the result of the new db that was loaded. However all the layers are plotting regardless of their state(frozen or thawed). Do you have any suggestions?
Reply
10/01/2015 at 11:32 AM

---
**内容**: Luke Bingham said...
Great info Fenton. I'm not a super hacker with .Net and this was very useful but not quite on target with what I'm doing as the Database object doesn't seem to reveal AEC data objects. I'd like to be able to open a dwg on the side, inspect the styles it contains (SurfaceStyle, AlignmentStyles, etc) and copy them into the current drawing. I've looked all over and can't seem to find a relevant post. Any ideas?
Reply
12/24/2024 at 12:07 PM

---
