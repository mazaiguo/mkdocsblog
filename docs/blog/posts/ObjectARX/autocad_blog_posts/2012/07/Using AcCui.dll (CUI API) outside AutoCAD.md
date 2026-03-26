---
title: "Using AcCui.dll (CUI API) outside AutoCAD"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - CUI
description: "I'm trying to use the CUI API from an external application, but when I'm using functions like Workspaces.Clone() I get an exception. What is wrong?"
author: Autodesk
---
# Using AcCui.dll (CUI API) outside AutoCAD

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/using-accuidll-cui-api-outside-autocad.html

## 文章内容

By Adam Nagy
I'm trying to use the CUI API from an external application, but when I'm using functions like Workspaces.Clone() I get an exception. What is wrong?
Solution
At the moment you need to create a class that implements the IHostServices interface and set that to CustomizationSection.HostServices in order to use AcCui.dll outside AutoCAD.
Note: the process is planned to be simplified in a future release, so that you do not even have to implement this interface anymore.
Because of the dependency on AcCui.dll you need to run your exe from the AutoCAD install folder.
The below sample copies a workspace from a custom cuix file into AutoCAD's cuix file.
When testing the sample make sure that the Copy Local property of the reference to AcCui.dll is set to False and you back up acad.cuix before running the sample
using System;
using System.Collections;
using System.Windows.Forms;
using Autodesk.AutoCAD.Customization;
  namespace CuiTestExe
{
  public class MyHostServices : IHostServices
  {
    void IHostServices.DisplayMessage(string message, string title)
    {
      System.Diagnostics.Debug.WriteLine(
        "IHostServices.DisplayMessage [" + message +
        ", " + title + "]");
    }
      CustomizationSection IHostServices.EnterpriseCUIFile()
    {
      System.Diagnostics.Debug.WriteLine(
        "IHostServices.EnterpriseCUIFile");
      return null;
    }
      string IHostServices.FindFile(string fileName)
    {
      System.Diagnostics.Debug.WriteLine(
        "IHostServices.FindFile [" + fileName + "]");
      // Only needs to be implemented if you want
      // to handle relative paths
      return null;
    }
      void IHostServices.GeneratePropertyCollection(
      ObjectType ot)
    {
      System.Diagnostics.Debug.WriteLine(
        "IHostServices.GeneratePropertyCollection [" +
        ot.ToString() + "]");
    }
      System.Drawing.Bitmap IHostServices.GetCachedImage(
      string imageId, bool return_null)
    {
      System.Diagnostics.Debug.WriteLine(
        "IHostServices.GetCachedImage [" + imageId +
        ", " + return_null.ToString() + "]");
      return null;
    }
      string IHostServices.GetDieselEvalString(
      string dieselExpression)
    {
      System.Diagnostics.Debug.WriteLine(
        "IHostServices.GetDieselEvalString [" +
        dieselExpression + "]");
      return dieselExpression;
    }
      ArrayList IHostServices.GetLoadedMenuGroupNames()
    {
      System.Diagnostics.Debug.WriteLine(
        "IHostServices.GetLoadedMenuGroupNames");
      return new System.Collections.ArrayList();
    }
      void IHostServices.InsertMenuOnMenuBar(
      string menuGroupName, string alias)
    {
      System.Diagnostics.Debug.WriteLine(
        "IHostServices.InsertMenuOnMenuBar [" + menuGroupName +
        ", " + alias + "]");
    }
      bool IHostServices.IsOEM()
    {
      System.Diagnostics.Debug.WriteLine("IHostServices.IsOEM");
      return false;
    }
      int IHostServices.QueryMode()
    {
      System.Diagnostics.Debug.WriteLine("IHostServices.QueryMode");
      return 0;
    }
      string IHostServices.RegistryProductRootKey()
    {
      System.Diagnostics.Debug.WriteLine(
        "IHostServices.RegistryProductRootKey");
      return null;
    }
      void IHostServices.WriteMessage(string message)
    {
      System.Diagnostics.Debug.WriteLine(
        "IHostServices.WriteMessage [" + message + "]");
    }
  }
    public class Commands
  {
    public static void merge()
    {
      try
      {
        // Since we run this code outside AutoCAD
        CustomizationSection.HostServices = new MyHostServices();
          CustomizationSection acad_cuix = new CustomizationSection(
          @"C:\Documents and Settings\Administrator\" +
          @"Application Data\Autodesk\AutoCAD 2011\R18.1\" +
          @"enu\Support\acad.cuix");
        CustomizationSection my_cuix = new CustomizationSection(
          @"C:\Documents and Settings\Administrator\Desktop\" +
          @"mytest\new.cuix");
          // Place the first (and only) workspace in my cuix
        // after the first workspace in the acad cuix
        Workspace my_workspace = my_cuix.Workspaces[0];
        Workspace acad_workspace = acad_cuix.Workspaces[0];
          ContainerCloneAction containerClnAction =
          new ContainerCloneAction();
        // The following line throws error when this code is run in
        // an external application and HostServices is not set
        Workspace acad_new_workspace = acad_cuix.Workspaces.Clone(
          my_workspace, acad_workspace, ref containerClnAction);
          if (acad_cuix.IsModified)
        {
          acad_cuix.Save();
        }
      }
      catch (System.Exception ex)
      {
        MessageBox.Show(ex.Message, "CUI API Test");
          return;
      }
    }
      static void Main(string[] args)
    {
      merge();
    }
  }
}

## 评论

**内容**: Chris said...
"Because of the dependency on AcCui.dll you need to run your exe from the AutoCAD install folder."
not necessarily, you can use some kind of AppDomain.AssemblyResolve EventHandler to load the needed assemblies from the AutoCAD install folder.
using System;
using System.IO;
using System.Reflection;
using Autodesk.AutoCAD.Customization;
namespace AcadCuiEdit
{
namespace AcadCui
{
class AcCuiCustomize
{
AppDomain appdom;
public AcCuiCustomize()
{
appdom =
AppDomain.CurrentDomain;
appdom.AssemblyResolve +=
new ResolveEventHandler(appdom_AssemblyResolve);
}
System.Reflection.Assembly
appdom_AssemblyResolve(
object sender,
ResolveEventArgs args)
{
/*get the path where autocad is installed
* //how to resolve the path of the AutoCAD install folder is up to you.
* Hardcoded, ask the user, get it from the registry
*/
string acp = "%ACADPATH%";
//get the assembly name
string dllName = args.Name.Split(new char[] { ',' })[0] + ".dll";
try
{
return Assembly.LoadFrom(Path.Combine(acp, dllName));
}
catch
{
return null;
}
}
///
/// Calling this function will trigger the assemblyresolve event and
/// throws an exception in case resolving of the needed assemlies failed.
///
public void CreateNew()
{
CustomizationSection cs =
new CustomizationSection();
}
}
}
}
Reply
09/13/2012 at 10:34 AM

---
**内容**: Adam Nagy said...
Hi Chris,
Thanks for the comment. :)
Did you test it and it seemed to work fine?
Cheers,
Adam
Reply
09/13/2012 at 10:40 AM

---
**内容**: Chris said...
I haven't tried this with your sample but for accessing a cuix file this works fine.
Reply
09/13/2012 at 10:40 AM

---
**内容**: Adam Nagy said...
Cool :)
Reply
09/13/2012 at 10:42 AM

---
**内容**: Ben said...
Is there any reason why the two CustomizationSection objects would both be full of nulls after initialization with their respective filenames? As soon as my code begins to declare the workspaces I get common language run time error and and illegalProgramException. Everything builds without error.
Reply
05/21/2013 at 11:48 AM

---
**内容**: Adam Nagy said...
Hi Ben,
Maybe some modules cannot get loaded or something wrong with the CUIx files? Not sure.
Best might be asking on the Customization Forum and provide a bit more information and sample project, sample CUIx if needed:
http://forums.autodesk.com/t5/NET/bd-p/152
Cheers,
Adam
Reply
05/27/2013 at 04:07 PM

---
