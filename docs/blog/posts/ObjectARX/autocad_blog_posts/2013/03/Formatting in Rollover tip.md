---
title: "Formatting in Rollover tip"
date: 2013-03-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Block
  - Unicode
description: "When displaying a rollover tip, AutoCAD uses the "additionalTooltipString" provided by us using the "monitorInputPoint" method to create a "TextBlo..."
author: Autodesk
---
# Formatting in Rollover tip

发布日期: 2013-03-01

原始链接: https://adndevblog.typepad.com/autocad/2013/03/formatting-in-rollover-tip.html

## 文章内容

By Balaji Ramamoorthy
When displaying a rollover tip, AutoCAD uses the "additionalTooltipString" provided by us using the "monitorInputPoint" method to create a "TextBlock" WPF element. Assuming that the additionalTooltipString provided by us was "Hello", the textblock gets created as :
<TextBlock TextWrapping="Wrap"><![CDATA[  Hello  ]]</TextBlock>
Here is a sample tooltip string to insert formatting tags such as Bold and Italic. This will work when the ROLLOVERTIPS system variable is set to "1".
additionalTooltipString
        = ACRX_T(   "Iam]]>
                    <LineBreak/>
                    <Bold>BOLD</Bold>
                    <LineBreak/>
                <![CDATA[Iam]]>
                    <LineBreak/>
                    <Italic>Italic</Italic>
                    <LineBreak/>
                <![CDATA[Iam Normal"
                );
To try this using the AutoCAD .Net API, here is a sample code snippet :
void IExtensionApplication.Initialize()
{
    Document activeDoc = Application.DocumentManager.MdiActiveDocument;
    activeDoc.Editor.PointMonitor += new PointMonitorEventHandler(Editor_PointMonitor);
}
  void Editor_PointMonitor(object sender, PointMonitorEventArgs e)
{
    if (e.Context.GetPickedEntities().Length > 0)
    {
        e.AppendToolTipText(
                        "Iam]]><LineBreak/>
                        <Bold>BOLD</Bold><LineBreak/>
                        <![CDATA[Iam]]><LineBreak/>
                        <Italic>Italic</Italic><LineBreak/>
                        <![CDATA[Iam Normal");
    }
}
  void IExtensionApplication.Terminate()
{
    Document activeDoc
                = Application.DocumentManager.MdiActiveDocument;
    if (activeDoc != null)
    {
        activeDoc.Editor.PointMonitor
            -= new PointMonitorEventHandler(Editor_PointMonitor);
    }
}
The rollover tooltip will then appear as :

## 评论

**内容**: Mario Minati said...
This is great, I was waiting for that :-)
But it is not working with .Net the same way. Using "AppendToolTipText" just shows the above XAML-Code.
Is there a way to achieve this with .Net?
Reply
03/23/2013 at 07:51 AM

---
**内容**: Balaji said in reply to Mario Minati...
Hi Mario,
I tried the code from a .Net PointMonitor event handler in AutoCAD 2013. It worked ok when the mouse was hovering over an entity and the text got displayed as it is when I did not hover over an entity.
So a check for the "e.Context.GetKeyPointEntities" before using the "AppendToolTipText" should help.
Regards,
Balaji
Reply
03/25/2013 at 05:15 AM

---
**内容**: HJohn said...
Hi Balaji, I think that customazing the tooltip is a great way to display additional info when hovering over entities. I have tried to implement a PointMonitorEventHandler, when it works it works however it after a while it crashes AC. It is crashing on the call to the AppendToolTipText method and I have no idea why. I am using AC 2012 Mech. on 64Bit Windows 7. Do you have any recomendations. I am using vbCrLf instead of \n, because it doesn't work. I posted the code on the .net customization forum.
msg = String.Format("Block Name: {0}", BlkName) & vbCrLf
msg = msg & String.Format("Block Inserts: {0}", Total) & vbCrLf
e.AppendToolTipText(msg)
Reply
09/24/2013 at 12:17 PM

---
**内容**: Balaji said in reply to HJohn...
Hi John,
I have found your forum post. I will try the sample code and will update you.
Regards,
Balaji
Reply
09/25/2013 at 06:55 AM

---
**内容**: Craig said...
Nice tip Balaji. Thanks.
Reply
10/08/2013 at 04:18 AM

---
**内容**: Balaji said in reply to Craig...
Thanks Craig :)
Reply
10/08/2013 at 11:20 PM

---
**内容**: Lucas said...
There is an issue with this when it comes to multiple entities being hovered over. When this happens AutoCAD decides to show the old drafting tool tip and shows the xaml in the tool tip. I was wondering if there is anyway to detect that this will happen in this situation?
Reply
10/14/2013 at 01:37 PM

---
**内容**: Balaji said in reply to Lucas...
Hi Lucas,
I will try it and get back to you. Thanks for letting me know about this limitation.
Regards,
Balaji
Reply
10/17/2013 at 12:08 PM

---
**内容**: f_schuepany@yahoo.de said in reply to Balaji...
Hello Balaji,
i have the same problem as Lucas, ist there a Workaround?
Reply
02/14/2014 at 03:08 PM

---
**内容**: Balaji said in reply to f_schuepany@yahoo.de...
Hi Ferdinand,
Sorry, We do not yet (as of AutoCAD 2014) have a way to format the tooltips without relying on internal API or workarounds. The sample code explained in this blog post is a woraround and has limitations and does not work in ACA and some other verticals. Unfortunately, I do not see a way to resolve this when hovering over multiple entities.
An alternate approach to show a formatted rollover tool tip, is to use the "Autodesk.Windows.ComponentManager.ToolTipOpened" event handler and replace the Tooltip content with your own WPF control. This approach uses the internal API but I hope this helps. I haven't tried this, but this seems to work ok as suggested by Keith Brown in this forum post :
http://forums.autodesk.com/t5/NET/Formatting-of-Rollover-ToolTips-in-AutoCAD-MEP-and-AutoCAD/m-p/4608959#M37610
You can find some clues on this approach here :
http://through-the-interface.typepad.com/through_the_interface/2011/07/modifying-autocad-tooltips-using-net.html
Hope this helps.
Regards,
Balaji
Reply
02/16/2014 at 08:07 PM

---
