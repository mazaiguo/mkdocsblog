---
title: "VBA block insertion not requesting attributes"
date: 2013-02-01
categories:
  - AutoCAD VBA
tags:
  - AutoCAD
  - Block
  - Unicode
  - VBA
description: "If a block has attribute definitions, AutoCAD inserts all attributes with its default values and does not ask for the attribute values."
author: Autodesk
---
# VBA block insertion not requesting attributes

发布日期: 2013-02-01

原始链接: https://adndevblog.typepad.com/autocad/2013/02/vba-block-insertion-not-requesting-attributes.html

## 文章内容

By Augusto Goncalves
If a block has attribute definitions, AutoCAD inserts all attributes with its default values and does not ask for the attribute values.
There is no ready-to-use function that asks for the attributes. Therefore, you will need to write your own function.
After inserting the attribute you can use the AcadBlockReference.GetAttributes method to get all attributes. Then you can iterate the attributes and ask for the values. If you want to use the original prompt string, you have to get the block definition object and to look for the right attribute in it. There you can get the prompt string.
The following function inserts the block 'test' and iterates the attributes. The 'UserForm1' object is a user form which contains:
- An "OK" button which has to be pressed after entering the value for the current attribute and which hides the form
- Three text boxes:
TextBox1 : receives the attribute name (locked)
TextBox2 : receives the attribute prompt string (locked)
TextBox3 : there you can enter the value of the attribute
The second function,  GetPromptString, finds the original prompt string of the attribute:
Sub TestFunction()
   Dim insPt As Variant
   Dim insert As Object
   Dim attribs As Variant
   Dim attrib As Object
   
   ' Activate AutoCAD
   AppActivate ThisDrawing.Application.Caption
   
   ' Get insertion point for insert entity
   insPt = ThisDrawing.Utility.GetPoint(, "Select insert point: ")
   ' Insert it
   Set insert = ThisDrawing.ModelSpace.InsertBlock(insPt, _ 
       "TEST", 1#, 1#, 1#, 0#)
   
   ' Ask for the attributes
   attribs = insert.GetAttributes
   For i = LBound(attribs) To UBound(attribs)
      Set attrib = attribs(i)
      UserForm1.TextBox1.Value = attrib.TagString
      UserForm1.TextBox2.Value = GetPromptString("TEST", attrib)
      UserForm1.TextBox3.Value = attrib.TextString
      UserForm1.Show
      If UserForm1.TextBox3.Value <> "" Then
         attrib.TextString = UserForm1.TextBox3.Value
      End If
   Next i
End Sub
Public Function GetPromptString(blockName, attrib) As String
   ' This function extracts the prompt string
   ' of an attribute definition (AcadAttribute).
   ' The needed parameters are the block name
   ' and the attribute (AcadAttributeReference).
   Dim blocks As Object
   Dim block As Object
   Dim count As Integer
   Dim i As Integer
   Dim ent As Object
   
   ' Get the block definition object of block 'blockName'
   Set block = ThisDrawing.blocks.Item(blockName)
   
   ' Find the attribute (specified by 'attrib')
   count = block.count
   For i = 0 To count - 1
      Set ent = block.Item(i)
      If ent.EntityType = acAttribute Then
         If ent.TagString = attrib.TagString Then
            GetPromptString = ent.PromptString
            Exit Function
         End If
      End If
   Next i
   GetPromptString = ""
End Function

