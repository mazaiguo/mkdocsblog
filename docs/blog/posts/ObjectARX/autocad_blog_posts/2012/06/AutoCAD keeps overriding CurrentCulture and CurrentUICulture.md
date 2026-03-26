---
title: "AutoCAD keeps overriding CurrentCulture and CurrentUICulture"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Plugin
description: "I have localized resources and would like to use the French Canadian ones even inside the English version of AutoCAD."
author: Autodesk
---
# AutoCAD keeps overriding CurrentCulture and CurrentUICulture

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/autocad-keeps-overriding-currentculture-and-currentuiculture.html

## 文章内容

By Adam Nagy
I have localized resources and would like to use the French Canadian ones even inside the English version of AutoCAD.
I set the CurrentCulture and CurrentUICulture to "fr-CA" in the Initialize() function of my IExternalApplication and the dialog I pop up directly after that comes up in French as it should. But later on, when I show another dialog of mine, that comes up in English, so it seems that for some reason AutoCAD changed the CurrentUICulture back to what it was before. Why does AutoCAD do it?
Solution
AutoCAD sets the CurrentUICulture to match the language version of the running instance of AutoCAD. This enables all its components and other add-ins to use the appropriate language resources.
E.g. if you were running the French version of AutoCAD (fr-FR) in that case your French resources (fr-FR) would be used automatically.
If your resources are not specific to Canada, then it's better to create a "fr" resource instead of a "fr-CA" one, so that no matter which variation of French is being used, your French resources will be loaded.
It's worth having a look at the Resource Fallback Process being used by the resource manager before deciding about how to organize your localized resources. You can find information about it on the net.
AutoCAD also sets the CurrentCulture.NumberFormat to 'invariant' for legacy reasons, like the fact that comma [,] is used as input value separator no matter what language version of AutoCAD you are using.
AutoCAD sets the above two things every time it starts a fiber. Fibers in AutoCAD correspond to 'Thread' objects in .NET
Fibers are created in the following situations:
Main thread is converted into a fiber during startup
When a document is created we create a fiber
Most commands run in their own fiber
Our advice to developers is to override the culture in the tightest possible scope. This ensures that interference with AutoCAD or other applications is minimised.
You could create a helper class for this:
using System;
using System.Globalization;
using System.Threading;
  class MyCultureOverride : IDisposable
{
  CultureInfo prevCulture = null, prevUICulture = null;
    public static CultureInfo cultureOverride = null;
    public MyCultureOverride()
  {
    if (cultureOverride != null)
    {
      prevCulture = Thread.CurrentThread.CurrentCulture;
      prevUICulture = Thread.CurrentThread.CurrentUICulture;
        Thread.CurrentThread.CurrentCulture = cultureOverride;
      Thread.CurrentThread.CurrentUICulture = cultureOverride;
    }
  }
    public void Dispose()
  {
    if (prevCulture != null && prevUICulture != null)
    {
      Thread.CurrentThread.CurrentCulture = prevCulture;
      Thread.CurrentThread.CurrentUICulture = prevUICulture;
    }
  }
}
In the IExternalApplication’s Initialize() function set the culture you want to use. E.g.:
public void Initialize()
{
  MyCultureOverride.cultureOverride =
    CultureInfo.CreateSpecificCulture("fr-CA");
}
And whenever you want to use your own resources, just use an instance of the above class:
using (new MyCultureOverride())
{
  Autodesk.AutoCAD.ApplicationServices.
    Application.ShowModalWindow(new WindowTest());
}
A colleague pointed out the following article, which seems to suggest that I may be misusing IDisposable in the above sample code, and also provided a very nice alternative, a better solution:
using System;
using System.Globalization;
using System.Threading;
  namespace CultureOverride
{
  class MyCultureOverride
  {
    CultureInfo prevCulture, prevUICulture;
      internal static readonly CultureInfo CultureOverride =
      CultureInfo.CreateSpecificCulture("fr-CA");
      MyCultureOverride()
    {
      if (CultureOverride != null)
      {
        prevCulture = Thread.CurrentThread.CurrentCulture;
        prevUICulture = Thread.CurrentThread.CurrentUICulture;
          Thread.CurrentThread.CurrentCulture = CultureOverride;
        Thread.CurrentThread.CurrentUICulture = CultureOverride;
      }
    }
      void Restore()
    {
      if (prevCulture != null && prevUICulture != null)
      {
        Thread.CurrentThread.CurrentCulture = prevCulture;
        Thread.CurrentThread.CurrentUICulture = prevUICulture;
      }
    }
      public static void Use(Action useAction)
    {
      if (useAction == null)
        throw new ArgumentNullException("useAction");
        var cultureOverride = new MyCultureOverride();
      try
      {
        useAction();
      }
      finally
      {
        cultureOverride.Restore();
      }
    }
  }
    class Program
  {
    static void Main(string[] args)
    {
      Console.WriteLine(
        Thread.CurrentThread.CurrentCulture.ToString());
      MyCultureOverride.Use(() =>
      {
        Console.Write("with MyCultureOverride() active: ");
        Console.WriteLine(
          Thread.CurrentThread.CurrentCulture.ToString());
        Console.WriteLine();
      });
        Console.ReadKey();
    }
  }
}

