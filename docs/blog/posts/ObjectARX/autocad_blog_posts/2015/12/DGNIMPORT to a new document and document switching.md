---
title: "DGNIMPORT to a new document and document switching"
date: 2015-12-01
categories:
  - AutoCAD
tags:
  - Unicode
description: "Recently, one of my colleague had this query :"
author: Autodesk
---
# DGNIMPORT to a new document and document switching

发布日期: 2015-12-01

原始链接: https://adndevblog.typepad.com/autocad/2015/12/dgnimport-to-a-new-drawing-and-document-switching.html

## 文章内容

By Balaji Ramamoorthy
Recently, one of my colleague had this query :
I am importing the DGN (not to the current drawing). This creates a new drawing and I want to switch to the new drawing and perform other commands. What is the best way to switch the current drawing to the other open drawing.
Here is a code snippet to do that.
The command that invokes the "DGNIMPORT", makes the newly imported document as Active. After the document is made active, you are in the new document’s context and to verify it, the editor.writemessage will output the message in the new document's command prompt.
[CommandMethod("Test1", CommandFlags.Session)]
public async static void Test1Method()
{
    DocumentCollection dm = Application.DocumentManager;
    Editor ed = 
    Application.DocumentManager.MdiActiveDocument.Editor;
    try
    {
        PromptResult promptDgnPath
                = ed.GetString("\nEnter DGN file name: ");
        if (promptDgnPath.Status != PromptStatus.OK)
            return;

        try
        {
            await dm.ExecuteInCommandContextAsync(
                async (obj) =>
                {
                    await ed.CommandAsync(new object[] 
                    { 
                        "_.-DGNIMPORT", 
                        promptDgnPath.StringResult, 
                        "Default", 
                        "Master", 
                        "Standard" 
                    });
                },
                null
            );
        }
        catch (System.Exception ex)
        {
            ed.WriteMessage("\nException: {0}\n", ex.Message);
        }

        DocumentCollection docs = Application.DocumentManager;
        foreach (Document doc in docs)
        {
            if (doc.Name.StartsWith("Drawing"))
            {
                Application.DocumentManager.MdiActiveDocument 
                                                        = doc;
                break;
            }
        }
        ed.WriteMessage("Hello !!");
    }
    catch (System.Exception ex)
    {
        ed.WriteMessage(ex.Message);
    }
}

