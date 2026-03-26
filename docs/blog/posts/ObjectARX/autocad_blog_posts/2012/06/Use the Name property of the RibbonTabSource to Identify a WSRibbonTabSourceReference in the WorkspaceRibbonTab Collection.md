---
title: "Use the Name property of the RibbonTabSource to Identify a WSRibbonTabSourceReference in the WorkspaceRibbonTab Collection"
date: 2012-06-01
categories:
  - AutoCAD .NET
tags:
  - AutoCAD
  - C#
description: "If you need to remove an existing tab from workspace tabs using the name of the tab, you can iterate the RibbonTabSource elements and get the Eleme..."
author: Autodesk
---
# Use the Name property of the RibbonTabSource to Identify a WSRibbonTabSourceReference in the WorkspaceRibbonTab Collection

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/use-the-name-property-of-the-ribbontabsource-to-identify-a-wsribbontabsourcereference-in-the-workspaceribbontab-collection.html

## 文章内容

By Wayne Brill
If you need to remove an existing tab from workspace tabs using the name of the tab, you can iterate the RibbonTabSource elements and get the ElementID from the RibbonTabSource. (The RibbonTabSource class has a name property) The ElementID will be the TabId of the WSRibbonTabSourceReference. Below is the pertinent code from the AutoCAD 2013 C# project. (_TestFindWithRibbonTab) The command "DELTAB" finds the Home 2D Tab and removes it from a workspace.
Download _Test_FindWithRibbonTab
Note: Keep in mind that it could be possible that there is more than one RibbonTabSource with the same name. (ElementID and TabId are unique in a menu group however)
[CommandMethod("DELTAB")]
public void delTab()
{
      WSRibbonRoot wrkSpaceRibbonRoot = null;
    WorkspaceRibbonTabCollection
              wsRibbonTabCollection = null;
      Editor ed =
        Autodesk.AutoCAD.ApplicationServices.
                 Application.DocumentManager.
                    MdiActiveDocument.Editor;
      try
    {
        WorkspaceCollection WsCollect =
                                cs.Workspaces;
        if ((WsCollect.Count <= 0))
        {
            ed.WriteMessage
    ("Failed to Get the WorkspaceCollection\n");
            return;
        }
          string strWrkSpaceName = "Acme Workspace";
          // If the workspace doesnot exist
        if (-1 == cs.Workspaces.
            IndexOfWorkspaceName(strWrkSpaceName))
        {
            // Create the workspace
            Workspace nwWs = new Workspace
                            (cs, strWrkSpaceName);
            wrkSpaceRibbonRoot =
                         nwWs.WorkspaceRibbonRoot;
        }
        else
        {
            for (int i = 0; i < WsCollect.Count; i++)
            {
                // If name of workspace is
                // "Acme Workspace" then get
                // the WSRibbonRoot
                if (WsCollect[i].Name ==
                                     strWrkSpaceName)
                {
                   wrkSpaceRibbonRoot =
                    WsCollect[i].WorkspaceRibbonRoot;
                   break;
                }
            }
        }
        //Get the Tabcollection in the
        // Acme Workspace
        wsRibbonTabCollection =
                   wrkSpaceRibbonRoot.WorkspaceTabs;
        if (wsRibbonTabCollection.Count <= 0)
        {
            ed.WriteMessage
     ("Acme Workspace does not contain any Tabs\n");
            return;
        }
          RibbonRoot ribbonRoot =
                      cs.MenuGroup.RibbonRoot;
        RibbonTabSourceCollection tabs = null;
        tabs = ribbonRoot.RibbonTabSources;
        // Change this to the name of the
        // tab to be removed
        string strRibTabSrcName = "Home - 2D";
        string strRibTabSrcTabId = null;
          foreach (RibbonTabSource ribTabSrc in tabs)
        {
              if (ribTabSrc.Name != null)
            {
                if (ribTabSrc.Name.ToString() ==
                                   strRibTabSrcName)
                {
                    strRibTabSrcTabId =
                     ribTabSrc.ElementID.ToString();
                    break;
                }
            }
        }
          foreach (WSRibbonTabSourceReference wsTabRef
                             in wsRibbonTabCollection)
        {
            if (wsTabRef.TabId.ToString() ==
                                   strRibTabSrcTabId)
            {
                wsRibbonTabCollection.Remove
                                          (wsTabRef);
                break;
            }
        }
        saveCui();
    }
    catch (System.Exception ex)
    {
        ed.WriteMessage(ex.ToString());
    }
}
  Note: If you are debugging the ribbon may be not shown the next time you start AutoCAD. (Run the RIBBON command).

