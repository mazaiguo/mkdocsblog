---
title: "How Get Adjacent Faces From a Selected Edge In Solid"
date: 2017-08-01
categories:
  - AutoCAD
tags:
  - API
  - Solid
description: "Using BREP API it is fairly straightforward to retrieve the adjacent faces from a particular edge in a 3dsolid."
author: Autodesk
---
# How Get Adjacent Faces From a Selected Edge In Solid

发布日期: 2017-08-01

原始链接: https://adndevblog.typepad.com/autocad/2017/08/how-get-adjacent-faces-from-a-selected-edge-in-solid.html

## 文章内容

By Madhukar Moogala

Using BREP API it is fairly straightforward to retrieve the adjacent faces from a particular edge in a 3dsolid.
We will use Boundary Loop to get all the loops consuming the edge, from Loop we can get associated Face.

static public void GetAdjacentFaces()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
    PromptKeywordOptions pko = new PromptKeywordOptions(
"\nSpecify sub-entity selection type:");
    pko.AllowNone = false;
    pko.Keywords.Add("Edge");
    pko.Keywords.Default = "Edge";

    PromptResult pkr = ed.GetKeywords(pko);

    if (pkr.Status != PromptStatus.OK)
        return;
    //User selection is Edge
    SubentityType subentityType = SubentityType.Edge;


    //Enable force pick sub-selection
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
    //To store adjacent Faces
    List<SubentityId> faceIds = new List<SubentityId>();
    using (Transaction Tx = db.TransactionManager.StartTransaction())
    {
        Solid3d solid = Tx.GetObject(so.ObjectId, OpenMode.ForWrite)
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

        using (Edge edge = new Edge(subEntityPath))
        {
            if (subentityType == SubentityType.Edge)
            {
                       
                    if (subentityId == edge.SubentityPath.SubentId)
                    {
                        ed.WriteMessage("\nCurve: " +  edge.Curve.ToString());
                        //Now color the adjacent faces.
                        foreach(BoundaryLoop loop in edge.Loops)
                        {
                        //For simplest loop,outward loop is our interest
                            if(loop.LoopType ==LoopType.LoopExterior)
                            {
                            AcBr.Face face = loop.Face;
                            faceIds.Add(face.SubentityPath.SubentId);
                            }

                        }
                        if(faceIds.Count > 1)
                        foreach (SubentityId subentId in faceIds)
                        {
                            Color col = Color.FromColorIndex(ColorMethod.ByColor, 1);
                            solid.SetSubentityColor(subentId, col);
                        }


                }
                        
            }

        }

        Tx.Commit();
    }


}
Demo Video

## 评论

**内容**: muğla kürtaj said...
nice blog, thank you for informative articles
Reply
10/28/2021 at 02:12 AM

---
**内容**: fethiye yat kiralama said...
Nice page thanks admin
Reply
02/01/2022 at 03:24 AM

---
