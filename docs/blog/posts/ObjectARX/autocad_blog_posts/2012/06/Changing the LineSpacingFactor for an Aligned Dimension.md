---
title: "Changing the LineSpacingFactor for an Aligned Dimension"
date: 2012-06-01
categories:
  - AutoLISP
tags:
  - AutoCAD
  - AutoLISP
  - Dimension
  - Unicode
description: "When placing an Aligned Dimension using the AutoCAD command, you can choose the MTEXT option and create multiple line text. Here is the sample code..."
author: Autodesk
---
# Changing the LineSpacingFactor for an Aligned Dimension

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/changing-the-linespacingfactor-for-an-aligned-dimension.html

## 文章内容

By Balaji Ramamoorthy
When placing an Aligned Dimension using the AutoCAD command, you can choose the MTEXT option and create multiple line text. Here is the sample code to change the Line Spacing Factor.
Lisp :
An existing dimension could be modifed using Lisp. In this sample code, we reduce the line spacing factor by 25%.
(setq e (car(entsel)))
(setq ed (entget e))
(entmod (subst (cons 41 0.75) (assoc 41 ed) ed))

ObjectARX :
It is also possible to change this setting with ObjectARX. The following example changes pDim->textLineSpacingFactor to .75x of its original value, and applies it to the selected dimension.
AcGePoint3d ptPick;
ads_name eName;
if (acedEntSel(
                ACRX_T("Select a dimension: "),
                eName,
                asDblArray (ptPick)
              ) != RTNORM )
    return;
  AcDbObjectId id;
acdbGetObjectId (id, eName);
  AcDbEntity *pEnt;
acdbOpenAcDbEntity (pEnt, id, AcDb::kForRead);
AcDbDimension *pDim = AcDbDimension::cast (pEnt);
pEnt->close ();
if (pDim == NULL)
    return;
  if (Acad::eOk != acdbOpenObject(pDim, id, AcDb::kForWrite))
    return;
  // get the current line spacing factor
double dimLSpcFac = pDim->textLineSpacingFactor();
  // Reduce the line spacing factor
pDim->setTextLineSpacingFactor(dimLSpcFac * 0.75);
  // update the dimension's block table record
pDim->recomputeDimBlock();
  AutoCAD .Net API :

Document doc = Application.DocumentManager.MdiActiveDocument;
Database db = doc.Database;
Editor ed = doc.Editor;
  PromptEntityOptions peo
            = new PromptEntityOptions("Select a dimension : ");
peo.SetRejectMessage("\nPlease select the dimension to modify");
peo.AddAllowedClass(typeof(Dimension), false);
  PromptEntityResult per = ed.GetEntity(peo);
if (per.Status != PromptStatus.OK)
    return;
  ObjectId id = per.ObjectId;
  using (Transaction tr = db.TransactionManager.StartTransaction())
{
    Dimension dim = tr.GetObject(id, OpenMode.ForWrite) as Dimension;
      // get the current line spacing factor
    double dimLSpcFac = dim.TextLineSpacingFactor;
      // Reduce the line spacing factor
    dim.TextLineSpacingFactor = dimLSpcFac * 0.75;
      // update the dimension's block table record
    dim.RecomputeDimensionBlock(true);
      tr.Commit();
}
Posted at 09:25 PM in .NET, AutoCAD, Balaji Ramamoorthy, LISP, ObjectARX | Permalink

