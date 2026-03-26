---
title: "How to Run Javascript Routines in AutoCAD .NET Plugin Using ClearScript Library"
date: 2024-04-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - C#
  - JavaScript
  - Plugin
description: "This code demonstrates how to execute JavaScript functions or routines in your AutoCAD .NET plugin using ClearScript library from Microsoft."
author: Autodesk
---
# How to Run Javascript Routines in AutoCAD .NET Plugin Using ClearScript Library

发布日期: 2024-04-01

原始链接: https://adndevblog.typepad.com/autocad/2024/04/how-to-run-javascript-routines-in-autocad-net-plugin-using-clearscript-library.html

## 文章内容

By Madhukar Moogala
This code demonstrates how to execute JavaScript functions or routines in your AutoCAD .NET plugin using ClearScript library from Microsoft.
This project is targeted to work with .NET 8.0  platform in AutoCAD 2025.
Exposing AutoCAD .NET Classes:
Enables access to AutoCAD functionality from JavaScript scripts.
Executing JavaScript Functions:
Allows you to run JavaScript functions within your AutoCAD application.
Calling C# Functions from JavaScript:
Facilitates interaction between your JavaScript code and C# functions.
//Exposing AutoCAD .NET classes to JavaScript
```csharp
public class PrintMessage
{
    private static Editor? _ed
    {
        get
        {
            Document doc = Application.DocumentManager.MdiActiveDocument;
            if (doc != null)
            {
                return doc.Editor;
            }
            return null;
        }
    }
    public static void Print(string message)
    {
        _ed?.WriteMessage($"{message}\n");
    }
}

public class Commands
{
    private const string _script = @"
                        function square(x) {
                            return x*x;
                        }";
        
    //Execute JS functions in DotNet runtime


    [CommandMethod("JSRoutine")]
    public static void JSRoutine()
    {
        Document doc = Application.DocumentManager.MdiActiveDocument;
        if (doc is null) return;
        Editor ed = doc.Editor;
    
        // Create aV8ScriptEngine instance, 
        using (var engine = new V8ScriptEngine())
        {
            engine.AccessContext = typeof(Commands);
    
                //Now expose the PrintMessage class from .NET to the script engine,
            // and then execute a JavaScript statement that writes a message to the AutoCAD Editor.
            engine.AddHostType("PrintMessage", typeof(PrintMessage));              
            engine.Execute("PrintMessage.Print('Hello from JavaScript!');");
    
            //Call the JS function square and retrieve the result.
            engine.Execute(_script);
            dynamic? result = engine.Script.square(5);
            ed.WriteMessage($"{Convert.ToString(result)}\n");


            //Execute the JS code and print the result to the AutoCAD Editor                
            engine.Execute("function print(x) {PrintMessage.Print(x); }");
            engine.Script.print(DateTime.Now.DayOfWeek.ToString());
    
            //Calling C# Functions from JavaScript:              
            engine.AddHostObject("Greet", new Func((name) => $"Hello, {name}!"));              
            engine.Execute("var message = Greet('World'); PrintMessage.Print(message);");
    
            // examine a script object            
            engine.Execute("var person = { name: 'Fred', age: 5 }");
            ed.WriteMessage($"From Script: \n{Convert.ToString(engine.Script.person.name)}");
        }
    }
}
```
Source Code: https://github.com/MadhukarMoogala/AcadPlugin/blob/main/README.md

