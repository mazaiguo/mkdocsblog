---
title: "Using GetRelatedRowIds method"
date: 2012-10-01
categories:
  - AutoCAD
tags:
  - API
description: "The P&ID API do not have a direct method to access all related entities of a given SLINE or Asset, but the Data Links Manager have a method, GetRel..."
author: Autodesk
---
# Using GetRelatedRowIds method

发布日期: 2012-10-01

原始链接: https://adndevblog.typepad.com/autocad/2012/10/using-getrelatedrowids-method.html

## 文章内容

By Augusto Goncalves
The P&ID API do not have a direct method to access all related entities of a given SLINE or Asset, but the Data Links Manager have a method, GetRelatedRowIds, that can give this information when we pass the appropriate parameters. The following code sample get all related entities (actually a array of PnPRowId) for a given entity.
<CommandMethod("listRelatedEntities")> _
Public Shared Sub CmdListRelatedEntities()
  Dim ed As Editor = _
    Application.DocumentManager.MdiActiveDocument.Editor
    ' select a SLINE ou Asset
  Dim selEntOp As New PromptEntityOptions( _
    "Select a SLINE or Asset: ")
  ' *** before AddAllowedClass
  selEntOp.SetRejectMessage("Only SLINE or Asset")
  selEntOp.AddAllowedClass(GetType(LineSegment), True)
  selEntOp.AddAllowedClass(GetType(Asset), True)
  Dim selEntRes As PromptEntityResult =  _
    ed.GetEntity(selEntOp)
  If (selEntRes.Status <> PromptStatus.OK) Then Exit Sub
  Dim entId As ObjectId = selEntRes.ObjectId
    ' access Data Links Manager
  Dim proj As PlantProject = PlantApplication.CurrentProject
  Dim projPnId As PnIdProject = _
    proj.ProjectParts.Item("PnID")
  Dim dataLinkMgr As DataLinksManager = _
    projPnId.DataLinksManager
    ' get related entities
  Dim nRowId As Integer = dataLinkMgr.FindAcPpRowId(entId)
  ' at start
  Dim startIds As PnPRowIdArray = _
    dataLinkMgr.GetRelatedRowIds( _
    "LineStartAsset", "Line", nRowId, "Asset")
  ' at end
  Dim endIds As PnPRowIdArray = _
    dataLinkMgr.GetRelatedRowIds( _
    "LineEndAsset", "Line", nRowId, "Asset")
  ' flow entities
  Dim flowIds As PnPRowIdArray = _
    dataLinkMgr.GetRelatedRowIds( _
    "LineFlowArrow", "Line", nRowId, "Arrow")
  ' and finally inline ents
  Dim inlineIds As PnPRowIdArray = _
    dataLinkMgr.GetRelatedRowIds( _
    "LineInlineAsset", "Line", nRowId, "Asset")
 End Sub

