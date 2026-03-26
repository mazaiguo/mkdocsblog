---
title: "Plant SDK: Reacting on Database Changes"
date: 2012-10-01
categories:
  - AutoCAD
tags:
  - Database
description: "I would like to get notified when some data changed in the project database. Which event shall I subscribe for?"
author: Autodesk
---
# Plant SDK: Reacting on Database Changes

发布日期: 2012-10-01

原始链接: https://adndevblog.typepad.com/autocad/2012/10/plant-sdk-reacting-on-database-changes.html

## 文章内容

By Marat Mirgaleev
Issue
I would like to get notified when some data changed in the project database. Which event shall I subscribe for?
Solution
You will need to create an event handler for the DataLinksManager.DataLinkOperationOccurred event. This is a code sample:
      static private bool _isActive = true; // To avoid recursion
      // Event Handler
    //---------------------------------------------------------------
    public static void dlm_DataLinkOperationOccurred(object sender,
                                                 DataLinkEventArgs e)
    {
      if (e.Action == DataLinkAction.RowModified && _isActive)
      {
        try
        {
          DataLinksManager dlm = PlantApplication.CurrentProject.
                             ProjectParts["Piping"].DataLinksManager;
          if (dlm.HasProperty(e.RowId, "MyProperty"))
          {
            StringCollection props = new StringCollection();
            props.Add("Size");
            props.Add("Spec");
              StringCollection values = null;
            values = dlm.GetProperties(e.RowId, props, true);
              PpObjectIdArray ppoids = dlm.FindAcPpObjectIds(e.RowId);
              StringCollection newprops = new StringCollection();
            newprops.Add("MyProperty");
              StringCollection newvals = new StringCollection();
            newvals.Add(values[0] + values[1]);
              _isActive = false;
            dlm.SetProperties(ppoids.First.Value, newprops, newvals);
          }
        }
        catch
        {
          System.Diagnostics.Debug.WriteLine(
                  "Error in the Event Handler:\n{0}", e.ToString() );
        }
        finally
        {
          _isActive = true;
        }
      }
    }
        // Subscribe to the event
    //---------------------------------------------------------------
    [CommandMethod("AddEventHandler", CommandFlags.Modal)]
    public static void AddEventHandler()
    {
      try
      {
        DataLinksManager dlm = PlantApplication.CurrentProject.
                             ProjectParts["Piping"].DataLinksManager;
        dlm.DataLinkOperationOccurred +=
             new DataLinkEventHandler(dlm_DataLinkOperationOccurred);
      }
      catch (Exception e)
      {
        System.Windows.Forms.MessageBox.Show(e.ToString(),
                                     "Cannot add the Event Handler");
      }
    }
        // Remove the subscription
    //---------------------------------------------------------------
    [CommandMethod("RemoveEventHandler", CommandFlags.Modal)]
    public static void RemoveEventHandler()
    {
      try
      {
        DataLinksManager dlm = PlantApplication.CurrentProject.
                             ProjectParts["Piping"].DataLinksManager;
        dlm.DataLinkOperationOccurred -=
             new DataLinkEventHandler(dlm_DataLinkOperationOccurred);
      }
      catch (Exception e)
      {
        System.Windows.Forms.MessageBox.Show(e.ToString(),
                                  "Cannot remove the Event Handler");
      }
    }

## 评论

**内容**: _davewolfe said...
The better way to do this is watch the PnPTable. On that table, you can watch for specific columns and get the changed values. It has better performance, as the datalinks manager values get check very frequently.
Reply
12/23/2014 at 07:36 AM

---
