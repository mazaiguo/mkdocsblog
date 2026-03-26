---
title: "Two common mistakes with Transactions"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - Database
  - Forge
description: "Maybe this will turn into a series of common mistakes  ."
author: Autodesk
---
# Two common mistakes with Transactions

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/two-common-mistakes-with-transactions.html

## 文章内容

By Stephen Preston
Maybe this will turn into a series of common mistakes  .
My last post was about event handler exception handling, and Adam wrote a note about unknown commands. Now, here are two very common mistakes people make with Transactions when they first start using the AutoCAD .NET API that can waste hours of time debugging (and make you feel really stupid when you find them ).
Forgetting to commit a Transaction
I once spent hours as a young and innocent AutoCAD .NET programmer trying to work out why the entities I was trying to add to the database weren’t there after my code had run. The problem was simply that I’d forgotten to call Transaction.Commit() before I Disposed of the Transaction. An uncommitted Transaction is Aborted when it is Disposed, so every change you made to the Database in the Transaction is rolled back.
This is the first thing to check when something you expect to have been added to the database by your code isn’t there.
Forgetting to end a Transaction
A typical symptom of forgetting to end your Transaction before you return control to AutoCAD is that AutoCAD graphics will start to behave strangely. Often you’ll notice that the entity you just added to the drawing isn’t displaying at all. And when you close AutoCAD you’ll either see an error dialog, or the Visual Studio Output window will show a non-zero return value from acad.exe.
The best way to ensure you clean up your Transactions is to make use of the Using statement. Here is some very basic VB.NET to demonstrate:
    <CommandMethod("MyCommand")> _
    Public Sub MyCommand()
      Using tr As Transaction = db.TransactionManager.StartTransaction
        'Do stuff
        tr.Commit()
      End Using
    End Sub

## 评论

**内容**: Renbo said...
you need commit the transaction always, even it's just reading/querying data. Otherwise, there will be performance issue, especially in 3d layout. you may try the following code:
AcadDoc acadDoc = AcadCore.DocumentManager.MdiActiveDocument;
for (int i = 0; i < 1000; i++)
{
using (Transaction tran = acadDoc.Database.TransactionManager.StartTransaction())
{ }
}
It takes more than 20 seconds in 3D layout.
Reply
12/11/2014 at 05:41 PM

---
**内容**: Madhukar Moogala said in reply to Renbo...
Absolutely Renbo. Only abort (or fail to commit) a transaction when you specifically want to roll back the changes you made.
Reply
12/11/2014 at 09:26 PM

---
**内容**: BJHuffine said...
Just a little clarification please... Renbo was referencing committing a transaction even on read and said there would be performance impacts if not? You said yes, but references "changes". Is it really better to commit even on read (with no changes)?
Also (if you don't mind), if for example you have nested methods sharing a transaction, how would you know if it's been committed already without causing an InvalidOperationException from the internal/private Transaction.CheckTopTransaction() validation? Maybe I've overlooked a property, but I couldn't find one that would help.
Reply
04/15/2015 at 06:14 AM

---
**内容**: Ben said in reply to BJHuffine...
oh yeah it's better to commit even on read only.
TransactionManager.NumberOfActiveTransactions should do the trick.
rgds
Reply
12/13/2016 at 04:35 AM

---
