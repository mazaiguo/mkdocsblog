---
title: "Retrieving a Solid3d face normal through brep API"
date: 2012-07-01
categories:
  - AutoCAD .NET
tags:
  - API
  - C#
  - Database
  - Solid
description: "The following C# post illustrates how to retrieve a solid face normal through some of the functionalities of the BRep API:"
author: Autodesk
---
# Retrieving a Solid3d face normal through brep API

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/retrieving-a-solid3d-face-normal-through-brep-api.html

## 文章内容

By Philippe Leefsma
The following C# post illustrates how to retrieve a solid face normal through some of the functionalities of the BRep API:
// Returns normal vector to a solid3d face [Philippe Leefsma, 7/11/2012]
[CommandMethod("FaceNormal")]
public void FaceNormal()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      PromptEntityOptions peo = new PromptEntityOptions(
        "\nSelect a 3D solid: ");
      peo.SetRejectMessage("\nInvalid selection...");
    peo.AddAllowedClass(typeof(Solid3d), true);
      PromptEntityResult per = ed.GetEntity(peo);
      if (per.Status != PromptStatus.OK)
        return;
      PromptPointOptions ppo = new PromptPointOptions(
        "\nSelect a point on a face: ");
      ppo.AllowArbitraryInput = false;
      PromptPointResult ppr = ed.GetPoint(ppo);
      if (ppr.Status != PromptStatus.OK)
        return;
      Point3d point = ppr.Value;
      using (Transaction Tx = db.TransactionManager.StartTransaction())
    {
        Solid3d solid = Tx.GetObject(per.ObjectId, OpenMode.ForRead)
            as Solid3d;
          ObjectId[] ids = new ObjectId[] { per.ObjectId };
          FullSubentityPath path = new FullSubentityPath(
            ids, new SubentityId(SubentityType.Null, IntPtr.Zero));
          using (Brep brep = new Brep(path))
        {
            foreach (Autodesk.AutoCAD.BoundaryRepresentation.Face face in
                brep.Faces)
            {
                PointContainment ptContainment = new PointContainment();
                  using (BrepEntity brepEnt = face.GetPointContainment(
                    point,
                    out ptContainment))
                {
                    if (ptContainment == PointContainment.Inside ||
                        ptContainment == PointContainment.OnBoundary)
                    {
                        ed.WriteMessage("\nFace Normal at " +
                            PointToStr(point) + " = " +
                            VectToStr(GetFaceNormal(face, point)));
                    }
                }
            }
        }
          Tx.Commit();
    }
}
  // Small utility methods
private string VectToStr(Vector3d v)
{
    return "[" +
        v.X.ToString("F2") + ", " +
        v.Y.ToString("F2") + ", " +
        v.Z.ToString("F2")
        + "]";
}
  Vector3d GetFaceNormal(
    Autodesk.AutoCAD.BoundaryRepresentation.Face face,
    Point3d point)
{
    PointOnSurface ptOnSurf = face.Surface.GetClosestPointTo(point);
      Point2d param = ptOnSurf.Parameter;
      Vector3d normal = ptOnSurf.GetNormal(param);
      // It seems we cannot trust the
    // face.Surface.IsNormalReversed property,
    // so I am applying a small offset to the point on surface
    // and check if the offset point is inside the solid
    // in case it is inside (or on boundary),
    // the normal must be reversed
      Vector3d normalTest = normal.MultiplyBy(1E-6 / normal.Length);
       Point3d ptTest = point.Add(normalTest);
      PointContainment ptContainment = new PointContainment();
      bool reverse = false;
      using(BrepEntity brepEnt =
        face.Brep.GetPointContainment(
            ptTest,
            out ptContainment))
    {
        if(ptContainment != PointContainment.Outside)
        {
            reverse = true;
        }
    }
      return normal.MultiplyBy(reverse ? -1.0 : 1.0);
}

## 评论

**内容**: Konstantin said...
The FaceNormal routine doesn't calculate the correct normal vectors if the points are selected on the Edges of the Solid
To reconstruct :
Draw a solid3d Box and section it 2 times in almost vertical and horizontal sense, so that you can pick diverse points on diverse faces but NOT on Edges.
Pick points on Edges(onBoundary) and you get mostly the reverse normal meaning for Faces facing to -X, -Y, -Z and X, Y, Z you get [1.00, 0.00, 0.00], [0.00, 1.00, 0.00], [0.00, 0.00, 1.00] and [-1.00, 0.00, 0.00], [0.00, -1.00, 0.00], [0.00, 0.00, -1.00] respectively.
Picking points on the the Slice-Regions (onBoundary Face) results in correct Normals.
Reply
07/12/2012 at 02:01 AM

---
**内容**: Philippe Leefsma said...
Can you send me a sample document at philippe.leefsma@autodesk.com, mentionning exactly which points coordinates return incorrect normals.
Thanks.
Reply
07/12/2012 at 06:59 AM

---
**内容**: Konstantin said in reply to Philippe Leefsma...
before sending you the document, i want to make sure that i understand the matter correctly and check again !
Therefore my question :
What is the direction of a face normal of a solid box ?
Facing inwards (towards the inside space of the box) ...or outwards ?
Reply
07/13/2012 at 04:01 AM

---
**内容**: Philippe Leefsma said...
The normal should point outward
Reply
07/13/2012 at 05:55 AM

---
**内容**: Konstantin said in reply to Philippe Leefsma...
an Email has been sent to you !
Reply
07/16/2012 at 01:41 AM

---
**内容**: Philippe Leefsma said in reply to Konstantin...
I've updated the GetFaceNormal method with following code:
if(ptContainment != PointContainment.Outside)
{
reverse = true;
}
instead. The problem was caused by ptContainment = OnBoundary for points lying on the edges.
That new version should return correct normals for any points on the solid.
Thanks for your feedback on that post.
Reply
07/16/2012 at 10:04 AM

---
**内容**: Konstantin said in reply to Philippe Leefsma...
Fine seen... Everything works OK now !
Thanks.
Reply
07/18/2012 at 01:27 AM

---
