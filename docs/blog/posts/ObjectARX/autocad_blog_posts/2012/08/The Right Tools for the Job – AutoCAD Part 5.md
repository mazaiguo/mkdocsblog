---
title: "The Right Tools for the Job – AutoCAD Part 5"
date: 2012-08-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - C++
  - DWG
description: "Leading on from Part 4, and staying with ‘Performance’ I wanted to take a look at some .NET code and show you how to access the DWG database in the..."
author: Autodesk
---
# The Right Tools for the Job – AutoCAD Part 5

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/the-right-tools-for-the-job-autocad-part-5.html

## 文章内容

by Fenton Webb
Leading on from Part 4, and staying with ‘Performance’ I wanted to take a look at some .NET code and show you how to access the DWG database in the fastest way.
Over the years, I’m sure some of you have noticed how I like to write my DWG Database .NET in a very similar way to any code I write in ObjectARX, I try to only use Open/Close() unless I absolutely need to use Transactions.
The reason for this comes from my own personal experience and preferences:
Open/Close is faster than Transaction/StartTransaction
Open/Close can be more easily used in Event/Reactor callbacks, Transaction/StartTransaction can, but you need to really think about what you are doing
Open/Close is neater to write, in my opinion
That said, other members in my team, including the original author of our AutoCAD .NET API, prefer to use the Transaction model because it’s more Object Oriented.
Here’s some code which shows the differences between using Transaction/StartTransaction and Open/Close…
First the Transaction version, which I personally don’t normally like writing…
public void StartTransaction()
{
  Database db = HostApplicationServices.WorkingDatabase;
  ObjectId msId = SymbolUtilityServices.GetBlockModelSpaceId(db);
  TransactionManager tm = db.TransactionManager;
  using (Transaction trx = tm.StartTransaction())
  {
    BlockTableRecord btr = (BlockTableRecord)tm.GetObject(msId, OpenMode.ForRead);
      foreach (ObjectId id in btr)
    {
      Entity ent = (Entity)tm.GetObject(id, OpenMode.ForWrite);
      // do something
    } 
    trx.Commit();
  }
} 
Now my preferred way, Open/Close – see how much nicer it is?
public void OpenClose()
{
  Database db = HostApplicationServices.WorkingDatabase;
  ObjectId msId = SymbolUtilityServices.GetBlockModelSpaceId(db);
  using (BlockTableRecord btr = (BlockTableRecord)msId.Open(OpenMode.ForRead))
  {
    foreach (ObjectId id in btr)
    {
      using (Entity ent = (Entity)id.Open(OpenMode.ForWrite))
      {
        // do something
      }
    }
  }
}
Now I have shown the differences between the two styles, I should explain that there is actually two more additional styles of coding DWG database handling inside of AutoCAD.NET; that is Transaction.StartOpenCloseTransaction() and ObjectId.GetObject().
The Transaction.StartOpenCloseTransaction() style is exactly the same as the normal Transaction.StartTransaction(), except that it wraps the Open/Close mechanism in a Transaction object. When I show the performance differences further down, you will understand the reasons to use it, but in the meantime, here’s a quick look at the code – the only difference between the ‘StartTransaction’ function above and this one is the call to StartOpenCloseTransaction() instead of StartTransaction()…
[CommandMethod("StartOpenCloseTransaction")]
 public void StartOpenCloseTransaction()
{
   Database db = HostApplicationServices.WorkingDatabase;
   ObjectId msId = SymbolUtilityServices.GetBlockModelSpaceId(db);
   TransactionManager tm = db.TransactionManager;
   using (Transaction trx = tm.StartOpenCloseTransaction())
   {
     BlockTableRecord btr = (BlockTableRecord)tm.GetObject(msId, OpenMode.ForRead);
       foreach (ObjectId id in btr)
     {
       Entity ent = (Entity)tm.GetObject(id, OpenMode.ForWrite);
       // do something
     }
       trx.Commit();
   }
}
The ObjectId.GetObject() style utilizes the normal Transaction object mechanism, but this way gives you a slightly difference access point.
Why would you use ObjectId.GetObject() instead of Transaction.GetObject() I hear some of you ask – basically, the ObjectId.GetObject() obtains the top most transaction in the transaction stack, so it can save time when coding (no need to pass the transaction around) – that said it can cost a few extra CPU cycles to use which you can see affecting the results below.
I have to confess that the sample code above was obtained from an original version that “Jeff H” of TheSwamp.org created as part of his own performance testing that he posted. I really liked what he did (and others that read the same post can relate to it also) so I thought I’d use it here for my own benchmarking – Thanks Jeff H!
His original code had some little bugs in it which he actually pointed out himself; his code opened some objects for read and then those same objects, in different test functions, for write which probably made each test function slightly unfair to the other. I corrected those issues, and removed the extra “false, false” parameters from the Open() and GetObject() see the bottom for the code…
I recommend that you only ever open for write when you absolutely need too, otherwise you may be costing yourself valuable CPU cycles.
Now here are the test results – AutoCAD 2013, 55,000 entities in Model Space, each command run 5 times to average out any of my computer’s normal running tasks interference…
So it seems that StartOpenCloseTransaction(), in this test, even beats Open/Close on performance. It also seems that both of the normal ‘Transaction’ models StartTransaction() and ObjectID.GetObject() are significantly slower, but not much real difference between the two (0.3 of a second).
About The Transaction object in AutoCAD... The Transaction model (StartTransaction()) was invented way back when for a specific reason - transacting multiple writes on the same objects(s) and allowing layered rollbacks of these multi-write transactions.
Here’s what I recommend: If you guys are using StartTransaction(), and you don’t need the multiple write feature I just mentioned in the above paragraph, simply change your StartTransaction() to StartOpenCloseTransaction()…
Here are the actual results from the Command line.
“StartTransaction”
Command: STARTTRANSACTION
StartTransaction
1286338
Command:
STARTTRANSACTION
StartTransaction
1301005
Command:
STARTTRANSACTION
StartTransaction
1206838
Command:
STARTTRANSACTION
StartTransaction
1243078
Command:
STARTTRANSACTION
StartTransaction
1231894
“OpenCloseTransaction”
Command: OPENCLOSETRANSACTION
OpenCloseTransaction
511723
Command:
OPENCLOSETRANSACTION
OpenCloseTransaction
494753
Command:
OPENCLOSETRANSACTION
OpenCloseTransaction
495462
Command:
OPENCLOSETRANSACTION
OpenCloseTransaction
509738
Command:
OPENCLOSETRANSACTION
OpenCloseTransaction
491686
“OpenClose”
Command: OPENCLOSE
OpenClose
568263
Command:
OPENCLOSE
OpenClose
558977
Command:
OPENCLOSE
OpenClose
562863
Command:
OPENCLOSE
OpenClose
570294
Command:
OPENCLOSE
OpenClose
549607
“IDGetObject”
Command: IDGETOBJECT
IdGetObject
1606375
Command:
IDGETOBJECT
IdGetObject
1562226
Command:
IDGETOBJECT
IdGetObject
1571498
Command:
IDGETOBJECT
IdGetObject
1562189
Command:
IDGETOBJECT
IdGetObject
1527295
Here’s the code I used, I hope I didn’t introduce any bugs of my own – my eyes started to glaze over!! Thanks one more time Jeff H!
Random ran = new Random();
Stopwatch sw = new Stopwatch();
// code taken from original version written by "Jeff H"
[CommandMethod("StartTransaction")]
public void StartTransaction()
{
  int colorIndex = ran.Next(1, 256);
  Database db = HostApplicationServices.WorkingDatabase;
  ObjectId msId = SymbolUtilityServices.GetBlockModelSpaceId(db);
  Autodesk.AutoCAD.DatabaseServices.TransactionManager tm = db.TransactionManager;
  sw.Reset();
  sw.Start();
  using (Transaction trx = tm.StartTransaction())
  {
    BlockTableRecord btr = (BlockTableRecord)tm.GetObject(msId, OpenMode.ForRead);
      foreach (ObjectId id in btr)
    {
      Entity ent = (Entity)tm.GetObject(id, OpenMode.ForWrite);
      ent.ColorIndex = colorIndex;
    }
      trx.Commit();
  }
  sw.Stop();
  Application.DocumentManager.MdiActiveDocument.Editor.WriteMessage("\nStartTransaction\n");
  Application.DocumentManager.MdiActiveDocument.Editor.WriteMessage(sw.ElapsedTicks.ToString());
}
    [CommandMethod("OpenClosetransaction")]
public void OpenClosetransaction()
{
  int colorIndex = ran.Next(1, 256);
  Database db = HostApplicationServices.WorkingDatabase;
  ObjectId msId = SymbolUtilityServices.GetBlockModelSpaceId(db);
  Autodesk.AutoCAD.DatabaseServices.TransactionManager tm = db.TransactionManager;
  sw.Reset();
  sw.Start();
  using (Transaction trx = tm.StartOpenCloseTransaction())
  {
    BlockTableRecord btr = (BlockTableRecord)trx.GetObject(msId, OpenMode.ForRead);
      foreach (ObjectId id in btr)
    {
      Entity ent = (Entity)trx.GetObject(id, OpenMode.ForWrite);
      ent.ColorIndex = colorIndex;
    }
      trx.Commit();
  }
  sw.Stop();
  Application.DocumentManager.MdiActiveDocument.Editor.WriteMessage("\nOpenCloseTransaction\n");
  Application.DocumentManager.MdiActiveDocument.Editor.WriteMessage(sw.ElapsedTicks.ToString());
}
    [CommandMethod("OpenClose")]
public void OpenClose()
{
  int colorIndex = ran.Next(1, 256);
  Database db = HostApplicationServices.WorkingDatabase;
  ObjectId msId = SymbolUtilityServices.GetBlockModelSpaceId(db);
  sw.Reset();
  sw.Start();
  BlockTableRecord btr = (BlockTableRecord)msId.Open(OpenMode.ForRead);
  foreach (ObjectId id in btr)
  {
    Entity ent = (Entity)id.Open(OpenMode.ForWrite);
    ent.ColorIndex = colorIndex;
    ent.Close();
  }
  btr.Close();
  sw.Stop();
  Application.DocumentManager.MdiActiveDocument.Editor.WriteMessage("\nOpenClose\n");
  Application.DocumentManager.MdiActiveDocument.Editor.WriteMessage(sw.ElapsedTicks.ToString());
}
  [CommandMethod("IdGetObject")]
public void IdGetObject()
{
  int colorIndex = ran.Next(1, 256);
  Database db = HostApplicationServices.WorkingDatabase;
  ObjectId msId = SymbolUtilityServices.GetBlockModelSpaceId(db);
  Autodesk.AutoCAD.DatabaseServices.TransactionManager tm = db.TransactionManager;
  sw.Reset();
  sw.Start();
  using (Transaction trx = tm.StartTransaction())
  {
    BlockTableRecord btr = (BlockTableRecord)msId.GetObject(OpenMode.ForRead);
      foreach (ObjectId id in btr)
    {
      Entity ent = (Entity)id.GetObject(OpenMode.ForWrite);
      ent.ColorIndex = colorIndex;
    }
      trx.Commit();
  }
  sw.Stop();
  Application.DocumentManager.MdiActiveDocument.Editor.WriteMessage("\nIdGetObject\n");
  Application.DocumentManager.MdiActiveDocument.Editor.WriteMessage(sw.ElapsedTicks.ToString());
}

## 评论

**内容**: Khoa Ho said...
Excellent post! Nice work. Thank you.
Reply
08/10/2012 at 09:19 PM

---
**内容**: Fenton Webb said...
My pleasure, thanks Khoa!
Reply
08/10/2012 at 10:19 PM

---
**内容**: pseudonym said...
Hi Fenton and thanks for the in-depth performance data.
There is one major difference between the Open/Close mechanism and Transaction. When a transaction is disposed, if it was not previously comitted, it results in a call to every resident object's AcDbObject::cancel() memeber.
Conversely, when a DBObject is disposed, it will always result in a call to AcDbObject::close() committing any changes made.
So, in the case of using the Open()/Close() mechanism, what happens when an exception causes control to leave the using() block that disposes a DBObject that was acquired via ObjectId.Open(), was opened for write, and has already had some changes made to it prior to the point where the exception was raised?

Reply
08/11/2012 at 03:18 PM

---
**内容**: pseudonym said...
"Now my preferred way, Open/Close – see how much nicer it is?"
That's the problem with apples-to-oranges comparisons.
Your OpenClose() method and the StartTransaction() method shown above are not functionally-equivalent.
One rolls back changes to all objects that were modified in the foreach() loop in the event that an exception terminates the loop prematurely, while the other does not.
Reply
08/11/2012 at 03:43 PM

---
**内容**: Ben said in reply to pseudonym...
So does that mean when using the OpenClose() method, if an exception is thrown, the objects opened for write are not closed (and/or disposed)? I'm fairly new to the API so please forgive me if I asked something terribly inane or ignorant.
Reply
01/26/2016 at 02:27 PM

---
**内容**: Antonym said in reply to Ben...
"So does that mean when using the OpenClose() method, if an exception is thrown, the objects opened for write are not closed (and/or disposed)?"
No, it means that if an exception is thrown, the objects that were opened for write and were modified before the exception occurred are closed and the changes are committed to the database. With a transaction, if an exception occurs after changes are made to open objects, the changes are rolled back.
Reply
08/20/2017 at 12:34 AM

---
**内容**: Ben said in reply to Antonym...
Woa that is significant.
So basically if:
(1) you are using OpenClose, and
(2) you are WRITING - i.e. modifying or making some changes
(3) and an exception is closed
(4) ....then those changes still persist, even though, perhaps the entire transaction should be aborted and the changes rolled back!?

So if you want to be super safe when writing: use TransactionManager.StartTransction()?
Reply
04/27/2024 at 03:57 PM

---
**内容**: Fenton Webb said in reply to pseudonym...
Correct, you should consider this fact when coding this way
Reply
08/21/2017 at 08:14 AM

---
**内容**: Kerry Brown said...

For anyone who want to test this code :
The drawings used to test are at Reply #31
http://www.theswamp.org/index.php?topic=42399.0
Thanks to Jeff for the Sample.
Regards
Reply
08/11/2012 at 05:36 PM

---
**内容**: Sanjay Kulkarni said...
1. It seems you can get the database of current drawing in following two ways:
A.
Dim db As Database = HostApplicationServices.WorkingDatabase
B.
Dim doc As Document = _
Application.DocumentManager.MdiActiveDocument
Dim db As Database = doc.Database
Can you elaborate difference between the along with which is better when and why?
2. Also, the statement
Dim tm As TransactionManager = db.TransactionManager
causes following error:
'TransactionManager' is ambiguous, imported from the namespaces or types 'Autodesk.AutoCAD.DatabaseServices, Autodesk.AutoCAD.ApplicationServices'.
I have imported both the namespaces, hence this error.
When I change it to
Dim tm As _
Autodesk.AutoCAD.DatabaseServices.TransactionManager = _
db.TransactionManager
the error disappears.
Can you also explain the difference between two namespaces?
Thank you for any help.
Reply
08/12/2012 at 12:09 AM

---
**内容**: User48 said...
What about the massive list of warnings about these methods being obsolete? A speed gain today in exchange for major code reworking when these functions are discontinued?
Reply
08/13/2012 at 07:32 AM

---
**内容**: Autocad Training said...
Fenton Truely amazing...Thanks for Showing it in detail..Keep sharing and guide us.
Reply
05/01/2015 at 12:54 AM

---
**内容**: Ben said...
Hello Fenton thank you for your article:
"About The Transaction object in AutoCAD... The Transaction model (StartTransaction()) was invented way back when for a specific reason - transacting multiple writes on the same objects(s) and allowing layered rollbacks of these multi-write transactions."
I am new to the API and I don't understand what you mean by "multiple writes" and "layered rollbacks" - any clarification would be appreciated.
regards
Ben
Reply
01/26/2016 at 03:10 PM

---
**内容**: Chuck Yocum said in reply to Ben...
This means you can start a transaction in one method and do a bunch of writes all over your application and commit them all at once or roll them all back at once. You can also start another transaction within a transaction and commit or roll it back independently
Reply
02/10/2017 at 10:38 AM

---
**内容**: Chuck Yocum said in reply to Chuck Yocum...
Ben contact me independently and I can show you some things to look at if you still need help
Reply
02/10/2017 at 10:40 AM

---
**内容**: Fenton Webb said in reply to Ben...
Transactions allow you to open the same object for write, multiple times. Normal open for write does not allow this, you get an eWasOpenForWrite error message.
Layered rollbacks are when you nest Transactions, you can undo a pending transaction without affecting the encapsulating transation
Reply
08/21/2017 at 08:17 AM

---
