---
title: "Displaying entities in different colors using DrawableOverrule"
date: 2013-03-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - Unicode
description: "Recently, a developer wanted to know a method to display the entities in different colors to visually represent the results of a drawing comparison..."
author: Autodesk
---
# Displaying entities in different colors using DrawableOverrule

发布日期: 2013-03-01

原始链接: https://adndevblog.typepad.com/autocad/2013/03/displaying-entities-in-different-colors-using-drawableoverrule.html

## 文章内容

By Balaji Ramamoorthy
Recently, a developer wanted to know a method to display the entities in different colors to visually represent the results of a drawing comparison. A way to set the color for entities including those that are nested is explained in Kean's blog post :
Changing the colour of nested AutoCAD entities through .NET
Another way to show the entity in different colors would be to use of DrawableOverrule. But, the WorldDraw of the DrawableOverrule class does not use the color setting from the DrawableTraits for some entities such as MText. To overcome this limitation, the drawable is cloned inside the WorldDraw method before being assigned a new color.
Here is a sample code using this approach. Some of the helper methods to highlight / unhighlight and pick nested entities are from Kean's blog post that I mentioned about previously.
using Autodesk.AutoCAD.GraphicsInterface;
using System.Collections.Generic;
  public class MyDrawOverrule : DrawableOverrule
{
    public static List<ObjectId> _redIds = new List<ObjectId>();
    public static List<ObjectId> _yellowIds = new List<ObjectId>();
      public override bool WorldDraw(Drawable drawable, WorldDraw wd)
    {
        Entity mydrawable = drawable.Clone() as Entity;
          short colorIndex = 1;
        if (_yellowIds.Contains(drawable.Id))
            colorIndex = 2;
          wd.SubEntityTraits.Color = colorIndex;
        mydrawable.ColorIndex = colorIndex;
          return base.WorldDraw(mydrawable, wd);
    }
      public override int SetAttributes(Drawable drawable,
                                        DrawableTraits traits)
    {
        return base.SetAttributes(drawable, traits);
    }
}
  public class ColorizeClass : IExtensionApplication
{
    static MyDrawOverrule _do = null;
      [CommandMethod("Colorize")]
    public void ColorizeMethod()
    {
        Document doc = Application.DocumentManager.MdiActiveDocument;
        Editor ed = doc.Editor;
          if (_do != null)
        {
            ed.WriteMessage("Overruling is already active");
            return;
        }
          Transaction tr = doc.TransactionManager.StartTransaction();
        using (tr)
        {
            List<FullSubentityPath> paths1;
            SelectNestedEntities(   ed,
                                    out MyDrawOverrule._redIds,
                                    out paths1,
                                    "Red"
                                );
              List<FullSubentityPath> paths2;
            SelectNestedEntities(  ed,
                                    out MyDrawOverrule._yellowIds,
                                    out paths2,
                                    "Yellow"
                                 );
              _do = new MyDrawOverrule();
              Overrule.AddOverrule(
                RXObject.GetClass(typeof(Entity)),
                _do,
                true);
              List<ObjectId> ids = new List<ObjectId>();
            ids.AddRange(MyDrawOverrule._redIds.ToArray());
            ids.AddRange(MyDrawOverrule._yellowIds.ToArray());
            _do.SetIdFilter(ids.ToArray());
              Overrule.Overruling = true;
              if (MyDrawOverrule._redIds.Count > 0)
                UnhighlightSubEntities(paths1);
              if (MyDrawOverrule._yellowIds.Count > 0)
                UnhighlightSubEntities(paths2);
              tr.Commit();
        }
          ed.Regen();
    }
      private static bool SelectNestedEntities
        (
            Editor ed,
            out List<ObjectId> ids,
            out List<FullSubentityPath> paths,
            String colorName
        )
    {
        ids = new List<ObjectId>();
        paths = new List<FullSubentityPath>();
          // Loop until cancelled or completed
        PromptNestedEntityResult rs;
          do
        {
            rs = ed.GetNestedEntity(
                String.Format("\nSelect entity to color {0}: ",
                colorName));
              if (rs.Status == PromptStatus.OK)
            {
                ids.Add(rs.ObjectId);
                FullSubentityPath path = FullSubentityPath.Null;
                path = HighlightSubEntity(rs);
                if (path != FullSubentityPath.Null)
                    paths.Add(path);
            }
        } while (rs.Status == PromptStatus.OK);
          return (rs.Status == PromptStatus.Cancel);
    }
      // Ask the user to select a number of sub-entities.
    // These will have their ObjectIds and their sub-entity
    // paths (returned from the HighlightSubEntity() helper)
    // added to collections that are returned to the caller.
    private static bool SelectNestedEntities
        (
            Editor ed,
            out ObjectIdCollection ids,
            out List<FullSubentityPath> paths
        )
    {
        ids = new ObjectIdCollection();
        paths = new List<FullSubentityPath>();
          // Loop until cancelled or completed
        PromptNestedEntityResult rs;
          do
        {
            rs = ed.GetNestedEntity("\nSelect nested entity: ");
            if (rs.Status == PromptStatus.OK)
            {
                ids.Add(rs.ObjectId);
                FullSubentityPath path = FullSubentityPath.Null;
                path = HighlightSubEntity(rs);
                if (path != FullSubentityPath.Null)
                    paths.Add(path);
            }
        } while (rs.Status == PromptStatus.OK);
          // Cancel is the status when "enter" is used to
        // terminate the selection, which means we can't
        // use it to distinguish from an actual
        // cancellation.
        return (rs.Status == PromptStatus.Cancel);
    }
      // Unhighlight a set of sub-entities
    private static void UnhighlightSubEntities(
                                List<FullSubentityPath> paths)
    {
        for (int i = 0; i < paths.Count; i++)
        {
            ObjectId[] ids = paths[i].GetObjectIds();
            Entity ent
                = ids[0].GetObject(OpenMode.ForRead) as Entity;
            if (ent != null)
            {
                ent.Unhighlight(paths[i], false);
            }
        }
    }
      // Highlight a sub-entity based on its nested
    // selection information.
    // Return the calculated sub-entity path, so
    // the calling application can later unhighlight.
    private static FullSubentityPath HighlightSubEntity(
                                    PromptNestedEntityResult rs)
    {
        // Extract relevant information from the prompt object
        ObjectId selId = rs.ObjectId;
        List<ObjectId> objIds = new List<ObjectId>(rs.GetContainers());
          // Reverse the "containers" list
        objIds.Reverse();
          // Now append the selected entity
        objIds.Add(selId);
          // Retrieve the sub-entity path for this entity
        SubentityId subEnt
            = new SubentityId(SubentityType.Null, System.IntPtr.Zero);
          FullSubentityPath path
            = new FullSubentityPath(objIds.ToArray(), subEnt);
          // Open the outermost container, relying on the open transaction...
        Entity ent = objIds[0].GetObject(OpenMode.ForRead) as Entity;
          // ... and highlight the nested entity
        if (ent == null)
            return FullSubentityPath.Null;
          ent.Highlight(path, false);
          // Return the sub-entity path for later unhighlighting
        return path;
    }
      void IExtensionApplication.Initialize() { }
      void IExtensionApplication.Terminate()
    {
        if (_do != null)
        {
            Overrule.Overruling = false;
            Overrule.RemoveOverrule(
                RXObject.GetClass(typeof(Entity)),
                _do);
        }
    }
}

## 评论

**内容**: mohan said...
Hi Balaji,
Thanks for the detailed implementation. It worked fine for me except one problem. In my architectural drawing I have 2 sofas(block references) that are referring the same block(sofa). Now, if I colorize one sofa, the other one also gets that color. Is there any way to fix this?
Regards,
Mohan.
Reply
03/28/2013 at 11:55 PM

---
**内容**: Balaji said in reply to mohan...
Hi Mohan,
I have tried to address this in a different blog post :
http://adndevblog.typepad.com/autocad/2013/11/drawableoverrule-to-highlight-entities-in-nested-block-references-and-xrefs.html
Sorry, I think I had given up too quickly when you first asked about it.
Hope this helps.
Regards,
Balaji
Reply
11/09/2013 at 08:12 AM

---
**内容**: Balaji said...
Hi Mohan,
Sorry, I couldnt reply promptly. I needed some time to investigate the possibility of doing it.
I dont think this is possible to do with DrawableOverule.
When AutoCAD calls the “WorldDraw” of the DrawableOverrule, the drawable that is obtained as the first parameter does not hold any information regarding the blockreference.
Inside the “WorldDraw” the “drawableEntity.OwnerId.Handle” refers to the block definition.
During the nested entity selection, the “FullSubentityPath” has the ObjectId of the block reference as well as the selected subentity. Since the same info isn’t available in the “WorldDraw” of the DrawableOverrule, there is no way to colorize the entities independently.
Reply
04/18/2013 at 04:08 AM

---
