---
title: "How to find out if an acedGetPoint was taken by an OSnap override?"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "When I use acedGetPoint() I want to be able to tell if the user has selected an OSnap override and if possible which override was used - is it poss..."
author: Autodesk
---
# How to find out if an acedGetPoint was taken by an OSnap override?

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/how-to-find-out-if-an-acedgetpoint-was-taken-by-an-osnap-override.html

## 文章内容

By Philippe Leefsma
Q:
When I use acedGetPoint() I want to be able to tell if the user has selected an OSnap override and if possible which override was used - is it possible?
A:
The way is to find out if an OSnap (any OSnap) has been used. This approach uses an AcEdInputPointMonitor, which allows to monitor the input data processed by AutoCAD. In the AcEdInputPointMonitor::monitorInput() simply test to see if the OSNAP mode is on, if it is, check to see if any entities are being processed for OSNAP calculations and if they are check to see if a click has been made, if that condition is true then you know the point picked was because of an OSNAP process.
Here's the relevant code from the attached project:
Acad::ErrorStatus asdkInputPointMonitor::monitorInputPoint(
     bool& appendToTooltipStr,
    TCHAR*& additionalTooltipString,
    AcGiViewportDraw* drawContext,
    AcApDocument* document,
    bool pointComputed,
    int history,
    const AcGePoint3d& lastPoint,
    const AcGePoint3d& rawPoint,
    const AcGePoint3d& grippedPoint,
    const AcGePoint3d& cartesianSnappedPoint,
    const AcGePoint3d& osnappedPoint,
    AcDb::OsnapMask osnapMask,
    const AcArray<AcDbCustomOsnapMode*>&
        customOsnapModes,
    AcDb::OsnapMask osnapOverrides,
    const AcArray<AcDbCustomOsnapMode*>&
        customOsnapOverrides,
    const AcArray<AcDbObjectId>& apertureEntities,
    const AcArray< AcDbObjectIdArray,
    AcArrayObjectCopyReallocator<AcDbObjectIdArray>>&
        nestedApertureEntities,
    const AcArray<int>& gsSelectionMark,
    const AcArray<AcDbObjectId>& keyPointEntities,
    const AcArray< AcDbObjectIdArray,
    AcArrayObjectCopyReallocator<AcDbObjectIdArray>>&
        nestedKeyPointEntities,
    const AcArray<int>& keyPointGsSelectionMark,
    const AcArray<AcGeCurve3d*>& alignmentPaths,
    const AcGePoint3d& computedPoint,
    const TCHAR* tooltipString)
{
     // if osnap mode is on    
     if (history & Acad::PointHistory::ePickMask)
     {
           // get any entities that have been
           // used to calculate an osnap
           int keyPointLength =
               keyPointEntities.length ();
           // if entities have been used to
           // calculate an osnap point
           if (keyPointLength)
           {
                // now we have the entities used
                // for the osnap calc the
                // computedPoint gives us the
                // snap point
                AcGePoint3d snappedPoint =
                    computedPoint;
                                // check for eNotDigitizer
                // i.e. No Digitizer movement,
                // but a pick
                if (history &
                    Acad::PointHistory::eNotDigitizer)
                {
                    // set that this point was input
                    // with an osnap enabled
                    DocVars.docData().mOsnappedPoint =
                         true;
                }
           }
     }
       return Acad::eOk;
}
  The second step is an extension to the first, shows how to find out which OSnap was used. This time we use another class called an AcEdInputPointFilter which has the needed information passed in:
Acad::ErrorStatus asdkInputPointFilter::processInputPoint(
     bool& changedPoint,
    AcGePoint3d& newPoint,
    bool& displayOsnapGlyph,
    bool& changedTooltipStr,
    TCHAR*& newTooltipString,
    bool& retry,
    AcGiViewportDraw* drawContext,
    AcApDocument* document,
    bool pointComputed,
    int history,
    const AcGePoint3d& lastPoint,
    const AcGePoint3d& rawPoint,
    const AcGePoint3d& grippedPoint,
    const AcGePoint3d& cartesianSnappedPoint,
    const AcGePoint3d& osnappedPoint,
    AcDb::OsnapMask osnapMask,
    const AcArray<AcDbCustomOsnapMode*>&
        customOsnapModes,
    AcDb::OsnapMask osnapOverrides,
    const AcArray<AcDbCustomOsnapMode*>&
        customOsnapOverrides,
    const AcArray<AcDbObjectId>& pickedEntities,
    const AcArray< AcDbObjectIdArray,
    AcArrayObjectCopyReallocator<AcDbObjectIdArray>>&
        nestedPickedEntities,
    const AcArray<int>& gsSelectionMark,
    const AcArray<AcDbObjectId>& keyPointEntities,
    const AcArray< AcDbObjectIdArray,
    AcArrayObjectCopyReallocator<AcDbObjectIdArray>>&
        nestedKeyPointEntities,
    const AcArray<int>& keyPointGsSelectionMark,
    const AcArray<AcGeCurve3d*>& alignmentPaths,
    const AcGePoint3d& computedPoint,
    const TCHAR* tooltipString)
{
     // remember what the osnaps used was
       // osnap currently being processed
     DocVars.docData().mOsnapMask = osnapMask;
     // overriden osnap, i.e.
     // typed at the command line
     DocVars.docData().mOsnapOverrides =
        osnapOverrides;
       return Acad::eOk;
}
  DetectOsnap.zip

## 评论

**内容**: gemeng said...
Hi, is this monitorInputPoint function an reactor function? and in which case it would be called?
Reply
08/29/2015 at 03:11 AM

---
