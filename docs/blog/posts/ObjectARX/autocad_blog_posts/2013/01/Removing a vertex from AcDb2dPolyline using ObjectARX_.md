---
title: "Removing a vertex from AcDb2dPolyline using ObjectARX?"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - C++
  - ObjectARX
  - Polyline
description: "Is there any way to remove a vertex from AcDb2dPolyline/AcDb3dPolyline (similar to AcDbPolyline::removeVertexAt() ) ?"
author: Autodesk
---
# Removing a vertex from AcDb2dPolyline using ObjectARX?

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/removing-a-vertex-from-acdb2dpolyline-using-objectarx.html

## 文章内容

By Fenton Webb
Issue
Is there any way to remove a vertex from AcDb2dPolyline/AcDb3dPolyline (similar to AcDbPolyline::removeVertexAt() ) ?
Solution
There is no analogous removal function for 2d and 3d polylines, mainly because the storage mechanisms are different.  AcDbPolyline more efficiently stores its vertices as an array within a single entity, whereas for 2d and 3d polylines, vertices are stored as separate entities.  Therefore, you will have to access an individual vertex entity and explicitly delete it; deletion doesn't occur through the 2d/3d polyline entity itself. Try following code snippet.
Look at the following code snippet: which will remove the first vertex.
void EraseVertex()
{
  ads_name name;  ads_point pt;
  // pick a polyline 2d
  int res = acedEntSel(_T("\nPick a 2dpolyline"), name, pt);
  // if ok
  if (res == RTNORM)
  {
    AcDbObjectId plineObjId;
    // convert the ename to an AcDbObjectId
    Acad::ErrorStatus es = acdbGetObjectId(plineObjId, name);    
      AcDbObjectPointer<AcDb2dPolyline> pPlineEnt(plineObjId, AcDb::kForRead);
    // if we have the right entity type
    if (pPlineEnt.openStatus() == Acad::eOk)
    {
      AcDbObjectIterator* pVertIter = pPlineEnt->vertexIterator();
      // select the 1st vertex in AcDb2dPolyline; regen to see change
      AcDbObjectPointer<AcDb2dVertex> pVertex(pVertIter->objectId(), AcDb::kForWrite); 
        // check to see if it is not already erased
      if (es != Acad::eWasErased)
      {
        Adesk::Boolean bErased = pVertex->isErased();
        if (!bErased)
          es = pVertex->erase();
      }
    }
    delete pVertIter; 
  }
}

## 评论

**内容**: Christian said...
Hi Fenton,
what I don't understand in your code is the check to see if a vertex was erased already. Does the 2d-Polyline not "let go" of Vertices that are erased? Does it keep the ObjectIds of aaaaall vertices it ever had?
The reason why I'm asking is because I've written a function SetPolyline2dCoordinates in .NET.. and I implemented it by erasing all existing vertices and then appending the new coordinates with AppendVertex.
Of course, when I read the vertices of a 2d-Polyline that I modified with SetPolyline2dCoordinates, I get "E_WAS_ERASED" errors etc.
I'd be glad if you could clarify things for me a bit :)
Thanks in advance!
Best Regards Christian
Reply
04/26/2013 at 03:34 AM

---
**内容**: Fenton Webb said...
Hey Christian
Actually, in this case it's probably over kill - that code was left over from the code that I ported this sample from. Apologies there...
That said, yes, all ObjectID's remain 'alive' in the DB even after being erased. That's because the operation can be undone, redone, and undone again - so it's much more efficient to store an 'erased' flag rather than the whole object in the undo filer
Reply
04/26/2013 at 08:54 AM

---
**内容**: Christian said...
Hi Fenton,
thanks for your reply. I see now why the object stays around, being marked as erased.
If you do have five minutes, I'd be glad if you could look over my two methods to get/set the coordinates/vertices of a Polyline2d-entity and tell me if that code is okay or downright wrong :D
http://pastebin.com/DCDWgg5b
Thanks in advance and Best Regards
Christian
Reply
04/28/2013 at 10:49 PM

---
**内容**: Fenton Webb said...
Hi Christian
as I have mentioned before in my Tools for the Job (starting at Part 3 Performance http://adndevblog.typepad.com/autocad/2012/07/the-right-tools-for-the-job-autocad-part-3.html) don't use StartTransaction() for utility functions. The overhead for calling StartTransaction() is huge, instead, use StartOpenCloseTransaction()
My personal preference is to use Open/Close directly.
Reply
04/29/2013 at 09:00 AM

---
**内容**: Christian said...
Hi Fenton,
okay, gotcha :) One last question (then I'll stop getting on your nerves :P): In part 5 of your blog series "The Right Tools for the Job" you mentioned that "The Transaction model (StartTransaction()) was invented way back when for a specific reason - transacting multiple writes on the same objects(s) and allowing layered rollbacks of these multi-write transactions."
Am I correct when I assume that multiple writes means writes to one object from multiple threads? As my application is purely single threaded, I think I could safely use StartOpenCloseTransaction everywhere...

Thanks for sharing your opinion!
Best Regards
Christian
Reply
04/29/2013 at 11:18 PM

---
