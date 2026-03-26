---
title: "Converting polyline arc to AcDbArc and vice-versa"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - Polyline
description: "Here is a way to convert an AcDbPolyline arc to an AcDbArc. The easiest procedure is to create an AcGeCircArc2d by calling AcDbPolyline::getArcSegA..."
author: Autodesk
---
# Converting polyline arc to AcDbArc and vice-versa

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/converting-polyline-arc-to-acdbarc-and-vice-versa.html

## 文章内容

By Balaji Ramamoorthy
Here is a way to convert an AcDbPolyline arc to an AcDbArc. The easiest procedure is to create an AcGeCircArc2d by calling AcDbPolyline::getArcSegAt(). You can then use "acutAngle" method to calculate the start and end angles using the center point of the AcGeCircArc2d and the start and end points of the polyline arc. Then create an AcDbArc with the AcGeCircArc2d center point, the polyline's normal, the AcGeCircArc2d's radius, and the start and end angles you just calculated. It is very important to call AcGeCircArc2d::isClockwise() to find out which way the bulge leans; if the arc is clockwise, construct the AcDbArc with the start and end points reversed in the AcDbArc constructor.
To convert AcDbArcs back to AcDbPolyline is somewhat simpler if you remember that bulge is the 1/4 of the tangent of the included angle. The included angle is easily calculated with the AcDbArc member functions startAngle() and endAngle().
The following sample illustrates how to convert AcDbPolyline arc segments to AcDbArcs.
static void AsdkConvertPolylineArc2Arc(void)
{
    ads_name ename;
    ads_point pt;
    int retval;
    retval = acedEntSel(L"\nPick a LW polyline:", ename, pt);
    if(retval != RTNORM)
        return;
      AcDbPolyline *pPoly;
    AcDbObjectId id;
    Acad::ErrorStatus es;
    acdbGetObjectId(id, ename);
    es = acdbOpenObject((AcDbObject*&)pPoly, id, AcDb::kForRead);
    if (es != Acad::eOk)
    {
        acutPrintf(L"\nERROR: %s", acadErrorStatusText(es));
        return;
    }
      if (pPoly->isA() != AcDbPolyline::desc())
    {
        acutPrintf(L"\nLW polyline not selected.");
        pPoly->close();
        return;
    }
      for (unsigned int i=0; i<pPoly->numVerts()-1; i++)
    {
        double bulge;
        pPoly->getBulgeAt(i, bulge);
        if (bulge == 0.0)  // line segment
            continue;
          AcGePoint2d startPt, endPt, centerPt, testPt;
        pPoly->getPointAt(i, startPt);
        pPoly->getPointAt(i+1, endPt);
        AcGeCircArc2d geArc;
          // easy AcDbPolyline method for creating an AcGeCircArc2d
        pPoly->getArcSegAt(i, geArc);
        double start = acutAngle(
                                    asDblArray(geArc.center()),
                                    asDblArray(startPt)
                                );
        double end = acutAngle(
                                asDblArray(geArc.center()),
                                asDblArray(endPt)
                              );
        AcGePoint3d center = AcGePoint3d(
                                            geArc.center().x,
                                            geArc.center().y,
                                            pPoly->elevation()
                                        );
          // if this polyline does not lie in WCS, get its ECS
        // and tranform the center point back to WCS
        if (pPoly->normal() != AcGeVector3d(0,0,1))
        {
            AcGeMatrix3d mat;
            pPoly->getEcs(mat);
            center = center.transformBy(mat);
        }
          AcDbArc* pArc;
        // Check the direction of the arc. If it's clockwise
        // (opposite the AutoCAD default)
        // reverse the start and end points for the AcDbArc.
        if (geArc.isClockWise())
        {
            pArc = new AcDbArc(
                                center,
                                pPoly->normal(),
                                geArc.radius(),
                                end,
                                start
                              );
        }
        else
        {
            pArc = new AcDbArc(
                                center,
                                pPoly->normal(),
                                geArc.radius(),
                                start,
                                end
                              );
        }
          AcCmColor yellow;
        yellow.setColorIndex(2);
        pArc->setColor(yellow);
          //set entity properties such as layer, linetype, color
        // User defined function to add entity to Model Space
        // ...
        postToModelSpace(pArc);
        pArc->close();
    }
    pPoly->close();
}
  static void postToModelSpace(AcDbEntity* pEntity)
{
    AcDbBlockTable *pBlockTable;
    AcDbBlockTableRecord *pSpaceRecord;
      AcDbDatabase *pDb
            = acdbHostApplicationServices()->workingDatabase();
      pDb->getSymbolTable(pBlockTable, AcDb::kForRead);
    pBlockTable->getAt
                    (
                        ACDB_MODEL_SPACE,
                        pSpaceRecord,
                        AcDb::kForWrite
                    );
    pSpaceRecord->appendAcDbEntity(pEntity);
      pBlockTable->close();
    pEntity->close();
    pSpaceRecord->close();
}
Here is a sample code to perform a similar conversion using the AutoCAD .Net API :
using Autodesk.AutoCAD.Geometry;
    Document doc = Application.DocumentManager.MdiActiveDocument;
Editor ed = doc.Editor;
Database db = doc.Database;
  PromptEntityOptions peo
            = new PromptEntityOptions("Select a polyline : ");
peo.SetRejectMessage("Not a polyline");
peo.AddAllowedClass(
    typeof(Autodesk.AutoCAD.DatabaseServices.Polyline), true);
  PromptEntityResult per = ed.GetEntity(peo);
if (per.Status != PromptStatus.OK)
    return;
  ObjectId plineId = per.ObjectId;
using (Transaction tr = db.TransactionManager.StartTransaction())
{
    BlockTableRecord btr = tr.GetObject
   (db.CurrentSpaceId, OpenMode.ForWrite) as BlockTableRecord;
      Autodesk.AutoCAD.DatabaseServices.Polyline pline = 
                tr.GetObject(
                                plineId,
                                OpenMode.ForRead,
                                false
                            )
                as Autodesk.AutoCAD.DatabaseServices.Polyline;
      if (pline != null)
    {
        int segCount = pline.NumberOfVertices - 1;
        for (int cnt = 0; cnt < segCount; cnt++)
        {
            Point3d vertexPt = pline.GetPoint3dAt(cnt);
            SegmentType type = pline.GetSegmentType(cnt);
              switch (type)
            {
                case SegmentType.Arc:
                {
                    CircularArc2d arc2d = pline.GetArcSegment2dAt(cnt);
                      Interval arc2dInterval = arc2d.GetInterval();
                    double startParam = arc2dInterval.LowerBound;
                    double endParam = arc2dInterval.UpperBound;
                    Point2d sp2d = arc2d.EvaluatePoint(startParam);
                    Point2d ep2d = arc2d.EvaluatePoint(endParam);
                    Point2d cp2d = arc2d.Center;
                    double startAngle =
                       (new Line2d(cp2d, sp2d)).Direction.Angle;
                    double endAngle =
                        (new Line2d(cp2d, ep2d)).Direction.Angle;
                      Point3d cp3d = new Point3d(
                                                cp2d.X,
                                                cp2d.Y,
                                                pline.Elevation
                                              );
                      // if this polyline does not lie in WCS, get its ECS
                    // and tranform the center point back to WCS
                    if (pline.Normal != Vector3d.ZAxis)
                    {
                        Matrix3d ecsMatrix = pline.Ecs;
                        cp3d = cp3d.TransformBy(ecsMatrix);
                    }
                      if (arc2d.IsClockWise)
                    {
                        Arc arc = new Arc(  cp3d,
                                            pline.Normal,
                                            arc2d.Radius,
                                            endAngle,
                                            startAngle
                                          );
                        arc.ColorIndex = 2;
                        btr.AppendEntity(arc);
                        tr.AddNewlyCreatedDBObject(arc, true);
                    }
                    else
                    {
                        Arc arc = new Arc(  cp3d,
                                            pline.Normal,
                                            arc2d.Radius,
                                            startAngle,
                                            endAngle
                                         );
                        arc.ColorIndex = 2;
                        btr.AppendEntity(arc);
                        tr.AddNewlyCreatedDBObject(arc, true);
                    }
                    break;
                }
                  case SegmentType.Line:
                {
                    LineSegment2d line2d
                                = pline.GetLineSegment2dAt(cnt);
                    Interval line2dInterval = line2d.GetInterval();
                    double startParam
                                   = line2dInterval.LowerBound;
                    double endParam
                                   = line2dInterval.UpperBound;
                    Point2d sp2d
                            = line2d.EvaluatePoint(startParam);
                    Point2d ep2d
                            = line2d.EvaluatePoint(endParam);
                    Point3d sp3d
                    = new Point3d(sp2d.X, sp2d.Y, pline.Elevation);
                      Point3d ep3d
                    = new Point3d(ep2d.X, ep2d.Y, pline.Elevation);
                      if (pline.Normal != Vector3d.ZAxis)
                    {
                        Matrix3d ecsMatrix = pline.Ecs;
                        sp3d = sp3d.TransformBy(ecsMatrix);
                        ep3d = ep3d.TransformBy(ecsMatrix);
                    }
                      Line line = new Line(sp3d, ep3d);
                    line.ColorIndex = 2;
                    btr.AppendEntity(line);
                    tr.AddNewlyCreatedDBObject(line, true);
                    break;
                }
            }
        }
    }
    tr.Commit();
}

## 评论

**内容**: Igor said...
The routine does not produce last segment of closed polyline. Or am I wrong?
Reply
11/20/2018 at 12:20 PM

---
