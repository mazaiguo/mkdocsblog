---
title: "Suppressing DataBinding ‘error’ messages in the Visual Studio output window"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Plugin
description: "There’s a thread on the Autodesk discussion forums about the ‘error’ messages displayed in the Visual Studio output window when you launch AutoCAD ..."
author: Autodesk
---
# Suppressing DataBinding ‘error’ messages in the Visual Studio output window

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/suppressing-databinding-error-messages-in-the-visual-studio-output-window.html

## 文章内容

By Stephen Preston
There’s a thread on the Autodesk discussion forums about the ‘error’ messages displayed in the Visual Studio output window when you launch AutoCAD from the debugger. These messages look like this:
System.Windows.Data Error: 5 : Value produced by BindingExpression is not valid for target property.; Value='<null>' BindingExpression:Path=AutomationName; DataItem='ToolBarCustomizeButton' (HashCode=44123454); target element is 'ToolBarToggleButton' (Name='mCustomizeButton'); target property is 'Name' (type 'String')
The messages are disconcerting because they makesit look like there’s something horribly wrong with your project. Don’t panic – these messages don’t mean you’ve got a problem. They’re just a result of how Microsoft handles WPF behind the scenes, and have been appearing in the output windows of AutoCAD plug-in developers around the world since the AutoCAD 2009 release was launched with a WPF ribbonbar. You can safely ignore them.
If you want to go one step further and remove them, you can edit your acad.exe.config file (located in your AutoCAD installation folder) to add the lines highlighted in yellow below:
<configuration>
  <startup useLegacyV2RuntimeActivationPolicy="true">
    <supportedRuntime version="v4.0"/>
  </startup>
<!--All assemblies in AutoCAD are fully trusted so there's no point generating publisher evidence-->
   <runtime>       
  <generatePublisherEvidence enabled="false"/>   
   </runtime>
  <system.diagnostics>
    <sources>
      <source name="System.Windows.Data" switchName="SourceSwitch">
        <listeners>
          <remove name="Default" />
        </listeners>
      </source>
    </sources>
  </system.diagnostics>
</configuration>
While we’re at it, you also don’t have to worry about the ‘First Chance Exception’ errors you also see in the debugger output window when AutoCAD starts. These just indicate an exception has been thrown for some reason or other. An exception being thrown isn’t a big deal – the problem only comes if the are not handled.

## 评论

**内容**: Loic Jourdan said...
Hi Preston,
Haven't you stolen this trick to Kean Walmsley?
(http://through-the-interface.typepad.com/through_the_interface/2011/03/making-autocad-less-noisy-when-debugging.html)
Just kidding, thank you, these log messages were a real pain.
Reply
07/27/2012 at 12:02 AM

---
**内容**: Madhukar Moogala said in reply to Loic Jourdan...
Oops! Naughty me. I'm not guilty of plagiarism - I'm guilty of the worse crime of not searching Kean's blog before researching elsewhere :-(.
BTW Thanks to George Varghese from our SWD team for giving me this tip :-).
Reply
07/27/2012 at 08:51 AM

---
