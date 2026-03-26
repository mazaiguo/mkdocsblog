---
title: "Display Forms inside async AutoCAD commands"
date: 2014-10-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - Unicode
description: "You may have given a try already at the very cool async .Net 4.5 feature."
author: Autodesk
---
# Display Forms inside async AutoCAD commands

发布日期: 2014-10-01

原始链接: https://adndevblog.typepad.com/autocad/2014/10/display-forms-inside-async-autocad-commands.html

## 文章内容

By Philippe Leefsma
You may have given a try already at the very cool async .Net 4.5 feature.
When displaying a form inside an async AutoCAD 2015 command, it happens that the synchronization context is not restored properly after closing the form, which provoke some undesirable behavior, for example the output of Editor.WriteMesage not being displayed in the command line.
A simple way to work around it is to save the current context prior to show the form and reset it once it closes.
An example of what I’m talking about just below:
// simulates an async function
private static async Task<string> AsyncTask(string name)
{
    await Task.Delay(5000);
      return "Hello " + name;
}
  [CommandMethod("ADN", "SyncContextCmd", CommandFlags.Transparent)]
async static public void SyncContextCmd()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      // saves current synchronization context
    var syncContext = SynchronizationContext.Current;
      AdnForm form = new AdnForm();
      var dialogResult = Application.ShowModalDialog(form);
      // restores synchronization context
    SynchronizationContext.SetSynchronizationContext(
        syncContext);
      if (dialogResult != System.Windows.Forms.DialogResult.OK)
        return;
      // process form result asynchronously
    string result = await AsyncTask(form.UserName);
      // editor.WriteMessage works OK now
    ed.WriteMessage("\nResult: " + result + "\n");
}

