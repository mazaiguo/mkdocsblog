---
title: "Selecting Solid3d sub-entities"
date: 2012-03-01
categories:
  - AutoCAD
tags:
  - API
  - Selection
  - Solid
description: "The following command illustrates a way to prompt user for subentity selection on a solid3d. It allows to select a single subentity and checks if t..."
author: Autodesk
---
# Selecting Solid3d sub-entities

发布日期: 2012-03-01

原始链接: https://adndevblog.typepad.com/autocad/2012/03/selecting-solid3d-sub-entities.html

## 文章内容

By Philippe Leefsma
  The following command illustrates a way to prompt user for subentity selection on a solid3d. It allows to select a single subentity and checks if the selected subentity type matches the specified type.
After the subentity has been selected, it uses the Brep API and retrieve the Brep entity representing this subentity. Further methods of the Brep object can be invoked in order to analyze the properties of the subentity.
//Command SubEntSelectBrep: Prompts user to select a single
//solid sub-entity and filters type of sub-entity selected.
//Philippe Leefsma, Developer Technical Services. March 2012.
[CommandMethod("SubEntSelectBrep")]
public void SubEntSelectBrep()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      PromptKeywordOptions pko = new PromptKeywordOptions(
        "\nSpecify sub-entity selection type:");
    pko.AllowNone = false;
    pko.Keywords.Add("Face");
    pko.Keywords.Add("Edge");
    pko.Keywords.Add("Vertex");
    pko.Keywords.Default = "Face";
      PromptResult pkr = ed.GetKeywords(pko);
      if (pkr.Status != PromptStatus.OK)
        return;
      SubentityType subentityType = SubentityType.Null;
      switch(pkr.StringResult)
    {
        case "Face":
            subentityType = SubentityType.Face;
            break;
        case "Edge":
            subentityType = SubentityType.Edge;
            break;
        case "Vertex":
            subentityType = SubentityType.Vertex;
            break;
        default:
            return;
    }
      PromptSelectionOptions pso = new PromptSelectionOptions();
    pso.MessageForAdding = "\nSelect solid " +
        pkr.StringResult + ": ";
    pso.SingleOnly = true;
    pso.SinglePickInSpace = true;
    pso.ForceSubSelections = true;
              PromptSelectionResult psr = ed.GetSelection(pso);
      if (psr.Status != PromptStatus.OK)
        return;
      SelectionSet ss = psr.Value;
      SelectedObject so = ss[0];
      if (!so.ObjectId.ObjectClass.IsDerivedFrom(
        RXClass.GetClass(typeof(Solid3d))))
    {
        ed.WriteMessage(
            "\nYou didn't select a solid, please try again...");
        return;
    }
      using (Transaction Tx = db.TransactionManager.StartTransaction())
    {
        Solid3d solid = Tx.GetObject(so.ObjectId, OpenMode.ForRead)
            as Solid3d;
          SelectedSubObject[] sso = so.GetSubentities();
          //Checks that selected type matches keyword selection
        if (subentityType != sso[0].FullSubentityPath.SubentId.Type)
        {
            ed.WriteMessage("\nInvalid Subentity Type: " +
                sso[0].FullSubentityPath.SubentId.Type +
                ", please try again...");
            return;
        }
          SubentityId subentityId = sso[0].FullSubentityPath.SubentId;
                       //Creates subentity path to use with GetSubentity
        FullSubentityPath subEntityPath = new FullSubentityPath(
            new ObjectId[] { solid.ObjectId },
            subentityId);
          //Returns a non-database resident entity
        //that represents the subentity
        using (Entity entity = solid.GetSubentity(subEntityPath))
        {
            ed.WriteMessage("\nSubentity Entity Type: "
                + entity.ToString());
        }
          //Creates entity path to generate Brep object from it
        FullSubentityPath entityPath = new FullSubentityPath(
            new ObjectId[] { solid.ObjectId },
            new SubentityId(SubentityType.Null, IntPtr.Zero));
          using (Brep brep = new Brep(entityPath))
        {
            switch (subentityType)
            {
                case SubentityType.Face:
                      foreach (
                        Autodesk.AutoCAD.BoundaryRepresentation.Face 
                            face in brep.Faces)
                    {
                        if (subentityId ==
                            face.SubentityPath.SubentId)
                        {
                            ed.WriteMessage("\nSurface: "
                                + face.Surface.ToString());
                              break;
                        }
                    }
                    break;
                  case SubentityType.Edge:
                      foreach (
                        Autodesk.AutoCAD.BoundaryRepresentation.Edge
                           edge
                        in brep.Edges)
                    {
                        if (subentityId ==
                            edge.SubentityPath.SubentId)
                        {
                            ed.WriteMessage("\nCurve: " +
                                edge.Curve.ToString());
                              break;
                        }
                    }
                    break;
                  case SubentityType.Vertex:
                      foreach (
                       Autodesk.AutoCAD.BoundaryRepresentation.Vertex
                           vertex
                        in brep.Vertices)
                    {
                        if (subentityId ==
                            vertex.SubentityPath.SubentId)
                        {
                            ed.WriteMessage("\nPoint: " +
                                PointToStr(vertex.Point));
                              break;
                        }
                    }
                    break;
                  default:
                    break;
            }
        }
                        Tx.Commit();
    }
}
  //Small utility function
private string PointToStr(Point3d point)
{
    return "[" +
        point.X.ToString("F2") + ", " +
        point.Y.ToString("F2") + ", " +
        point.Z.ToString("F2")
        + "]";
}
  Contributed by
Philippe Leefsma, Developer Consultant.
Autodesk Developer Network.

## 评论

**内容**: Konstantin said...
is it possible to highlight the selected face or edge of the 3Dsolid ??
Reply
07/12/2012 at 02:57 AM

---
**内容**: Philippe Leefsma said...
You can use "Entity.Highlight(FullSubentityPath, [MarshalAs(UnmanagedType.U1)] bool)"
To highlight a sub-entity. Please refer to the help files for more details.
Reply
07/12/2012 at 06:56 AM

---
**内容**: Konstantin said in reply to Philippe Leefsma...
Thanks Philippe,
it already works !
Reply
07/13/2012 at 04:03 AM

---
**内容**: Konstantin said...
Hi Phillipe,
I have noticed that the command returns an error message if
you try to select solid3d subentities on COMPOSITE SOLIDS (unioned, subtracted, intersected) CREATED with "Solid history ON".
-----Invalid Subentity Type: Class, please try again...
For NON composite solid primitives (BOX, CONE etc) the command functions as expected, independently of the history settings !
Reply
08/10/2012 at 04:02 AM

---
