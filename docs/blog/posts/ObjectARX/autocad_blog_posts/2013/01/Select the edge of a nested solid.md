---
title: "Select the edge of a nested solid"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - ObjectARX
  - Solid
description: "The answer to this question is a combination of two requirements:"
author: Autodesk
---
# Select the edge of a nested solid

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/select-the-edge-of-a-nested-solid.html

## 文章内容

By Augusto Goncalves
The answer to this question is a combination of two requirements:
1. Selecting a subentity
2. Selecting a nested entity
1. Selecting a subentity
First we should clarify what a subentity is:
A subentity is a pseudo entity which is a logical part of a real entity. In our sample drawing the solid is the real entity (AcDb3dSolid) and the edge is the pseudo entity (there is no AcDbEdge class). In AutoCAD we rely on IDs called GS (short for graphics system) markers to get to these subentities.
The ObjectARX help file contains a small piece of sample code showing how to highlight one of a solid's internal edges. Unfortunately, it does not work in shaded mode - the face will always be selected - and it will not find the subentity in the case of a nested entity.
2. Selecting a nested entity
Again, let's start by defining things:
For the purposes of this article, we are defining a nested entity as an entity that is placed inside a block (AcDbBlockTableRecord) other than one of the internal layout blocks (e.g. Model Space).
We can use a standard function such as acedNEntSelP() to select a nested entity, which gives back the bottommost selected entity and all its nesting entities - you can find information about it in the ObjectARX help file. But what about the GS markers we need?
3. The two combined
We really need a function that can select the bottommost nested entity and also gives back the correct GS marker of the subentity.
Fortunately, there is such a function, the undocumented brother of acedNEntSelP(). It does exactly what we need and is called acedNEntSelPEx(). It gives back the correct GS marker (even in shaded mode), provides the list of nesting entities and gives back the selected bottommost nested entity. Not only does it select edges and return the GS marker as we have seen, it also picks through spaces. e.g. say you are in paper space with no model space selected, from that mode you can use this function to select an entity in model space.
In the attached drawing we have the following structure:
SolidBlock2 -> SolidBlock -> Solid
(SolidBlock2 contains a reference to SolidBlock, which contains the Solid entity).
When using acedNEntSelPEx() (or acedNEntSelP), we will get back a result buffer that contains the selected entity's nesting entities in the same order as getSubentPathsAtGsMarker() needs them - starting from the directly nesting entity going upwards until we reach the top-most nesting entity that contains all the others. In case where we select the solid in SolidBlock2 in our sample drawing, the path is:
SolidBlock reference
SolidBlock2 reference [which contains SolidBlock]
Now we just have to create an array filled with the above entities in the same order, but starting with the solid entity itself:
Solid entity
SolidBlock reference
SolidBlock2 reference
We call the getSubentPathsAtGsMarker() function of the topmost nesting entity (SolidBlock2 reference) with the GS marker and the array we just created. From this we get the correct subentity path that we need to highlight the subentity.
The following highlightTest sample function demonstrate it. This is based on the help file code under "HelpfileSelect" command help topic.
// declare this undocumented function on your header files
// more information here
extern int acedNEntSelPEx(const TCHAR *str, ads_name entres,
              ads_point ptres, int pickflag,
              ads_matrix xformres,
              struct resbuf **refstkres,
              unsigned int uTransSpaceFlag,
              int* gsmarker);
// call this function from a custom command
static void highlightTest()
{
  AcDbObjectId objId;
  AcGePoint3d pt3d;
  int marker;
  ads_matrix mx;
  // contains the nesting blockreferences
  resbuf* rbChain = NULL;
    if (getObjectAndGsMarker(objId, pt3d, mx, rbChain, marker)
    != Acad::eOk)
    return;
    highlightEdge(objId, pt3d, mx, rbChain, marker);
    ads_free(rbChain);
}
  static Acad::ErrorStatus
  getObjectAndGsMarker(
  AcDbObjectId& objId,
  AcGePoint3d& pt3d,
  ads_matrix& mx,
  resbuf*& rbChain,
  int& marker)
{
  ads_name ename;
  ads_point pt;
  unsigned int uTransSpaceFlag = 1;
    // set uTransSpaceFlag to 0, if the current layout
  // is in model space
  struct resbuf rb;
  acedGetVar(L"CVPORT", &rb);
  if (rb.resval.rint != 1)
    uTransSpaceFlag = 0; // Model space
    // this function will give back the marker that
  // is needed for subentity selection and the
  // nesting entities of the selected entity
  if (acedNEntSelPEx(L"\nPick edge : ", ename,
    pt, NULL, mx, &rbChain, uTransSpaceFlag,
    &marker) != RTNORM) {
    acutPrintf(L"\nacedNEntSelPEx has failed");
    return Acad::eInvalidAdsName;
  }
    pt3d.x = pt[0];
  pt3d.y = pt[1];
  pt3d.z = pt[2];
    acdbGetObjectId(objId, ename);
    return Acad::eOk;
}
  static void highlightEdge(
  const AcDbObjectId& objId,
  AcGePoint3d& pt3d,
  ads_matrix& mx,
  resbuf*& rbChain,
  const int marker)
{
  // the solid object
  AcDbEntity *pSolid = NULL;
  // topmost blockreference - if there is one
  AcDbEntity* pTMBlockRef = NULL;
  // it's either the solid or the block reference that contains it
  AcDbEntity* pEntHighlight = NULL;
    // open the solid
  acdbOpenAcDbEntity(pSolid, objId, AcDb::kForRead);
    // Get the subentity ID for the edge that is picked
  //
  AcGeMatrix3d xform;
  int numIds;
  AcDbFullSubentPath* subentIds;
    xform.setCoordSystem(
    (const AcGePoint3d&)AcGePoint3d(mx[0][0], mx[0][1], mx[0][2]),
    (const AcGeVector3d&)AcGeVector3d(mx[1][0], mx[1][1], mx[1][2]),
    (const AcGeVector3d&)AcGeVector3d(mx[2][0], mx[2][1], mx[2][2]),
    (const AcGeVector3d&)AcGeVector3d(mx[3][0], mx[3][1], mx[3][2]));
    // count containing block references
  int numInserts = 0;
  // should be one less than the total number of
  // entries in entAndInsertStack  because the first
  // entry is the entity itself, which is not a BlockReference
  for (resbuf* currentInsert = rbChain; currentInsert != NULL;
    currentInsert = currentInsert->rbnext)
    numInserts++;
    Acad::ErrorStatus err;
    // it is inside a block
  if (numInserts > 0)
  {
    // create an array
    AcDbObjectId* Inserts = new AcDbObjectId[numInserts + 1];
    Inserts[0] = objId;
      // we need to fill up the list going from the direct block
    // reference that contains the solid
    // to the topmost block reference
    int currNumber = 1;
    for (resbuf* current = rbChain;
      current != NULL;
      current = current->rbnext, currNumber++)
      acdbGetObjectId(Inserts[currNumber],
      current->resval.rlname);;
      // get topmost blockreference
    acdbOpenAcDbEntity(pTMBlockRef, Inserts[numInserts],
      AcDb::kForRead);
      // xform and pt3d are not used in case of AcDb3dSolid
    AcGePoint3d point;
    AcGeMatrix3d matrix;
    err = pTMBlockRef->getSubentPathsAtGsMarker
      (AcDb::kEdgeSubentType,
      marker, point, matrix, /*pt3d, xform, */numIds, subentIds,
      numInserts, Inserts);
      // as an extra check let's highlight the topmost
    // blockreference as well
    pEntHighlight = pTMBlockRef;
  }
  else
  {
    // xform and pt3d are not used in case of AcDb3dSolid
    err = pSolid->getSubentPathsAtGsMarker(AcDb::kEdgeSubentType,
      marker, pt3d, xform, numIds, subentIds);
      pEntHighlight = pSolid;
  }
    // At this point the subentId's variable contains the
  // address of an array of AcDbFullSubentPath objects.
  // The array should be one element long, so the picked
  // edge's AcDbFullSubentPath is in subentIds[0].
  //
  // For objects with no edges (such as a sphere), the
  // code to highlight an edge is meaningless and must
  // be skipped.
  //
  if (numIds > 0)
  {
    ACHAR dummy[133]; // space for acedGetString pauses below
      // Highlights the edge on the solid in the right block
    pEntHighlight->highlight(subentIds[0]);
    // Pause to let user see the effect.
    acedGetString(0,
      _T("\nEdge is highlighted. Press <RETURN> to continue..."),
      dummy);
    pEntHighlight->unhighlight(subentIds[0]);
      // highlights the entire block reference
    // - if the solid is inside one
    pEntHighlight->highlight();
    // Pause to let user see the effect.
    acedGetString(0,
      _T("\nTopmost nesting block reference is highlighted. Press <RETURN> to continue..."),
      dummy);
    pEntHighlight->unhighlight();
  }
    // delete temporary array
  delete []subentIds;
    // close opened entities
  pSolid->close();
  if (pTMBlockRef)
    pTMBlockRef->close();
}

## 评论

**内容**: Abhay Joshi said...
I am getting linking error for 64 bit (AutoCAD 2014). Do I need to change something?
Reply
10/11/2015 at 11:31 PM

---
**内容**: Augusto Goncalves said in reply to Abhay Joshi...
Abhay,
I don't believe this is related to the code, but most likely to your project settings. Did you use the project template/wizard? What's the error message?
Regards,
Augusto Goncalves
Reply
10/13/2015 at 07:07 AM

---
**内容**: Abhay Joshi said in reply to Augusto Goncalves...
It was my mistake. problem was for last parameter, integer pointer. I used below signature to work with 32 and 64 bit.
extern int acedNEntSelPEx(const ACHAR *str, ads_name entres,
                           ads_point ptres, int pickflag,
                           ads_matrix xformres,
                           struct resbuf **refstkres,
                           unsigned int uTransSpaceFlag,
                           intptr_t* gsmarker);
Reply
10/14/2015 at 12:06 AM

---
