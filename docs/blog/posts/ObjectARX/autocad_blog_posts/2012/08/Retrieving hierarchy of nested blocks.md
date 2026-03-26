---
title: "Retrieving hierarchy of nested blocks"
date: 2012-08-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - Block
  - Selection
description: "I recently handled one case that wants to get the hierarchy of nested blocks if the nested entity is selected. This is similar to when you double c..."
author: Autodesk
---
# Retrieving hierarchy of nested blocks

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/retrieving-hierarchy-of-nested-blocks.html

## 文章内容

By Xiaodong Liang
I recently handled one case that wants to get the hierarchy of nested blocks if the nested entity is selected. This is similar to when you double click a block reference (BEdit), AutoCAD will provide you with the hierarchy of the blocks and ask you which one you want to edit.
We can use acedSSGet, passing :N as the argument. When we pick an entity within the block, the method acedSSNameX will return a resbuf which tells the information we need.
Following is from API help reference on acedSSNameX:
For entities selected by a pick point, information about the point will follow the GS marker information. The point information will be bracketed by an RTLB/RTLE pair 
The point information describes the pick point in a display independent manner. In a normal view this is done by describing an infinite line that passes through the actual pick point and is parallel to the users line of sight. In a perspective view, or a view with one clipping plane active, the line becomes a ray. If front and back clipping planes are on, the line becomes a line segment. 
To describe the line/ray/line-segment, a type descriptor, a point, and either a unit vector describing the direction of the infinite-line/ray or a vector describing the direction and distance to the other side of the line segment are used. 
The data items for a complete entity sublist involving a pick point selection are:
RTLB
start of entity data sublist
RTSHORT
selection method
RTENAME
picked entity's entity name 
RTSHORT
GS marker
RTLB
start of list for pick point
RTSHORT
point descriptor
RT3DPOINT
point descriptor
RT3DPOINT
vector describing direction of pick line or direction & distance to other end of line segment (only present if viewpoint is not plan WCS)
RTLE
end of list for pick point
RT3DPOINT
first of four points that provide a transformation matrix in the same format (and for the same purpose) as provided by acedNEntSel() (only present if :N option of acedSSGet() was used during selection)
RT3DPOINT
second of four points that provide a transformation matrix in the same format (and for the same purpose) as provided by acedNEntSel() (only present if :N option of acedSSGet() was used during selection)
RT3DPOINT
third of four points that provide a transformation matrix in the same format (and for the same purpose) as provided by acedNEntSel() (only present if :N option of acedSSGet() was used during selection)
RT3DPOINT
last of four points that provide a transformation matrix in the same format (and for the same purpose) as provided by acedNEntSel() (only present if :N option of acedSSGet() was used during selection)
RTENAME 
entity name of innermost nested container of the selected entity (only present if :N option of acedSSGet() was used during selection)
  entity names of other nested containers in innermost to outermost order (only present if :N option of acedSSGet() was used during selection)
RTENAME 
entity name of outermost nested container (in other words, the one in Model Space or Paper Space) of the selected entity (only present if :N option of acedSSGet() was used during selection)
RTLE
end of entity data sublist
  In a word, this tells many information, including the nested entities/containers. Please pay attention to the type marked in red. So assume we have a block:
top_block
  sub_block
       entity in sub block (non-block)
   other entity (non-block) in top block
With the code demo below:
if we pick the other entity in top block, it will list
   other entity (non-block) in top block
   top_block
if we pick the entity in sub block (non-block), it will list
   entity in sub block (non-block)
   sub_block
    top_block
  static void Retrieving_block_hierarchy(void)
{  
ads_name sset, eName;
AcDbObjectId id;
   // "_:n" return nested entity info
 //
 if (RTNORM == acedSSGet(L"_:n", NULL, NULL, NULL, sset))
{
      acutPrintf(L"\n");
      long len = 0;
      acedSSLength(sset, &len);
      for (long i = 0;
          i < len;
          i++)
      {             
       resbuf *rb = NULL;
         if (RTNORM ==
           acedSSNameX(&rb, sset, i))
       {
            resbuf *rbWalk = rb;
            while (NULL != rbWalk)
            {
                 if (RTENAME ==
                     rbWalk->restype)
                 {
                      eName[0] =
                          rbWalk->resval.rlname[0];
                      eName[1] =
                          rbWalk->resval.rlname[1];
                      if(Acad::eOk ==
                          acdbGetObjectId(id, eName))
                      {
                           acutPrintf(L"Entity %d: %x",
                               i,
                               id.asOldId());
                           AcDbEntity *pEnt;
                           if (Acad::eOk ==
                               acdbOpenObject(pEnt,
                               id,
                               AcDb::kForRead))
                           {
                           // dump the entity name
                            acutPrintf(L"(%s)\n",
                                pEnt->isA()->name());
                              if(pEnt->isKindOf(
                                AcDbBlockReference::desc()))
                            {
                                AcDbBlockReference *blkref =
                              (AcDbBlockReference *)pEnt;
                                AcDbObjectId blkid =
                              blkref->blockTableRecord();
                                AcDbObject *ptmpObj;
                                if (Acad::eOk ==
                                    acdbOpenObject(ptmpObj,
                                            blkid,
                                            AcDb::kForRead) )
                                {
                               // if it is a block reference
                           AcDbBlockTableRecord *blk =

                                   (AcDbBlockTableRecord*)
                                               ptmpObj;
                                    const ACHAR *blkname =
                                        NULL;
                                    blk->getName(blkname);
                                    acutPrintf(
                                   L"(block name: %s)\n",
                                        blkname);
                                    ptmpObj->close();
                                }   
                                else
                                {
                                     acutPrintf(
                                 L"\nCouldn't open block");
                               }
                              }
                              pEnt->close();
                           }
                           else
                           {
                                acutPrintf(
                           L"\nCouldn't open object");
                           }
                      }
                   }
                   // move to the next resbuf node
                 rbWalk = rbWalk->rbnext;
              }
            acutRelRb(rb);
       }
      }
      acedSSFree(sset);

