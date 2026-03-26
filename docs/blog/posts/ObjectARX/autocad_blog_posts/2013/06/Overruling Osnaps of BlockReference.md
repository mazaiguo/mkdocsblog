---
title: "Overruling Osnaps of BlockReference"
date: 2013-06-01
categories:
  - AutoCAD
tags:
  - Block
description: "When overruling the osnap points for a BlockReference, you may not want the osnap points of the entities that make the Block reference from getting..."
author: Autodesk
---
# Overruling Osnaps of BlockReference

发布日期: 2013-06-01

原始链接: https://adndevblog.typepad.com/autocad/2013/06/overruling-osnaps-of-blockreference.html

## 文章内容

By Balaji Ramamoorthy
When overruling the osnap points for a BlockReference, you may not want the osnap points of the entities that make the Block reference from getting snapped. For this, override the "IsContentSnappable" method of the "OsnapOverrule" class.
Here is a sample code to add the center point of the BlockReference as a osnap point and prevent all other osnap points, including those of the entities that make the BlockReference.
using System.Collections.Generic;
  public class ExtApp : IExtensionApplication
{
    static ObjectSnapOverrule m_osnapOverrule
                                    = new ObjectSnapOverrule();
    static Overrule[] m_overrules = new Overrule[]
    {
        m_osnapOverrule,
    };
    static List<ObjectId> m_overruledObjects = new List<ObjectId>();
    static bool m_overruleAdded = false;
      [CommandMethod("startOverrule")]
    static public void Start()
    {
        Document doc = Application.DocumentManager.MdiActiveDocument;
        Editor ed = doc.Editor;
          PromptEntityOptions peo = new PromptEntityOptions(
                        "Select a blockreference to overrule :"
                       );
          peo.SetRejectMessage("Not a block reference");
        peo.AddAllowedClass(
            typeof(Autodesk.AutoCAD.DatabaseServices.BlockReference),
            false);
          PromptEntityResult per = ed.GetEntity(peo);
        if (per.Status != PromptStatus.OK)
            return;
          ObjectId brefId = per.ObjectId;
          if (!m_overruledObjects.Contains(per.ObjectId))
        {
            m_overruledObjects.Add(brefId);
        }
          ObjectId[] ids = m_overruledObjects.ToArray();
        foreach (Overrule o in m_overrules)
        {
            o.SetIdFilter(ids);
            if (!m_overruleAdded)
            {
                Overrule.AddOverrule(
                    RXObject.GetClass(typeof(BlockReference)),
                    o,
                    false);
            }
        }
          Overrule.Overruling = true;
        m_overruleAdded = true;
          Application.DocumentManager.MdiActiveDocument.Editor.Regen();
    }
      [CommandMethod("stopOverrule")]
    static public void End()
    {
        foreach (Overrule o in m_overrules)
        {
            Overrule.RemoveOverrule(
                RXObject.GetClass(typeof(BlockReference)),
                o);
        }
        Overrule.Overruling = false;
        Application.DocumentManager.MdiActiveDocument.Editor.Regen();
    }
      void IExtensionApplication.Initialize() { }
      void IExtensionApplication.Terminate() { }
}
  class ObjectSnapOverrule : OsnapOverrule
{
    public override void GetObjectSnapPoints(
                                Entity entity,
                                ObjectSnapModes snapMode,
                                IntPtr gsSelectionMark,
                                Point3d pickPoint,
                                Point3d lastPoint,
                                Matrix3d viewTransform,
                                Point3dCollection snapPoints,
                                IntegerCollection geometryIds)
    {
        BlockReference bref = entity as BlockReference;
        if (bref != null)
        {
            Database db = entity.Database;
            using (Transaction t
                    = db.TransactionManager.StartTransaction())
            {
                BlockTableRecord btr
                    = t.GetObject(
                                    bref.BlockTableRecord,
                                    OpenMode.ForRead
                                 ) as BlockTableRecord;
                  // Add only the centerpoint as snap point
                Extents3d exts = bref.GeometricExtents;
                snapPoints.Add(
                    exts.MinPoint + (exts.MaxPoint - exts.MinPoint) * 0.5);
            }
        }
    }
      // Return false to prevent the entities that make the
    // block reference from getting snapped
    public override bool IsContentSnappable(Entity entity)
    {
        return false;
    }
}

## 评论

**内容**: 寺雷颠 said...
Balaji thanks for this helpful article, it really gives me great help.
While utilizing this code, i wanted to define some custom points(such as an endpoint of a line in a block reference)rather than MaxPoint or MinPoint in Extent of the block as the osnap point but failed to do it.
Do you have any idea about how to define a normal points(such as vertexes of polyline) in a block reference?
Thanks a lot.
Vincent
Reply
01/04/2015 at 07:38 PM

---
**内容**: Balaji said in reply to 寺雷颠...
Hi Vincent,
There should be no problem in doing that.
If you already know that point, simply add it to the snapPoints.
If not, explode the block reference to get a collection of entities and iterate them to identify the point. Add the point to the snapPoints collection. The entity collection resulting out of Explode can be discarded without adding them to the database.
Regards,
Balaji
Reply
01/05/2015 at 09:31 PM

---
