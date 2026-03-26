---
title: "Retrieving dimensional constraints and their associative properties"
date: 2013-02-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - Block
  - C#
  - Dimension
description: "Here is some handy code for those of you working with the .Net associative API. The C# sample below illustrates how to dump all dimensional constra..."
author: Autodesk
---
# Retrieving dimensional constraints and their associative properties

发布日期: 2013-02-01

原始链接: https://adndevblog.typepad.com/autocad/2013/02/retrieving-dimensional-constraints-and-their-associative-properties.html

## 文章内容

By Philippe Leefsma
Here is some handy code for those of you working with the .Net associative API. The C# sample below illustrates how to dump all dimensional constraints in the current space. It also shows how to dig from the constraint objects down to the dependent entities and the controlling associative parameter.
/////////////////////////////////////////////////////////////
// Use: Dumps to command line the dimensional constraints
//      in current BlockTableRecord
//      Lists constraint type, dependent entity and
//      controlling parameter.
//
// Author: Philippe Leefsma.
/////////////////////////////////////////////////////////////
[CommandMethod("DumpDimConstraints")]
public void DumpDimConstraints()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      ObjectId networkId = AssocNetwork.GetInstanceFromObject(
        db.CurrentSpaceId,
        false,
        true,
        "ACAD_ASSOCNETWORK");
      if (networkId == ObjectId.Null)
        return;
      using (Transaction Tx =
        db.TransactionManager.StartTransaction())
    {
        using (AssocNetwork network =
            Tx.GetObject(
                networkId,
                OpenMode.ForRead, false) as AssocNetwork)
        {
            foreach (ObjectId actionId in network.GetActions)
            {
                if (actionId == ObjectId.Null)
                    continue;
                  DBObject obj = Tx.GetObject(
                    actionId,
                    OpenMode.ForRead);
                    if (actionId.ObjectClass.IsDerivedFrom(
                    RXObject.GetClass(
                        typeof(Assoc2dConstraintGroup))))
                {
                    Assoc2dConstraintGroup group = obj
                        as Assoc2dConstraintGroup;
                      foreach(GeometricalConstraint constraint
                        in group.Constraints)
                    {
                        if(constraint.GetRXClass().IsDerivedFrom(
                            RXObject.GetClass(
                                typeof(ExplicitConstraint))))
                            DumpDimConstraint(Tx, constraint
                           as ExplicitConstraint);
                    }
                }
            }
        }
    }
}
  void DumpDimConstraint(
    Transaction Tx,
    ExplicitConstraint constraint)
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Editor ed = doc.Editor;
      ed.WriteMessage("\n ---- Dimensional Constraint ---- ");
      ed.WriteMessage("\n - Constraint type: " +
        constraint.ToString().Remove(0, 34));
      //1- Dump Constrained geometry
    //-> Gives access to constrained Entity
    DumpConstrainedGeometry(Tx, constraint.ConnectedGeometries);
      //2- Dump AssocDependency
    //-> Gives access to Dimension Entity
    AssocDependency dep = Tx.GetObject(
        constraint.DimDependencyId,
        OpenMode.ForRead)
            as AssocDependency;
      Dimension depDim = Tx.GetObject(
        dep.DependentOnObject,
        OpenMode.ForRead)
            as Dimension;
      ed.WriteMessage("\n - Dependent dimension entity: " +
        depDim.ToString().Remove(0, 34));
      //3- Dump AssocValueDependency
    //-> Gives access to AssocVariable
    AssocValueDependency valueDep = Tx.GetObject(
        constraint.ValueDependencyId,
        OpenMode.ForRead)
            as AssocValueDependency;
      if (valueDep.DependentOnObject.ObjectClass.IsDerivedFrom(
        RXObject.GetClass(typeof(AssocVariable))))
    {
        AssocVariable var = Tx.GetObject(
            valueDep.DependentOnObject,
            OpenMode.ForRead)
                as AssocVariable;
          ed.WriteMessage("\n - Dim Parameter "
            + var.Name + " = " + var.Expression);
    }
}
  void DumpConstrainedGeometry(
    Transaction Tx,
    ConstrainedGeometry[] geometries)
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Editor ed = doc.Editor;
      foreach (ConstrainedGeometry goemetry in geometries)
    {
        ed.WriteMessage("\n  - Constrained Geometry: " +
            goemetry.ToString().Remove(0, 34));
          if(goemetry.GeomDependencyId != ObjectId.Null)
        {
            AssocGeomDependency goemDep = Tx.GetObject(
                goemetry.GeomDependencyId,
                OpenMode.ForRead)
                    as AssocGeomDependency;
              Entity entity = Tx.GetObject(
                goemDep.DependentOnObject,
                OpenMode.ForRead)
                    as Entity;
              ed.WriteMessage(" with Constrained Entity: " +
                entity.ToString().Remove(0, 34));
              return;
        }
          DumpConstrainedGeometry(Tx, goemetry.ConnectedGeometries);
    }
}
-
Here is the result of the command when run on a database where I created a radial dimension constraint on a Circle and an aligned dimension constraint on a Line:
-

## 评论

**内容**: karl said...
is this code "framework 4.5"? it's not working for me & i'm 4.0.
Reply
08/25/2014 at 08:21 AM

---
**内容**: Philippe said...
That depends of the Acad version you are using. It should work under 2014 / .Net 4.0
Reply
08/25/2014 at 09:36 AM

---
