---
title: "How to determine if an entity is going to be dragged or not?"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - Selection
description: "Consider this: When you pick on an entity, the AcDbEntity::getGripPoints() function is invoked and the grip points are drawn. The grip points remai..."
author: Autodesk
---
# How to determine if an entity is going to be dragged or not?

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/how-to-determine-if-an-entity-is-going-to-be-dragged-or-not.html

## 文章内容

By Gopinath Taget
Consider this: When you pick on an entity, the AcDbEntity::getGripPoints() function is invoked and the grip points are drawn. The grip points remain until any other AutoCAD command is issued or when Esc is pressed.
So, is there a way to check whether an entity is currently drawing its grip points or not?
One way of doing this is using acedSSGetFirst() and a Windows Hook.  Here's the relevant ARX code:
BOOL ArxWinHookFct (MSG *pMsg)
{
 // create a flag so that we don't call the function multiply
 static bool flag = false;
 // if not already processing
 if (!flag)
{
  // set that we are now processing
  flag = true;
  struct resbuf *grip_set = NULL, *ents = NULL;
  // get the pick first selection set
  int res = acedSSGetFirst(&grip_set, &ents);
  // if ok
  if (res == RTNORM)
  {
   long length = 0l;
   // make sure we have some fata
   if (ents != NULL)
   {
    // print out what we have
    acedSSLength(ents->resval.rlname, &length);
    acutPrintf (_T("\nLength ents = %ld"), length);
    acedSSFree (ents->resval.rlname);
   }
  }
    // ok, now we can flag that we have finished
  flag = false;
}
   // Return TRUE to destroy the message
 return (FALSE) ;
}

