---
title: "Get P&ID item class hierarchy"
date: 2012-10-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "For a given P&ID item, let’s say an Asset, we can get its class name, but what about the hierarchy of it? It is possible access the respective tabl..."
author: Autodesk
---
# Get P&ID item class hierarchy

发布日期: 2012-10-01

原始链接: https://adndevblog.typepad.com/autocad/2012/10/get-pid-item-class-hierarchy.html

## 文章内容

By Augusto Goncalves
For a given P&ID item, let’s say an Asset, we can get its class name, but what about the hierarchy of it? It is possible access the respective table of that class and then get the base class, and keep looping until the top of the tree. The following code show an example where the output will be like:
Command: GETITEMCLASS
Command: Select an asset:
HorizontalCentrifugalPump
Pumps
Equipment
EngineeringItems
PnPBase
<CommandMethod("getItemClass")> _
Public Shared Sub CmdGetItemPnIdClass()
  ' access editor
  Dim ed As Editor = Application. _
    DocumentManager.MdiActiveDocument.Editor
    ' select an asset
  Dim opSelAsset As New PromptEntityOptions _
    ("Select an asset: ")
  opSelAsset.SetRejectMessage("Only assets")
  opSelAsset.AddAllowedClass(GetType(Asset), True)
  Dim resSelAsset As PromptEntityResult = _
    ed.GetEntity(opSelAsset)
  If (resSelAsset.Status <> PromptStatus.OK) _
    Then Exit Sub
  Dim assetId As ObjectId = resSelAsset.ObjectId
    Dim db As Database = Application. _
    DocumentManager.MdiActiveDocument.Database
  Using trans As Transaction = db. _
    TransactionManager.StartTransaction
      ' access PnId DLM
    Dim proj As PlantProject = _
      PlantApplication.CurrentProject
    Dim projPnId As PnIdProject = _
      proj.ProjectParts.Item("PnID")
    Dim dataLinkMgr As DataLinksManager = _
      projPnId.DataLinksManager
      Dim classes As New StringCollection
      ' open the asset
    Dim assetPnId As Asset = _
      trans.GetObject(assetId, OpenMode.ForRead)
      Dim className As String = assetPnId.ClassName
    Do
      ' add to the list
      classes.Add(className)
        ' get the table of the asset class
      Dim classTable As PnPTable = _
        dataLinkMgr.GetPnPDatabase(). _
        Tables.Item(className)
        ' get the base class
      className = classTable.BaseTableName
        If (String.IsNullOrWhiteSpace(className)) _ 
         Then Exit Do
    Loop
      ' write the names
    For Each cn As String In classes
      ed.WriteMessage("{0}{1}", _
                      Environment.NewLine, _
                      cn)
    Next
  End Using
End Sub

