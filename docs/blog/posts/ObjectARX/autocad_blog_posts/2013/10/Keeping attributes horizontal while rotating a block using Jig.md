---
title: "Keeping attributes horizontal while rotating a block using Jig"
date: 2013-10-01
categories:
  - AutoCAD
tags:
  - Block
description: "Here is a sample code to specify the rotation of a block reference using a Jig while retaining the attribute rotation as demonstrated in this video."
author: Autodesk
---
# Keeping attributes horizontal while rotating a block using Jig

发布日期: 2013-10-01

原始链接: https://adndevblog.typepad.com/autocad/2013/10/keeping-attributes-horizontal-while-rotating-a-block-using-jig.html

## 文章内容

By Balaji Ramamoorthy
Here is a sample code to specify the rotation of a block reference using a Jig while retaining the attribute rotation as demonstrated in this video.
  class BlockJigCmds
{
    [CommandMethod("BJig")]
    public static void BJig()
    {
        Editor ed
        = Application.DocumentManager.MdiActiveDocument.Editor;
          PromptEntityOptions peo
        = new PromptEntityOptions("\nSelect a block reference: ");
          peo.SetRejectMessage("\nMust be a block reference...");
        peo.AddAllowedClass(typeof(BlockReference), true);
          PromptEntityResult per = ed.GetEntity(peo);
        if (per.Status != PromptStatus.OK)
            return;
          ObjectId brefId = per.ObjectId;
          BRotateJig bjig = new BRotateJig(brefId);
        if (bjig.DoIt())
        {
            // Jigging complete.
            // Make changes to the BlockReference based on the
            // final rotation value.
            Database db = HostApplicationServices.WorkingDatabase;
            using (Transaction tr
                    = db.TransactionManager.StartTransaction())
            {
                BlockReference bref = tr.GetObject(
                   brefId, OpenMode.ForWrite) as BlockReference;
                  // Update the final block reference rotation
                bref.Rotation = bjig._brefAngle;
                  // Update the final positions of the attribute references
                foreach (ObjectId id in bref.AttributeCollection)
                {
                    AttributeReference attref = tr.GetObject
                    (id, OpenMode.ForRead) as AttributeReference;
                      if (attref == null
                || bjig._attPos.ContainsKey(attref.Tag) == false)
                        continue;
                      attref.UpgradeOpen();
                    attref.Position = bjig._attPos[attref.Tag];
                }
                tr.Commit();
            }
        }
    }
}
  public class BRotateJig : DrawJig
{
    public Point3d _insPoint;
    public double _brefAngle = 0.0;
    private ObjectId _brefId = ObjectId.Null;
    private ObjectId _btrId = ObjectId.Null;
    private Extents3d _attExts = new Extents3d();
    private Dictionary<String, Vector3d> _attDisps;
    public Dictionary<String, Point3d> _attPos;
      public BRotateJig(ObjectId brefId)
    {
        // Id of the block reference that we will jig
        _brefId = brefId;
          Database db = HostApplicationServices.WorkingDatabase;
        using (Transaction tr = db.TransactionManager.StartTransaction())
        {
            BlockReference bref = tr.GetObject(
                brefId, OpenMode.ForWrite) as BlockReference;
              _btrId = bref.BlockTableRecord;
            _insPoint = bref.Position;
            _brefAngle = bref.Rotation;
              // We want to determine the extents of the
            // attributes without considering the rotation
            // that the block reference might already have.
            bref.Rotation = 0.0;
              // Determines the overall extents of the attribute
            // references in the block
            BlockTableRecord btr = tr.GetObject(
                _btrId, OpenMode.ForRead) as BlockTableRecord;
            foreach (ObjectId id in btr)
            {
                DBObject obj = id.GetObject(OpenMode.ForRead);
                AttributeDefinition attDef
                                = obj as AttributeDefinition;
                  if ((attDef != null) && (!attDef.Constant))
                {
                    using (AttributeReference attRef
                                    = new AttributeReference())
                    {
                        attRef.SetAttributeFromBlock(
                                attDef, bref.BlockTransform);
                          Extents3d exts = attRef.GeometricExtents;
                        _attExts.AddExtents(exts);
                    }
                }
            }
              // Stores the displacement of each attribute
            //reference with mid point as the reference
            // This is needed to keep the attribute references
            // straight after the block reference is rotated.
            Point3d midPt = _attExts.MinPoint +
                (_attExts.MaxPoint - _attExts.MinPoint) * 0.5;
              _attDisps = new Dictionary<string, Vector3d>();
            foreach (ObjectId id in btr)
            {
                DBObject obj = id.GetObject(OpenMode.ForRead);
                AttributeDefinition attDef
                                = obj as AttributeDefinition;
                  if ((attDef != null) && (!attDef.Constant))
                {
                    using (AttributeReference attRef
                                    = new AttributeReference())
                    {
                        attRef.SetAttributeFromBlock(
                                 attDef, bref.BlockTransform);
                          _attDisps.Add(attRef.Tag,
                                     attRef.Position - midPt);
                    }
                }
            }
              // Stores the positions of the attributes in the
            // rotated state.
            _attPos = new Dictionary<string, Point3d>();
                // The block reference rotation was set to 0.0
            // for calculating extents.
            // We do not want to save that change
            //tr.Commit();
        }
    }
      public bool DoIt()
    {
        Editor ed
        = Application.DocumentManager.MdiActiveDocument.Editor;
          PromptResult jigRes = null;
        jigRes = null;
        jigRes = ed.Drag(this);
        if (jigRes.Status != PromptStatus.OK)
            return false;
        return true;
    }
      protected override SamplerStatus Sampler(JigPrompts prompts)
    {
        JigPromptAngleOptions jigOpts = new JigPromptAngleOptions();
        jigOpts.UserInputControls =
                (UserInputControls.Accept3dCoordinates |
                 UserInputControls.NullResponseAccepted);
          jigOpts.Message = "Specify rotation :";
        jigOpts.BasePoint = _insPoint;
        jigOpts.UseBasePoint = true;
        jigOpts.Cursor = CursorType.RubberBand;
        PromptDoubleResult jigRes = prompts.AcquireAngle(jigOpts);
          double angle = jigRes.Value;
          if (_brefAngle == angle)
            return SamplerStatus.NoChange;
          _brefAngle = angle;
          if (jigRes.Status == PromptStatus.OK)
            return SamplerStatus.OK;
          return SamplerStatus.Cancel;
    }
      protected override bool WorldDraw(
            Autodesk.AutoCAD.GraphicsInterface.WorldDraw draw)
    {
        using (BlockReference bref
                       = new BlockReference(_insPoint, _btrId))
        {
            Database db = HostApplicationServices.WorkingDatabase;
            using (Transaction tr
                    = db.TransactionManager.StartTransaction())
            {
                BlockTableRecord btr = tr.GetObject(
                _btrId, OpenMode.ForRead) as BlockTableRecord;
                  foreach (ObjectId id in btr)
                {
                    DBObject obj = id.GetObject(OpenMode.ForRead);
                    AttributeDefinition attDef
                                  = obj as AttributeDefinition;
                    if ((attDef != null) && (!attDef.Constant))
                    {
                        using (AttributeReference attRef
                                    = new AttributeReference())
                        {
                            attRef.SetAttributeFromBlock
                                 (attDef, bref.BlockTransform);
                              Point3d midPt = _attExts.MinPoint
                            + (_attExts.MaxPoint-_attExts.MinPoint)
                                                        * 0.5;
                              Vector3d dir = midPt - bref.Position;
                              dir = dir.RotateBy(
                                   _brefAngle, Vector3d.ZAxis);
                              midPt = bref.Position.TransformBy
                                 (Matrix3d.Displacement(dir));
                              if (_attDisps.ContainsKey(attRef.Tag))
                            {
                                Point3d attPos =
                                midPt.TransformBy(
                                Matrix3d.Displacement(
                                       _attDisps[attRef.Tag]));
                                  attRef.Position = attPos;
                                  if (_attPos.ContainsKey(attRef.Tag))
                                    _attPos[attRef.Tag] = attPos;
                                else
                                    _attPos.Add(attRef.Tag, attPos);
                                  draw.Geometry.Draw(attRef);
                            }
                        }
                    }
                }
                tr.Commit();
            }
              bref.Rotation = _brefAngle;
            draw.Geometry.Draw(bref);
        }
        return true;
    }
}
Here is a sample drawing to try the "BJig" command. Download Test

## 评论

**内容**: Adam McAllister said...
Thank you for publishing this! How do I run this code in autocad?
Reply
07/21/2017 at 01:00 PM

---
