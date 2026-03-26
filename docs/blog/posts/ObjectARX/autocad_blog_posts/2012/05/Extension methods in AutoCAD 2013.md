---
title: "Extension methods in AutoCAD 2013"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - C++
  - COM
description: "There’s been a bit of a kerfuffle over on TheSwamp about the use of extension methods in AutoCAD 2013, so I thought I’d write a quick blog post to ..."
author: Autodesk
---
# Extension methods in AutoCAD 2013

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/extension-methods-in-autocad-2013.html

## 文章内容

By Stephen Preston
There’s been a bit of a kerfuffle over on TheSwamp about the use of extension methods in AutoCAD 2013, so I thought I’d write a quick blog post to document some basics here, along with a few useful references. This post is also intended to supplement my DevTV on AutoCAD 2013 .NET Migration, where I didn’t spend much time discussing extension methods and was a little slack with my terminology because I was focusing on the migration demo. (My apologies if I confused anyone by waving my mouse at an extension class and calling it something else – but it doesn’t change the end result if you follow the code examples). Anyway – to business …
AutoCAD 2013 is the first release to fully implement the Big Split architectural work. Big Split was a major refactoring of the AutoCAD core to separate the core business logic from the user interface. The business logic resides in AcCore.dll, which is referenced by acad.exe. Acad.exe provides the basic AutoCAD UI. Kean has discussed the need for and consequences of the Big Split, so I won’t go through all that again here. 
The primary change for your plug-ins is that the splitting of AutoCAD into two components (the core and the UI) means you have to reference an additional AutoCAD .NET API assembly – AcCoreMgd.dll. This is because some of the functionality that was formerly in AcMdg.dll has now been moved from acad.exe to AcCore.dll. If you use P/Invoke a lot, you’ll also have to change some of your code to account for functions formerly exported from acad.exe now being exported from accore.dll.
  Get on with it Stephen – tell us about the extension methods!
Ok! Ok! Some classes in the .NET API cause a problem because they span both the core logic and the platform specific behavior. A good example of this is the Document class. Most of its methods, properties and events are core AutoCAD business logic – they are platform independent – and so fit nicely into AcCoreMgd.dll in the .NET API). (Strictly speaking, the entire AutoCAD .NET API is platform dependent, of course, because AutoCAD for Mac doesn’t have a .NET API - but in AutoCAD .NET we inherit the architecture imposed on us by the C++). However, there are a few methods and properties which are platform dependent. The most obvious one to use as an example is the AcadDocument() property (which is now the GetAcadDocument() extension method). There’s no place for this property in AcCoreMgd.dll, which knows nothing about the AutoCAD for Windows ActiveX API, and so this and a few other methods and properties remain in AcMgd.dll where they’ve always been. But they’ve now been converted to extension methods …
Extension methods are a powerful way of extending a class in .NET without having to derive from that class. They’ve been around in .NET since Framework 3.5, but the first time I came across them was when reviewing the API changes in the AutoCAD 2013 Beta  - when I noticed they were used to bridge the AcMgd/AcCoreMdg gap for classes like Document.
  So what does an extension method look like?
MSDN has some good basic documentation on extension methods in VB.NET and C#, which I recommend you refer to. I’ll use some of the sample code from those documents to demonstrate the concept and highlight something annoying.
Let’s say we want to extend the .NET String class using an extension method - we’d write an extension method like this in C#:
namespace ExtensionMethods
{
  public static class MyExtensions
  {
    public static int WordCount(this String str)
    {
      return str.Split(new char[] { ' ', '.', '?' },
                       StringSplitOptions.RemoveEmptyEntries).Length;
    }
  }
}
If you’ve never seen an extension method before, but you’d spotted these functions in the Visual Studio Object Browser. You’d probably try to use those functions like this:
using System;
using ExtensionMethods;
  namespace ClassLibrary2
{
  class Class2
  {
    public void Test()
    {
      String str = "Hello World!";
      MyExtensions.WordCount(str);
    }
  }
}
The above code will work, but the parameter in the declaration for the WordCount method (‘this String’) is a hint that this isn’t a normal static class method. That little ‘this‘ tells you its an extension method, which you can more succinctly (and correctly) use like this:
using ExtensionMethods;
  public class Test
{
  public void TestFunc()
  {
    string s = "Hello Extension Methods";
    int i = s.WordCount();
  }
}
The code I’ve highlighted in yellow show the power of the extension method - you can call an extension method just like any other method of the String class. You just have to make sure you’ve imported the namespace in which the extension class is defined.
VB.NET  is basically the same, but also a little different . The difference is that you can only define extension methods in VB.NET in a module (not in a class like C#). A VB.NET extension method declaration looks like this:
Imports System.Runtime.CompilerServices
  Module StringExtensions
  <Extension()>
  Public Sub Print(ByVal aString As String)
    Console.WriteLine(aString)
  End Sub
    <Extension()>
  Public Sub PrintAndPunctuate(ByVal aString As String,
                                 ByVal punc As String)
    Console.WriteLine(aString & punc)
  End Sub
End Module
Instead of using ‘this String’ as a parameter to your extension method, you now add the <Extension()> attribute to the methods you want to use as extension methods. The method still takes a String as a parameter, but there is no ‘this’.
You use the extension methods you defined in your extension module like this:
Imports ConsoleApplication2.StringExtensions
Module Module1
    Sub Main()
      Dim example As String = "Example string"
    example.Print()
      example = "Hello"
    example.PrintAndPunctuate(".")
    example.PrintAndPunctuate("!!!!")
    End Sub
End Module
That’s a bit like C#, except you imported the module instead of the namespace containing the class. Which brings us to something I really dislike in .NET – a rare difference in code between C# and VB.NET. Here is the VB.NET code to make use of the extension class I defined in C#:
Imports ExtensionMethods.MyExtensions
  Namespace MyNamespace
  Public Class TestClass
      Public Sub test()
      Dim example As String = "Hello World"
      example.WordCount()
    End Sub
    End Class
End Namespace
Compare the VB.NET imports statement with the C# using statement:
In VB.NET we import ‘ExtensionMethods. MyExtensions’ – i.e. Namespace.Classname.
In C# we import ‘ExtensionMethods’ – i.e. Namespace.
MyExtensions is a static class, but VB.NET makes it look like you’re importing a module – presumably because you have to declare extension methods in modules in VB.NET.
  Ok I get the idea. So how does it work in AutoCAD 2013 .NET?
I thought you’d never ask.
There are four classes in the AutoCAD .NET API that have been split between  AcCore.Mdg.dll and AcMgd.dll (with their core implementation in AcCoreMgd.dll and their extension methods in AcMgd.dll). These are:
Document (and DocumentExtension)
DocumentCollection (and DocumentCollectionExtension)
Editor (and EditorExtension)
Window (and WindowExtension)
Let’s take the DocumentExtension.GetAcadDocument() extension method as a usage example. To use it, I reference AcMdg.dll and AcCoreMdg.dll in my project, import the Autodesk.AutoCAD.ApplicationServices namespace, and then I can use the extension method just as in my examples above. Here is the C# code :
using System;
using Autodesk.AutoCAD.Runtime;
using Autodesk.AutoCAD.ApplicationServices;
  namespace AutoCAD_CSharp_plug_in
{
  public class MyCommands
  {
    [CommandMethod("TEST")]
    public void MyCommand()
    {
      Document doc = Application.DocumentManager.MdiActiveDocument;
      object oAcadDoc = doc.GetAcadDocument();
    }
  }
}
The VB.NET code is similar, but, again, we have that issue with the import being slightly different:
Imports System
Imports Autodesk.AutoCAD.Runtime
Imports Autodesk.AutoCAD.ApplicationServices
Imports Autodesk.AutoCAD.ApplicationServices.DocumentExtension
  Namespace AutoCAD_VB_plug_in
    Public Class MyCommands
    <CommandMethod("TEST")> _
    Public Sub MyCommand()
      Dim doc As Document = Application.DocumentManager.MdiActiveDocument
      Dim oAcadApp As Object = doc.GetAcadDocument()
    End Sub
  End Class
End Namespace
As a final note - if you only use the AutoCAD .NET APIs defined in AcCoreMgd.dll, then you don’t have to reference AcMdg.dll. This then becomes interesting when writing plug-ins to run in other applications that make use of AcCore.dll such as AcCoreConsole, or some other interesting AcCore projects the Autodesk boffins are playing around with.

## 评论

**内容**: Hui Tan said...
why has autocad not updated it's developer help files to reflect these code changes? It's pretty annoying to have to search through so many forums when this can be avoided by updating Autocad 2013 Help. I need to create a new drawing using a specific template and can't use the 'Add' method. Can you please give some directions
Reply
06/10/2012 at 12:52 PM

---
**内容**: Madhukar Moogala said in reply to Hui Tan...
I've submitted a bug report to our techpubs team about the ObjectARX Developers Guide section on Managed Wrappers not being updated to mention the AcCore changes introduced in AutoCAD 2013. (BTW You can report bugs in those docs yourself using the 'Comments' link at the bottom of the page you're reporting a bug for).
My ultimate goal is that you should just have to search in one place for AutoCAD API information - you'd search on Google, Bing, or whatever your favorite search engine happens to be.
Reply
06/11/2012 at 05:27 PM

---
**内容**: sm said...
here i have some extension methods.
http://www.codingsack.com/2016/01/17/bunch-of-useful-extension-methods/
Reply
02/01/2016 at 07:41 AM

---
