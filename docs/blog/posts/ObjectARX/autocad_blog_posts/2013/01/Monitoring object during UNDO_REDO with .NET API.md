---
title: "Monitoring object during UNDO/REDO with .NET API"
date: 2013-01-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - Database
description: "When an object is added, modified or deleted from the drawing, a common scenario consist in write that information to an XML file by using the Obje..."
author: Autodesk
---
# Monitoring object during UNDO/REDO with .NET API

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/monitoring-object-during-undoredo-with-net-api.html

## 文章内容

By Augusto Goncalves
When an object is added, modified or deleted from the drawing, a common scenario consist in write that information to an XML file by using the ObjectAdded and ObjectErased events of the database reactor. But when UNDO and REDO commands are used in between, these events did not work. Is there any way to handle this situation with reactors?
In this situation, two reactors need to be used, one is document reactor and the other is database reactor. For example, monitor two events of the document, CommandWillStart and CommandEnded to know when the UNDO/REDO command is going to start and when it ends. Then in the events of the current database, ObjectReappended and ObjectUnappended, make records what objects have been unappended or reappended.
Then in the CommandEnded event of the current document iterate through those recorded objects, check if some particular information you want and do any other operations if necessary such as updating your XML file.
Generally speaking, avoid manipulating objects and database in any events other than CommandEnded since the current database is most of times in a flux state and related objects are already in read/write mode.

## 评论

**内容**: joantopo said...
I am using this:
public static void callback_ObjectErased(object sender, ObjectErasedEventArgs e)
{
bool NoUndo= e.Erased;
if(NoUndo==true)
{
//object erased.
}
else
{
//UNDO
}
}
And it works.
ObjectErased event says: Triggered when an object is erased or unerased from a database.
Regards
Reply
08/26/2016 at 04:30 AM

---
**内容**: Augusto Goncalves said in reply to joantopo...
Thanks for sharing.
Reply
08/26/2016 at 05:52 AM

---
**内容**: Joan said...
I have noticed that ObjectErased event works fine when the object is unerased (this means that you erased it previously at some point), but if you create a polyline, for example and then you do multiple undos, the object dissapears but objecterased event is not triggered. This means that I also need to monitoring the CommandEnded event for undo command.
In fact, in the first case I have to check if objecterased event is triggered before CommandEnded when I call undo command.
I hope this to put a bool var within the ObjectErased event to not to execute the CommandEnded method then.
Reply
02/02/2017 at 07:50 PM

---
