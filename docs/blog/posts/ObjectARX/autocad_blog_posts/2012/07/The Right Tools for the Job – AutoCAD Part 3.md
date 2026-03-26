---
title: "The Right Tools for the Job – AutoCAD Part 3"
date: 2012-07-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - AutoLISP
  - C++
description: "Leading on from Part 2 – it’s time to start looking at performance (finally)."
author: Autodesk
---
# The Right Tools for the Job – AutoCAD Part 3

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/the-right-tools-for-the-job-autocad-part-3.html

## 文章内容

by Fenton Webb
Leading on from Part 2 – it’s time to start looking at performance (finally).
Just so you understand where I’m going with this ‘Performance’ section – I’m going to start by giving you an overview of the different language performance by looking into what I consider a good generic test scenario for all of the languages, namely “Storing Data inside of AutoCAD”. I’ll be using Xrecords, Xdata and ObjectARX Custom Objects.
Then, in some following posts, I’m going to drill into ObjectARX and .NET specifically to provide you with all of the performance techniques that I think you should know. I’ll show you how to optimize your ObjectARX and .NET code so it runs the fastest way I know how. I won’t show any techniques for optimizing VBA or LISP as I figure it’s now common knowledge that if you use those languages you don’t really mind that much about performance.
Let’s first start by looking at the different languages API support that comes inside of AutoCAD which all related to “Storing Data inside of AutoCAD” topic…
As you can see, ObjectARX is the most versatile of them all providing the developer with all of the above. As you would expect with such a common API task, all of the other languages compare very nicely if you exclude Custom Objects and Persistent Reactor referencing.
If you are wondering what Persistent Reactor referencing is, let me explain. So in ObjectARX you can create Reactors (Events) that are persisted with the DWG file. These Persistent Reactors are implemented via a Custom Object which has special event functions that are specifically called when an event happens. You need to use Persistent Reactor referencing to setup the reactor link between the object that you want to receive the events from and to your Custom Reactor Object. A cheap trick I like to use when programming ObjectARX is to setup a hard pointer reference to some other object inside of AutoCAD using the Persistent Reactor referencing functionality. I mention it because you often want to link a data object to an entity using a hard pointer, so this is a cheap way to do it (rather than creating your own links internally to your objects), but it can cost a few extra CPU cycles when accessing the linked objects because AutoCAD sends wasted notifications to the linked object.
Now before you look below at the results, Stephen did mention that this was an old presentation. Looking at the old results I decided to go through and rerun all the tests so I could remember some more of the details. Here are some points you should be aware of:
Back then, the 64bit version of AutoCAD was not available so I had to create my own VB6 Out of Process test harness, whereas now days, simply running the same VBA code on 64bit AutoCAD gives the same results as the old VB6 exe.
I didn’t take care to fully optimize all of the code I wrote, however, I did tweak the Release mode ObjectARX compiler settings. I wanted to be fair to all of the languages, so I created fairly generic code that performs the same task in each language. Nevertheless, it works and I feel that it does give a good measure of relative performance between all of the languages.
If I remember right, all of the code was written for AutoCAD 2007. Rather than spend all my time migrating to AutoCAD 2013, I decided that the easiest path to rerunning the tests was to migrate the .NET and ObjectARX Visual Studio projects to run on AutoCAD 2011 64bit – AutoCAD 2011 64bit was the test platform on my HP Elitebook 8540w.
I’m not posting the code used for these tests now, because I don’t want people to focus on the code here, given that I will be discussing that in later posts.
Lastly, as with all computer programs, performance really depends what you are doing in your code, how you are doing it, which parts of your execution run as part of an API or actually inside of your own code and the computer you are running on. What I’m trying to say is that the actual speed of any computer program will vary – therefore you should take these results as a rough indicator, not as a definitive benchmark.
Enough details, let’s look at some data.
As I mentioned, there were three data storage categories that I ran my tests on:
Creating a Dictionary entry and storing an XRecord to it
Creating a Dictionary entry and and storing a Custom Object to it
Creating a Dictionary entry and storing XData to it
I created sample code for each language and ran them for 1 million cycles (performing the same operation 1 million times) with a timer routine which timed the whole process.
You’ll notice in the above slide that I have missed out the VB6/VBA (Out of Process) results – this is because they are *so* much slower than ObjectARX, .NET, VBA (In process) and LISP that if I were to apply the data to this slide you wouldn’t even see ObjectARX or .NET data showing up on the scale!
Check out why VBA developers needed to migrate their applications to VB.NET using COM Interop if they want to run on 64bit!
Of course, all of my tests showed that ObjectARX was significantly faster than all the other languages, no surprise there. That said, you can now clearly see why I don’t use Transactions in any of my sample code, it’s slower than Open/Close for both .NET and ObjectARX. I’ll dig into why this is in a later post.
What I found really surprising, is how well VBA (In Process 32bit) and LISP performed. Yes, .NET is about 5 times faster for this specific test benchmark, but considering that the time is only 75-80 seconds for 1,000,000 records, that’s pretty impressive. Looking into why this is happening, I can see that the reason is that most of the work is actually done under the hood by AutoCAD (C++ code), reinforcing my earlier point that it really depends on what you are doing whether you see dramatic (or not) resulting time differences.
The specific Xdata test I ran though, in my opinion, is not really a good real life benchmark because generally speaking Xdata will not be attached to a Dictionary entry that we just created. So I decided to run a pure test against attaching Xdata to an existing object. Surprisingly in my tests, attaching Xdata to an existing entity only gave slightly better results for .NET and ObjectARX 8 seconds instead of 9 for ObjectARX and 14 seconds instead of 15. 
Next I’m going to look into ObjectARX compiler settings, and show you what a difference the correct settings can make… I’ll address all of your performance questions as best I can in future posts, so keep them coming.
Read Part 4 here

## 评论

**内容**: Loic Jourdan said...
Hi Fenton,
what surprising me here are the poor performances of out-of-process method.
It reminds me a discussion I had with a colleague about the com-automation interface we had to develop, the point was to decide how high this interface had to be:
- exposing our custom objects methods and properties at a very low level as all Acad objects do
- exposing a higher level interface with only a set of high level methods processing more "business-oriented" stuffs.
The most important criteria was the development and maintenance cost (since we were a very small team) so we decided to expose only high level interface (in addition to limited custom object propertes for OPM support). We somewhat guessed that performances would be improved but I now much more realize how.
----
In my opinion, if a programmer cares of performances, he should take a special care of interop cost. I mean, even if C++/CLI interop is fast enough to allow .net programmers to use/call it with a very small performance cost, calling a P-Invoked or com-wrapped method in a million-times-loop seems not to be free.
Loic
Reply
07/23/2012 at 04:44 AM

---
**内容**: Michael Robertson said...
Interesting the statement about not using transactions since that is the way everything was taught to our office in an onsite ADN programming class. Are you suggesting to never use transactions if you want performance?
Reply
07/23/2012 at 04:51 AM

---
**内容**: Madhukar Moogala said in reply to Michael Robertson...
Hi Michael. Choice of programming language or API is always a trade-off. You need to decide what aspect is most important for you to optimize in a given situation.
I would continue to recommend use of Transactions in the AutoCAD .NET API. In absolute terms, they are still extremely fast and give you a lot of power to easily handle things like (for example) rolling back database changes if the user cancels a command midway through. That's *a lot* harder to deal with using open/close.
There may be some situations where you really need to save those extra few CPU cycles - in which case you may start thinking about using unmanaged C++ instead to save even more cycles. And then you get into other optimizations too - transactions aren't the only fruit in the orchard :-).
I'm looking forward to Fenton's next installment :-).
Reply
07/23/2012 at 02:35 PM

---
**内容**: Fenton Webb said...
Just to be clear about the COM interface being slow... It's not slow at all, in fact it's really fast.
What *is* slow is running the COM interface out-of-process.
About transactions - transactions were built for a specific need in ObjectARX, dealing with undos and large datasets. It has a big over head when all you are doing is 'tickling' the database.
The early versions of .NET did not have 'using' statements so diposing (closing) AutoCAD objects using Open/Close was confusing at best, but mostly caused lots of untraceable crashing to happen. Therefore, we decided to push the transaction model as it worked out much better for our .NET developers to use.
If you want to keep the transaction model in your code, but want a performance upgrade, simple change your StartTransation() to StartOpenCloseTransaction().
Reply
07/23/2012 at 09:51 AM

---
**内容**: Kevin said in reply to Fenton Webb...
Fenton,
Thanks for the blog. I followed your recommendation and swapped StartTransaction with StartOpenCloseTransaction, hoping to increase the performance of my plugin (this plugin is very large and makes heavy use of transactions because all sample code I could find did so).
After making these changes, my plugin completely stopped functioning. Is there some way for me to determine when it is safe to replace StartTransaction with StartOpenCloseTransaction?
A small sample of an instance where my code failed after the swap (first the error and stack trace, then the source for the function which failed):
Error: Exception: eWasOpenForWrite
at Autodesk.AutoCAD.DatabaseServices.Database.Insert(String blockName, Database dataBase, Boolean preserveSourceDatabase)
at Automotion.AutoPrice.AutoCAD.DynamicBlockHelper.AddDynBlockToDrawingFromFile(String BlockFilePath, String BlockName)
Public Shared Sub AddDynBlockToDrawingFromFile(BlockFilePath As String, BlockName As String)
Dim doc As Document = ApplicationServices.Application.DocumentManager.MdiActiveDocument
Dim ed As Editor = doc.Editor
Using lock As DocumentLock = doc.LockDocument()
Using tr = doc.TransactionManager.StartTransaction
Try
Dim dwgName As String = HostApplicationServices.Current.FindFile(BlockFilePath, ApplicationServices.Application.DocumentManager.MdiActiveDocument.Database, FindFileHint.Default)
Using db As Database = New Database(False, False)
db.ReadDwgFile(dwgName, IO.FileShare.Read, True, Nothing)
Dim takeBlkId As ObjectId
Using tbt As BlockTable = tr.GetObject(db.BlockTableId, OpenMode.ForWrite)
If (tbt.Has(BlockName)) Then
takeBlkId = tbt(BlockName)
db.WblockCloneObjects(New ObjectIdCollection(New ObjectId() {takeBlkId}), doc.Database.BlockTableId, New IdMapping(), DuplicateRecordCloning.Replace, False)
Else
doc.Database.Insert(BlockName, db, False)
End If
End Using
End Using
tr.Commit()
Catch ex As System.Exception
tr.Abort()
Try
EventLog.WriteEntry("NiC", "Error: " + ex.GetType().Name + ": " + ex.Message + Environment.NewLine + ex.StackTrace, EventLogEntryType.Error)
Catch eex As System.Exception
End Try
End Try
End Using
End Using
End Sub

So it seems that locking the document is not compatible with StartOpenCloseTransaction?
Thank you in advance.
Kevin
Reply
10/10/2014 at 09:59 AM

---
**内容**: Adam Davis said...
Hi Fenton,
You have always preferred not using transaction in .NET and I can see why.
I get not using transactions for modifying entities but how do you make an entity without a transaction? transaction.AddNewlyCreatedDBObject seems the only option.
Currently we are making a transaction at the beginning of one of out commands(and only at one level) and then as we don't want to have to pass that transaction around every sub routine we use
blockTableRecord.Database.TransactionManager.TopTransaction to get the transaction. Is there any issue with that?
Thanks
Adam
Reply
07/25/2012 at 02:46 AM

---
**内容**: Fenton Webb said...
Hey Adam
I'll show that all in the next post for you... I'll also show you what is slow and what is not...
Reply
07/25/2012 at 01:53 PM

---
**内容**: Yvon Bourgouin said...
We currently have an application which is creating many entities in the drawing. The memory use is growing exponentially and is not released until we close AutoCAD. Would using open/close would be better for us?
Reply
07/26/2012 at 06:11 AM

---
**内容**: Fenton Webb said in reply to Yvon Bourgouin...
It's hard to say without seeing the code but I doubt changing to open and close will make much memory difference.
If you are using .NET then a quick try would be to do a search and replace of all StartTransaction() calls and make them all StartOpenCloseTransaction(). Remember to always call Dispose on your AutoCAD.NET objects.
If you are using ObjectARX, you probably have a memory leak somewhere.
Reply
07/26/2012 at 09:32 AM

---
**内容**: Kerry Brown said...
I have a question
If StartOpenCloseTransaction() if the preferred operation why have we NOT seen it in any AutoDesk samples in the last 7 years ??
and another ..
>>[quote] Remember to always call Dispose on your AutoCAD.NET objects.
<<
would someone care to make a public definitive statement regarding the disposing of objects ?
... and is the process different when using
StartOpenCloseTransaction() ??
Regards
Kerry
Reply
07/28/2012 at 09:26 PM

---
**内容**: Fenton Webb said in reply to Kerry Brown...
Hey Kerry
it's preferred if you want to squeeze performance out of your code. The reason StartTransaction() is slower is because it does more things.
About Dispose... All of our .NET code wraps ObjectARX... Our ObjectARX code is single threaded... The .NET Garbage Collector runs on a background thread... If you don't call Dispose of our objects, you run the risk of the GC garbage collecting our objects on a background thread which may cause AutoCAD to crash, depending on what the dispose code does under the hood. If the dispose simply does a memory free then there's probably no issues, but if the dispose does other things like fire events, update UI, etc etc, then you are most likely looking at a crash.
I recommend you Dispose objects using the .NET 'using' statement (the ones you create in your code).
Reply
07/30/2012 at 10:35 AM

---
**内容**: Fenton Webb said in reply to Fenton Webb...
Kerry, I just posted this also on the subject:
http://adndevblog.typepad.com/autocad/2012/07/forcing-the-gc-to-run-on-the-main-thread.html
Reply
07/30/2012 at 04:31 PM

---
**内容**: David said...
Hello Fenton,
Is not having Undo the only downside for Open/Close transaction ?
It would be great to see a comparison, in detail, between
Transaction and Open/Close.
Regards,
David
Reply
12/11/2012 at 08:13 PM

---
**内容**: Fenton Webb said...
Hey David!
Open/Close has full access to UNDO - each opened entity has a method called cancel() which rolls back any changes. Problem with it is that you have to make the calls one by one, so transactions are usually preferred.
That said, it's should be totally possible to mix Open/Close with transactions, and for the Open/Close to be handled by a started transaction... It's been a while, but you should be able to start a transaction, then use Open/Close for your stuff, then commit the transaction. If you decide something went wrong, simply call abort() and everything should be rolled back, including the Open/Close objects.
Reply
12/12/2012 at 09:39 AM

---
