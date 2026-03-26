---
title: "Implementing AcDbCustomOsnapMode"
date: 2015-07-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "While I was working on customer query regarding Customosnapmode2, to embed icons in OSNAP right click menu, I felt the need to migrate a very old s..."
author: Autodesk
---
# Implementing AcDbCustomOsnapMode

发布日期: 2015-07-01

原始链接: https://adndevblog.typepad.com/autocad/2015/07/implementing-acdbcustomosnapmode.html

## 文章内容

By Madhukar Moogala
While I was working on customer query regarding Customosnapmode2, to embed icons in OSNAP right click menu, I felt the need to migrate a very old sample of ours, in my next blog I will updating on how to update\load OSNAP with icon in right click menu.
Following sample code shows how to implement a simple custom object snap to divide curves of all types
into thirds. If the mode is active, then two "1/3" snap points will exist for each open curve,
and three for each closed curve.
class AsdkThirdGlyph : public AcGiGlyph
{
public:
virtual Acad::ErrorStatus setLocation(const AcGePoint3d& dcsPoint)
{
m_center = dcsPoint;
return Acad::eOk;
}
virtual void subViewportDraw(AcGiViewportDraw* vportDrawContext)
{
// Calculate the size of the glyph in WCS (use for text height factor)
int glyphPixels = acdbCustomOsnapManager()->osnapGlyphSize();
AcGePoint2d glyphSize;
vportDrawContext->viewport().getNumPixelsInUnitSquare( m_center, glyphSize );
double glyphHeight = glyphPixels / glyphSize[ Y ];
  // Get the extents of the glyph text, so we can centre it
AcGiTextStyle style;
AcGePoint2d ptExt = style.extents( ASDK_GLYPH_TEXT, Adesk::kFalse, -1, Adesk::kFalse );
  struct resbuf rbFrom, rbTo;
rbFrom.restype = RTSHORT;
rbFrom.resval.rint = 2; // From DCS
rbTo.restype = RTSHORT;
rbTo.resval.rint = 0; // To WCS
  // Translate the X-axis of the DCS to WCS co-ordinates (as a displacement vector)
AcGeVector3d ptDir;
acedTrans( asDblArray( AcGeVector3d::kXAxis ),
            &rbFrom,
            &rbTo,
            1,
            asDblArray( ptDir ));
  // Translate the centre of the glyph from DCS to WCS co-ordinates
AcGePoint3d ptPos, ptCen;
AcGeVector3d vecExt( ptExt[ X ] / 2, ptExt[ Y ] / 2, 0 );
ptPos = m_center - vecExt / 2;
if ( RTNORM != acedTrans( asDblArray( ptPos ),
               &rbFrom,
               &rbTo,
               0,
               asDblArray( ptCen )))
ptCen = m_center;
  // Draw the centred text representing the glyph
vportDrawContext->geometry().text( ptCen,
                                  vportDrawContext->viewport().viewDir(),
                                  ptDir,
                                  glyphHeight,
                                  1.0,
                                  0.0,
                                  ASDK_GLYPH_TEXT );
  }
  private:
AcGePoint3d m_center;
};
class AsdkThirdOsnapInfo : public AcDbCustomOsnapInfo
{
public:
ACRX_DECLARE_MEMBERS(AsdkThirdOsnapInfo);
  virtual Acad::ErrorStatus   getOsnapInfo(
    AcDbEntity*            pickedObject,
    Adesk::GsMarker        gsSelectionMark,
    const AcGePoint3d&        pickPoint,
    const AcGePoint3d&        lastPoint,
    const AcGeMatrix3d&    viewXform,
    AcArray<AcGePoint3d>&    snapPoints,
    AcArray<int>&            geomIdsForPts,
    AcArray<AcGeCurve3d*>& snapCurves,
    AcArray<int>&            geomIdsForLines) = 0;
};
ACRX_NO_CONS_DEFINE_MEMBERS( AsdkThirdOsnapInfo, AcDbCustomOsnapInfo );
// AcDbEntity level protocol extension
    class AsdkThirdOsnapEntityInfo : public AsdkThirdOsnapInfo
{
public:
virtual Acad::ErrorStatus   getOsnapInfo(
    AcDbEntity*            pickedObject,
    Adesk::GsMarker        gsSelectionMark,
    const AcGePoint3d&        pickPoint,
    const AcGePoint3d&        lastPoint,
    const AcGeMatrix3d&    viewXform,
    AcArray<AcGePoint3d>&    snapPoints,
    AcArray<int>&            geomIdsForPts,
    AcArray<AcGeCurve3d*>& snapCurves,
    AcArray<int>&            geomIdsForLines)
{
// Base definition with no functionality
return Acad::eOk;
}
};
  // AcDbCurve level protocol extension
  class AsdkThirdOsnapCurveInfo : public AsdkThirdOsnapInfo
{
public:
virtual Acad::ErrorStatus   getOsnapInfo(
    AcDbEntity*            pickedObject,
    Adesk::GsMarker        gsSelectionMark,
    const AcGePoint3d&        pickPoint,
    const AcGePoint3d&        lastPoint,
    const AcGeMatrix3d&    viewXform,
    AcArray<AcGePoint3d>&    snapPoints,
    AcArray<int>&            geomIdsForPts,
    AcArray<AcGeCurve3d*>& snapCurves,
    AcArray<int>&            geomIdsForLines)
{
// Generic curve function for all AcDbCurves (except AcDbPolylines)
  // Protocol Extension insures that the following assertion is always
// true, but check in non-prod versions just to be safe.
assert( pickedObject->isKindOf( AcDbCurve::desc() ));
  // but in production, a hard cast is fastest
AcDbCurve *pCurve = (AcDbCurve*)pickedObject;
  double startParam, endParam;
AcGePoint3d pt;
  Acad::ErrorStatus es;
es=pCurve->getStartParam( startParam);
es=pCurve->getEndParam( endParam );
es=pCurve->getPointAtParam( startParam + ((endParam - startParam) / 3), pt );
assert( Acad::eOk == es);
snapPoints.append( pt );
es=pCurve->getPointAtParam( startParam + ((endParam - startParam) * 2 / 3), pt );
assert(Acad::eOk==es);
snapPoints.append( pt );
if ( pCurve->isClosed() )
{
es=pCurve->getStartPoint( pt );
assert(Acad::eOk==es);
snapPoints.append( pt );
}
return Acad::eOk;
}
};
  // AcDbPolyline level protocol extension
  class AsdkThirdOsnapPolylineInfo : public AsdkThirdOsnapInfo
{
public:
virtual Acad::ErrorStatus   getOsnapInfo(
    AcDbEntity*            pickedObject,
    Adesk::GsMarker        gsSelectionMark,
    const AcGePoint3d&        pickPoint,
    const AcGePoint3d&        lastPoint,
    const AcGeMatrix3d&    viewXform,
    AcArray<AcGePoint3d>&    snapPoints,
    AcArray<int>&            geomIdsForPts,
    AcArray<AcGeCurve3d*>& snapCurves,
    AcArray<int>&            geomIdsForLines)
{
// Specialised implementation for AcDbPolylines:
//  Parametrisation of AcDbPolylines is different: each whole numbered paramater appears
//  at a vertex, so we cannot simply divide by three to get the correct parameter.
  // Protocol Extension insures that the following assertion is always
// true, but check in non-prod versions just to be safe.
assert( pickedObject->isKindOf( AcDbPolyline::desc() ));
  // but in production, a hard cast is fastest
AcDbPolyline *pPline = (AcDbPolyline*)pickedObject;
  Acad::ErrorStatus es;
  if ( bSnapToSegments )
{
// Snap to a third of each of the segments
unsigned int numSegs = pPline->numVerts() - 1;
AcGeLineSeg3d segLn;
AcGeCircArc3d segArc;
double startParam, endParam, newParam, dist;
AcGePoint3d pt;
  for ( unsigned int idx = 0; idx < numSegs; idx++ )
{
switch( pPline->segType( idx ))
{
case AcDbPolyline::kLine:
es=pPline->getLineSegAt( idx, segLn );
startParam = segLn.paramOf( segLn.startPoint() );
endParam = segLn.paramOf( segLn.endPoint() );
snapPoints.append(segLn.evalPoint( startParam + ((endParam - startParam) / 3 )));
snapPoints.append(segLn.evalPoint( startParam + ((endParam - startParam) * 2 / 3 )));
break;
case AcDbPolyline::kArc:
es=pPline->getArcSegAt( idx, segArc );
startParam = segArc.paramOf( segArc.startPoint() );
endParam = segArc.paramOf( segArc.endPoint() );
dist = segArc.length( startParam, endParam );
newParam = segArc.paramAtLength( startParam, dist / 3 );
snapPoints.append( segArc.evalPoint( newParam ));
newParam = segArc.paramAtLength( startParam, dist * 2 / 3 );
snapPoints.append( segArc.evalPoint( newParam ));
break;
default:
break;
}
}
}
else {
double endParam;
AcGePoint3d pt;
double dist;
  es=pPline->getEndParam( endParam );
es=pPline->getDistAtParam( endParam, dist );
es=pPline->getPointAtDist( dist / 3, pt );
assert(Acad::eOk==es);
snapPoints.append( pt );
es=pPline->getPointAtDist( dist * 2 / 3, pt );
assert(Acad::eOk==es);
snapPoints.append( pt );
if ( pPline->isClosed() )
{
es=pPline->getStartPoint( pt );
snapPoints.append( pt );
}
}
return Acad::eOk;
}
};
  class AsdkThirdOsnapMode : public AcDbCustomOsnapMode
{   
public:
AsdkThirdOsnapMode()
{
m_pGlyph = new AsdkThirdGlyph;
}
virtual ~AsdkThirdOsnapMode()
{
delete m_pGlyph;
m_pGlyph = NULL;
}
virtual const TCHAR* localModeString() const
{
return _T("THIrd");
}
virtual const TCHAR* globalModeString() const
{
return _T("_THIrd");
}
virtual const AcRxClass* entityOsnapClass() const
{
return AsdkThirdOsnapInfo::desc();
}
virtual AcGiGlyph* glyph() const
{
return m_pGlyph;
}
virtual const TCHAR* tooltipString() const{
return _T("Third of length");
}
virtual const ACHAR * displayString()
{
return localModeString();
}
private:
AsdkThirdGlyph *m_pGlyph;
};
  AsdkThirdOsnapMode thirdMode;
bool bSnapToSegments = false;
You can download the sample here
Commands:
---------
SNAP2PLINE      Chooses to snap to a third of each polyline segment
SNAP2SEG        Chooses to snap to a third of the whole polyline
Classes:
--------
AsdkThirdOsnapInfo          Abstract base class for the protocol extension.
AsdkThirdOsnapEntityInfo    Generic definition providing no functionality.
AsdkThirdOsnapCurveInfo     Generic function for all curves, except AcDbPolylines.
AsdkThirdOsnapPolylineInfo  Specialized function for AcDbPolylines and derived classes.
AsdkThirdOsnapMode          Object snap mode describing the third object snap.
AsdkThirdGlyph              Glyph definition.
To use test this sample applilcation do the following:
1. Draw a polyline.
2. Run the APPLOAD command and Load the .arx
3. Run the line command, before selecting a point move the cursor over the previously drawn polyline
Results.
A snap point with the text of 1/3 appears on the polyline

## 评论

**内容**: WolframKuss said...
Sorry, but I can't find the follow-up blog post. Can you send a link or otherwise say how to add an icon to a AcDbCustomOsnapMode?
TIA,
Wolfram.
Reply
10/28/2015 at 01:37 AM

---
**内容**: Madhukar Moogala said...
While I was working on my follow up blog, I found an issue with osnapmode2 API, hence I stopped from publishing it, will do it once the API behaviour gets solved.
Sorry for bad news.
Anyways, you can add in icon in the following way:
Please download the attached sample:
https://github.com/MadhukarMoogala/MyBlogs/tree/CustomOsnap2/CustomOsnap2

Reply
10/28/2015 at 02:10 AM

---
**内容**: WolframKuss said...
Thank you, it works :-).
Reply
10/28/2015 at 05:59 AM

---
**内容**: dinosaur game said...
The custom object snap keyword that the user types in to activate the object snap. Both local and global keywords must be specified.
Reply
02/07/2023 at 07:04 PM

---
**内容**: twom said...
In your example code you don't use the activateOsnapMode or deactivateOsnapMode. When I use these methods the Object Snap Menu from the status bar doesn't reflect the actual state. When I first start my custom mode it is visible in the menu and has a check mark beside it. If I call a command that uses the deactivateOsnapMode the state of the check mark doesn't change. If I use -OSNAP all the snaps are turned off, but if you look at the menu, it still has the check mark. Is this just a bug I should report or am I missing some other action I should be taking? I tried this with both 2022 and 2023.
Reply
03/30/2023 at 11:44 AM

---
