---
title: "How to test the winding (turn) of a closed polyline?"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - Polyline
description: "You can determine whether a polyline is winding clockwise or counterclockwise by tracking round the polyline, and checking if each segment bends to..."
author: Autodesk
---
# How to test the winding (turn) of a closed polyline?

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/how-to-test-the-winding-turn-of-a-closed-polyline.html

## 文章内容

By Gopinath Taget
You can determine whether a polyline is winding clockwise or counterclockwise by tracking round the polyline, and checking if each segment bends to the left or the right.  The following code snippet does this. It sums up the total turn of each segment. This can be within the segment ( if its an arc ) or between one segment and the next. The result of the function is a winding number. If it winds to the left, it will be positive; if it winds to the right, it will be negative. Note that the algorithm does not determine whether the polyline is self-intersecting and could even fail if the polyline is indeed self-intersecting.
Adesk::Boolean polyWindingNumber( AcDbPolyline*pPoly, int&winding )
{ 
 if( !pPoly->isClosed() )
{   
  return Adesk::kFalse;  
}  
 double turn = 0; 
 int nSegs = pPoly->numVerts(); 
AcGeVector3dArray startTans(nSegs);  
AcGeVector3dArray endTans(nSegs);  
 double TWOPI = 6.28318530718; 
 double PIBYTWO = 1.570796326795;  
 for( int i=0;i<nSegs; i++ )
{
  if( pPoly->segType(i) == AcDbPolyline::kArc )
  {    
   AcGeCircArc2d arc;   
   pPoly->getArcSegAt(i, arc );  
   AcGeVector2d startTan;  
   AcGeVector2d endTan;    
   AcGeVector2dArray startDerivs;  
   arc.evalPoint( arc.startAng(), 1, startDerivs );
   startTan = startDerivs[0];     
   AcGeVector2dArray endDerivs;     
   arc.evalPoint( arc.endAng(), 1, endDerivs);   
   endTan = endDerivs[0];   
   startTans.append(AcGeVector3d(startTan.x, startTan.y,0.0));
   endTans.append(AcGeVector3d(endTan.x, endTan.y, 0.0));        
   double ang = arc.endAng() - arc.startAng();     
   turn += arc.isClockWise() ? -ang : ang;     
  }    
  else if(pPoly->segType(i) == AcDbPolyline::kLine )
  {
   AcGeLineSeg2d line;
   pPoly->getLineSegAt(i, line );
   AcGeVector2d tan2d = line.endPoint() -line.startPoint();  
   AcGeVector3d tan = AcGeVector3d( tan2d.x, tan2d.y, 0.0);  
   startTans.append(tan);  
   endTans.append(tan);
  }
}
nSegs = startTans.length();  
   for(int i=0;i<nSegs; i++ )
{
  double angle = endTans[i].angleTo( startTans[(i+1)%nSegs] );   
  AcGeVector3d norm =  endTans[i].crossProduct(
   startTans[(i+1)%nSegs] ); 
  angle = norm.z > 0 ? angle: -angle;
  turn += angle; 
}
turn = turn / TWOPI;
 double lower = floor( turn ); 
 double tol = 1e-6; 
 if( (turn - lower ) < tol)     
  winding = (int)lower;  
 else if( (( lower + 1 ) - turn ) <  tol )
  winding = (int)(lower + 1); 
 else
  return Adesk::kFalse;
   return Adesk::kTrue;
}
  static void AsdkUtilsPolyWind(void)
{
ads_name eName;
ads_point pt;
 if( RTNORM !=
  acedEntSel(L"\nPlease pick a polyline to test", eName, pt) )
  return;
AcDbObjectId id; 
acdbGetObjectId( id, eName ); 
AcDbPolyline*pPoly;  
acdbOpenObject(pPoly, id, AcDb::kForRead );
 if(pPoly == NULL )     
  return;
 int winding =0;
 if( polyWindingNumber(pPoly, winding ) )
{  
  acutPrintf(L"\nPolygon has winding number %d", winding ); 
} 
 else
{ 
  acutPrintf(L"\nCannot calculate winding number for polyline");
}
pPoly->close();
}

## 评论

**内容**: Dale Bartlett said...
Hi Gopinath, Is this possible in .NET? Also many thanks for your very helpful blog. Dale
Reply
10/30/2013 at 10:35 PM

---
**内容**: fixo said in reply to Dale Bartlett...
It's may be too late, anyway:
//http://adndevblog.typepad.com/autocad/2013/01/how-to-test-the-winding-turn-of-a-closed-polyline.html
// by Gopinath Taget, ugly converted by me
static bool polyWindingNumber(Polyline pPoly, out int winding)
{
if (!pPoly.Closed)
{
winding = 0;
return false;
}
double turn = 0;
int nSegs = pPoly.NumberOfVertices;
Vector3dCollection startTans = new Vector3dCollection();
Vector3dCollection endTans = new Vector3dCollection();
double PI2 = Math.Round(Math.PI * 2, 12); //6.28318530718;
for (int i = 0; i < nSegs; i++)
{
if (pPoly.GetSegmentType(i) == SegmentType.Arc)
{
CircularArc2d arc = pPoly.GetArcSegment2dAt(i);
Vector2d startTan;
Vector2d endTan;
Vector2dCollection startDerivs = new Vector2dCollection();
startDerivs.Add(arc.EvaluatePoint(arc.StartAngle).GetAsVector());
startTan = startDerivs[0];
Vector2dCollection endDerivs = new Vector2dCollection();
Point2d ap2 = arc.EvaluatePoint(arc.EndAngle);
endDerivs.Add(arc.EvaluatePoint(arc.StartAngle).GetAsVector());
endTan = endDerivs[0];
startTans.Add(new Vector3d(startTan.X, startTan.Y, 0.0));
endTans.Add(new Vector3d(endTan.X, endTan.Y, 0.0));
double ang = arc.EndAngle - arc.StartAngle;
turn += arc.IsClockWise ? -ang : ang;
}
else if (pPoly.GetSegmentType(i) == SegmentType.Line)
{
LineSegment2d line = pPoly.GetLineSegment2dAt(i);
Vector2d tan2d = line.EndPoint - line.StartPoint;
Vector3d tan = new Vector3d(tan2d.X, tan2d.Y, 0.0);
startTans.Add(tan);
endTans.Add(tan);
}
}
nSegs = startTans.Count;
for (int i = 0; i < nSegs; i++)
{
double angle = endTans[i].GetAngleTo(startTans[(i + 1) % nSegs]);
Vector3d norm = endTans[i].CrossProduct(startTans[(i + 1) % nSegs]);
angle = norm.Z > 0 ? angle : -angle;
turn += angle;
}
turn = turn / PI2;
double lower = Math.Floor(turn);
double tol = 1e-6;
if ((turn - lower) < tol)
winding = (int)lower;
else if (((lower + 1) - turn) < tol)
winding = (int)(lower + 1);
else
{
winding = 0;
return false;
}
return true;
}
[CommandMethod("ISCC")]
public static void TestAsdkUtilsPolyWind()
{
Document doc = Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument;
Editor ed = doc.Editor;
Database db = doc.Database;
SelectionFilter filt = new SelectionFilter(new TypedValue[]{
new TypedValue(0,"lwpolyline"),
new TypedValue(70,1)});
PromptSelectionResult res = ed.GetSelection(filt);
if (res.Status != PromptStatus.OK) return;
SelectionSet sset = res.Value;
SelectedObject obj = sset[0];
using (Transaction tr = db.TransactionManager.StartTransaction())
{
Entity ent = tr.GetObject(obj.ObjectId, OpenMode.ForRead) as Entity;
if (ent == null)
return;
Polyline poly = ent as Polyline;
if (poly == null) return;
int winding = 0;
if (polyWindingNumber(poly, out winding))
{
ed.WriteMessage("\nPolygon has winding number {0}", winding == 1 ? "CounterClockWise" : "ClockWise");
}
else
{
ed.WriteMessage("\nCannot calculate winding number for polyline");
}
tr.Commit();
}
}
Reply
12/18/2013 at 11:36 AM

---
