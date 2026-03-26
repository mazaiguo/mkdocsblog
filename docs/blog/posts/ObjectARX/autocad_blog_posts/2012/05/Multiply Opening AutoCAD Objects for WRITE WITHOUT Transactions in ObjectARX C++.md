---
title: "Multiply Opening AutoCAD Objects for WRITE WITHOUT Transactions in ObjectARX C++"
date: 2012-05-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - ObjectARX
description: "Remembering to close an Object after you have opened it in AutoCAD can be a pain, that's why we gave you the AcDbObjectPointer class template. Howe..."
author: Autodesk
---
# Multiply Opening AutoCAD Objects for WRITE WITHOUT Transactions in ObjectARX C++

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/multiply-opening-autocad-objects-for-write-without-transactions-in-objectarx-c.html

## 文章内容

by Fenton Webb
Remembering to close an Object after you have opened it in AutoCAD can be a pain, that's why we gave you the AcDbObjectPointer class template. However, what if you want the same autoclosing functionality, but with the added ability to multiply open objects for write just like you get with Transactions?
Introducing The all new AcDbSmartObjectPointer Template Class!!!
Declared in dbobjptr2.h, this class is protocol-compatible with AcDbObjectPointer (so you can just replace AcDbObjectPointer with AcDbSmartObjectPointer) and has the added capability to avoid open conflicts to access an object when given an object id, in addition to the longstanding capability to always "close" an object or at least revert it to the open state it was in prior to being assigned to the pointer.
AcDbSmartObjectPointer works by NOT opening an object at all if it's open state is already what was requested, or even closing an object multiple times before opening in the desired manner. It also treats kForNotify and kForRead in the same manner, which is effectively kForRead. While this doesn't make the class foolproof, it does eliminate open conflicts cause of failure to obtain access to objects.
Some of the remaining conditions that can still cause failure to open are as follows, indicated by the associated errors:
eNotThatKindOfClass Returned when the specified object id points to an object that is not the specified class.
ePermanentlyErased Returned when the specified object id has no underlying object, whether due to undo of creation or erase/delete.
eObjectWasErased Returned if the object is erased and the openErased flag is false.
eNullObjectId Returned when the input object id is null.
eWasNotifying Returned when the specified object is currently closing from kForWrite mode, is sending notification and kForWrite mode is requested again. At that point undo recording has been done, and all reactors get to see the same object state. The workaround for this status is to record that the notification happened then wait until the AcDbObject::objectClosed(AcDbObjectId) callback is made, at which point the object can be opened for write.
Like AcDbObjectPointer, this template can also "acquire" non-database-resident (NDBR) objects and previously open objects, which it will close just once. If the DBOBJPTR_EXPOSE_PTR_REF option is enabled, then accessing the object pointer member disables the template's ability to symmetrically close or revert the object. Instead it is closed once, and the caller is responsible for it afterwards.
All members of this template have the same description and semantics of AcDbObjectPointer's corresponding members, except that open conflicts are eliminated.
One note before I leave this little topic, just to say that it is not always good to modify an object when another caller has it open for write. However, if you do want to use instances of this class to obtain read or write access to objects that it may already have open and knows that the interaction is safe, then use of this class is highly recommended by me.

## 评论

**内容**: Owen Wengerd said...
This sounds like a bad idea to me. It might be useful in very specific cases, but especially for inexperienced programmers this will not only encourage poor programming practice, but make the resulting problems more difficult to diagnose. I see very little benefit and a lot of potential downside.
Reply
05/23/2012 at 09:28 AM

---
**内容**: Fenton Webb said...
I hear you Owen, good points.
But remember, this is an ObjectARX only template class which already requires significant expertise to use.
For those people who require this functionality it creates a very excited jumping up and down celebration!
Reply
05/23/2012 at 11:01 AM

---
