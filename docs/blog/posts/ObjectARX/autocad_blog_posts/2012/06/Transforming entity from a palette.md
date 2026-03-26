---
title: "Transforming entity from a palette"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - Palette
  - Selection
description: "To transform a selected entity on button click from your own palette, you could simply send a command that transforms the entity. A small inconveni..."
author: Autodesk
---
# Transforming entity from a palette

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/transforming-entity-from-a-palette.html

## 文章内容

By Balaji Ramamoorthy
To transform a selected entity on button click from your own palette, you could simply send a command that transforms the entity. A small inconvenience in this approach is that the entity that was selected becomes deselected after the command ends. To continue to transform the same entity using the palette, the user will again have to select it.
A way to overcome this behavior is to set the implied selection back to what it was originally. Here is a sample code to rotate a selected entity on click of a button placed in our palette. The selected entity is retained for rotation until the user deselects by pressing the escape key.
Here is the implementation of the rotate command that transforms the selected entity
RotationUserControl ctrl = null;
PaletteSet set = null;
  [CommandMethod("RotationPal")]
public void commandMethodTest()
{
    Document activeDoc = Application.DocumentManager.MdiActiveDocument;
    Database db = activeDoc.Database;
    Editor ed = activeDoc.Editor;
      if (set == null)
    {
        set = new PaletteSet("Entity Rotate Palette");
          if (ctrl == null)
        {
            ctrl = new RotationUserControl();
            set.Add("Rotation palette", ctrl);
              set.MinimumSize = new System.Drawing.Size(300, 300);
            set.Style = PaletteSetStyles.ShowTabForSingle |
                        PaletteSetStyles.NameEditable |
                        PaletteSetStyles.ShowCloseButton;
        }
    }
    set.Visible = true;
}
  [CommandMethod("RotateSelected", CommandFlags.UsePickSet | CommandFlags.Redraw)]
public void RotateSelectedMethod()
{
    Document activeDoc = Application.DocumentManager.MdiActiveDocument;
    Database db = activeDoc.Database;
    Editor ed = activeDoc.Editor;
      try
    {
        PromptSelectionResult result = ed.SelectImplied();
        if (result.Status != PromptStatus.OK)
            return;
          SelectionSet ss = result.Value;
        ObjectId[] ids = ss.GetObjectIds();
          ObjectId oid = ids[0];
          using (Transaction tr
                    = db.TransactionManager.StartTransaction())
        {
            Entity ent = tr.GetObject(
                                        oid,
                                        OpenMode.ForWrite
                                     ) as Entity;
            ent.TransformBy
                            (
                            Matrix3d.Rotation(
                                                Math.PI / 4.0,
                                                Vector3d.ZAxis,
                                                Point3d.Origin
                                              )
                            );
              tr.Commit();
        }
        ed.SetImpliedSelection(ids);
    }
    catch (System.Exception ex)
    {
        ed.WriteMessage(ex.Message);
    }
}
Here is the button click event handler that calls our rotate command
// Button click event handler in the user control class
// associated with our palette
private void RotateSelectedBtn_Click(object sender, EventArgs e)
{
    Document activeDoc = acadApp.DocumentManager.MdiActiveDocument;
    activeDoc.SendStringToExecute
                (
                    "RotateSelected ",
                    false,
                    false,
                    false
                );
}
The selected entity remains selected and can be transformed by clicking on the palette button. Here is a screenshot :

