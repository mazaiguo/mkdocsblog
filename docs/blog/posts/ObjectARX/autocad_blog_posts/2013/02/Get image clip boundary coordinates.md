---
title: "Get image clip boundary coordinates"
date: 2013-02-01
categories:
  - AutoCAD C++
tags:
  - C++
  - COM
  - Dimension
  - ObjectARX
description: "I can set image’s clip by AcadRasterImage.ClipBoundary, but how do I get the AcadRasterImage's clip boundary coordinates? I know if it is rectangul..."
author: Autodesk
---
# Get image clip boundary coordinates

发布日期: 2013-02-01

原始链接: https://adndevblog.typepad.com/autocad/2013/02/get-image-clip-boundary-coordinates.html

## 文章内容

By Xiaodong Liang
Issue
I can set image’s clip by AcadRasterImage.ClipBoundary, but how do I get the AcadRasterImage's clip boundary coordinates? I know if it is rectangular, I can get its bounding box, width and height. But, if the clip boundary is of a irregular shape, I can't find any exposed methods to get such data.
Solution
The ObjectARX AcDbRasterImage::clipBoundary() equivalent functionality is not exposed in the current ActiveX Automation Model.
We can work around this limitation by exposing an interface that does exactly that. The whole project is attached:  Download ImgClipBoundary
STDMETHODIMP CClipBoundaryObj::GetImageClipBoundary(
    VARIANT* pVarDblArray,
    VARIANT acadImage)
{
    // TODO: Add your implementation code here
    try
    {
        CComQIPtr<IAcadRasterImage>
            pAcadImage(acadImage.punkVal);
        if(!pAcadImage)
            throw E_POINTER;
        CComQIPtr<IAcadBaseObject>
            pBaseObj(pAcadImage);
        if(!pBaseObj)
            throw E_POINTER;
        AcDbObjectId id;
        pBaseObj->GetObjectId(&id);
        AcDbObjectPointer<AcDbRasterImage>
            pImage(id, AcDb::kForRead);
          if(pImage.openStatus() != Acad::eOk)
            throw E_UNEXPECTED;
        AcGePoint2dArray array =
            pImage->clipBoundary();
          int len = array.length();
        if(len == 0)
            throw E_FAIL;
          AcGeMatrix3d mat;
        pImage->getPixelToModelTransform(mat);
        mat.inverse();
        AcAxPoint2dArray pts;
        for(int i=0; i<len; i++)
        {
            AcGePoint3d pt(array[i].x, array[i].y, 0);
            pt.transformBy(mat);
            pts.append(AcGePoint2d(pt.x, pt.y));
        }
        pts.setVariant(pVarDblArray);
    }
      catch(const HRESULT h)
    {
        // for now
        acutPrintf(_T("\nSomething is wrong."));
        return h;
    }
      return S_OK;
}
To use the ability above,
1. build the attached project, load it in AutoCAD
2.  open VBA IDE
3. Tools >> Reference: select ARX. now you can see one library is available in the list.
4. Run the VBA code below. It creates an image and set its clip, and gets its clip boundary by the method provided in asdkImgClipBoundary.
Sub Example_ClipBoundary()
    ' This example adds a raster image in model space.
    ' It then clips the image based on a clip boundary.
    ' This example uses the "downtown.jpg" found in the sample
    ' directory. If you do not have the image, or it is located
    ' in a different directory, insert a valid path and name for the
    ' imageName variable below.
    Dim insertionPoint(0 To 2) As Double
    Dim scalefactor As Double
    Dim rotationAngle As Double
    Dim imageName As String
    Dim rasterObj As AcadRasterImage
    imageName = "C:\01_SDK\ObjectARX 2012\samples\graphics\AsdkTransientGraphicsSampFolder\Airport-Image.jpg"
    insertionPoint(0) = 5#: insertionPoint(1) = 5#: insertionPoint(2) = 0#
    scalefactor = 2#
    rotationAngle = 0
    On Error Resume Next
    ' Creates a raster image in model space
    Set rasterObj = ThisDrawing.ModelSpace.AddRaster(imageName, insertionPoint, scalefactor, rotationAngle)
    If Err.Description = "Filer error" Then
        MsgBox imageName & " could not be found."
        Exit Sub
    End If
    ZoomAll
    MsgBox "Clip the image?", , "ClipBoundary Example"
    ' Establish the clip boundary with an array of points
    Dim clipPoints(0 To 9) As Double
    clipPoints(0) = 6: clipPoints(1) = 6.75
    clipPoints(2) = 7: clipPoints(3) = 6
    clipPoints(4) = 6: clipPoints(5) = 5
    clipPoints(6) = 5: clipPoints(7) = 6
    clipPoints(8) = 6: clipPoints(9) = 6.75
    ' Clip the image
    rasterObj.ClipBoundary clipPoints
    ' Enable the display of the clip
    rasterObj.ClippingEnabled = True
    ThisDrawing.Regen acActiveViewport
    'MsgBox "The image has been clipped.", , "ClipBoundary Example"
    On Error GoTo 0
    Dim xObj As asdkImgClipBoundaryLib.ClipBoundaryObj
    Set xObj = ThisDrawing.Application.GetInterfaceObject("ImgClipBoundary.ClipBoundaryObj.1")
    Dim boundary As Variant
    xObj.GetImageClipBoundary boundary, rasterObj
End Sub

## 评论

**内容**: Alexander Rivilis said...
Typo: not AcadAcadRasterImage but AcadRasterImage
Reply
02/18/2013 at 02:33 AM

---
**内容**: Xiaodong Liang said in reply to Alexander Rivilis...
fixed, thank you Alexander!
Reply
03/01/2013 at 02:20 AM

---
