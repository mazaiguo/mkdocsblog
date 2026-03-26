---
title: "Solids created with booleanOper() may crash AutoCAD on some PC's"
date: 2012-07-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - Database
  - Solid
description: "I'm using booleanOper() to merge some solids in the drawing. It seems to work fine, however, on some PC's the created solids may crash AutoCAD when..."
author: Autodesk
---
# Solids created with booleanOper() may crash AutoCAD on some PC's

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/solids-created-with-booleanoper-may-crash-autocad-on-some-pcs.html

## 文章内容

By Adam Nagy
I'm using booleanOper() to merge some solids in the drawing. It seems to work fine, however, on some PC's the created solids may crash AutoCAD when the user moves them.
Solution
Looking at your code I can see that you are not deleting the input solid from the database.
You should delete it, because booleanOper() removes the geometry of the input solid and you should not leave degenerate solids in the database:
static void ArxTestMyCommand1(void)
{
  AcDbDatabase * pDb =
    acdbHostApplicationServices()->workingDatabase();
  ads_name name;
  ads_point pt;
  AcDbObjectId id;
  AcDbObjectPointer<AcDb3dSolid> solids[2];
    for (int i = 0; i < 2; i++)
  {
    if (RTNORM != acedEntSel(L"\nSelect a solid", name, pt))
      return;
      acdbGetObjectId(id, name);
    solids[i].open(id, AcDb::kForWrite);  
  }
    // This will merge the geometry of the input solid (solids[1])
  // into the geometry of solids[0] and then erase the geometry of
  // the input solid (solids[1])
  solids[0]->booleanOper(AcDb::kBoolUnite, solids[1]);  
    // We should delete solids[1] otherwise we leave a solid with
  // degenerate geometry (i.e. zero geometry) in the database
  // and that could cause issues
  solids[1]->erase();
}

## 评论

**内容**: quiz said...
How can I speedup boolean operations (I use C#)? It's too slooooow (about 85% of all time in profiler)!
Reply
08/01/2012 at 04:38 AM

---
**内容**: Adam Nagy said...
Hi there,
One thing you could check is if the history recording is switched on for the solids that you are trying to perform boolean operations on. Maybe switching that off would help.
Apart from that I'm not sure what you could try. Boolean operations are computation intensive and because of that I'm not really surprised that your program spends the majority of its time there - depends on the complexity of the solids you are working with.
Sorry that I cannot help more.
Cheers,
Adam
Reply
08/10/2012 at 07:39 AM

---
