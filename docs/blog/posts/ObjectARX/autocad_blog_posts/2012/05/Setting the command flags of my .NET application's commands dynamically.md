---
title: "Setting the command flags of my .NET application's commands dynamically"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - C++
  - COM
  - ObjectARX
description: "I have a .NET application for AutoCAD and I would like to set the command flags in it dynamically. Is this possible?"
author: Autodesk
---
# Setting the command flags of my .NET application's commands dynamically

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/setting-the-command-flags-of-my-net-applications-commands-dynamically.html

## 文章内容

By Adam Nagy
I have a .NET application for AutoCAD and I would like to set the command flags in it dynamically. Is this possible?
Solution
You need to get the command stack and call its functions in order to change the command flags of registered commands.
This only seems possible using ObjectARX.
You could also create a COM server ARX AddIn or a managed wrapper for this functionality that could be called to do the command stack modifications.
In .NET I have this command - as you can see CommandFlags.UsePickSet is not added to the CommandMethod attribute:
[CommandMethod("TestGroup", "TestCommand", CommandFlags.Modal)]
static public void test()
{
  Document doc = Application.DocumentManager.MdiActiveDocument;
  Editor ed = doc.Editor;
    try
  {
    PromptSelectionResult psr = ed.SelectImplied();
    ed.WriteMessage("No. of selected objects = " +
    psr.Value.Count.ToString());
  }
  catch
  {
    ed.WriteMessage("Error in TestCommand");
  }
}
I select a couple of entities on the screen and then call TestCommand, but it returns an error message for the pickfirst set is not available for it.
Then I run the command defined in my ARX module to change the command flags:
static void ArxDynamicCommandFlag_SetCommandFlags(void)
{
  AcEdCommandStack* pCmdStack =
    AcEdCommandStack::cast(acrxSysRegistry()->at(ACRX_COMMAND_DOCK));
    AcEdCommand *pCmd = pCmdStack->lookupGlobalCmd(L"TestCommand");
  AcRxFunctionPtr pFunc = pCmd->functionAddr();
  ACHAR localName[31], globalName[31], groupName[31] = L"TestGroup";
  _tcscpy(localName, pCmd->localName());
  _tcscpy(globalName, pCmd->globalName());
    Acad::ErrorStatus errCode;
  errCode = pCmdStack->removeCmd(groupName, globalName);
  errCode = pCmdStack->addCommand(groupName, globalName, localName,
    ACRX_CMD_USEPICKSET, pFunc);
}
Now, when I select a couple of entities and run TestCommand again, then it prints out the number of selected entities alright.

## 评论

**内容**: Ben said...
Hi there
thank you for your article.
do you have a practical example of where changing the command flags are required?
Reply
07/23/2017 at 08:03 PM

---
