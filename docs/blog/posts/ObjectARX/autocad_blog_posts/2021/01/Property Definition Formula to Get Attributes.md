---
title: "Property Definition Formula to Get Attributes"
date: 2021-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Block
description: "Some properties return array of IDispatch which cannot be used in vbscript of formula definition, for instance the attributes returned by BlockRefe..."
author: Autodesk
---
# Property Definition Formula to Get Attributes

发布日期: 2021-01-01

原始链接: https://adndevblog.typepad.com/autocad/2021/01/property-definition-formula-to-get-attributes.html

## 文章内容

Some properties return array of IDispatch which cannot be used in vbscript of formula definition, for instance the attributes returned by BlockReference are of VarType 8201 which is indicates an array of IDispatch pointers.
Using ConvertToVariantArray can convert it to array of variant so that the elements can be reached in vbscript, just like the way how it converts a point value (array of double).
NOTE: AutoCAD.Application.24 – AutoCAD 2021
AecX.AecBaseApplication.8.3 – AutoCAD Architecture 2021.
To know versions of various AEC libraries installed AutoCAD Architecture.
Take a note of ACADVER of your current installed AutoCAD.
AutoCAD Architecture
ACADVER
AEC Lib
2021
24.0
8.3
2020
23.1
8.2
2019
23.0
8.1
2018
22.0
8.0
2017
21.0
7.9
2016
20.1
7.8
2015
20.0
7.7
2014
19.1
7.5
2013
19.0
7.0
2012
18.2
6.7
 RESULT="--"
On Error Resume Next
set acad = GetObject(, "AutoCAD.Application.24")
set aec = acad.GetInterfaceObject("AecX.AecBaseApplication.8.3")
aec.Init acad
set utility = aec.ActiveDocument.Utility
set obj = acad.ActiveDocument.ObjectIDToObject([ObjectID])
attributes = utility.ConvertToVariantArray(obj.GetAttributes)
set attribute = attributes(0)
RESULT = attribute.TextString

## 评论

**内容**: Sonic exe said...
I struggle to articulate my opinions on topics, but I felt compelled to do so in this instance. Your essay is fantastic. I appreciate how you presented this information.
Reply
03/05/2023 at 10:37 PM

---
**内容**: tunnel rush said...
You've come this far and I think that's great, keep chasing your dreams and one day you'll reach the top and then you'll see how great you've become .
Reply
08/03/2023 at 02:24 AM

---
**内容**: wordle said...
This makes it accessible from VBScript.
Reply
10/17/2023 at 09:14 PM

---
**内容**: io games said...
My thoughts are difficult to express, but in this case, I felt obliged to. That is an excellent essay. I like the manner in which you conveyed this data.
Reply
03/23/2024 at 12:50 AM

---
**内容**: Connections Unlimited said...
Whether you’re a seasoned wordsmith or a casual player looking for a fun way to pass the time, this game promises endless hours of entertainment and mental stimulation.
Reply
06/13/2024 at 07:48 PM

---
