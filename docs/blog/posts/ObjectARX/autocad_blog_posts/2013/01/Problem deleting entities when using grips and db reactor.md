---
title: "Problem deleting entities when using grips and db reactor"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Database
  - Selection
description: "Problem scenario: You are using grips to modify entities that have database reactors attached to them in such a way that modifying them can cause o..."
author: Autodesk
---
# Problem deleting entities when using grips and db reactor

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/problem-deleting-entities-when-using-grips-and-db-reactor.html

## 文章内容

By Gopinath Taget
Problem scenario: You are using grips to modify entities that have database reactors attached to them in such a way that modifying them can cause other entities to be erased. Typically, you select several entities using grips, then modify one, causing the attached database reactor to delete one of the other selected entities. If you then try to pick any other selected entity, AutoCAD crashes. What could be going wrong and how can you work around this?
The root of the problem is that when using grips to modify objects, AutoCAD is creating an internal selection set that cannot be accessed or modified by the user called "PICKFIRST". The problem you are having is that when you erase one of the entities that is in a selection set of many, the code returns, but the selection of the rest of the entities are still active, meaning that the PICKFIRST selection set is still active. So when you pick an entity's grip, AutoCAD tries to update the selection set that contains a deleted entity...crash.
The only way to remedy this is to clear the selection set by way of the internal CANCELCMD command. This should be done immediately after any entities are ever removed from the PICKFIRST selection set. The use of CANCELCMD is relatively benign, and will not affect your code flow.
The following is a simple example showing this remedy inside a database reactor handler:
extern Adesk::Boolean acedPostCommand(const ACHAR*);
// global declaration required
void DbTestReactor::modified(const AcDbObject* pDbObject)
{
...
...
pEntity->erase();// Code to erase an entity
pEntity->close();// Code to close the entity
 // Code to cancel the internal selection set.
acedPostCommand(L"CANCELCMD");
...
}

