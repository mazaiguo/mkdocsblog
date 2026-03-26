---
title: "Mirroring a DBText Entity"
date: 2013-10-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - Database
  - Unicode
description: "Some time ago when this blog did not yet exist, I wrote the following .Net code to mirror a DBText entity in order to solve one of our ADN case. Ma..."
author: Autodesk
---
# Mirroring a DBText Entity

发布日期: 2013-10-01

原始链接: https://adndevblog.typepad.com/autocad/2013/10/mirroring-a-dbtext-entity.html

## 文章内容

By Philippe Leefsma
Some time ago when this blog did not yet exist, I wrote the following .Net code to mirror a DBText entity in order to solve one of our ADN case. Many moons later that question popped up again, so here is the proposed solution. You will see that it isn’t so straightforward that you may think:
// Mirrors a DBText entity, by Philippe Leefsma 4/10/2013
  [CommandMethod("MirrorTextCmd")]
public void MirrorTextCmd()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      //Entity selection
    PromptEntityOptions peo = new PromptEntityOptions(
        "\nSelect a text entity:");
      peo.SetRejectMessage("\nMust be text entity...");
    peo.AddAllowedClass(typeof(DBText), true);
      PromptEntityResult perText = ed.GetEntity(peo);
      if (perText.Status != PromptStatus.OK)
        return;
      peo = new PromptEntityOptions("\nSelect a mirror line:");
    peo.SetRejectMessage("\nMust be a line entity...");
    peo.AddAllowedClass(typeof(Line), true);
      PromptEntityResult perLine = ed.GetEntity(peo);
      if (perLine.Status != PromptStatus.OK)
        return;
      using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        Line line = tr.GetObject(perLine.ObjectId, OpenMode.ForRead)
            as Line;
          Line3d mirrorLine = new Line3d(
            line.StartPoint,
            line.EndPoint);
          MirrorText(perText.ObjectId, mirrorLine);
          tr.Commit();
    }
}
  void MirrorText(ObjectId TextId, Line3d mirrorLine)
{
    Database db = TextId.Database;
      using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        BlockTableRecord btr = tr.GetObject(
            db.CurrentSpaceId,
            OpenMode.ForWrite) as BlockTableRecord;
          // Get text entity
        DBText dbText = tr.GetObject(TextId, OpenMode.ForRead)
            as DBText;
          // Clone original entity
        DBText mirroredTxt = dbText.Clone() as DBText;
          // Create a mirror matrix
        Matrix3d mirrorMatrix = Matrix3d.Mirroring(mirrorLine);
          // Do a geometric mirror on the cloned text
        mirroredTxt.TransformBy(mirrorMatrix);
          // Get text bounding box
        Point3d pt1, pt2, pt3, pt4;
        GetTextBoxCorners(
            dbText,
            out pt1,
            out pt2,
            out pt3,
            out pt4);
          // Get the perpendicular direction to the original text
        Vector3d rotDir =
            pt4.Subtract(pt1.GetAsVector()).GetAsVector();
          // Get the colinear direction to the original text
        Vector3d linDir =
            pt3.Subtract(pt1.GetAsVector()).GetAsVector();
          // Compute mirrored directions
        Vector3d mirRotDir = rotDir.TransformBy(mirrorMatrix);
        Vector3d mirLinDir = linDir.TransformBy(mirrorMatrix);
          //Check if we need to mirror in Y or in X
        if (Math.Abs(mirrorLine.Direction.Y) >
            Math.Abs(mirrorLine.Direction.X))
        {
            // Handle the case where text is mirrored twice
            // instead of doing "oMirroredTxt.IsMirroredInX = true"
            mirroredTxt.IsMirroredInX = !mirroredTxt.IsMirroredInX;
            mirroredTxt.Position = mirroredTxt.Position + mirLinDir;
        }
        else
        {
            mirroredTxt.IsMirroredInY = !mirroredTxt.IsMirroredInY;
            mirroredTxt.Position = mirroredTxt.Position + mirRotDir;
        }
          // Add mirrored text to database
        btr.AppendEntity(mirroredTxt);
        tr.AddNewlyCreatedDBObject(mirroredTxt, true);
          tr.Commit();
    }
}
  // We need a bunch of P/Invoked functions to retrieve a DBtext
// bounding box because "acedTextBox" API is not exposed to .Net
  public struct ads_name
{
    public IntPtr a;
    public IntPtr b;
};
  // Exported function names valid only for R19
  [DllImport("acdb19.dll",
    CallingConvention = CallingConvention.Cdecl,
    EntryPoint = "?acdbGetAdsName@@YA?AW4ErrorStatus@Acad@@AAY01JVAcDbObjectId@@@Z")]
public static extern int acdbGetAdsName32(
    ref ads_name name,
    ObjectId objId);
  [DllImport("acdb19.dll",
    CallingConvention = CallingConvention.Cdecl,
    EntryPoint = "?acdbGetAdsName@@YA?AW4ErrorStatus@Acad@@AEAY01_JVAcDbObjectId@@@Z")]
public static extern int acdbGetAdsName64(
    ref ads_name name,
    ObjectId objId);
  public static int acdbGetAdsName(ref ads_name name, ObjectId objId)
{
    if (Marshal.SizeOf(IntPtr.Zero) > 4)
        return acdbGetAdsName64(ref name, objId);
      return acdbGetAdsName32(ref name, objId);
}
  [DllImport("accore.dll",
    CharSet = CharSet.Unicode,
    CallingConvention = CallingConvention.Cdecl,
    EntryPoint = "acdbEntGet")]
public static extern System.IntPtr acdbEntGet(
    ref ads_name ename);
  [DllImport("accore.dll",
    CharSet = CharSet.Unicode,
    CallingConvention = CallingConvention.Cdecl,
    EntryPoint = "acedTextBox")]
public static extern System.IntPtr acedTextBox(
    IntPtr rb,
    double[] point1,
    double[] point2);
  void GetTextBoxCorners(
    DBText dbText,
    out Point3d pt1,
    out Point3d pt2,
    out Point3d pt3,
    out Point3d pt4)
{
    ads_name name = new ads_name();
      int result = acdbGetAdsName(
        ref name,
        dbText.ObjectId);
      ResultBuffer rb = new ResultBuffer();
      Interop.AttachUnmanagedObject(
        rb,
        acdbEntGet(ref name), true);
      double[] point1 = new double[3];
    double[] point2 = new double[3];
      // Call imported arx function
    acedTextBox(rb.UnmanagedObject, point1, point2);
      pt1 = new Point3d(point1);
    pt2 = new Point3d(point2);
      // Create rotation matrix
    Matrix3d rotMat = Matrix3d.Rotation(
        dbText.Rotation,
        dbText.Normal,
        pt1);
      // The returned points from acedTextBox need
    // to be transformed as follow
    pt1 = pt1.TransformBy(rotMat).Add(dbText.Position.GetAsVector());
    pt2 = pt2.TransformBy(rotMat).Add(dbText.Position.GetAsVector());
      Vector3d rotDir = new Vector3d(
        -Math.Sin(dbText.Rotation),
        Math.Cos(dbText.Rotation), 0);
      Vector3d linDir = rotDir.CrossProduct(dbText.Normal);
      double actualWidth =
        Math.Abs((pt2.GetAsVector() - pt1.GetAsVector())
            .DotProduct(linDir));
      pt3 = pt1.Add(linDir * actualWidth);
    pt4 = pt2.Subtract(linDir * actualWidth);
}
Here is a screenshot of the astonishing result!

## 评论

**内容**: imadhabash@hotmail.com said...
Hi,
Is there a way to mirror a text and attributes inside Xref's ?
Thanks,
Reply
10/07/2013 at 11:54 PM

---
**内容**: Philippe Leefsma said in reply to imadhabash@hotmail.com...
Hi, doing the mirroring in an xref should be not much different than in the current drawing, you would just need to access the xref database and work with it as side database. We have several examples on our or Kean's blog dealing with that topic. Here is one I could spot:
http://through-the-interface.typepad.com/through_the_interface/2009/05/importing-autocad-layers-from-xrefs-using-net.html
Reply
10/10/2013 at 04:44 AM

---
**内容**: shay said...
Hi,
Is it possible to mirror the whole layout. for example i have a layout of the house floor plan and i wanted to mirror out.
Reply
05/10/2017 at 08:08 AM

---
