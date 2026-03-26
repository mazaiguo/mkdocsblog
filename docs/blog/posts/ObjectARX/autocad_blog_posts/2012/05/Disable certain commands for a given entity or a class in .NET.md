---
title: "Disable certain commands for a given entity or a class in .NET"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - Block
  - C#
  - Database
description: "One way to achieve this is not to allow the user to select the entity type on the screen. This will prevent the user from running any command on th..."
author: Autodesk
---
# Disable certain commands for a given entity or a class in .NET

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/disable-certain-commands-for-a-given-entity-or-a-class-in-net.html

## 文章内容

By Virupaksha Aithal
One way to achieve this is not to allow the user to select the entity type on the screen. This will prevent the user from running any command on the entity. Using the SelectionAdded event, one can watch for the entity that is being added to the selection set of the command. In the event, check for the current running command and if the entity or the entity type is one that needs to be blocked. If so, remove the entity from the selection set.
The sample C# code below shows how this can be achieved. In the sample, all entities of type Circle are removed during the COPY command. You can check for a specific entity by checking its handle or object id against a list.
using System;
using System.Collections.Generic;
  using Autodesk.AutoCAD.DatabaseServices;
using Autodesk.AutoCAD.ApplicationServices;
using Autodesk.AutoCAD.EditorInput;
using Autodesk.AutoCAD.Runtime;
using acApp = Autodesk.AutoCAD.ApplicationServices.Application;
  public class MyCommands
{
    [CommandMethod("MyReactor")]
    public void MyReactor()
    {
        Editor ed = acApp.DocumentManager.MdiActiveDocument.Editor;
        ed.SelectionAdded +=
                 new SelectionAddedEventHandler(ed_SelectionAdded);
    }
      void ed_SelectionAdded(object sender,
                                        SelectionAddedEventArgs e)
    {
        string cmds = (string)acApp.GetSystemVariable("CMDNAMES");
          if (!cmds.StartsWith("COPY"))
            return;
          int i = 0;
        List<int> indices = new List<int>();
        foreach (SelectedObject selObj in e.AddedObjects)
        {
            // Need to go from the top so that the other indices
            // do not change when we remove an item, that's why
            // using Insert(0, i), which reverses the order
              if (selObj.ObjectId.ObjectClass ==
                                RXClass.GetClass(typeof(Circle)))
                indices.Insert(0, i);
              i++;
        }
          foreach (int current in indices)
            e.Remove(current);
    }
}

## 评论

**内容**: Norman Yuan said...
Does this approach (handling SelectionAdded event) work with pick-first command execution?
Reply
06/10/2013 at 03:17 PM

---
