---
title: "Return to command prompt when ESCAPE is pressed using .NET"
date: 2013-02-01
categories:
  - AutoCAD .NET
tags:
  - .NET
description: "Consider this: You have a .NET routine that takes some time to complete. While this routine runs, you decide you have had enough of the waiting and..."
author: Autodesk
---
# Return to command prompt when ESCAPE is pressed using .NET

发布日期: 2013-02-01

原始链接: https://adndevblog.typepad.com/autocad/2013/02/return-to-command-prompt-when-escape-is-pressed-using-net.html

## 文章内容

By Gopinath Taget
Consider this: You have a .NET routine that takes some time to complete. While this routine runs, you decide you have had enough of the waiting and would like to stop this routine and return to the command prompt when the user presses the ESCAPE key. Is there a way to do this?
The HostApplicationServices.UserBreak method allows the application to check the escape key and take the appropriate action.
The code below shows this approach. A long process is started in a simple loop that calls thread sleep. On each iteration the code checks the current HostApplicationServices to see if the escape key was pressed. If it was pressed the code throws an exception where the program can finish gracefully.
[CommandMethod("lfunc")]
public static void myLongFunction()
{
    //show the progress of the function
    ProgressMeter pm = new ProgressMeter();
    pm.Start("Long process");
    pm.SetLimit(100);
    try
    {
        //start a long process
        for (int i = 0; i < 100; i++)
        {
            //did user press ESCAPE?
            if (HostApplicationServices.Current.UserBreak())
                throw new Autodesk.AutoCAD.Runtime.Exception(
                    ErrorStatus.UserBreak, "ESCAPE pressed");
            //update progress bar
            pm.MeterProgress();
            //delay 10 miliseconds
            System.Threading.Thread.Sleep(10);
        }
    }
    catch (System.Exception ex)
    {
        //some error
        Application.DocumentManager.MdiActiveDocument.
            Editor.WriteMessage(ex.Message);
    }
    finally
    {
        pm.Stop();
    }
}

