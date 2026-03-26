---
title: "Change Profile settings from .NET"
date: 2016-02-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - AutoLISP
  - C++
description: "There are many settings which are stored in various parts of the registry folders that AutoCAD is using. Many of them you can also read and write t..."
author: Autodesk
---
# Change Profile settings from .NET

发布日期: 2016-02-01

原始链接: https://adndevblog.typepad.com/autocad/2016/02/change-profile-settings-from-net.html

## 文章内容

By Adam Nagy
There are many settings which are stored in various parts of the registry folders that AutoCAD is using. Many of them you can also read and write through getenv/setenv in LISP or acedGetEnv/acedSetEnv in ObjectARX - here is a .NET version:
http://adndevblog.typepad.com/autocad/2012/06/a-simple-alternative-to-accessing-the-com-preferences-object-in-autocad.html
If it's not an environment variable then you can use Registry API to modify the value.
Note: if the value you are interested in is a string value then you could also use the UserConfigurationManager object for read/write:
http://through-the-interface.typepad.com/through_the_interface/2008/05/storing-custom.html
As an example, let's try to toggle the state of "Enable Balloon Notification" for plotting from .NET.
If you want to find out where a given setting is stored in the Registry (if it is stored there) then you can use a tool like Process Monitor to see which property in the registry gets modified when you change the setting through the UI. In case of the plot balloon this property was set:
So now we can change it using a code like this:
using System;

using Autodesk.AutoCAD.Runtime;
using Autodesk.AutoCAD.ApplicationServices;
using Autodesk.AutoCAD.DatabaseServices;

using acApp = Autodesk.AutoCAD.ApplicationServices.Application;
using Win32 = Microsoft.Win32;

[assembly: CommandClass(typeof(SimpleDotNet.Commands))]

namespace SimpleDotNet
{
  public class Commands
  {
    [CommandMethod("ToggleDisplayPlotBubble", CommandFlags.Session)]
    public void ToggleDisplayPlotBubble()
    {
      const string sectionName = "General";
      const string propertyName = "DisplayPlotBubble";

      string productKeyName = HostApplicationServices.Current.UserRegistryProductRootKey;
      string profileName = acApp.GetSystemVariable("CPROFILE").ToString();
      using (RegistryKey genKey = Registry.CurrentUser.OpenSubKey(
        string.Format(@"{0}\Profiles\{1}\{2}", productKeyName, profileName, sectionName), true))
      {
        int displayOn = (int)genKey.GetValue(propertyName);
        displayOn = (displayOn == 0) ? 1 : 0;
        genKey.SetValue(propertyName, displayOn, Win32.RegistryValueKind.DWord);
      }
    }
  }
}

## 评论

**内容**: Alexander Rivilis said...
Hi Adam!
As far as I remember AutoCAD read changed registry variables only after it restart (next session) unlike of getenv/setenv. So it is not ideal solution.
Reply
02/13/2016 at 11:53 AM

---
**内容**: Alexander Rivilis said in reply to Alexander Rivilis...
P.S.: I've tested this code and find that AutoCAD check this variable from registry every time. So for this variable it is a quite well solution. Thanks!
Reply
02/13/2016 at 12:10 PM

---
