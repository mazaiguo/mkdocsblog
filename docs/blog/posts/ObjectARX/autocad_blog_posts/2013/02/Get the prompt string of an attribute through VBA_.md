---
title: "Get the prompt string of an attribute through VBA?"
date: 2013-02-01
categories:
  - AutoCAD VBA
tags:
  - Block
  - VBA
description: "We can get the prompt string of an Attribute from the Attribute Definition contained in the Block Definition. The following sample code demonstrate..."
author: Autodesk
---
# Get the prompt string of an attribute through VBA?

发布日期: 2013-02-01

原始链接: https://adndevblog.typepad.com/autocad/2013/02/get-the-prompt-string-of-an-attribute-through-vba.html

## 文章内容

By Augusto Goncalves
We can get the prompt string of an Attribute from the Attribute Definition contained in the Block Definition. The following sample code demonstrates this:
Private Sub GetBlockAttributePrompts()
    Dim elem As Object
    For Each elem In ThisDrawing.ModelSpace
        If elem.EntityName = "AcDbBlockReference" Then
            If elem.HasAttributes Then
                'Get The Block Definition
                Dim block As AcadBlock
                Set block = ThisDrawing.Blocks.item(elem.Name)
                
                Dim prompt As String
                prompt = ""
                
                Dim item As Object
                For Each item In block                   
                    If item.EntityName = "AcDbAttributeDefinition" Then
                        prompt = prompt + Chr(13) + item.PromptString
                    End If
                Next item
                Debug.Print prompt
            End If
        End If
    Next elem
End Sub

