---
title: "Solution for many errors when debugging my first plug-in with VB.net Express 2010"
date: 2012-03-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - Plugin
description: "If you are new to programming and AutoCAD .net plug-in development, you will want to check the“My First AutoCAD Plug-in”on AutoCAD Developer Center..."
author: Autodesk
---
# Solution for many errors when debugging my first plug-in with VB.net Express 2010

发布日期: 2012-03-01

原始链接: https://adndevblog.typepad.com/autocad/2012/03/solution-for-many-errors-when-debugging-my-first-plug-in-with-vbnet-express-2010.html

## 文章内容

By Daniel Du
If you are new to programming and AutoCAD .net plug-in development, you will want to check the“My First AutoCAD Plug-in”on AutoCAD Developer Center, which is a self-paced tutorial guide for a smooth introduction into the programming world. It is a "one-stop shop" learning path for users who know Autodesk products but are absolutely new to programming and are thinking about taking the plunge. In this guide, you will be working with the AutoCAD .NET Application Programming Interface (API) and the Visual Basic .NET programming language to create a ‘plug-in’ – a module that loads into AutoCAD to extend its functionality. Once you have finished this tutorial, you will understand the basics of .NET programming and how they are applied to AutoCAD.
You can create a simple AutoCAD.net plug-in template with The AutoCAD 2010-2012 .NET Wizards, it also allows you to launch AutoCAD from your debugger – something that isn’t possible through the Visual Studio Express user interface.  If you are using VB.net Express 2010, you many get many errors in Immediate Window when debugging, it does not block your debugging process, but it takes time before you can actually start debug and test working.
The error messages are similar like below:
'----Immediate Window--------------------------------------
System.Windows.Data Error: 5 : Value produced by BindingExpression is not valid for target property.; Value='<null>' BindingExpression:Path=AutomationName; DataItem='ToolBarCustomizeButton'(HashCode=44123454); target element is 'ToolBarToggleButton' (Name='mCustomizeButton'); target property is 'Name' (type 'String') 
System.Windows.Data Error: 5 : Value produced by BindingExpression is not valid for target property.; Value='<null>' BindingExpression:Path=AutomationName; DataItem='ToolBarCustomizeButton'(HashCode=44123454); target element is 'ToolBarToggleButton' (Name='mCustomizeButton'); target property is 'Name' (type 'String') 
System.Windows.Data Error: 5 : Value produced by BindingExpression is not valid for target property.; Value='<null>' BindingExpression:Path=AutomationName; DataItem='ToolBarCustomizeButton'(HashCode=44123454); target element is 'RibbonItemControl' (Name=''); target property is 'Name' (type'String') 
System.Windows.Data Error: 5 : Value produced by BindingExpression is not valid for target property.; Value='<null>' BindingExpression:Path=AutomationName; DataItem='InfoCenterTextBox'(HashCode=52380055); target element is 'RibbonItemControl' (Name=''); target property is 'Name' (type'String') 
System.Windows.Data Error: 5 : Value produced by BindingExpression is not valid for target property.; Value='<null>' BindingExpression:Path=AutomationName; DataItem='InfoCenterTextBox'(HashCode=52380055); target element is 'Button' (Name='PART_AcceptButton'); target property is 'Name'(type 'String') 
System.Windows.Data Error: 5 : Value produced by BindingExpression is not valid for target property.; Value='<null>' BindingExpression:Path=AutomationName; DataItem='WebServicesLoginButton'(HashCode=720995); target element is 'LoginButtonRibbonItemControl' (Name='mContainer'); target property is 'Name' (type 'String') 
System.Windows.Data Error: 5 : Value produced by BindingExpression is not valid for target property.; Value='<null>' BindingExpression:Path=AutomationName; DataItem='RibbonToggleButton'(HashCode=43678569); target element is 'RibbonItemControl' (Name=''); target property is 'Name' (type'String') 
System.Windows.Data Error: 5 : Value produced by BindingExpression is not valid for target property.; Value='<null>' BindingExpression:Path=AutomationName; DataItem='WebServicesLoginButton'(HashCode=720995); target element is 'WebservicesLoginButtonControl' (Name='mDropDownButton'); target property is 'Name' (type 'String') 
System.Windows.Data Error: 4 : Cannot find source for binding with reference 'RelativeSource FindAncestor,AncestorType='Autodesk.Private.Windows.ToolBars.ToolBarControl', AncestorLevel='1''.BindingExpression:Path=IsVisible; DataItem=null; target element is 'ImageControl' (Name='mImage'); target property is 'NoTarget' (type 'Object') 
System.Windows.Data Error: 4 : Cannot find source for binding with reference 'RelativeSource FindAncestor, AncestorType='Autodesk.Private.Windows.ToolBars.ToolBarControl', AncestorLevel='1''. BindingExpression:Path=IsVisible; DataItem=null; target element is 'ImageControl' (Name='mImage'); target property is 'NoTarget' (type 'Object') 
System.Windows.Data Error: 4 : Cannot find source for binding with reference 'RelativeSource FindAncestor,AncestorType='Autodesk.Private.Windows.ToolBars.ToolBarControl', AncestorLevel='1''.BindingExpression:Path=IsVisible; DataItem=null; target element is 'ImageControl' (Name='mImage'); target property is 'NoTarget' (type 'Object') 
System.Windows.Data Error: 4 : Cannot find source for binding with reference 'RelativeSource FindAncestor,AncestorType='Autodesk.Private.Windows.ToolBars.ToolBarControl', AncestorLevel='1''.BindingExpression:Path=IsVisible; DataItem=null; target element is 'ImageControl' (Name='mImage'); target property is 'NoTarget' (type 'Object') 
System.Windows.Data Error: 4 : Cannot find source for binding with reference 'RelativeSource FindAncestor,AncestorType='Autodesk.Private.Windows.ToolBars.ToolBarControl', AncestorLevel='1''.
The solution is to add <system.diagnostics> into Acad.exe.Config, which can be found in your AutoCAD installation folder. Add following section right after </runtime>:
    <system.diagnostics>
    <sources>                                                                                                                                                                                      
      <source name="System.Windows.Data"               
              switchName="SourceSwitch">
        <listeners>
          <remove name="Default" />
        </listeners>
      </source>
    </sources>
  </system.diagnostics>
It will look like below(I am using Civil 3D):
<configuration>
    <startup useLegacyV2RuntimeActivationPolicy="true">
        <supportedRuntime version="v4.0"/>
    </startup>
    <!--All assemblies in AutoCAD are fully trusted 
        so there's no point generating publisher evidence-->
    <runtime>
        <generatePublisherEvidence enabled="false"/>
        <assemblyBinding xmlns="urn:schemas-microsoft-com:asm.v1">          
          <probing privatePath="bin\FDO;bin;Plugins\Workflow\Activities"/>
        </assemblyBinding>
     </runtime>
        
    <system.diagnostics>
    <sources>                                                                                                                                                                                      
      <source name="System.Windows.Data"               
              switchName="SourceSwitch">
        <listeners>
          <remove name="Default" />
        </listeners>
      </source>
    </sources>
  </system.diagnostics>

</configuration>
This solution applies to AutoCAD vertical products as well, including Map 3D and Civil 3D. Hope this helps.

