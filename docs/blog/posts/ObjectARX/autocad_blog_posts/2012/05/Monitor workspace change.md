---
title: "Monitor workspace change"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
description: "If you need to monitor the workspace change, e.g. so that you can update the Ribbon with the controls you placed using the Ribbon Runtime API, then..."
author: Autodesk
---
# Monitor workspace change

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/monitor-workspace-change.html

## 文章内容

By Adam Nagy
If you need to monitor the workspace change, e.g. so that you can update the Ribbon with the controls you placed using the Ribbon Runtime API, then you can listen to the system variable changed event, and watch out for WSCURRENT
using System;
  using Autodesk.AutoCAD.Runtime;
using acApp = Autodesk.AutoCAD.ApplicationServices.Application;
using Autodesk.AutoCAD.ApplicationServices;
  [assembly:CommandClass(typeof(TestProject.Commands))]
  namespace TestProject
{
  public class Commands
  {
    [CommandMethod("MonitorWorkspaceChange")]
    public void MonitorWorkspaceChange()
    {
      acApp.SystemVariableChanged +=
        new SystemVariableChangedEventHandler(
          acApp_SystemVariableChanged);
    }
      void acApp_SystemVariableChanged(
      object sender, SystemVariableChangedEventArgs e)
    {
      if (e.Name == "WSCURRENT")
      {
        string currentWorkspaceName =
          (string)acApp.GetSystemVariable(e.Name);
          // Do whatever you need
      }
    }
  }
}

## 评论

**内容**: PDOTeam said...
I think you also have to monitor the Profile changing. For example, if a user changes the profile via the options command, I don't believe the WSCURRENT setting notifies that the workspace has changed.
Reply
05/18/2012 at 08:19 AM

---
**内容**: Adam Nagy said in reply to PDOTeam...
Thank you for the comment.
Even then the event for WSCURRENT does seem to fire - first with an empty string, then with the actual workspace name.
I checked it in AutoCAD 2012.
Reply
05/18/2012 at 08:30 AM

---
