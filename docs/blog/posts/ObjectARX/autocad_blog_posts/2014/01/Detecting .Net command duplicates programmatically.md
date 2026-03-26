---
title: "Detecting .Net command duplicates programmatically"
date: 2014-01-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
description: "Here is an annoying thing about CommandMethod attributes in AutoCAD .Net dlls: you can have two different commands that have the same name but refe..."
author: Autodesk
---
# Detecting .Net command duplicates programmatically

发布日期: 2014-01-01

原始链接: https://adndevblog.typepad.com/autocad/2014/01/detecting-net-command-duplicates-programmatically.html

## 文章内容

By Philippe Leefsma
Here is an annoying thing about CommandMethod attributes in AutoCAD .Net dlls: you can have two different commands that have the same name but refer to different .Net methods, for example consider the following code:
[CommandMethod("Test")]
public void SomeMethod()
{
    // Implementation ...
}
  [CommandMethod("Test")]
public void SomeOtherMethod()
{
    // Implementation ...
}
  What is going on if you try to netload a dll containing that code in AutoCAD? It will compile fine as there is no syntax error in the code, but you will get a frustrating error message in the command line:
  Cannot load assembly. Error details: Autodesk.AutoCAD.Runtime.Exception: eDuplicateKey at Autodesk.AutoCAD.Runtime.CommandClass.AddCommand(ICommandLineCallable ca, MethodInfo mi) at Autodesk.AutoCAD.ApplicationServices.AutoCADApplicationHolder.Initialize(Assembly assembly) at Autodesk.AutoCAD.ApplicationServices.ExtensionLoader.ProcessAssembly(Assembly assembly)
  There is no way to know which command name has caused that exception. Rather straightforward to fix it in that scenario, but in my case I work with a .Net dll that contains hundreds of commands split across dozen of files, so when I quickly cut and paste some code to test it, I can end up with duplicate commands which are hard to find.
  A solution to that can be to use .Net reflection capabilities to find out the duplicates. This is what is doing the following piece of code: you need to run it from a separate .Net dll and load the dll that contains the duplicates using FindCmdDuplicates (path):
  [CommandMethod("FindCmdDuplicates")]
public void FindCmdDuplicatesCmd()
{
    string asmPath = SelectAssembly();
      if (asmPath == null)
        return;
      FindCmdDuplicates(asmPath);
}
  private string SelectAssembly()
{
    System.Windows.Forms.OpenFileDialog dlg =
        new System.Windows.Forms.OpenFileDialog();
      dlg.Title = "Load Assembly File";
      dlg.InitialDirectory = Environment.GetFolderPath(
        Environment.SpecialFolder.Desktop);
      dlg.Filter = ".Net Assembly (*.dll)|*.dll";
    dlg.FilterIndex = 1;
    dlg.RestoreDirectory = true;
      while (dlg.ShowDialog() == System.Windows.Forms.DialogResult.OK)
    {
        try
        {
            AssemblyName asmName =
                AssemblyName.GetAssemblyName(dlg.FileName);
              return dlg.FileName;
        }
        catch (BadImageFormatException ex)
        {
            System.Windows.Forms.MessageBox.Show(
                "Sorry the file is not a valid .Net assembly...",
                "Invalid Assembly",
                System.Windows.Forms.MessageBoxButtons.OK,
                System.Windows.Forms.MessageBoxIcon.Error);
        }
    }
      return null;
}
  public void FindCmdDuplicates(string asmPath)
{
    Dictionary<string, List<MethodInfo>> map =
        new Dictionary<string, List<MethodInfo>>();
      Assembly asm = Assembly.LoadFile(asmPath);
      Type[] expTypes = asm.GetTypes();
      foreach (Type type in expTypes)
    {
        MethodInfo[] methods = type.GetMethods();
          foreach (MethodInfo method in methods)
        {
            CommandMethodAttribute attribute =
                GetCommandMethodAttribute(method);
              if (attribute == null)
                continue;
              if (!map.ContainsKey(attribute.GlobalName))
            {
                var methodInfo = new List<MethodInfo>();
                                        map.Add(attribute.GlobalName, methodInfo);
            }
              map[attribute.GlobalName].Add(method);
        }
    }
      Document doc = Application.DocumentManager.MdiActiveDocument;
    Editor ed = doc.Editor;
      foreach (var keyValuePair in map)
    {
        if (keyValuePair.Value.Count > 1)
        {
            ed.WriteMessage(
                "\nDuplicate Attribute: " + keyValuePair.Key);
              foreach (var method in keyValuePair.Value)
            {
                ed.WriteMessage(
                    "\n – Method: " + method.Name);               
            }
        }
    }
}
  public CommandMethodAttribute GetCommandMethodAttribute(
        MethodInfo method)
{
    object[] attributes = method.GetCustomAttributes(true);
      foreach (object attribute in attributes)
    {
        if (attribute is CommandMethodAttribute)
        {
            return attribute as CommandMethodAttribute;
        }
    }
      return null;
}

