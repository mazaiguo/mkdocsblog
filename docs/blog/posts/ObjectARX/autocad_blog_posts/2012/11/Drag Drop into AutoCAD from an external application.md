---
title: "Drag Drop into AutoCAD from an external application"
date: 2012-11-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "If you have a WinForm application with a ListBox displaying the drawing file paths and you wish to perform a drag and drop of those ListBox items i..."
author: Autodesk
---
# Drag Drop into AutoCAD from an external application

发布日期: 2012-11-01

原始链接: https://adndevblog.typepad.com/autocad/2012/11/drag-drop-into-autocad-from-an-external-application.html

## 文章内容

If you have a WinForm application with a ListBox displaying the drawing file paths and you wish to perform a drag and drop of those ListBox items into AutoCAD, then here is a code snippet to ensure that AutoCAD takes appropriate action on those dropped items.
Step 1)
Handle the MouseMove event of the ListBox. As an example, if the ListBox is named "fileNamesListBox" then you would add the event handler as :
this.fileNamesListBox.MouseMove
    += new System.Windows.Forms.MouseEventHandler(this.fileNamesListBox_MouseMove);
Step 2)
Inside the MouseMove event handler of the ListBox, call the DoDragDrop with the appropriate parameters. In this case the list of drawing file paths that were selected in the ListBox.
private void fileNamesListBox_MouseMove(object sender, MouseEventArgs e)
{
    if (System.Windows.Forms.Control.MouseButtons
                    == System.Windows.Forms.MouseButtons.Left)
    {
        System.Windows.Forms.DataObject myDataObject
                        = new System.Windows.Forms.DataObject();
          System.Collections.Specialized.StringCollection dwgFileNames
            = new System.Collections.Specialized.StringCollection();
          foreach (Object so in fileNamesListBox.SelectedItems)
        {
            dwgFileNames.Add(so.ToString());
        }
          if (dwgFileNames.Count > 0)
        {
            myDataObject.SetFileDropList(dwgFileNames);
              System.Windows.Forms.DragDropEffects dropEffect
                = fileNamesListBox.DoDragDrop
                            (
                                myDataObject,
                                System.Windows.Forms.DragDropEffects.Copy
                            );
        }
    }
}
If you now select multiple items (drawing file paths) from the ListBox and drop it inside the AutoCAD command window, the drawings from those file paths should get opened in the AutoCAD Editor.

## 评论

**内容**: Joseba said...
I need to capture files dragged into AutoCAD document.
I can do it with some file extensions (.png, .txt) using de AcadApplication.BeginFileDrop event.
In other cases, the file is inserted as an OLE Object, and the event is not fired.
Is there any way for capturing files being dragged into AutoCAD (i need to capture it depending on file extension)?
Reply
08/07/2013 at 01:12 AM

---
**内容**: Balaji said in reply to Joseba...
Hi Joseba,
You may be interested in having a look at the drag-drop sample that was part of ObjectARX 2004.
I had earlier migrated this sample to work in AutoCAD 2011 and here is the link to download that :
https://www.dropbox.com/s/el4yd94th4xjf7u/arxdd.zip
In this sample, when you drop a word document, you get an option to list the dropped files instead of embedding them as OLE.
Hope this sample helps.
Regards,
Balaji
Reply
08/07/2013 at 05:13 AM

---
**内容**: Balaji said...
Hi Joseba,
Sorry, I do not find a .Net API to do that.
In ObjectARX, you can register a custom drop target using the "acedRegisterCustomDropTarget" method. Please note that there can only be one drop target registered with AutoCAD and so registering your custom drop target will affect AutoCAD's default drag-drop behavior.
On creating a custom drop target, this blog post might help :
http://adndevblog.typepad.com/autocad/2013/02/override-drag-drop-behavior.html
Reply
08/07/2013 at 04:21 AM

---
**内容**: alexb said in reply to Balaji...
Hi Balaji,
Can the custom drop target be registered and un-registered at will (thus restoring AutoCAD default)?
Would it be possible to drag-and-drop from an out of process C# application, into the OARX custom drop target?
I would like to d-and-d text from the external app and use it in the OARX running inside Acad.
Thanks
alex
Reply
01/02/2014 at 09:55 PM

---
**内容**: Joseba said...
Thanks for your help, I'll take a look to the sample posted. It seems a little bit 'dangerous' to override the default drag-drop behavior, but it can be usefull.
Thanks
Reply
08/07/2013 at 11:39 PM

---
