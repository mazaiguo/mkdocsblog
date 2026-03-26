---
title: "How to ensure your Ribbon runtime items remain visible ?"
date: 2014-01-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - CUI
description: "The AutoCAD ribbon runtime API is pretty handy to customize the user interface. However changes made through this API are not persistent. That mean..."
author: Autodesk
---
# How to ensure your Ribbon runtime items remain visible ?

发布日期: 2014-01-01

原始链接: https://adndevblog.typepad.com/autocad/2014/01/how-to-ensure-your-ribbon-runtime-items-remain-visible.html

## 文章内容

By Philippe Leefsma
The AutoCAD ribbon runtime API is pretty handy to customize the user interface. However changes made through this API are not persistent. That means there are situations where you need some extra code to make sure your Ribbon items will still be there: that’s typically the case after a workspace switch or when changes occur due to CUI or QUICKCUI commands.
Here is a suggestion on how to handle those scenario and ensure your Ribbons remain visible:
[CommandMethod("SimpleButton")]
public void SimpleButton()
{
    Autodesk.AutoCAD.ApplicationServices.Application.
        SystemVariableChanged +=
        new Autodesk.AutoCAD.ApplicationServices.
            SystemVariableChangedEventHandler(
            Application_SystemVariableChanged);
      Autodesk.AutoCAD.ApplicationServices.Application.
        DocumentManager.MdiActiveDocument.CommandEnded +=
        new CommandEventHandler(MdiActiveDocument_CommandEnded);
      CreateSimpleButton();
}
  void MdiActiveDocument_CommandEnded(
    object sender, CommandEventArgs e)
{
    if (e.GlobalCommandName == "QUICKCUI" ||
        e.GlobalCommandName == "CUI")
    {
        Autodesk.AutoCAD.ApplicationServices.Application.Idle +=
            new EventHandler(Application_Idle);
    }
}
  void Application_Idle(object sender, EventArgs e)
{
    if (Autodesk.Windows.ComponentManager.Ribbon != null)
    {
        Autodesk.AutoCAD.ApplicationServices.Application.Idle -=
            new EventHandler(Application_Idle);
          CreateSimpleButton();
    }
}
  void Application_SystemVariableChanged(
    object sender,
    Autodesk.AutoCAD.ApplicationServices.
    SystemVariableChangedEventArgs e)
{
    if (e.Name == "WSCURRENT")
    {
        string cmdNames =
            (string)Autodesk.AutoCAD.ApplicationServices.Application.
                GetSystemVariable(
                    "CMDNAMES");
                        // if the QUICKCUI or CUI command is active, returns
        if (cmdNames.ToUpper().IndexOf("QUICKCUI") >= 0 ||
            cmdNames.ToUpper().IndexOf("CUI") >= 0)
            return;
                        CreateSimpleButton();
    }
}
  public void CreateSimpleButton()
{
    Autodesk.Windows.RibbonControl ribbonControl =
        Autodesk.Windows.ComponentManager.Ribbon;
      RibbonTab Tab = new RibbonTab();
    Tab.Title = "Test Ribbon";
    Tab.Id = "TESTRIBBON_TAB_ID";
      ribbonControl.Tabs.Add(Tab);
      Autodesk.Windows.RibbonPanelSource srcPanel =
        new RibbonPanelSource();
    srcPanel.Title = "Panel1";
      RibbonPanel Panel = new RibbonPanel();
    Panel.Source = srcPanel;
    Tab.Panels.Add(Panel);
      Autodesk.Windows.RibbonButton button1 = new RibbonButton();
    button1.Text = "Button";
    button1.Size = RibbonItemSize.Large;
    button1.Image =
        getBitmap(Properties.Resources.Apps, 16, 16);
    button1.LargeImage =
        getBitmap(Properties.Resources.Apps, 32, 32);
    button1.ShowText = true;
    button1.CommandParameter = "._LINE ";
    button1.CommandHandler = new SimpleButtonCmdHandler();
      srcPanel.Items.Add(button1);
                Tab.IsActive = true;
}
  //Use: getBitmap(Properties.Resources.a_large);
BitmapImage getBitmap(Bitmap bitmap, int height, int width)
{
    MemoryStream stream = new MemoryStream();
    bitmap.Save(stream, System.Drawing.Imaging.ImageFormat.Png);
      BitmapImage bmp = new BitmapImage();
    bmp.BeginInit();
    bmp.StreamSource = new MemoryStream(stream.ToArray());
    bmp.DecodePixelHeight = height;
    bmp.DecodePixelWidth = width;
    bmp.EndInit();
      return bmp;
}
  public class SimpleButtonCmdHandler :
    System.Windows.Input.ICommand
{
    public bool CanExecute(object parameter)
    {
        return true;
    }
      public event EventHandler CanExecuteChanged;
      public void Execute(object parameter)
    {
        if (parameter is RibbonButton)
        {
            // builds escape sequence to cancel active commands
            string esc = "";
              string cmds =
            (string)Autodesk.AutoCAD.ApplicationServices.Application.
                GetSystemVariable("CMDNAMES");
              if (cmds.Length > 0)
            {
                int cmdNum = cmds.Split(new char[] { '\'' }).Length;
                  for (int i = 0; i < cmdNum; i++)
                    esc += '\x03';
            }
              RibbonButton button = parameter as RibbonButton;
              Document doc =
                Autodesk.AutoCAD.ApplicationServices.Application.
                    DocumentManager.MdiActiveDocument;
              doc.SendStringToExecute(esc + button.CommandParameter,
                true, false, false);
        }
    }
}

## 评论

**内容**: Alok said...
Hi Philippe,
Is there an equivalent sample of this that works with the ACAD 2015 api?
Thanks!
Reply
02/27/2015 at 01:46 PM

---
**内容**: Philippe said in reply to Alok...
Hi Alok,
Here is a vb.net sample that was working on 2015...
Public Sub CreateSimpleButton()
Dim ribbonControl As RibbonControl =
ComponentManager.Ribbon
Dim tab As RibbonTab = New RibbonTab()
tab.Title = "Test Ribbon"
tab.Id = "ADN_TAB_ID"
ribbonControl.Tabs.Add(tab)
Dim srcPanel As RibbonPanelSource =
New RibbonPanelSource()
srcPanel.Title = "Panel1"
Dim Panel As RibbonPanel = New RibbonPanel()
Panel.Source = srcPanel
tab.Panels.Add(Panel)
Dim button1 As Autodesk.Windows.RibbonButton =
New RibbonButton()
button1.Text = "Nested" + vbCr + "Explode"
button1.Size = RibbonItemSize.Large
'button1.Image = getBitmap(My.Resources.explode, 16, 16)
'button1.LargeImage = getBitmap(My.Resources.explode, 32, 32)
button1.ShowText = True
button1.CommandParameter = "EXPLODE "
button1.CommandHandler = New SimpleButtonCmdHandler()
srcPanel.Items.Add(button1)
tab.IsActive = False
End Sub
Function getBitmap(bitmap As Bitmap,
height As Integer,
width As Integer) As BitmapImage
Dim stream As MemoryStream = New MemoryStream()
bitmap.Save(stream,
System.Drawing.Imaging.ImageFormat.Png)
Dim bmp As BitmapImage = New BitmapImage()
bmp.BeginInit()
bmp.StreamSource = New MemoryStream(stream.ToArray())
bmp.DecodePixelHeight = height
bmp.DecodePixelWidth = width
bmp.EndInit()
Return bmp
End Function
Public Class SimpleButtonCmdHandler
Implements System.Windows.Input.ICommand
Public Function CanExecute(parameter As Object) As Boolean _
Implements Windows.Input.ICommand.CanExecute
Return True
End Function
Public Event CanExecuteChanged(sender As Object, e As EventArgs) _
Implements Windows.Input.ICommand.CanExecuteChanged
Public Sub Execute(parameter As Object) _
Implements Windows.Input.ICommand.Execute
Dim esc As String = ""
Dim cmds As String =
Application.GetSystemVariable("CMDNAMES")
If cmds.Length > 0 Then
Dim separator As Char() = {"""'"}
Dim cmdNum As Integer =
cmds.Split(separator).Length
For i As Integer = 0 To cmdNum
esc = esc + Chr(27)
Next
End If
Dim button As RibbonButton = parameter
Dim doc As Document = Application.
DocumentManager.MdiActiveDocument
doc.SendStringToExecute(
esc + button.CommandParameter,
True, False, False)
End Sub
End Class

Public Sub LoadRibbonButton()
If Not Autodesk.Windows.ComponentManager.Ribbon Is Nothing Then
CreateSimpleButton()
Else
AddHandler Autodesk.Windows.ComponentManager.ItemInitialized,
AddressOf ComponentManager_ItemInitialized
AddHandler Application.SystemVariableChanged,
AddressOf Application_SystemVariableChanged
End If
End Sub
Sub Application_SystemVariableChanged(
sender As Object,
e As Autodesk.AutoCAD.ApplicationServices.
SystemVariableChangedEventArgs)
If e.Name = "WSCURRENT" Then
Dim cmdNames As String =
Application.GetSystemVariable("CMDNAMES")
'' if the QUICKCUI or CUI command is active, returns
If (cmdNames.ToUpper().IndexOf("QUICKCUI") >= 0 Or
cmdNames.ToUpper().IndexOf("CUI") >= 0) Then
Return
End If
CreateSimpleButton()
End If
End Sub
Sub ComponentManager_ItemInitialized(
sender As Object,
e As RibbonItemEventArgs)
RemoveHandler Autodesk.Windows.ComponentManager.ItemInitialized,
AddressOf ComponentManager_ItemInitialized
Dim palette As RibbonPaletteSet =
RibbonServices.RibbonPaletteSet
AddHandler palette.Load,
AddressOf RibbonPaletteSet_Loaded
End Sub
Sub RibbonPaletteSet_Loaded(
sender As Object,
e As Autodesk.AutoCAD.Windows.PalettePersistEventArgs)
If Not Autodesk.Windows.ComponentManager.Ribbon Is Nothing Then
CreateSimpleButton()
Else
AddHandler Application.Idle, AddressOf Application_Idle
Dim doc = Application.DocumentManager.MdiActiveDocument
doc.SendStringToExecute("RIBBON ", True, False, False)
End If
End Sub
Sub Application_Idle(sender As Object, e As EventArgs)
If Not Autodesk.Windows.ComponentManager.Ribbon Is Nothing Then
RemoveHandler Application.Idle,
AddressOf Application_Idle
Dim ribbon = Autodesk.Windows.ComponentManager.Ribbon
Dim tab = ribbon.FindTab("ADN_TAB_ID")
If (tab Is Nothing Or Not tab.IsVisible) Then
CreateSimpleButton()
End If
End If
End Sub
End Class
Reply
03/10/2015 at 10:45 AM

---
**内容**: Health Tourism said...
This is great news! Finally, someone with some spunk is perhaps showing some interest in Dzhokhar’s innocence.
Reply
03/09/2015 at 08:03 AM

---
**内容**: Steve said...
Thank you for this post! Exactly what I needed! I had the Workspace change event in there, just not the CUI / QUICK CUI changes.
Reply
10/26/2016 at 12:03 PM

---
**内容**: JamesOneil said...
Yes, the range of the commercial roofing contractors in suffolk county
is signed for the contract. Agreement is done for the typical chain of the events for the turns for the semi-final matter for all people.
Reply
03/31/2023 at 01:40 PM

---
