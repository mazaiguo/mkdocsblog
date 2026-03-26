---
title: "How to Crop a Point Cloud using API"
date: 2017-02-01
categories:
  - AutoCAD
tags:
  - API
description: "In this post we will discuss about cropping a point cloud, first we will look at how we can attach a point cloud from .rcs which is an Autodesk Rec..."
author: Autodesk
---
# How to Crop a Point Cloud using API

发布日期: 2017-02-01

原始链接: https://adndevblog.typepad.com/autocad/2017/02/how-to-crop-a-point-cloud-using-api.html

## 文章内容

By Madhukar Moogala
In this post we will discuss about cropping a point cloud, first we will look at how we can attach a point cloud from *.rcs which is an Autodesk Recap Scan File.
Later, in the code we will crop the attached Point Cloud, I will add two types of cropping boundary namely, Rectangular and Circular.
The core logic of cropping is to ensure giving the proper cropping plane and cropping points that fits within cropping boundary.
The other elements in API used is self explanatory.
namespace PointCloudData
{
public class Class1
{
    //Get RCP file from Solution Directory
    private static string getPCFile()
    {
        /*
        SolutionFolder
        │   
        ├───bin
        └───Debug
        │
        assembly.dll

        */
        var assemblyLoc =
                Assembly.GetExecutingAssembly().Location;
        var debugFolder = 
                Path.GetDirectoryName(assemblyLoc);
        var binFolder = 
                Path.GetDirectoryName(debugFolder);
        var solutionFolder = 
                Path.GetDirectoryName(binFolder);
        var FilePath = 
                solutionFolder +
                       "\\MyOfficeRoom.rcs";
        return FilePath;
    }
    //Write to Editor
    private static void Report(string v)
    {
        Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
        ed.WriteMessage("\n" + v);
    }

    public static ObjectId AttachPointCloudEx(string filename,
                                              double scale, 
                                              double rotation)
    {
        Point3d location = new Point3d(0, 0, 0);
        Database db = HostApplicationServices.WorkingDatabase;
        ObjectId objid = PointCloudEx.AttachPointCloud(filename,
                                                        location,
                                                        scale,
                                                        rotation,
                                                        db);
        if (objid.IsNull)
            Report("\nFail to get object id of attach point cloud"+
                "by PointCloudEx.AttacPointCloud API");

        return objid;

    }
    
    //Cropping Logic
    //
    public static ErrorStatus addcropping(PointCloudEx pointcloud,
                                          PointCloudCropType type, 
                                          Point3d pt1, Point3d pt2,
                                          bool bInside, bool bInverted)
    {

        PointCloudCrop crop = PointCloudCrop.Create(IntPtr.Zero);
        if (crop == null)
            Report("\nFail to create crop by pointcloudcrop.Create method");
        Point3dCollection points = new Point3dCollection();
        points.Add(pt1);
        points.Add(pt2);
        crop.Vertices = points;
        //In SW Isometric View or OrthoGraphic View
        Vector3d norm = new Vector3d(0, 1, 0);           
        Plane cropPlane = new Plane(pt1, norm);
        crop.CropPlane = cropPlane;
        crop.CropType = type;
        crop.Inside = bInside;
        crop.Inverted = bInverted;
        pointcloud.addCroppingBoundary(crop);
        return ErrorStatus.OK;
    }

       
    [CommandMethod("CropPC")]
    public static void CropPC()
    {
        //attach point cloud into the drawing
        Database db = 
            HostApplicationServices.WorkingDatabase;
        ObjectId objid = 
            AttachPointCloudEx(getPCFile(), 1.0, 0.0);
        Editor ed = 
            Application.DocumentManager.MdiActiveDocument.Editor;
        //get the point cloud object
        using (Transaction t = db.TransactionManager.StartTransaction())
        {
            ViewTableRecord activeVTR = ed.GetCurrentView() as ViewTableRecord;
            //Set VS Preset to Realistic, in Wireframe PC Attach is not supported.
            DBDictionary dict = t.GetObject(db.VisualStyleDictionaryId,
                                OpenMode.ForRead) as DBDictionary;
            activeVTR.VisualStyleId = dict.GetAt("Realistic");
            ed.SetCurrentView(activeVTR);
            ed.UpdateTiledViewportsFromDatabase();
                

            PointCloudEx pcloudex = 
                t.GetObject(objid, OpenMode.ForWrite) as PointCloudEx;

                             
            //Add two cropping to the point cloud
            Point3d crop1_pt1 = new Point3d(-7.0, 12.0, 0);
            Point3d crop1_pt2 = new Point3d(-4.0, 9.0, 0);
            Point3d crop2_pt1 = new Point3d(3.5, 15.0, 0);
            Point3d crop2_pt2 = new Point3d(6.0, 13.0, 0);
            /*Cropping PC in not supported in PerspectiveView*/
            if (activeVTR.PerspectiveEnabled)
            {
                activeVTR.PerspectiveEnabled = false;
            }
            //Rectangle - first corner point, 2nd, 3rd, 4th and first corner point again. 
            addcropping(pcloudex, 
                        PointCloudCropType.Rectangular, 
                        crop1_pt1, crop1_pt2,
                        false, false);
            //Circular - there are 2 points, center point and any point which is on the circle's circumference. 
            addcropping(pcloudex, 
                        PointCloudCropType.Circular, 
                        crop2_pt1, crop2_pt2,
                        false, true);

            //show Cropping
            pcloudex.ShowCropped = true;
            //Now lets us traversing list of croppings
            for (int Index = 0; Index < pcloudex.getCroppingCount(); Index++)
            {

                //Retrieving Croptype
                PointCloudCrop tmpcrop = pcloudex.getPointCloudCropping(Index);
                Report(tmpcrop.CropType.ToString());
            }

            //Zoom the View to PC Extents
            using (ViewTableRecord vtr = new ViewTableRecord())
            {
                vtr.CenterPoint = 
                    new Point2d(pcloudex.Location.X, pcloudex.Location.Z);
                Extents3d extents = 
                    pcloudex.GeomExtents;
                Point2d min2d = 
                    new Point2d(extents.MinPoint.X, extents.MinPoint.Y);
                Point2d max2d =
                    new Point2d(extents.MaxPoint.X, extents.MaxPoint.Y);
                vtr.Height = 
                    max2d.Y - min2d.Y;
                vtr.Width =
                    max2d.X - min2d.X;
                vtr.Target = 
                    activeVTR.Target;
                                       
                ed.SetCurrentView(vtr);
            }
                
            t.Commit();

        }
           
    }

        

    }
}
  Source project can be downloaded from here
Note: I intentionally didn’t upload Pointcloud file (*.rcs), as it is bulky size.

## 评论

**内容**: Linh 7cad said...
Thanks for your code.
How can I get PointCloudEx API? I downloaded, open it and VS says "the name 'PointCloudEx' doesn't exist in current context"
Reply
11/28/2017 at 06:01 PM

---
**内容**: Madhukar Moogala said in reply to Linh 7cad...

Typepad HTML Email

Thanks for stopping by.
 
Have your referenced AcDbMgd.dll in your project apart from AcCoreMgd.dll & AcMgd.dll.
Can you put the screenshot of the error, for me to understand.
 
 
  Reply
11/28/2017 at 07:08 PM

---
**内容**: Linh 7cad said in reply to Madhukar Moogala...
OK, I find it out. Got to use AutoCAD 2018 dll. I used to add reference of AutoCAD 2013. Thanks.
Reply
11/28/2017 at 08:22 PM

---
**内容**: Thomas Bailey said...
Previewing your Comment
Thomas Bailey
Madhukar,
Thank you for your sample! I know this is an old post, but I have a question hopefully you may answer?
I'm attempting to run your code on a point cloud of my own. I have modified your code so that the point cloud in question is selected by the user. This is working. What I am confused about is the plane in which the crop is performed. I have tried entering different coordinates for these values:
Point3d crop1_pt1 = new Point3d(-7.0, 12.0, 0);
Point3d crop1_pt2 = new Point3d(-4.0, 9.0, 0);

But it appears to be cropping somewhere far outside the bounds of my point cloud. I know this because if I invert the cropping, my entire cloud disappears. The center of my point cloud is around the coordinates of (0,0,1200). What values should I give for the above variables given that my point cloud is up high? Note: I tried lowering it down to Z=0 but still could not get it to visibly crop anything. I would be more than happy to provide a trimmed down version of the point cloud for you to look at. Thank you!
Reply
01/13/2020 at 03:08 PM

---
**内容**: Madhukar Moogala said in reply to Thomas Bailey...
Hi,
For some reason I did get notification for your post.
I would be more than happy to provide a trimmed down version of the point cloud for you to look at.

can you please do that I will spend sometime this weekend.
Reply
03/30/2020 at 10:09 PM

---
**内容**: Amir Ash said...
Hi Madhukar,
Thank you for your code. I have tested it on my point cloud and the Circular cropping works perfectly and I created more than 1000 cropped PCs, however the rectangular type which I am looking for doesn't work at all. I tired to change the code in so much ways even updated the Autocad .net core but nothing happens in my point cloud. For example when I show/hide or invert the cropped section in the toolbar, nothing changed(I mean the whole point cloud doesn't appear/disappear which means nothing was cropped at the first place). I would appreciate it if you could help me with this.
Thank you.
Reply
03/30/2020 at 09:25 PM

---
**内容**: Madhukar Moogala said...
Hi,
It is important ensure the cropping points fit in cropping boundary, were you able to crop to rectangular for the sample in the blog ?
Reply
03/30/2020 at 10:07 PM

---
**内容**: Amir Ash said...
Madhukar,
Thank you for you answer. I am not sure what you mean by fitting in cropping boundary, but for your information I passed two points(first upper-left corner point and third bottom-right corner point) from the cropping rectangular to the "addcropping" function. Also in the function I changed the norm vector to use the top view (0,0,1) and it works well for the circular crop but nothing for rectangular.
I tested the code on my own point cloud not the blog sample.
Please let me know what you think.
Thank you,
Reply
03/31/2020 at 09:01 AM

---
**内容**: Hossam Moussa said...
Hi,
Rectangle - first corner point, 2nd, 3rd, 4th and first corner point again.
but you use just two point for the rectangle
and the normal of the crop plan is Y-axis, it has to be Z-axis
I dont understand this ??
can you help me to beter understanding.
Regards Hossam
Reply
06/28/2021 at 05:30 AM

---
**内容**: Anh-Tuan NGUYEN said...
Hi Madhukar
Thanks alot for your code, it's very intersting for me to make un plugin to control point cloud for my team. I tried with your code but it made only Circular cropping and not Rectangle cropping. Can you tell me what is the error that i made please.
Best regards
Anh-Tuan
Reply
06/18/2022 at 02:45 AM

---
