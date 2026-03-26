---
title: "Perimeter of a hatch using ObjectARX and AutoCAD .Net API"
date: 2012-04-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - C++
  - Hatch
description: "A hatch entity in AutoCAD stores its geometry information in its "loops". Traversing the loops of a hatch can help in computing its perimeter by ac..."
author: Autodesk
---
# Perimeter of a hatch using ObjectARX and AutoCAD .Net API

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/perimeter-of-a-hatch-using-objectarx-and-autocad-net-api.html

## 文章内容

By Balaji Ramamoorthy
A hatch entity in AutoCAD stores its geometry information in its "loops". Traversing the loops of a hatch can help in computing its perimeter by accessing the geometry. Also, based on whether a loop is an "internal" or an "external" one, the perimeter of the islands can be separately computed if required. Here is a sample code that computes the perimeter of a hatch entity using ObjectARX and the AutoCAD .Net API. Error checking has been kept limted to improve readability of the code.
// Perimeter calculation of a hatch using ObjectARX
static void ADS_HatchTest(void)
{
    ads_name en;
    ads_point pt;
    if( acedEntSel(
                    ACRX_T("\nSelect a hatch :"),
                    en,
                    pt
                   ) != RTNORM )
    {
        return;
    }
      AcDbObjectId entId = AcDbObjectId::kNull;
    Acad::ErrorStatus es;
    es = acdbGetObjectId(entId, en);
    if(es != Acad::eOk)
          return;
      HatchPerimeter(entId);
}
  static void HatchPerimeter(AcDbObjectId entId)
{
    Acad::ErrorStatus es;
    AcDbEntity *pEnt;
    es = acdbOpenAcDbEntity(
                            pEnt,
                            entId,
                            AcDb::kForRead
                           );
    if( es != Acad::eOk )
        return;
      if( pEnt->isA() != AcDbHatch::desc() )
    {
        acutPrintf(ACRX_T("\n Please select a hatch."));
        pEnt->close();
        return;
    }
      AcDbHatch* pHatch = AcDbHatch::cast(pEnt);
      int nLoops = pHatch->numLoops(); 
    double totalExternalPerimeter =0.0; 
    double totalInternalPerimeter =0.0;
      for(int i=0; i < nLoops; i++)
    {  
        double loopLength = 0.0;
        long loopType;
          if( pHatch->loopTypeAt( i )
          & AcDbHatch::kPolyline )
        {    
            AcGePoint2dArray vertices;     
            AcGeDoubleArray bulges;     
            pHatch->getLoopAt(
                                i,
                                loopType,
                                vertices,
                                bulges
                             );   
            int nVertices = vertices.length();
              AcDbPolyline testPoly(nVertices);  
              for( int vx=0; vx < nVertices; vx++)
            {
                double bulge = 0.0;
                if(bulges.length() < nVertices)
                  bulge = 0.0;
                else
                  bulge = bulges[vx]; 
                testPoly.addVertexAt(
                                        vx,
                                        vertices[vx],
                                        bulge
                                    );
            }  
              AcGeLineSeg3d ls;
            AcGeCircArc3d as;
            double d = 0.0, p1 = 0.0, p2 = 1.0;
              for(int ver = 0; ver < nVertices; ver++)
            {
                es = testPoly.getBulgeAt( i, d );
                if( es != Acad::eOk )
                    break;
                  if( d <= 1e-5 )
                {
                    es = testPoly.getLineSegAt(ver, ls);
                    if( es != Acad::eOk )
                          break;
                    loopLength += ls.length();
                }
                else
                {
                    AcGePoint2d v1;
                    AcGePoint2d v2;
                    v1.set(
                            vertices[ver].x,
                            vertices[ver].y
                          );
                      if (ver == (nVertices - 1))
                    {
                        v2.set(
                                vertices[0].x,
                                vertices[0].y
                              );
                    }
                    else
                    {
                        v2.set(
                                 vertices[ver+1].x,
                                 vertices[ver+1].y
                              );
                    }
                      if (v1.isEqualTo(v2, AcGeContext::gTol)
                                        == Adesk::kFalse)
                    {
                        es = testPoly.getArcSegAt( i, as );
                        if( es != Acad::eOk )
                            break;
                          p1 = as.paramOf(as.startPoint());
                        p2 = as.paramOf(as.endPoint());
                          loopLength += as.length( p1, p2 );
                    }
                }
            }
        }   
        else
        {    
            AcGePoint2dArray vertices;    
            AcGeDoubleArray bulges;
            AcGeVoidPointerArray edgePtrs; 
            AcGeIntArray edgeTypes; 
              pHatch->getLoopAt(i, loopType,edgePtrs, edgeTypes ); 
            AcGeCompositeCurve2d compCurve( edgePtrs ); 
              AcGeInterval interval;   
            compCurve.getInterval( interval );
              loopLength
                = compCurve.length(
                                    interval.lowerBound(),
                                    interval.upperBound()
                                  );
        }  
          if( nLoops > 1 && !(loopType & AcDbHatch::kExternal ))    
            totalInternalPerimeter += loopLength;
        else
            totalExternalPerimeter += loopLength;
    } 
      acutPrintf(
                ACRX_T("\nExternal Perimeter : %lf"),
                totalExternalPerimeter
              );
      acutPrintf(
                ACRX_T("\nInternal Perimeter : %lf"),
                totalInternalPerimeter
              );
      pEnt->close();
}
      // Perimeter calculation of a hatch using AutoCAD.Net API
[CommandMethod("HatchTest")]
public void HatchTestMethod()
{
    Document activeDoc
            = Application.DocumentManager.MdiActiveDocument;
    Editor ed = activeDoc.Editor;
      PromptEntityOptions peo
        = new PromptEntityOptions("Select a hatch : ");
      peo.SetRejectMessage("\nPlease select a hatch");
    peo.AddAllowedClass(typeof(Hatch), true);
      PromptEntityResult per = ed.GetEntity(peo);
    if (per.Status != PromptStatus.OK)
        return;
      HatchPerimeter(per.ObjectId);
}
    void HatchPerimeter(ObjectId entId)
{
    Document activeDoc = Application.DocumentManager.MdiActiveDocument;
    Database db = activeDoc.Database;
    Editor ed = activeDoc.Editor;
      using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        Hatch hatch = tr.GetObject(entId, OpenMode.ForRead) as Hatch;
        int nLoops = hatch.NumberOfLoops;
          double totalExternalPerimeter =0.0;
        double totalInternalPerimeter =0.0;
          for(int i=0; i < nLoops; i++)
        {
            double loopLength = 0.0;
            HatchLoopTypes hlt = hatch.LoopTypeAt(i);
            HatchLoop hatchLoop = hatch.GetLoopAt(i);
              if ((hatch.LoopTypeAt(i) & HatchLoopTypes.Polyline)
                                    == HatchLoopTypes.Polyline)
            {
                BulgeVertexCollection bulges
                                            = hatchLoop.Polyline;
                  int nVertices = bulges.Count;
                Polyline testPoly = new Polyline(nVertices);
                  for(int vx = 0; vx < bulges.Count; vx++)
                {
                    BulgeVertex bv = bulges[vx];
                    testPoly.AddVertexAt(
                                            vx,
                                            bv.Vertex,
                                            bv.Bulge,
                                            1.0,
                                            1.0
                                        );
                }
                  LineSegment3d ls = new LineSegment3d();
                CircularArc3d cs = new CircularArc3d();
                double d = 0.0, p1 = 0.0, p2 = 1.0;
                  for(int ver = 0; ver < nVertices-1; ver++)
                {
                    d = testPoly.GetBulgeAt(ver);
                    if( d <= 1e-5 )
                    {
                        ls = testPoly.GetLineSegmentAt(ver);
                        loopLength += ls.Length;
                    }
                    else
                    {
                        Point2d v1
                            = new Point2d(
                                            bulges[ver].Vertex.X,
                                            bulges[ver].Vertex.Y
                                         );
                        Point2d v2
                            = new Point2d(
                                            bulges[ver + 1].Vertex.X,
                                            bulges[ver + 1].Vertex.Y
                                         );
                        if (v1.IsEqualTo(v2) == false)
                        {
                            cs = testPoly.GetArcSegmentAt(ver);
                            p1 = cs.GetParameterOf(cs.StartPoint);
                            p2 = cs.GetParameterOf(cs.EndPoint);
                              loopLength +=
                                cs.GetLength
                                (
                                    p1,
                                    p2,
                                    Tolerance.Global.EqualPoint
                                );
                        }
                    }
                }
            }
            else
            {
                Curve2dCollection curves = hatchLoop.Curves;
                if (curves != null)
                {
                    foreach (Curve2d curve in curves)
                    {
                        if (hatchLoop.LoopType
                            == HatchLoopTypes.External)
                        {
                            totalExternalPerimeter +=
                                    curve.GetLength(0.0, 1.0);
                        }
                        else
                        {
                            totalInternalPerimeter +=
                                    curve.GetLength(0.0, 1.0);
                        }
                    }
                }
            }
              if (    nLoops > 1 &&
                    ((hlt & HatchLoopTypes.External) != HatchLoopTypes.External))
            {
                totalInternalPerimeter += loopLength;
            }
            else
            {
                totalExternalPerimeter += loopLength;
            }
        }
          ed.WriteMessage(
                            string.Format
                            (
                                "\nExternal Perimeter : {0}",
                                totalExternalPerimeter
                            )
                       );
          ed.WriteMessage(
                            string.Format
                            (
                                "\nInternal Perimeter : {0}",
                                totalInternalPerimeter
                            )
                       );
        tr.Commit();
    }
}

## 评论

**内容**: Alexander Rivlis said...
Hi Balaji!
My colleague found a bug in your's code. As far as bulge can be < 0.0 then instead of:
if( d <= 1e-5 )
have to be in ObjectARX:
if( fabs(d) <= 1e-5 )
and in .NET:
if( Math.Abs(d) <= 1e-5)
Discussion: http://adn-cis.org/forum/index.php?topic=6078.msg18136#msg18136
Reply
03/16/2016 at 02:41 PM

---
