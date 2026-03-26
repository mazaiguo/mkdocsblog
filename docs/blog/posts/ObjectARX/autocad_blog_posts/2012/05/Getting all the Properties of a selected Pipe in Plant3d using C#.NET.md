---
title: "Getting all the Properties of a selected Pipe in Plant3d using C#.NET"
date: 2012-05-01
categories:
  - Plant 3D
tags:
  - .NET
  - C#
  - Plant 3D
description: "I was just looking around to see if there was some sample code out on the web which showed how to obtain the properties of a given pipe in Plant3d ..."
author: Autodesk
---
# Getting all the Properties of a selected Pipe in Plant3d using C#.NET

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/getting-all-the-properties-of-a-selected-pipe-in-plant3d-using-cnet.html

## 文章内容

by Fenton Webb
I was just looking around to see if there was some sample code out on the web which showed how to obtain the properties of a given pipe in Plant3d and found nothing, so I thought I’d put one together for you all to enjoy!!
Just get hold of the DataLinksManager and utilize the GetAllProperties(). Here’s what I am talking about…
// get all the properties of a selected object in Plant3d
// by Fenton Webb, Autodesk, 29/05/2012
[CommandMethod("GetPipingProperties")]
public void GetPipingProperties()
{
  // get the AutoCAD Editor object so we can print to the command line
  Editor ed = AcadApp.DocumentManager.MdiActiveDocument.Editor;
    // select the object
  PromptEntityResult res = ed.GetEntity("Pick Object obtain properties : ");
  // if something selected
  if (res.Status == PromptStatus.OK)
  {
    // get the current project object
    PlantProject currentProj = PlantApplication.CurrentProject;
    // get the Piping project part
    PipingProject pipingProj = (PipingProject)currentProj.ProjectParts["Piping"];
      // get the data links manager
    DataLinksManager dlm = pipingProj.DataLinksManager;
    // and then get the row id for the selected object
    int rowId = dlm.FindAcPpRowId(res.ObjectId);
      List<KeyValuePair<string, string>> properties;
    properties = dlm.GetAllProperties(rowId, true);
    // Iterate through the entries in the list.
    for (int i = 0; i < properties.Count; i++)
      ed.WriteMessage("\nProperty name:" + properties[i].Key +
                            " = " + properties[i].Value);
  }
}

## 评论

**内容**: Tim said...
Is there any way to tell the datatype of the property that is retrieved?
Reply
07/10/2012 at 10:39 AM

---
**内容**: Fenton Webb said...
You can use properties[i].Value.GetType() to work out the datatype.
Reply
07/10/2012 at 01:43 PM

---
**内容**: Samuel Wu said...
Hi, Fenton, do you know how to use the method SetProperties() to set the PipelineGroup's Tag?
Reply
08/16/2012 at 01:23 AM

---
**内容**: RF Lin said...
Hi,
why the properties = dlm.GetAllProperties(rowId, true);
can't get weld number of WELD?
Reply
08/28/2015 at 11:39 PM

---
**内容**: Marat Mirgaleev said...
> can't get weld number of WELD
Can't get "ValveCode" of a Valve as well :(
So, the method's name is wrong.
The Plant SDK Developer Reference (plantsdk_ref.chm) says:
This is GetAllProperties, a member of class DataLinksManager.
Reply
06/30/2020 at 05:22 AM

---
**内容**: anonymous said...
how to Convert 2D pipe To #D using API
Reply
11/28/2022 at 04:01 AM

---
**内容**: Gokul said...
How to get only specific properties? For example i want to get only General properties from Properties tab for a model..
Reply
04/27/2023 at 04:42 AM

---
**内容**: rohitraghavraghav1@gmail.com said...
i have doubt how can i get only object visual view check is true property only
Reply
11/06/2023 at 04:26 AM

---
**内容**: rohitraghavraghav1@gmail.com said...
please help me is it possible to get only showing property form property in plant 3D
dlm.GettAllProp() from this function I got all property but i want only object visual view (True) checked property . any one can help me
Reply
11/08/2023 at 05:00 AM

---
**内容**: Muhammad Shoaib Anjum said...
Good code. Is there a way to change the value of any of these property?
Reply
04/28/2024 at 12:57 AM

---
