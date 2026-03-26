---
title: "Importing ToolPalette/ToolPaletteGroup from XTP/XPG files"
date: 2013-11-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - CUI
  - ObjectARX
  - Palette
description: "Importing ToolPalette and ToolPaletteGroup from xtp and xtg files require user interaction in AutoCAD. Here is a sample ObjectARX code to automate ..."
author: Autodesk
---
# Importing ToolPalette/ToolPaletteGroup from XTP/XPG files

发布日期: 2013-11-01

原始链接: https://adndevblog.typepad.com/autocad/2013/11/importing-toolpalettetoolpalettegroup-from-xtpxtg-files.html

## 文章内容

By Balaji Ramamoorthy
Importing ToolPalette and ToolPaletteGroup from xtp and xtg files require user interaction in AutoCAD. Here is a sample ObjectARX code to automate that. Some portion of this code retrieves information from the xtp / xtg files by accessing them as plain XML document. This code worked ok for simple xtp and xtg files that I used during my tests. It might however still need more error handling code which Iam sure you can include based on your needs.
CAcTcUiManager *pTcUiManager = AcTcUiGetManager();
CAcTcUiToolPaletteSet *pTpset = AcTcUiGetToolPaletteWindow();
  // List of xtp files to import
AcArray<AcString> xtpFiles;
xtpFiles.append(ACRX_T("C:\\Temp\\MyTP.xtp"));
  // List of xpg files to import
AcArray<AcString> xpgFiles;
xpgFiles.append(ACRX_T("C:\\Temp\\MyTPGroup.xpg"));
  // Import the ToolPalette from the xtp file
// By default the toolpalette is added to the "AllPalettesGroup"
// After importing from the xtp file, get its name
// We will need the names to move the toolpalette to the
// toolpalette groups that will be imported from xpg file.
AcArray<AcString> toolPaletteNames;
for(int xtpFileIndex =0;
        xtpFileIndex < xtpFiles.length(); xtpFileIndex++)
{
    // Get the xtp file path
    AcString xtpFilePath = xtpFiles.at(xtpFileIndex);
      if(pTcUiManager->Import(xtpFilePath))
    {
        acutPrintf(ACRX_T("\nImported %s"), xtpFilePath);
    }
      // The ToolPalette was imported, but we need to find its
    // name so we can relocate it to our ToolPaletteGroup
    // Find the name of the ToolPalette that was now imported
    // from the XTP file.
    CComPtr<IXMLDOMDocument> pXTPDoc;
    HRESULT hr = pXTPDoc.CoCreateInstance(CLSID_DOMDocument,
                                NULL, CLSCTX_INPROC_SERVER);
    if (FAILED(hr))
        return;
      CComVariant xmlSource = xtpFilePath.constPtr();
    VARIANT_BOOL varSuccess = VARIANT_FALSE;
    hr = pXTPDoc->load(xmlSource, &varSuccess);
    if (FAILED(hr) || ! varSuccess)
        return;
      // Find the "<Palette></Palette> nodes from the xml
    CComPtr<IXMLDOMNodeList> pTPNodeList = NULL;
    hr = pXTPDoc->getElementsByTagName(ACRX_T("Palette"),
                                                &pTPNodeList);
    if (FAILED(hr))
        return;
      long tpCount = 0;
    hr = pTPNodeList->get_length(&tpCount);
    if(FAILED(hr))
        return;
      pTPNodeList->reset();
    for(int ii = 0; ii < tpCount; ii++)
    {
        CComPtr<IXMLDOMNode> pTPNode = NULL;
        hr = pTPNodeList->get_item(ii, &pTPNode);
        if(FAILED(hr))
            return;
          if(pTPNode)
        {
            CComPtr<IXMLDOMNode> pTPParentNode = NULL;
            hr = pTPNode->get_parentNode(&pTPParentNode);
            if(SUCCEEDED(hr))
            {
                // Check the node's parent name
                // to be sure we can use it to find the
                // ToolPalette name
                CComBSTR bstrParentNodeName;
                hr = pTPParentNode->get_nodeName
                                        (&bstrParentNodeName);
                if(SUCCEEDED(hr)
                && bstrParentNodeName == ACRX_T("ToolSource"))
                {
                    BSTR bstrTPName = NULL;
                    hr = pTPNode->get_text(&bstrTPName);
                    if(SUCCEEDED(hr))
                    {
                        AcString toolPaletteName(bstrTPName);
                        toolPaletteNames.append(toolPaletteName);
                        ::SysFreeString(bstrTPName);
                    }
                }
            }
        }
    }
}
  // Import the ToolPaletteGroup from the xpg file
// By default the toolpalettegroup is empty
// After importing from the xpg file,
// We will move the toolpalettes that were imported to the
// toolpalette group that is imported from xpg file.
for(int xpgFileIndex =0;
            xpgFileIndex < xpgFiles.length(); xpgFileIndex++)
{
    AcString xpgFilePath = xpgFiles.at(xpgFileIndex);
      // Create an XML Doc instance
    CComPtr<IXMLDOMDocument> pXPGDoc;
    HRESULT hr = pXPGDoc.CoCreateInstance(CLSID_DOMDocument,
                                 NULL, CLSCTX_INPROC_SERVER);
    if (FAILED(hr))
        return;
      // Load the XPG file as an XML doc
    CComVariant xmlSource = xpgFilePath.constPtr();
    VARIANT_BOOL bSuccess = VARIANT_FALSE;
    hr = pXPGDoc->load(xmlSource, &bSuccess);
    if (FAILED(hr) || ! bSuccess)
        return;
      // Get the XML nodes from the XPG file that corresponds to
    // a ToolPalette Group
    CComPtr<IXMLDOMNodeList> pTPGNodeList = NULL;
    hr = pXPGDoc->getElementsByTagName(
                                  ACRX_T("ToolPaletteGroup"),
                                  &pTPGNodeList);
    if (FAILED(hr))
        return;
      // Find the number of ToolPalette group nodes
    // from the XPG file
    long tpgCount = 0;
    hr = pTPGNodeList->get_length(&tpgCount);
    if(FAILED(hr))
        return;
      pTPGNodeList->reset();
    for(int tpgIndex = 0; tpgIndex < tpgCount; tpgIndex++)
    {
        // Get a single XML node that corresponds
        // to a ToolPalette Group
        CComPtr<IXMLDOMNode> pTPGNode = NULL;
        hr = pTPGNodeList->get_item(tpgIndex, &pTPGNode);
        if(FAILED(hr) || pTPGNode == NULL)
            return;
          // Create a new ToolPalette group and
        CAcTcUiToolPaletteGroup *pRootTpgroup
                        = pTpset->GetToolPaletteGroup(FALSE);
        CAcTcUiToolPaletteGroup * pMyToolPaletteGroup = NULL;
        pRootTpgroup->Clone(pMyToolPaletteGroup);
        pMyToolPaletteGroup->Reset();
          // Import the ToolPalette group settings
        // from the XPG file
        if(pMyToolPaletteGroup->Load(pTPGNode))
        {
            pRootTpgroup->AddItem(pMyToolPaletteGroup);
            pTpset->SetActivePaletteGroup(pMyToolPaletteGroup);
            acutPrintf(ACRX_T("\nImported %s"), xpgFilePath);
        }
          // Add the custom ToolPalettes
        // to the custom ToolPalette group.
        CAcTcUiToolPaletteGroup *pAllPalettesGroup
                            = pTpset->GetAllPalettesGroup();
        for(int ii =0; ii < toolPaletteNames.length(); ii++)
        {
            AcString toolPaletteName = toolPaletteNames.at(ii);
            CAcTcUiToolPalette *pMyCustomPalette
                = pAllPalettesGroup->FindPalette(
                                    toolPaletteName, NULL);
            if(pMyCustomPalette != NULL)
            {
                // Add the custom ToolPalette to the
                // custom ToolPalette group.
                pMyToolPaletteGroup->AddItem(pMyCustomPalette);
            }
        }
    }
}

## 评论

**内容**: Zimmermann Francine said...
Hello
What is the name of this ObjectArx and how can I load it in Autocad
I'm not a programmer,I work with Autocad and I have problem with tool palette modification
Many thank
Reply
04/01/2014 at 02:44 AM

---
**内容**: Balaji said...
Hi Francine,
If you want to do this using the AutoCAD UI, it can be done as follows :
1. Right click in the empty area of the tool palette window and select "customize palettes"
2. In the window that appears, select a tool palette and right click on it to export/import to or from an xtp file.
Regards,
Balaji
Reply
04/01/2014 at 02:54 AM

---
**内容**: Chockalingam said in reply to Balaji...
Hi Balaji,
Can you please explain how to load the xtp file via bundle.
Regards,
Chockalingam
Reply
10/29/2014 at 06:24 PM

---
**内容**: Balaji said in reply to Chockalingam...
Hi Chockalingam,
I do not think Autoloader supports loading XTP files. I will need to verify that with my colleagues. It would be easier to deploy your tool palettes using the Autoloader, if you create .atc files for your tool palettes and place them in your bundle folder. The folder path can be specified using the "ToolPalettePath" attribute in the "RuntimeRequirements" and AutoCAD will load the tool palettes automatically. But please note that the grouping of the tool palettes is not possible as that would require importing XPG files. Autoloader does not have support for that at present.
Regards,
Balaji
Reply
10/30/2014 at 12:29 AM

---
**内容**: Balaji said in reply to Chockalingam...
And just wanted to add to my reply.
How about loading the XTP file using the "StartupCommand" ? You can then import an XPG too.
http://adndevblog.typepad.com/autocad/2013/04/autoloader-example-for-invoking-a-startup-command-in-autocad.html
Regards,
Balaji
Reply
10/30/2014 at 12:32 AM

---
**内容**: Zimmermann Francine said...
Hi Balaji,
I know this way, is fine for me but my problem is that all my collegues have to do the same to get my modification.
Regards
Francine
Reply
04/01/2014 at 06:28 AM

---
**内容**: Zimmermann Francine said...
I found an other way with a macro using the toolpalettepath. Thnak you anyway for your help.
Francine
Reply
04/01/2014 at 06:31 AM

---
**内容**: Oscar Quintero said...
Hi Balaji, is it possible to do this with .NET API? Thanks.
Reply
01/24/2015 at 07:22 AM

---
**内容**: Oscar Quintero said...
Hi, is ti possible to do this with VB.NET?
Reply
01/24/2015 at 07:25 AM

---
**内容**: Balaji said...
Hi Oscar,
The "CAcTcUiToolPaletteGroup" is not exposed in .Net, so I do not think it will possible to completely work with VB.Net while importing XTP and XPG files. But it should be possible to create a mixed-managed code and use it in your VB.Net project.
Here is a blog post that can give you some hints :
http://adndevblog.typepad.com/autocad/2013/06/working-with-toolpalette-groups-using-net.html
Regards,
Balaji
Reply
01/24/2015 at 09:33 AM

---
