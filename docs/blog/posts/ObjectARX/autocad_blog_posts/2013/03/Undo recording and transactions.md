---
title: "Undo recording and transactions"
date: 2013-03-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "How does the Undo recording and transactions interact? The documentation seems to indicate that using transactions will result in smaller undo info..."
author: Autodesk
---
# Undo recording and transactions

发布日期: 2013-03-01

原始链接: https://adndevblog.typepad.com/autocad/2013/03/undo-recording-and-transactions.html

## 文章内容

By Xiaodong Liang
Issue
How does the Undo recording and transactions interact? The documentation seems to indicate that using transactions will result in smaller undo information.
Solution
The documentation states that when an object is open, it gets its own temporary Undo filer and Undo file. While the object is open, any modifications to that object are recorded to the object's temporary Undo file. If the object is canceled rather than closed, then this temporary Undo file is used to take the object back to the state it was in when it was opened. If the object is closed, then the undo information in the temporary Undo file is moved over to the
"global" document Undo file.
A transaction opens the object and holds it open until the outermost transaction is ended, at which time all the objects in the transaction are closed.Essentially, a transaction (or nested transactions) is the same as one long opening of the object. Therefore, if you were to simply open an object for write and keep it open for the same duration as you would have had it in a transaction, then there is certainly no savings in the Undo file by using a transaction.
Another issue that needs to be examined is the concept of partial undo recording versus full object state undo recording (autoUndo). When an object is opened for write and then its assertWriteEnabled() method is called with its autoUndo
argument set to True, the object's full state is recorded to undo (via
dwgOutFields()). If assertWriteEnabled() is called with autoUndo set to False, then the partial undo mechanism is used and undo only records whatever state information the object's partial undo mechanism gives it (the object's undoFiler() method is used to get a pointer to the undo filer and that filer's methods are then used to write out the desired state information). Most of all the AcDbObject and AcDbEntity level data (such as layer, linetype, color,
swapidWith(), etc.) is recorded via partial undo.
Once an object's full state has been recorded (as in a call to
assertWriteEnabled(true)), then, until the object is closed (or cancelled), no more full undo recordings will be made because one is all that is needed. This means that doing many operations on an object during one open close cycle rather than doing the operations over several open close cycles can result in much
smaller undo recording if a full object state undo recording happens in one of the first operations done to the object. Many of the operations done would have resulted in full state undo recording bcause transactions typically result in the object being opened once for many operations. This is how a transaction can
result in undo size savings.
One thing to keep in mind, though, is that partial undo recording will still be done throughout the time the object is open even if a full state recording was already made. This is necessary because events such as swapIdWith() involve changes to two objects so a full state recording of just one object is not enough (in the case of swapIdWith(), undo simply calls swapIdWith() to swap the
IDs back, so you can see that a full state recording of just one entity wouldn't do any good at all). So, if the operations done on an object while it is open are all doing partial undo recording, then there's no Undo file size savings between all the operations being done during one long open versus being spread out through several shorter open/close sessions.
If you use swapIdWith() on your transacted objects then please read on: When the outermost transaction is ended, the objects in the transaction are closed in the order they were added to the transaction. This means that all of the undo information for the first object added to the transaction is put into the "global" document undo file, then all of the second object's undo info, etc. This means that the undo information can be out of order with the actual sequence of modification events that occurred while the transaction was active.
Since an undo will undo everything done during the life of the outermost transaction, and most operations are entity specific, this is not usually a problem. But, there can be situations where this can be a problem. For example, using swapIdWith() and then erasing the "other" object in the swapIdWith() can cause
unexpected undo results if the circumstances are just right (or wrong depending on how you want to look at it).
The problem situation is:
1) start outermost transaction
2) get object A into the transaction
3) get object B into the transaction
4) call swapIdWith() on object B passing the id of A
5) erase object A
6) end transaction
7) execute the undo command to undo the transaction
What will happen is that when the transaction is ended, object A's undo info is moved to the global undo file, then object B's undo info is moved. But because the objects that are involved were both open for write throughout the whole sequence of events (for swapIdWith() this is only possible because the objects are open in a transaction which turns off the "exclusive open for write" that is
usually in effect) and the sequence of modification events was not "first do all modifications on object A and then do all modifications on object B", the global undo file ends up with information that is not in the order that the events actually occurred. When undo occurs, the undo information is processed in the reverse order from the way it was added to the undo file. The idea is to undo
in the reverse order of the way the operations were carried out - for example, undo newest to oldest operations. Therefore, in this case, when an undo occurs, the object B's undo information is processed first, which means that the swapIdWith() is undone first and then the erase is undone. BUT, this is not the reverse of the way these operations were actually carried out! And, the erase
undo information relies on the object's objectId in order to know which object needs to be unerased. Object A was the object erased, but since the swapIdWith() was undone first, the objectId that object A had when it was erased is now the objectId for object B, so the undo of erase will be carried out on object B!
This entire situation can be avoided by simply calling swapIdWith() on the object that will be erased. That way, the swapIdWith() and the erase() will both be in the same object's temporary undo file and they will be moved to the global undo file in their proper sequence order which means they will be undone in the proper order.

## 评论

**内容**: JeffH said...
Hi,
Just wanted to say thank you for nice explanation.
Reply
03/20/2013 at 06:40 AM

---
**内容**: Diego Ordonez said...
Hi.
What is the recommended approach to identify the features that have been erased/added/modified during an UNDO/REDO operation?
What event should I subscribe to detect these process ?
Thanks in advance
Diego.
Reply
03/31/2014 at 09:29 AM

---
