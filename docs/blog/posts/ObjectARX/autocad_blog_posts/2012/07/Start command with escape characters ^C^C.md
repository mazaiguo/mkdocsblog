---
title: "Start command with escape characters ^C^C"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "I'd like to start some commands from my modeless dialog's buttons. I already found that in case of SendStringToExecute I should use '\x03' characte..."
author: Autodesk
---
# Start command with escape characters ^C^C

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/start-command-with-escape-characters-cc.html

## 文章内容

By Adam Nagy
I'd like to start some commands from my modeless dialog's buttons. I already found that in case of SendStringToExecute I should use '\x03' characters instead of ^C. My only problem is that in this case if no command is running then I end up with two *Cancel* strings in the Command Window, whereas a menu's ^C^C does not cause *Cancel* to appear if no command is running when the menu item is clicked.
How could I achieve the same?
Solution
You could check the CMDNAMES system variable and depending on how many commands are currently running you could add that many escape characters to the beginning of your command string.
Here is a sample that demonstrates this:
using System;
using System.Windows.Forms;
using acApp = Autodesk.AutoCAD.ApplicationServices.Application;
using Autodesk.AutoCAD.ApplicationServices;
  namespace CsMgdAcad1
{
  public partial class Form1 : Form
  {
    public Form1()
    {
      InitializeComponent();
    }
      private void button1_Click(object sender, EventArgs e)
    {
      string esc = "";
        string cmds = (string)acApp.GetSystemVariable("CMDNAMES");
      if (cmds.Length > 0)
      {
        int cmdNum = cmds.Split(new char[] { '\'' }).Length;
          for (int i = 0; i < cmdNum; i++)
          esc += '\x03';
      }
        Document doc = acApp.DocumentManager.MdiActiveDocument;
      doc.SendStringToExecute(esc + "_.LINE ", true, false, true);
    }
  }
}

