---
title: "Get the constant attributes of a blockref through VBA"
date: 2013-02-01
categories:
  - AutoCAD VBA
tags:
  - Block
  - VBA
description: "How can we get the block name, the attribute values, and find how many times the block is inserted and put this information into a spreadsheet usin..."
author: Autodesk
---
# Get the constant attributes of a blockref through VBA

发布日期: 2013-02-01

原始链接: https://adndevblog.typepad.com/autocad/2013/02/get-the-constant-attributes-of-a-blockref-through-vba.html

## 文章内容

By Augusto Goncalves
How can we get the block name, the attribute values, and find how many times the block is inserted and put this information into a spreadsheet using VBA? Getting the block information from the block definition in the block table.
The following sample demonstrates this by getting all the attributes of all the block references found in model space. You need to create a simple form which contains a listbox named ListBox1 and a button that starts the following procedure:
Private Sub CommandButton1_Click()
  Dim elem As Object
  Dim block As AcadBlock
  Dim item As Object
  Dim Array1 As Variant
  Dim count As Integer
  Dim MBtest1 As String
  Dim str As String
  For Each elem In ThisDrawing.ModelSpace
    If elem.EntityName = "AcDbBlockReference" Then
    If elem.HasAttributes Then
      Array1 = elem.GetAttributes
      For count = LBound(Array1) To UBound(Array1)
        If (Array1(count).EntityName) = "AcDbAttribute" Then
        MBtest1 = Array1(count).TagString & _
          " - " & Array1(count).TextString
        ListBox1.AddItem MBtest1
        End If
      Next count
      'Get the block definition from the block table
      str = elem.Name
      Set block = ThisDrawing.Blocks.item(str)
      For Each item In block
        str = item.EntityName
        'Get the Constant attributes
        If item.EntityName = "AcDbAttributeDefinition" Then
        If item.Mode = acAttributeModeConstant Then
        ListBox1.AddItem item.TagString & " - " _
          & item.TextString
        End If
        End If
      Next item
    End If
    End If
   Next elem
End Sub

## 评论

**内容**: Zakaria said...
I need to know how many is repeated a block in the model space In AutoCad through a VBA Code
Please HELP
Reply
06/13/2013 at 12:37 AM

---
**内容**: Augusto Goncalves said in reply to Zakaria...
Hi Zakaria,
Not sure if I'm understood your question...can you clarify?
Thanks,
Augusto Goncalves
Reply
06/13/2013 at 06:54 AM

---
**内容**: Zakaria said in reply to Augusto Goncalves...
Hi Augusto,
I have an autocad drawing contains many blocks and blocks under the same name,
My question is how can I count the blocks that have a certain name? For example I need to know how many blocks in my drawing have the name: "Block1" through a VBA Code.
Thank you a lot for your help
Zakaria
Reply
06/15/2013 at 12:29 AM

---
**内容**: Zakaria said in reply to Zakaria...

Or how many times the "Block1" is used in my drawing?
Thanks a lot & Best Regards
Zakaria
Reply
06/15/2013 at 12:45 AM

---
**内容**: Augusto Goncalves said in reply to Zakaria...
Zakaria,
You may need to open the model space, then run through the collection of entities, check if is a AcadBlockReference, if so, check the Name property, which points to the block name defined for it.
Hope this help.
Regards,
Augusto Goncalves
Reply
06/19/2013 at 07:17 AM

---
**内容**: keunsung said...
Hi Augusto.
How to get just one text of tag(specified) in 1 block(specified) what i want?
I need to put one value of a tag into textbox1
ex)
I have "GAD" block which has "OH" tag
and I want to put value of tag"OH" in textbox1
Can you help me?
Reply
07/19/2013 at 11:59 PM

---
**内容**: Augusto Goncalves said in reply to keunsung...
Hi,
Please take a look at this help topic: http://docs.autodesk.com/ACD/2014/PLK/files/GUID-BA69D85A-2AED-43C2-B5B7-73022B5F28F8.htm (at the bottom you'll find a VBA sample code).
Regards
Augusto Goncalves
Reply
07/22/2013 at 11:27 AM

---
