---
title: "Extend the AutoCAD Help menu on the window title bar"
date: 2012-10-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "I would like to add some menu items to the Help menu on the AutoCAD window title bar. Is there a way to do this?"
author: Autodesk
---
# Extend the AutoCAD Help menu on the window title bar

发布日期: 2012-10-01

原始链接: https://adndevblog.typepad.com/autocad/2012/10/extend-the-autocad-help-menu-on-the-window-title-bar.html

## 文章内容

By Philippe Leefsma
Q:
I would like to add some menu items to the Help menu on the AutoCAD window title bar. Is there a way to do this?
A:
There are two ways to do this:
1) Through the registry on a per profile basis:

You can add a registry key for each of your menu item under the "Help Button" AutoCAD registry key and then populate them with information similar to the example below. The "Help Button" Key will not exist by default so you may need to add it. All of the entries are strings. (With regedit use New > "String Value")

[HKEY_CURRENT_USER\Software\Autodesk\AutoCAD\R19.0\ACAD-8001:409\Profiles\<<Unnamed Profile>>\Help Button\MyHelp]

"Text"="Test Help"
"InsertBefore"="AcHelpAbout"
"Command"="_LINE"
"Separator"="After"
Note: "Command" is interpreted as a Help Topic, not an actual AutoCAD "command", so "_LINE" will not start the line command, but will display the LINE help topic instead. You can use acedSetFunHelp() to associate the topic with a specific help file if you wish.
"InsertBefore" requires the id of the menu item that should follow your item. E.g. it is "AcHelpAbout" for "ABOUT".
  2) Programmatically, using the Ribbon Runtime API
  public class MyCommandHandler : System.Windows.Input.ICommand
{
    public bool CanExecute(object parameter)
    {
        return true;
    }
      public event EventHandler CanExecuteChanged;
      public void Execute(object parameter)
    {
        Document doc = Application.DocumentManager.MdiActiveDocument;
        Editor ed = doc.Editor;
          ed.WriteMessage("\nMy Help Item got clicked!");
    }
}
  [CommandMethod("AddMyHelpMenuItem")]
static public void AddMyHelpMenuItem()
{
    RibbonMenuItem helpItem = new Autodesk.Windows.RibbonMenuItem();
    helpItem.Text = "My Help Item";
    helpItem.CommandHandler = new MyCommandHandler();
      RibbonMenuButton helpButton = ComponentManager.HelpButton;
    helpButton.Items.Insert(0, helpItem);
}

## 评论

**内容**: Andrey Bushman (@AndreyBushman) said...
Hi Philippe,
Windows 8 x64 Rus;
AutoCAD 2013 x64 Enu SP 1.1;
I wrote such REG-file:

Windows Registry Editor Version 5.00
[HKEY_CURRENT_USER\Software\Autodesk\AutoCAD\R19.0\ACAD-B001:409\Profiles\<>\Help Button\MyHelp]
"Text"="Test Help"
"InsertBefore"="AcHelpAbout"
"Command"="_LINE"
"Separator"="After"

I run it, but nothing happens: new item on Help menu not appear. It not working for me.
Has are you tried to run such REG file?
Regards,
Andrey
Reply
10/13/2012 at 10:40 AM

---
**内容**: Andrey Bushman (@AndreyBushman) said...
This site incorrect display registry path from my comment. It not displayed the <Unnamed Profile> fragment name.
Reply
10/13/2012 at 10:43 AM

---
**内容**: Andrey Bushman (@AndreyBushman) said...
http://img13.imageshost.ru/img/2012/10/13/image_5079aa1ee2bf5.png
Reply
10/13/2012 at 10:49 AM

---
**内容**: Andrey said...
I have tried and for Windows 7 x64 too. It is not working for me.
Reply
10/16/2012 at 01:24 AM

---
**内容**: Balaji said in reply to Andrey...
Hi Andrey,
It does work correctly on my Windows 7, 64 bit system.
The problem could be due to the difference in the registry keys for the Russian version of AutoCAD. The keys provided in the blog post correspond to the English version.
The list of the locale ID for the other language versions are listed here :
http://adn.autodesk.com/adn/servlet/devnote?siteID=4814862&id=5413196&linkID=4900509
Reply
10/24/2012 at 10:16 PM

---
**内容**: Andrey said in reply to Balaji...
Yes, you are right. Thank you, Balaji!
Reply
10/24/2012 at 11:25 PM

---
