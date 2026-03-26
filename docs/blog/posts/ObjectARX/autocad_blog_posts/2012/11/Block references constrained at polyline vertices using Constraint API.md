---
title: "Block references constrained at polyline vertices using Constraint API"
date: 2012-11-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - Block
  - Polyline
description: "To have block references inserted at each vertex of a polyline and ensure that they are transformed together, the block reference and the polyline ..."
author: Autodesk
---
# Block references constrained at polyline vertices using Constraint API

发布日期: 2012-11-01

原始链接: https://adndevblog.typepad.com/autocad/2012/11/block-references-constrained-at-polyline-vertices-using-constraint-api.html

## 文章内容

By Balaji Ramamoorthy
To have block references inserted at each vertex of a polyline and ensure that they are transformed together, the block reference and the polyline entity can be constrained together using "coincident point" constraint. This will ensure that AutoCAD is aware of the association between them.
Here is a sample code to demonstrate the creation of such coincident point constraint :
private static string _blockName = "Autodesk";
  /// <summary>
/// Creates a Polyline with block references inserted at each vertex.
/// The block references are then constrained to the polyline vertex.
/// </summary>
[CommandMethod("Demo")]
static public void TestMethod()
{
    CreatePlineWithConstrainedBlockRefs();
}
  public static void CreatePlineWithConstrainedBlockRefs()
{
    CreateBlockDef();
      Database db
        = Application.DocumentManager.MdiActiveDocument.Database;
      Autodesk.AutoCAD.DatabaseServices.TransactionManager tm
                                = db.TransactionManager;
    using (Transaction myT = tm.StartTransaction())
    {
        BlockTable bt = tm.GetObject(
                                        db.BlockTableId,
                                        OpenMode.ForRead,
                                        false
                                    ) as BlockTable;
          BlockTableRecord blockDefinition
            = tm.GetObject
                    (
                        bt[_blockName],
                        OpenMode.ForRead,
                        false
                    ) as BlockTableRecord;
          BlockTableRecord btr
            = tm.GetObject
                    (
                        bt[BlockTableRecord.ModelSpace],
                        OpenMode.ForWrite,
                        false
                    ) as BlockTableRecord;
          Polyline polyline = new Polyline();
        polyline.Closed = false;
          ObjectIdCollection blkRefIds
                            = new ObjectIdCollection();
          polyline.AddVertexAt(
                                0,
                                new Point2d(0.0, 0.0),
                                0.0,
                                0.0,
                                0.0
                            );
        BlockReference blockRef1
            = new BlockReference
                (
                    Point3d.Origin,
                    blockDefinition.ObjectId
                );
        blkRefIds.Add(btr.AppendEntity(blockRef1));
        tm.AddNewlyCreatedDBObject(blockRef1, true);
          polyline.AddVertexAt
                        (
                            1,
                            new Point2d(10.0, 10.0),
                            0.0, 0.0, 0.0
                        );
          BlockReference blockRef2
            = new BlockReference
                    (
                        new Point3d(10.0, 10.0, 0.0),
                        blockDefinition.ObjectId
                    );
          blkRefIds.Add(btr.AppendEntity(blockRef2));
        tm.AddNewlyCreatedDBObject(blockRef2, true);
          polyline.AddVertexAt
                    (
                        2,
                        new Point2d(20.0, 0.0),
                        0.0, 0.0, 0.0
                    );
        BlockReference blockRef3
            = new BlockReference
                    (
                        new Point3d(20.0, 0.0, 0.0),
                        blockDefinition.ObjectId
                    );
        blkRefIds.Add(btr.AppendEntity(blockRef3));
        tm.AddNewlyCreatedDBObject(blockRef3, true);
          polyline.AddVertexAt
                    (
                        3,
                        new Point2d(30.0, 10.0),
                        0.0, 0.0, 0.0
                    );
        BlockReference blockRef4
            = new BlockReference
                    (
                        new Point3d(30.0, 10.0, 0.0),
                        blockDefinition.ObjectId
                    );
        blkRefIds.Add(btr.AppendEntity(blockRef4));
        tm.AddNewlyCreatedDBObject(blockRef4, true);
          ObjectId plineOid = btr.AppendEntity(polyline);
        tm.AddNewlyCreatedDBObject(polyline, true);
          AssociatePline_BlockReference
                    (
                        myT,
                        db,
                        blkRefIds[0],
                        plineOid,
                        0,
                        0,
                        false
                    );
          AssociatePline_BlockReference
                    (
                        myT,
                        db,
                        blkRefIds[1],
                        plineOid,
                        0,
                        1,
                        false
                    );
          AssociatePline_BlockReference
                    (
                        myT,
                        db,
                        blkRefIds[2],
                        plineOid,
                        1,
                        1,
                        false
                    );
          AssociatePline_BlockReference
                    (
                        myT,
                        db,
                        blkRefIds[3],
                        plineOid,
                        2,
                        1,
                        true
                    );
          myT.Commit();
    }
}
  // This method creates a coincident constraint between
// the block reference and the polyline vertex.
public static void AssociatePline_BlockReference
                            (    Transaction trans,
                                Database db,
                                ObjectId blkReferenceOid,
                                ObjectId pLineOid,
                                int edgeIndex,
                                int vertexIndex,
                                bool evaluate
                            )
{
    // Finding the subentityId of the BlockReference vertex
    FullSubentityPath subentPath2 = new FullSubentityPath();
    using (Entity entity =
        (Entity)trans.GetObject(   
                                    blkReferenceOid,
                                    OpenMode.ForRead,
                                    false
                                ))
    {
        AssocPersSubentityIdPE subentityIdPE;
        RXClass peCls
            = AssocPersSubentityIdPE.GetClass(
                                typeof(AssocPersSubentityIdPE));
          IntPtr pSubentityIdPE = entity.QueryX(peCls);
        if (pSubentityIdPE == IntPtr.Zero)
        {
            System.Windows.MessageBox.Show("cannot get pSubentityIdPE1");
            return;
        }
        subentityIdPE
            = AssocPersSubentityIdPE.Create(
                                                pSubentityIdPE,
                                                false
                                            ) as AssocPersSubentityIdPE;
        if (subentityIdPE == null)
        {
            System.Windows.MessageBox.Show("cannot get subentityIdPE1");
            return;
        }
        SubentityId[] vertexSubentityId = null;
        vertexSubentityId
            = subentityIdPE.GetAllSubentities
                                            (
                                                entity,
                                                SubentityType.Vertex
                                            );
          if (vertexSubentityId.Length > 0)
        {
            subentPath2
                = new FullSubentityPath
                    (
                        new ObjectId[1] { blkReferenceOid },
                        vertexSubentityId[0]
                    );
        }
    }
      FullSubentityPath subentEdgePath1 = new FullSubentityPath();
    FullSubentityPath subentPath1 = new FullSubentityPath();
    using (Entity entity
                = (Entity)trans.GetObject(
                                            pLineOid,
                                            OpenMode.ForRead,
                                            false
                                        ))
    {
        AssocPersSubentityIdPE subentityIdPE;
        RXClass peCls
            = AssocPersSubentityIdPE.GetClass
                            (
                                typeof(AssocPersSubentityIdPE)
                            );
        IntPtr pSubentityIdPE = entity.QueryX(peCls);
        if (pSubentityIdPE == IntPtr.Zero)
        {
            System.Windows.MessageBox.Show("cannot get pSubentityIdPE");
            return;
        }
        subentityIdPE
            = AssocPersSubentityIdPE.Create
                            (
                                pSubentityIdPE,
                                false
                            ) as AssocPersSubentityIdPE;
        if (subentityIdPE == null)
        {
            System.Windows.MessageBox.Show("cannot get subentityIdPE");
            return;
        }
        SubentityId[] edgeSubentityIds = null;
        edgeSubentityIds
            = subentityIdPE.GetAllSubentities
                                            (
                                                entity,
                                                SubentityType.Edge
                                            );
          SubentityId sid = SubentityId.Null;
        sid = edgeSubentityIds[edgeIndex];
          SubentityId start = SubentityId.Null,
                    end = SubentityId.Null;
        SubentityId[] other = null;
        subentityIdPE.GetEdgeVertexSubentities
                            (
                                entity,
                                sid,
                                ref start,
                                ref end,
                                ref other
                            );
          subentEdgePath1 = new FullSubentityPath
                            (
                                new ObjectId[1] { pLineOid },
                                sid
                            );
          if (vertexIndex == 0)
            subentPath1 = new FullSubentityPath
                            (
                                new ObjectId[1] { pLineOid },
                                start
                            );
        else
            subentPath1 = new FullSubentityPath
                            (
                                new ObjectId[1] { pLineOid },
                                end
                            );
    }
      ObjectId consGrpId = GetConstraintGroup(true);
      ConstrainedGeometry consGeomEdge1 = null;
    ConstrainedGeometry consGeomEdge2 = null;
    using (Assoc2dConstraintGroup constGrp =
        (Assoc2dConstraintGroup)trans.GetObject
                                        (
                                            consGrpId,
                                            OpenMode.ForWrite,
                                            false
                                        ))
    {
        try
        {
            consGeomEdge2
                = constGrp.AddConstrainedGeometry(subentPath2);
              consGeomEdge1
                = constGrp.AddConstrainedGeometry(subentEdgePath1);
        }
        catch (System.Exception ex)
        {
            // The Geometry might already be in the constraint
            // group, in which case we can ignore it and only
            // try and add the geometrical constraint.
        }
          FullSubentityPath[] paths
            = new FullSubentityPath[2]
                                        {
                                            subentPath1,
                                            subentPath2
                                        };
          GeometricalConstraint newConstraint
            = constGrp.AddGeometricalConstraint
                    (
                        GeometricalConstraint.ConstraintType.Coincident,
                        paths
                    );
          if (evaluate)
        {
            String temp = "";
            ObjectId networkId
                = AssocNetwork.GetInstanceFromDatabase
                                                    (
                                                        db,
                                                        true,
                                                        temp
                                                    );
            using (AssocNetwork network
                = (AssocNetwork)trans.GetObject(
                                                    networkId,
                                                    OpenMode.ForWrite,
                                                    false
                                                ))
            {
                AssocEvaluationCallback callBack = null;
                network.Evaluate(callBack);
            }
        }
    }
}
  public static void CreateBlockDef()
{
    Document activeDoc = Application.DocumentManager.MdiActiveDocument;
    Database db = activeDoc.Database;
    Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
      using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        BlockTable bt
            = (BlockTable)tr.GetObject
                                    (
                                        db.BlockTableId,
                                        OpenMode.ForRead
                                    );
          if (bt.Has(_blockName) == false)
        {
            bt.UpgradeOpen();
            BlockTableRecord btr = new BlockTableRecord();
            btr.Name = _blockName;
            btr.Origin = Point3d.Origin;
            bt.Add(btr);
            tr.AddNewlyCreatedDBObject(btr, true);
              // Circle
            Circle circle
                = new Circle(Point3d.Origin, Vector3d.ZAxis, 1.0);
            btr.AppendEntity(circle);
            tr.AddNewlyCreatedDBObject(circle, true);
        }
        tr.Commit();
    }
}
  // Helper function to retrieve (or create) constraint group
static private ObjectId GetConstraintGroup(bool createIfDoesNotExist)
{
    // get the current UCS plane
    Autodesk.AutoCAD.EditorInput.Editor ed
        = Application.DocumentManager.MdiActiveDocument.Editor;
      Matrix3d ucsMatrix = ed.CurrentUserCoordinateSystem;
    Point3d origin = ucsMatrix.CoordinateSystem3d.Origin;
    Vector3d xAxis = ucsMatrix.CoordinateSystem3d.Xaxis;
    Vector3d yAxis = ucsMatrix.CoordinateSystem3d.Yaxis;
    Vector3d zAxis = ucsMatrix.CoordinateSystem3d.Zaxis;
      origin += (double)Application.GetSystemVariable("ELEVATION") * zAxis;
    Plane currentPlane = new Plane(origin, xAxis, yAxis);
      // get the constraint group from block table record
    Database database = HostApplicationServices.WorkingDatabase;
    ObjectId idConstrGroup = ObjectId.Null;
    if (database == null)
    {
        System.Windows.MessageBox.Show("working database is null");
        return idConstrGroup;
    }
      ObjectId networkId
        = AssocNetwork.GetInstanceFromObject(
                                                database.CurrentSpaceId,
                                                createIfDoesNotExist,
                                                true,
                                                ""
                                            );
    if (networkId.IsNull)
    {
        System.Windows.MessageBox.Show("network id is null");
        return idConstrGroup; // AcDbObjectId::kNull;
    }
      // Try to find the constraint group in the associative network
    Database db = Application.DocumentManager.MdiActiveDocument.Database;
      Autodesk.AutoCAD.DatabaseServices.TransactionManager tm
                                        = db.TransactionManager;
    using (Transaction myT = tm.StartTransaction())
    {
        using (AssocNetwork network
            = (AssocNetwork)myT.GetObject(
                                            networkId,
                                            OpenMode.ForRead,
                                            false
                                         ))
        {
            if (network == null)
                return idConstrGroup;
              ObjectIdCollection actionsInNetwork = network.GetActions;
            for (int nCount = 0; nCount < actionsInNetwork.Count; nCount++)
            {
                ObjectId idAction = actionsInNetwork[nCount];
                if (idAction == ObjectId.Null)
                    continue;
                  if (idAction.ObjectClass.IsDerivedFrom(
                    RXObject.GetClass(
                            typeof(Assoc2dConstraintGroup))))
                {
                    using (AssocAction action
                        = (AssocAction)myT.GetObject
                                    (
                                        idAction,
                                        OpenMode.ForRead,
                                        false
                                    ))
                    {
                        if (action == null)
                            continue;
                          Assoc2dConstraintGroup constGrp
                            = (Assoc2dConstraintGroup)action;
                          // In AutoCAD 2011
                        //constGrp.GetWorkPlane.IsCoplanarTo(currentPlane)
                          // In AutoCAD 2013
                        if (constGrp.WorkPlane.IsCoplanarTo(currentPlane))
                        {
                            return idAction;
                        }
                    }
                }
            }
        }
          if (idConstrGroup.IsNull && createIfDoesNotExist)
        {
            using (AssocNetwork network
                = (AssocNetwork)myT.GetObject(
                                                networkId,
                                                OpenMode.ForWrite,
                                                false
                                            ))
            {
                Database databaseN = network.Database;
                bool bIsModelSpace = database.TileMode;
                Point3d extmin
                    = bIsModelSpace ? database.Extmin : database.Pextmin;
                Point3d extmax
                    = bIsModelSpace ? database.Extmax : database.Pextmax;
                  //If model extent is far far away from origin
                // then we need to shift construction plane
                // origin within the model extent.
                  Plane constraintPlane = new Plane(currentPlane);
                  if (extmin.GetAsVector().Length > 1.0e8)
                {
                    Point3d originL
                        = extmin + (extmax - extmin) / 2.0;
                      PointOnSurface result
                        = currentPlane.GetClosestPointTo(originL);
                      constraintPlane.Set(result.GetPoint(), currentPlane.Normal);
                }
                using (Assoc2dConstraintGroup constGrp
                    = new Assoc2dConstraintGroup(constraintPlane))
                {
                    idConstrGroup = database.AddDBObject(constGrp);
                }
                network.AddAction(idConstrGroup, true);
            }
        }
        myT.Commit();
    }
    return idConstrGroup;
}

## 评论

**内容**: Matthias Mueller said...
Thanks! Finally there is an example where BlockReferences are attached with coincident constraints.
Any ideas how to set the coincident point not to the blocks "base point" but to a custom point, e.g. from an entity within the block?
Regards, Matthias
Reply
01/22/2013 at 11:29 PM

---
**内容**: Balaji said in reply to Matthias Mueller...
Hi Matthias,
I tried creating a coincident constraint using a vertex from a nested entity in a block reference but havent got it to work correctly.
I will need some time to figure this out and will update you based on what I find.
Simplest way is to send the "gccoincident" command and provide the point inputs and let AutoCAD do the rest.
Reply
01/24/2013 at 08:16 AM

---
**内容**: Matthias Mueller said in reply to Balaji...

Balaji, thanks for your response. In the meantime I worked with Phillipe Leefsmas High-Level-Api "AssocUtil": http://adndevblog.typepad.com/autocad/2013/01/a-simplified-net-api-for-accessing-autocad-parameters-and-constraints.html
Thanks to Phillipe who recently updated this great util - it also works with polyline and blockreferences now :-) To create a coincident constraint, all you need is to choose the entities and define the points where they should meet. The util itself looks for the closest point (vertex/edge) in the nested entities that can be applied with the constraint.
Reply
01/27/2013 at 11:01 AM

---
**内容**: Balaji said...
Hi Matthias,
Thanks for the update.
I had tried it with the earlier version of the AssocUtil that was posted in Keans blog and it did not work.
I am glad it works with the updated version that Philippe has posted.
I will convey your appreciation to Philippe.
Cheers,
Balaji
Reply
01/27/2013 at 08:44 PM

---
**内容**: Nik said...
I am not sure if this is AutoCAD 2015 new bug, but AutoCAD crashes on this line: "subentityIdPE.GetEdgeVertexSubentities(..)". I have posted a question on the forum with very similar code. Here's a link https://forums.autodesk.com/t5/net/autocad-2015-associative-framework-getedgevertexsubentities/td-p/8419652
I hope there is a solution as I really want this to work out!
Reply
11/22/2018 at 06:32 PM

---
