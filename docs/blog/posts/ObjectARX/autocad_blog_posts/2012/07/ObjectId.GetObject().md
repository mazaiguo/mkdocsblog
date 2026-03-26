---
title: "ObjectId.GetObject()"
date: 2012-07-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - Database
description: "Much of the sample code for the AutoCAD .NET API makes use of the Transaction.GetObject() method to open database-resident objects. Code that uses ..."
author: Autodesk
---
# ObjectId.GetObject()

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/objectidgetobject.html

## 文章内容

By Stephen Preston
Much of the sample code for the AutoCAD .NET API makes use of the Transaction.GetObject() method to open database-resident objects. Code that uses this method will look something like this:
[CommandMethod("test1")]
public static void  transtest1()
{
  Document doc = Application.DocumentManager.MdiActiveDocument;
  Database db = doc.Database;
  using (Transaction trans = db.TransactionManager.StartTransaction())
  {
    BlockTable bt =
        trans.GetObject(db.BlockTableId, OpenMode.ForRead) as BlockTable;
    foreach (ObjectId btrId in bt)
    {
      BlockTableRecord btr =
        trans.GetObject(btrId, OpenMode.ForRead) as BlockTableRecord;
      //Do something
    }
  }
}
However, there is a more succinct way to open an object in a transaction – using ObjectId.GetObject(). For some reason this function is often overlooked – perhaps because sample code writers prefer to emphasize that transactions are being used by showing the more explicit Transaction.GetObject(). The same code using ObjectId.GetObject() looks like this:
[CommandMethod("test2")]
public static void  transtest2()
{
  Document doc = Application.DocumentManager.MdiActiveDocument;
  Database db = doc.Database;
  using (Transaction trans = db.TransactionManager.StartTransaction())
  {
    BlockTable bt =
        db.BlockTableId.GetObject(OpenMode.ForRead) as BlockTable;
    foreach (ObjectId btrId in bt)
    {
      BlockTableRecord btr =
        btrId.GetObject(OpenMode.ForRead) as BlockTableRecord;
      //Do something
    }
  }
}
Under the hood (and as explained in the helpfiles) , the ObjectId.GetObject() method is calling the TransactionManager.GetObject() method on the topmost transaction. If there is no Transaction active, then an exception is thrown.
Of course, there are even more ways to open database-resident objects that we’ve discussed before on this blog. There is the Dynamic .NET introduced in AutoCAD 2013, and the (non-transaction)Open/Close technique (which is conveniently wrapped by the OpenCloseTransaction object if you want to not use transactions in exactly the same way as you’d use transactions ).

## 评论

**内容**: Anonymoose said...
As convenient as it may seem, something that only recently came to my attention is that Objectid.GetObject() is woefully inefficient. Each call to that method results in the creation of a managed wrapper for the owning database, followed by this:
Database.TransactionManager.TopTransaction.GetObject(...)
If you have code that makes a potentially huge number of calls to ObjectId.GetObject(), I would suggest changing it to call the TransactionManager's GetObject() method instead, as it is far more efficient.
Reply
07/06/2012 at 09:36 AM

---
**内容**: Madhukar Moogala said in reply to Anonymoose...
Thank you Tony. That is useful information. If you're performing a large (batch) operation that is tying up the user's machine while he waits then that is certainly a consideration. For that scenario, its also worth reading Fenton's comments on relative performance in the open/close article I referenced above. (But note that ObjectId.GetObject doesn't work with OpenCloseTransactions).
Its very different when you're writing a command that is requesting user input and performing a relatively small number of operations based on that input. In this case, the user is the bottleneck, and the speed of your code really doesn't matter (unless its incredibly slow) - and there are other ways to invest your time to make the user feel your application is fast - I'll write a quick post on that now.
Reply
07/06/2012 at 10:24 AM

---
**内容**: Tony Tanzillo said in reply to Madhukar Moogala...
Yes, as I mentioned in this thread over on the swamp (http://www.theswamp.org/index.php?topic=42197.0), casual use (for lack of a better term) is not a problem. But many of us write code that iterates over potentially-large selection sets or BlockTableRecords, and that's where it matters most.
Reply
07/06/2012 at 11:04 AM

---
**内容**: Madhukar Moogala said in reply to Madhukar Moogala...
And here is the post - http://adndevblog.typepad.com/autocad/2012/07/performance-perception-versus-reality.html.
Reply
07/06/2012 at 12:44 PM

---
