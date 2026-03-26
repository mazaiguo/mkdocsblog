---
title: "Comparing properties of two entities"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - Dimension
description: "Using .NET Property enumeration it is possible compare each property on two entities to identify which one is different. Why? Suppose you have two ..."
author: Autodesk
---
# Comparing properties of two entities

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/comparing-properties-of-two-entities.html

## 文章内容

By Augusto Goncalves
Using .NET Property enumeration it is possible compare each property on two entities to identify which one is different. Why? Suppose you have two dimensions and want to make one equals to other but do not know which property change.
The Type object, accessible from any object from GetType() method, can enumerate properties in a collection of Reflection.PropertyInfo objects. It is also possible to get the value of each property and then compare both values.
[CommandMethod("compEnt")]
public static void CmdCompareEntities()
{
  Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
  ObjectId id1, id2;
    //select the entities
  PromptEntityResult per1, per2;
  per1 = ed.GetEntity("\nSelect first entity: ");
  id1 = per1.ObjectId;
  per2 = ed.GetEntity("\nSelect second entity: ");
  id2 = per2.ObjectId;
    //some error check
  if (per1.Status != PromptStatus.OK ||
    per2.Status != PromptStatus.OK) return;
    Database db =
    Application.DocumentManager.MdiActiveDocument.Database;
  using (Transaction trans =
    db.TransactionManager.StartTransaction())
  {
    //open the entities
    Entity ent1 = (Entity)trans.GetObject(id1, OpenMode.ForRead);
    Entity ent2 = (Entity)trans.GetObject(id2, OpenMode.ForRead);
      Type entType1 = ent1.GetType();
    Type entType2 = ent2.GetType();
      //the two entities should be the same type
    if (!entType1.Equals(entType2)) return;
      //get the list of properties and iterate
    System.Reflection.PropertyInfo[] props =
      entType1.GetProperties();
    foreach (System.Reflection.PropertyInfo prop in props)
    {
      try
      {
        //get both values property value
        object val1, val2;
        val1 = prop.GetValue(ent1, null);
        val2 = prop.GetValue(ent2, null);
        if (val1 != null & val2 != null)
        {
          //are equal?
          if (!(val1.Equals(val2)))
          {
            //if not, write the value
            ed.WriteMessage("\n{0} is different: {1}  |  {2}",
                prop.Name, val1.ToString(), val2.ToString());
          }
        }
      }
      catch (Autodesk.AutoCAD.Runtime.Exception ex)
      {
      }
    }
    trans.Commit();
  }
}
Usage tips: try isolate the property you want to research. Suppose you have 2 dimensions, put them at the same position, with all known properties with the same value. Otherwise this function may return a lot of unwanted values.
Some important information: this function supposes to be used for debug process. The enumeration may return properties that may not be available, and as the AutoCAD .NET just wrap unmanaged code, the code my throw exceptions (such as NotApplicable).

