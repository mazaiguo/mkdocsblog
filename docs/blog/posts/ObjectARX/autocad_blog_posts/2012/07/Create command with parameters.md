---
title: "Create command with parameters"
date: 2012-07-01
categories:
  - AutoCAD .NET
tags:
  - .NET
description: "I've created some commands in .NET but I cannot see how to set them up so that they will accept parameters."
author: Autodesk
---
# Create command with parameters

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/create-command-with-parameters.html

## 文章内容

By Adam Nagy
I've created some commands in .NET but I cannot see how to set them up so that they will accept parameters.
Solution
The function that implements the command cannot accept parameters, but inside the command implementation you can accept parameters using command line input functions like GetString(), GetInteger(), etc. that can be found under the Editor class.
[CommandMethod("CommandWithParameters")]
public void CommandWithParameters()
{
  Editor ed = acApp.DocumentManager.MdiActiveDocument.Editor;
    PromptResult pr = ed.GetString("\nProvide a string: ");
  if (pr.Status != PromptStatus.OK)
  {
    ed.WriteMessage("No string was provided\n");
    return;
  }
    PromptIntegerResult pir = ed.GetInteger("\nProvide an integer: ");
  if (pir.Status != PromptStatus.OK)
  {
    ed.WriteMessage("No integer was provided\n");
    return;
  }
    ed.WriteMessage(
    "\nCommand got following parameters: {0} and {1}\n",
    pr.StringResult, pir.Value.ToString());
}
In case of the above command I can call the command and pass in the parameters one by one, or pass them at the same time e.g. using the (command) LISP function. Here is what it would look like in the Command Line:
Command: COMMANDWITHPARAMETERS
Provide string: mystring
Provide an integer: 12
Command got following parameters: mystring and 12
Command: (command "COMMANDWITHPARAMETERS" "mystring" 12)
COMMANDWITHPARAMETERS
Provide string: mystring
Provide an integer: 12
Command got following parameters: mystring and 12
Command: nil
Depending on your requirements you could also create a LISP function in .NET instead of a command that could accept parameters. In that case you'd need to use the LispFunction attribute instead of CommandMethod.

