---
title: "Overruling grips for a Group"
date: 2013-11-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "From the class hierarchy we realize that a Group is not derived from Entity class. It is a DBObject and resides in a dictionary. So, to overrule th..."
author: Autodesk
---
# Overruling grips for a Group

发布日期: 2013-11-01

原始链接: https://adndevblog.typepad.com/autocad/2013/11/overruling-grips-for-a-group.html

## 文章内容

By Balaji Ramamoorthy
From the class hierarchy we realize that a Group is not derived from Entity class. It is a DBObject and resides in a dictionary. So, to overrule the grips of a Group, we need to overrule the grips of entities that belong to the group. When a group is selected in AutoCAD, it displays the grips of the entities that belong to the group or a single grip, depending on the value set for the "GroupDisplayMode" system variable. The overruling demonstrated in this sample code requires the "GroupDisplayMode" system variable to be set to "0". In that case, AutoCAD attempts to display the grips of the all entities that are part of the group and our overruling then takes effect.
Here is a sample code and a screenshot of the result 
static GripPointOverrule m_gripOverrule
                                    = new GripPointOverrule();
static Overrule[] m_overrules = new Overrule[]
{
    m_gripOverrule,
};
static bool m_overruleAdded = false;
  [CommandMethod("GGO")]
static public void GroupGripOverrule()
{
    if (! m_overruleAdded)
    {
        m_gripOverrule = new GripPointOverrule();
        Overrule.AddOverrule
        (
            RXObject.GetClass(
            typeof(Autodesk.AutoCAD.DatabaseServices.Entity)),
            m_gripOverrule,
            true
        );
        m_gripOverrule.SetCustomFilter();
        Overrule.Overruling = true;
          m_overruleAdded = true;
    }
    else
    {
        Overrule.RemoveOverrule
        (
            RXObject.GetClass(
            typeof(Autodesk.AutoCAD.DatabaseServices.Entity)),
            m_gripOverrule
        );
        Overrule.Overruling = false;
        m_gripOverrule.Dispose();
        m_gripOverrule = null;
          m_overruleAdded = false;
    }
      Application.DocumentManager.MdiActiveDocument.Editor.Regen();
}
  class GripPointOverrule : GripOverrule
{
    internal GripPointOverrule() { }
      internal class MyGrip : GripData
    {
        public MyGrip() { }
          public override bool ViewportDraw
            (
                ViewportDraw vd,
                ObjectId entityId,
                GripData.DrawType type,
                Point3d? imageGripPoint,
                int gripSize
            )
        {
            Point2d unit
            = vd.Viewport.GetNumPixelsInUnitSquare(GripPoint);
            vd.SubEntityTraits.Color = 2;
              vd.SubEntityTraits.FillType = FillType.FillAlways;
            double radius = gripSize / unit.X;
            vd.Geometry.Circle
                (GripPoint, radius, vd.Viewport.ViewDirection);
              return true;
        }
    }
      List<GripData> m_grips = new List<GripData>();
      public override void GetGripPoints
        (
            Entity entity,
            GripDataCollection grips,
            double curViewUnitSize,
            int gripSize,
            Vector3d curViewDir,
            GetGripPointsFlags bitFlags
        )
    {
        // We do not want the default entity grips
        //base.GetGripPoints(entity, grips, curViewUnitSize, gripSize, curViewDir, bitFlags);
          // Find the extents of the entities in the group
        Extents3d groupExts = new Extents3d();
        using (Transaction tr
        = entity.Database.TransactionManager.StartTransaction())
        {
            ObjectIdCollection ids = entity.GetPersistentReactorIds();
            foreach (ObjectId id in ids)
            {
                DBObject obj = tr.GetObject(id, OpenMode.ForRead);
                if (obj is Group)
                {
                    Group group = obj as Group;
                    ObjectId[] entIds = group.GetAllEntityIds();
                    foreach (ObjectId entId in entIds)
                    {
                        Entity cogroupEnt =
                        tr.GetObject
                        (
                            entId,
                            OpenMode.ForRead
                        ) as Entity;
                          if (cogroupEnt != null)
                        {
                            Extents3d exts
                                = cogroupEnt.GeometricExtents;
                            groupExts.AddExtents(exts);
                        }
                    }
                }
            }
            tr.Commit();
        }
          // Add a single grip at the min point of the
        // group extents
        MyGrip myGripData = new MyGrip();
        myGripData.GripPoint = groupExts.MinPoint;
        m_grips.Add(myGripData);
        grips.Add(myGripData);
    }
      public override void MoveGripPointsAt
        (
            Entity entity,
            GripDataCollection grips,
            Vector3d offset,
            MoveGripPointsFlags bitFlags
        )
    {
        foreach(GripData grip in grips)
        {
            MyGrip myGrip = grip as MyGrip;
            if (myGrip != null)
            {
                entity.TransformBy(
                                Matrix3d.Displacement(offset));
            }
            else
                base.MoveGripPointsAt(
                            entity, grips, offset, bitFlags);
        }
    }
      // Overrule only entities that belong to a group
    public override bool IsApplicable(RXObject overruledSubject)
    {
        bool isApplicable = false;
        try
        {
            Entity ent = overruledSubject as Entity;
            if (ent != null && ent.Database != null)
            {
                // Check if the entity is part of a group
                using (Transaction tr
                    = ent.Database.TransactionManager.StartTransaction())
                {
                    ObjectIdCollection ids
                                = ent.GetPersistentReactorIds();
                    foreach (ObjectId id in ids)
                    {
                        DBObject obj
                        = tr.GetObject(id, OpenMode.ForRead);
                        if (obj is Group)
                        {
                            Group group = obj as Group;
                            if (group != null)
                            {
                                // If the entity belongs to
                                // a group, we will overrule it
                                isApplicable = true;
                            }
                        }
                    }
                    tr.Commit();
                }
            }
        }
        catch (System.Exception ex)
        {
            Application.DocumentManager.MdiActiveDocument
                            .Editor.WriteMessage(ex.Message);
        }
        return isApplicable;
    }
}

## 评论

**内容**: kelo said...
In my program, IsApplicable not running
Reply
11/30/2013 at 05:22 PM

---
**内容**: Balaji said in reply to kelo...
Hi Kelo,
For "isApplicable" to be called, you will need to call the SetCustomFilter as in the sample code from this blog post.
Regards,
Balaji
Reply
12/01/2013 at 02:51 AM

---
**内容**: kelo said in reply to Balaji...
Thank you!You're right.
Reply
12/01/2013 at 07:02 PM

---
**内容**: kelo said...
My GripOverrule, Use custom GripData, In GetGripPoints, read entity Xrecord, when grip entity, modify object properties, if the use of features preview, AutoCAD crashes
Reply
11/30/2013 at 06:09 PM

---
**内容**: kelo said...
My GripOverrule
mygrip.AlternateBasePoint = CType (pt, System.Nullable (Of Point3d))
when grip entity, AutoCAD crashes
Reply
11/30/2013 at 06:14 PM

---
**内容**: Balaji said in reply to kelo...
Hi Kelo,
I do not think it is permitted to change the entity properties from the GetGripPoints which might explain the crash.
As you see in the sample code, we only retrieve information that can help us determine the grip point. It does not change the entity itself.
You may need to refactor your code to do such changes in a more appropriate callback.
Regards,
Balaji
Reply
12/01/2013 at 03:03 AM

---
**内容**: kelo said in reply to Balaji...
Thank you.I find,same code,work in Windows XP No problem,work in Windows 8 63bit AutoCAD crashes
.
Reply
12/01/2013 at 07:05 PM

---
**内容**: Tony Tanzillo said...
Hi Balaji.
Is your code listing complete? It seems that there is an enclosing class missing.
Also, doesn't your overrule's GetGripPoints() override get called (redundantly) for every selected entity in a group, each time producing the same result?
You might want to rethink your approach to solving this problem, and take into account (1) that the work done by your Grip overrule will be done redundantly for every selected entity in the same group, and (2) that entities can be members of more than one group, and (3) that you don't have to open the ObjectIds returned by GetPersistentReactorIds() to find out if one of them is the ObjectId of a Group (by using the ObjectId's ObjectClass property).
Reply
12/12/2013 at 09:30 PM

---
**内容**: Balaji said in reply to Tony Tanzillo...
Hi Tony,
Yes, the post does not include the class that encloses the command. I had intentionally left it out. I thought the developers would only be interested in the command method and would copy that portion to their command class.
Thanks for your nice suggestions. I had not thought much about optimizing it and I will include your suggestions and update the post.
Regards,
Balaji
Reply
12/13/2013 at 02:27 AM

---
