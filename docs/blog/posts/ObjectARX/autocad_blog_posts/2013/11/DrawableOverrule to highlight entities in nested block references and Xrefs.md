---
title: "DrawableOverrule to highlight entities in nested block references and Xrefs"
date: 2013-11-01
categories:
  - AutoCAD
tags:
  - Block
  - XREF
description: "Some time back, I had posted this blog post to change the color of entities using DrawableOverrule. But it did not handle entities in block referen..."
author: Autodesk
---
# DrawableOverrule to highlight entities in nested block references and Xrefs

发布日期: 2013-11-01

原始链接: https://adndevblog.typepad.com/autocad/2013/11/drawableoverrule-to-highlight-entities-in-nested-block-references-and-xrefs.html

## 文章内容

By Balaji Ramamoorthy
Some time back, I had posted this blog post to change the color of entities using DrawableOverrule. But it did not handle entities in block references well. Here is a completely rewritten code snippet that handles entities in block references, nested block references and Xrefs.
public class MyDrawOverrule : DrawableOverrule
{
    private bool mRegistered = false;
      private static bool mOldOverruleValue;
    public List<ObjectId> _containerIds = new List<ObjectId>();
    public ObjectId _selectedId = ObjectId.Null;
      public List<ObjectId> ContainerIds
    {
        get { return _containerIds; }
        set { _containerIds = value; }
    }
      public ObjectId SelectedId
    {
        get { return _selectedId; }
        set { _selectedId = value; }
    }
      public void Highlight()
    {
        if (!mRegistered)
        {
            Overrule.AddOverrule(RXObject.GetClass
                                (typeof(Entity)), this, false);
            SetCustomFilter();
            mOldOverruleValue = Overrule.Overruling;
            mRegistered = true;
        }
        Overrule.Overruling = true;
          Application.DocumentManager.MdiActiveDocument
                                              .Editor.Regen();
    }
      public override bool WorldDraw(    Drawable drawable,
                                    WorldDraw wd)
    {
        bool status = false;
          Entity ent = drawable as Entity;
          if(ContainerIds.Count == 0)
        {
            if(ent.ObjectId.Equals(_selectedId))
            {
                // Not a nested entity, but selected
                // for overruling
                  short oldColor = wd.SubEntityTraits.Color;
                wd.SubEntityTraits.Color = 2;
                  status = base.WorldDraw(drawable, wd);
                  wd.SubEntityTraits.Color = oldColor;
            }
            else
                status = base.WorldDraw(drawable, wd);
        }
        else if (ContainerIds.Contains(ent.ObjectId))
        { // Selected a nested entity
              status = base.WorldDraw(drawable, wd);
              ColorizeNested(ent, Matrix3d.Identity, wd);
        }
        else
        {
            status = base.WorldDraw(drawable, wd);
        }
          return status;
    }
      public bool ColorizeNested(    Entity ent,
                                Matrix3d transform,
                                WorldDraw wd)
    {
        bool status = false;
        if (ent is BlockReference
            && ContainerIds.Contains(ent.ObjectId))
        {
            BlockReference br = ent as BlockReference;
            transform
                = transform.PreMultiplyBy(br.BlockTransform);
              if (br.Database != null)
            {
                using (Transaction tr
                    = br.Database.TransactionManager
                                .StartOpenCloseTransaction())
                {
                    BlockTableRecord btr
                        = tr.GetObject(    br.BlockTableRecord,
                                        OpenMode.ForRead
                                      ) as BlockTableRecord;
                    foreach (ObjectId id in btr)
                    {
                        Entity btrEnt = tr.GetObject
                            (
                                id,
                                OpenMode.ForRead
                            ) as Entity;
                        if (btrEnt is BlockReference)
                        {
                            status = ColorizeNested(
                                    btrEnt, transform, wd);
                        }
                        else
                        {
                            if (btrEnt.ObjectId.Equals(
                                                _selectedId))
                            {
                                using (Entity entClone
                                    = btrEnt.Clone() as Entity)
                                {
                                    entClone.TransformBy
                                                  (transform);
                                    entClone.ColorIndex = 2;
                                    status
                                    = wd.Geometry.Draw(entClone);
                                }
                            }
                        }
                    }
                    tr.Commit();
                }
            }
        }
        return status;
    }
      public override bool IsApplicable(RXObject overruledSubject)
    {
        bool isApplicable = false;
        Entity ent = overruledSubject as Entity;
        if (ent != null)
        {
            if (ContainerIds.Count == 0)
            {
                if(ent.ObjectId.Equals(SelectedId))
                {
                    isApplicable = true;
                }
            }
            else if (ent.ObjectId.Equals(ContainerIds[0]))
            {
                isApplicable = true;
            }
        }
        return isApplicable;
    }
}
  public class Commands : IExtensionApplication
{
    private static MyDrawOverrule _myDrawOverrule
                                       = new MyDrawOverrule();
      [CommandMethod("HighlightEnt")]
    static public void HighlightEnt()
    {
        Document doc
              = Application.DocumentManager.MdiActiveDocument;
        Database db = doc.Database;
        Editor ed = doc.Editor;
          _myDrawOverrule.SelectedId = ObjectId.Null;
        _myDrawOverrule.ContainerIds.Clear();
        ObjectId selId = ObjectId.Null;
          PromptNestedEntityOptions pneo
            = new PromptNestedEntityOptions(
                           "\nSelect entity to highlight : ");
        PromptNestedEntityResult pner = ed.GetNestedEntity(pneo);
        if (pner.Status == PromptStatus.OK)
        {
            selId = pner.ObjectId;
            _myDrawOverrule.SelectedId = selId;
              List<ObjectId> objIds
                   = new List<ObjectId>(pner.GetContainers());
            if (objIds.Count > 0)
            {
                objIds.Reverse();
                foreach (ObjectId id in objIds)
                    _myDrawOverrule.ContainerIds.Add(id);
            }
              _myDrawOverrule.Highlight();
        }
    }
      void IExtensionApplication.Initialize(){}
      void IExtensionApplication.Terminate(){}
}

## 评论

**内容**: Macgyver700210 said...
Thank you for the code sample. It does exactly what I want. The only issue is that WorldDraw is only triggered in 2D wireframe, and not in any of the shaded Visual styles. Is this normal behavior?
Reply
07/31/2015 at 06:48 AM

---
**内容**: Macgyver700210 said in reply to Macgyver700210...
It looks like I have to send REGEN3 to the commandline. Is there a better way?
Reply
07/31/2015 at 08:17 AM

---
**内容**: John Herman said...
I ran the code and tried to highlight a cogopoint in a xref with no success. What extra measures are needed to enable the functionality on Civil 3d objects? Thanks.
Reply
10/29/2015 at 09:20 AM

---
