---
title: "What’s the meaning of getallobjects() in the context of nested transactions?"
date: 2012-08-01
categories:
  - AutoCAD C++
tags:
  - C++
  - Unicode
description: "Can you explain to me how getAllObjects() suppose to work in a nested transaction scenario? I can't find any related topics in the OARX Developer's..."
author: Autodesk
---
# What’s the meaning of getallobjects() in the context of nested transactions?

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/whats-the-meaning-of-getallobjects-in-the-context-of-nested-transactions.html

## 文章内容

By Philippe Leefsma
Q:
Can you explain to me how getAllObjects() suppose to work in a nested transaction scenario? I can't find any related topics in the OARX Developer's Reference/Guide.
A:
Let's say you have a scenario like this (in pseudo-code, all transactions are of AcDbTransaction type),
-
T1
    ...
    T1->getAllObjects();
    T2
        ...   
        T2->getAllObjects();
        T1->getAllObjects();
        T3
            ...
            T3->getAllObjects();
            T2->getAllObjects();
            T1->getAllObjects();
        end T3
        T2->getAllObjects();
    end T2
    T1->getAllObjects();
end T1
-
The AcDbTransaction::getAllObjects() method gets only those objects in the object list of the transaction on which the method is called. So, the real question is what objects are in a transaction's object list.
When an object is opened in a transaction (or a newly created object is added to a transaction), it can only be opened/added to the current transaction. So, in the above example, transaction T1 will only have objects that were opened/added before transaction T2 was created. Transaction T2 will only have objects that were opened/added after T2 was started, but before T3 was started. And, T3 will only have objects opened/added after it was started.
That covers what happens before any transaction is ended. When a nested transaction is ended, all the objects in that transaction are moved over to the transaction next up in the nesting. So, when T3 is ended, all its objects become part of T2's object list, and when T2 ends, all its objects become part of T1's object list.
So, within the above scenario,
-
T1
    ...
    T1->getAllObjects();            //only T1 objects
    T2
        ...   
        T2->getAllObjects();        //only T2 objects
        T1->getAllObjects();        //only T1 objects
        T3
            ...
            T3->getAllObjects();    //only T3 objects
            T2->getAllObjects();    //only T2 objects
            T1->getAllObjects();    //only T1 objects
        end T3
        T2->getAllObjects();        //both T2 and T3 objects
    end T2
    T1->getAllObjects();            //T1, T2 and T3 objects  
end T1
If you use the AcTransactionManager::getAllObjects() method, then you will get all objects from all transactions active at the time of the call.

