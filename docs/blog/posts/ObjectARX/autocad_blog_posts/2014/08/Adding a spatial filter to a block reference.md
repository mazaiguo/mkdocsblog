---
title: "Adding a spatial filter to a block reference"
date: 2014-08-01
categories:
  - AutoCAD
tags:
  - Block
  - Database
  - Plugin
description: "This blog post is minor tweak to the existing post written by my colleague Xiaodong back in 2013, with the recent development changes internally, t..."
author: Autodesk
---
# Adding a spatial filter to a block reference

发布日期: 2014-08-01

原始链接: https://adndevblog.typepad.com/autocad/2014/08/adding-a-spatial-filter-to-a-block-reference.html

## 文章内容

By Madhukar Moogala
This blog post is minor tweak to the existing post written by my colleague Xiaodong back in 2013, with the recent development changes internally, the code flow is causing crash in ACAD 2015 -32 machines, to avoid such mishap and to have seamless code across both the machines I have re written the code.
Reason for new change in the code :
The existing code sets the filter's definition (including clip boundary) before the filter is added to the database.  That causes the wrong type of internal clip boundary object to be created.  There are two types of clip boundaries possible, one is only for use in databases that are open in the Acad editor and the other is for databases that are not open in the Acad editor. If the filter doesn't have a database, then we create the clip boundary type that is for non-editor databases. Then, if the filter is added to a database that is open in the editor, it has the wrong type of clip boundary and that causes problems.
  static void Test_Clip ()
{
ads_point pt1, pt2;
ads_name ent;
if (acedEntSel(_T("Select xref:"), ent, pt1) != RTNORM)
return;
AcDbObjectId idXref;
if (acdbGetObjectId(idXref,ent) != Acad::eOk)
return;
AcDbObjectPointer<AcDbBlockReference> pRef(idXref, AcDb::kForRead);
if (pRef.openStatus() != Acad::eOk) {
acutPrintf(_T("Not an xref!\n"));
return;
}
AcGePoint2dArray pts;
if (acedGetPoint(NULL,_T("First point:"), pt1) != RTNORM) {
pRef->close();
return;
}
//the ECS of the vertices must be defined in the
//coordinate system of the _block_ so let's calculate
//transform all points to that coordinate system
AcGeMatrix3d mat(pRef->blockTransform());
mat.invert();
AcGePoint3d pt3d(asPnt3d(pt1));
pt3d.transformBy(mat);
pts.append(AcGePoint2d(pt3d.x, pt3d.y));
while (acedGetPoint(pt1,_T("Next point:"), pt2) == RTNORM) {
acedGrDraw(pt1, pt2, 1, 1);
pt3d = asPnt3d(pt2);
pt3d.transformBy(mat);
pts.append(AcGePoint2d(pt3d.x, pt3d.y));
memcpy(pt1, pt2, sizeof(ads_point));
}
acedRedraw(NULL,0);
AcDbDatabase* pDb = acdbHostApplicationServices()->workingDatabase();
AcGeVector3d normal;
double elev;
if (pDb->tilemode()) {
normal = pDb->ucsxdir().crossProduct(pDb->ucsydir());
elev = pDb->elevation();
} else {
normal = pDb->pucsxdir().crossProduct(pDb->pucsydir());
elev = pDb->pelevation();
}
normal.normalize();
Acad::ErrorStatus es = pRef.object()->upgradeOpen();
if (es != Acad::eOk) {
pRef->close();
return;
}
//create the filter
AcDbSpatialFilter* pFilter = new AcDbSpatialFilter;
//add it to the extension dictionary of the block reference
//the AcDbIndexFilterManger class provides convenient utility functions
if (AcDbIndexFilterManager::addFilter(pRef.object(), pFilter) != Acad::eOk)
delete pFilter;
else {
acutPrintf(_T("Filter has been succesfully added!\n"));
pRef.object()->downgradeOpen();
}
if (pFilter->setDefinition(pts,normal,elev,
ACDB_INFINITE_XCLIP_DEPTH,-ACDB_INFINITE_XCLIP_DEPTH, true) != Acad::eOk)
{
acutPrintf(L"Filter setDefinition failed.");
//remove the filter if setDefinition fails.
pFilter->erase();
  }
es = pFilter->erase();
pFilter->close();
pRef->close();
  }

## 评论

**内容**: Alexander Rivilis said...
Hi Madhukar!
You can explain why in case of "Filter setDefinition failed" you call pFilter->erase(); twice?
Reply
08/20/2014 at 03:10 PM

---
**内容**: Madhukar Moogala said...
Hi Alex,
Sorry, it is typo , thanks for pointing out.
Reply
08/20/2014 at 09:43 PM

---
**内容**: oliver253 said...
Thank you for the correction, I was wondering why AutoCAD would crash when stretching the clip area, if the filter definition was set before adding it. And BTW, the crashing happens on 64-bit AutoCAD 2015 as well.
Reply
08/21/2014 at 06:59 AM

---
