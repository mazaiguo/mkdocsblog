---
title: "Working with UCS and Ordinate Dimensions in AutoCAD using .NET API"
date: 2024-10-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - Dimension
  - UCS
description: "In the world of CAD (Computer-Aided Design), precision is key."
author: Autodesk
---
# Working with UCS and Ordinate Dimensions in AutoCAD using .NET API

发布日期: 2024-10-01

原始链接: https://adndevblog.typepad.com/autocad/2024/10/working-with-ucs-and-ordinate-dimensions-in-autocad-using-net-api.html

## 文章内容

By Madhukar Moogala
In the world of CAD (Computer-Aided Design), precision is key.
AutoCAD provides developers with powerful tools to manipulate objects and dimensions programmatically. One of the most critical concepts in AutoCAD development is the use of coordinate systems. This blog post will guide you through the process of working with the User Coordinate System (UCS) and creating ordinate dimensions using the AutoCAD .NET API.
Understanding Coordinate Systems in AutoCAD
AutoCAD operates using two main coordinate systems: the World Coordinate System (WCS) and the User Coordinate System (UCS).
World Coordinate System (WCS): This is the fixed global coordinate system in AutoCAD. All points, lines, and objects are placed relative to the WCS by default.
User Coordinate System (UCS): UCS allows you to define a custom coordinate system, aligning objects, views, or dimensions to any plane or orientation in 3D space. It’s particularly useful when working with objects at odd angles or creating dimensions aligned to specific geometric features.
By transforming points and objects to UCS, you can create more flexible and intuitive designs, and AutoCAD’s .NET API provides all the necessary tools to do this programmatically.
Exploring Ordinate Dimensions
Ordinate dimensions are used to measure the X or Y coordinates of a point in a drawing. Unlike linear dimensions, ordinate dimensions don’t rely on start and end points. Instead, they measure the position relative to a predefined origin—making them perfect for designs that require a high degree of coordinate accuracy, such as mechanical parts or assembly plans.
AutoCAD’s .NET API allows developers to create and customize ordinate dimensions with precision, ensuring that the correct values are displayed in the right locations.
Code Walkthrough: Creating and Manipulating UCS and Ordinate Dimensions
Now that we understand the concepts, let's dive into some code.
1. Setting Up the UCS
In AutoCAD, we can define a custom UCS and apply it to a viewport. This allows for precise control over the orientation of the drawing, aligning it with the real-world axes or a specific plane.
Here’s how we create a UCS programmatically and apply it to a viewport:

    
    public static void TestDimOrdinate()
    {
    var doc = Application.DocumentManager.MdiActiveDocument;
    var db = doc.Database;
    var ed = doc.Editor;

    using (var tr = db.TransactionManager.StartTransaction())
    {
        // Access the BlockTable and UCS Table
        var bt = (BlockTable)tr.GetObject(db.BlockTableId, OpenMode.ForRead);
        var ucsTbl = (UcsTable)tr.GetObject(db.UcsTableId, OpenMode.ForRead);
        
        UcsTableRecord ucstr;
        if (!ucsTbl.Has("TestUcs"))
        {
            ucstr = new UcsTableRecord { Name = "TestUcs" };
            ucsTbl.UpgradeOpen();
            ucsTbl.Add(ucstr);
            tr.AddNewlyCreatedDBObject(ucstr, true);
        }
        else
        {
            ucstr = (UcsTableRecord)tr.GetObject(ucsTbl["TestUcs"], OpenMode.ForWrite);
        }

        // Define the UCS origin and axes
        ucstr.Origin = Point3d.Origin;
        ucstr.XAxis = new Vector3d(1, 1, 0);
        ucstr.YAxis = new Vector3d(-1, 1, 0);

        // Apply UCS to the active viewport
        var vptr = (ViewportTableRecord)tr.GetObject(ed.ActiveViewportId, OpenMode.ForWrite);
        vptr.SetUcs(ucstr.ObjectId);
        doc.Editor.UpdateTiledViewportsFromDatabase();
        
        tr.Commit();
    }
  }
    
  
Here, we create a new UCS named "TestUcs", define its origin, X-axis, and Y-axis, and apply it to the active viewport. This UCS is then used to place ordinate dimensions based on the user’s input points.
2. Handling User Input and Transforming Points
To place ordinate dimensions, we first need to gather two points from the user and transform them from the WCS into the current UCS:
    
    PromptPointOptions pPtOpts = new PromptPointOptions("");
    Point3d[] point3Ds = new Point3d[2];

    for (int i = 0; i < 2; i++)
    {
        pPtOpts.Message = $"\nEnter point {i + 1}: ";
        var pPtRes = doc.Editor.GetPoint(pPtOpts);

        if (pPtRes.Status != PromptStatus.OK)
        {
            doc.Editor.WriteMessage("\nPoint input was canceled or invalid.");
            break;
        }

        point3Ds[i] = pPtRes.Value;
    }

    // Transform points to UCS
    Matrix3d activeUCS = ed.CurrentUserCoordinateSystem;
    Point3d ucsDp = point3Ds[0].TransformBy(activeUCS);
    Point3d ucsLp = point3Ds[1].TransformBy(activeUCS);
    
  

This code collects two points from the user, transforming them from WCS to UCS using TransformBy().
3. Fixing Angles and Floating-Point Precision
When dealing with floating-point operations, tiny precision errors can lead to discrepancies in different systems. To address this, we normalize angles to ensure they fall within the [0, 2π] range and fix close-to-zero negative values:
    
      const double ANGLE_EPSILON = 1E-15;

      public static bool IsNearZero(double num)
      {
          return num < ANGLE_EPSILON && num > -ANGLE_EPSILON;
      }

      public static double FixAngle(double angle)
      {
          const double TWOPI = 2 * Math.PI;
          double retang = angle / TWOPI;
          retang = (retang - (int)retang) * TWOPI;

          if (retang < 0 && IsNearZero(retang))
          {
              retang = 0.0;
          }

          if (retang < 0.0) retang += TWOPI;
          if (retang >= TWOPI) retang -= TWOPI;

          return retang;
      }
    
  
Here, we ensure angles like -2E-16 are unified to zero, addressing differences in floating-point precision across different architectures.
Though AutoCAD is designed for x64-based processor architectures only as of today, sake of brevity considered other architectures like ARM
4. Creating Ordinate Dimensions
Finally, we can create ordinate dimensions based on the transformed points:
    
      double rotation = UserToLocalAngle(activeUCS.CoordinateSystem3d.Zaxis, activeUCS.CoordinateSystem3d.Xaxis);

      OrdinateDimension ordDim = new OrdinateDimension
      {
          DefiningPoint = ucsDp,
          LeaderEndPoint = ucsLp,
          Normal = activeUCS.CoordinateSystem3d.Xaxis.CrossProduct(activeUCS.CoordinateSystem3d.Yaxis),
          UsingXAxis = false,
          DimensionStyle = db.Dimstyle,
          HorizontalRotation = -rotation
      };

      btr.AppendEntity(ordDim);
      tr.AddNewlyCreatedDBObject(ordDim, true);

    
  
This snippet defines an ordinate dimension using the points transformed into UCS, sets its dimension style, and applies the necessary rotation to ensure the dimension aligns correctly with the current UCS.
Note: we are setting a rotation angle to the dimension, so the Ordinate Dimension is correctly aligned with UCS
This is the angle from the dimension's positive horizontal axis (which is the X axis of the UCS in effect when the dimension was created) to the X axis of the dimension's OCS (as defined by the dimension's normal vector and the arbitrary axis algorithm). Positive angles are counterclockwise when looking down the OCS Z axis towards the OCS origin. The dimension's positive horizontal axis direction is used as the default left-to-right direction for the dimension text.
Common Pitfalls and Best Practices
Handling Floating-Point Precision:
Small errors can accumulate when performing geometric calculations. Always normalize your values and use an epsilon threshold for comparing floating-point numbers.
Working with UCS:
Always ensure you’re transforming points to the correct coordinate system before performing operations. This avoids misalignment issues, especially when working in 3D space.
Testing on Different Architectures *:
Differences in floating-point precision between architectures (Intel vs ARM) can affect calculations. Normalize close-to-zero values to avoid discrepancies.
Conclusion
In this blog, we’ve explored how to create and manipulate UCS in AutoCAD using the .NET API, gathering user input, fixing floating-point precision issues, and creating ordinate dimensions. Understanding these concepts allows developers to create more complex and accurate drawings programmatically, especially when precision is essential.
Experiment with the provided code, and see how you can enhance your AutoCAD projects by harnessing the power of the UCS and the .NET API. Happy coding!
    // Tolerance for detecting near-zero values,
    // used to account for floating-point precision errors.
    const double ANGLE_EPSILON = 1E-15;

    // Checks if a given number is near zero, within a defined tolerance.
    public static bool IsNearZero(double num)
    {
        return num < ANGLE_EPSILON && num > -ANGLE_EPSILON;
    }

    // Normalizes an angle to the range [0, 2π], correcting for floating-point precision issues.
    // This handles small imprecisions when dealing with angles across different architectures.
    public static double FixAngle(double angle)
    {
        const double TWOPI = 2 * Math.PI; // Constant representing 2π (full circle in radians)
        double retang;

        if (angle - 1.0 == angle) // Check for infinity
            angle = 0; // Treat infinity as zero for angles

        retang = angle / TWOPI;
        retang = (retang - (int)retang) * TWOPI; // Normalize angle within [0, 2π]

        // Unify close-to-zero negative values to zero
        // to avoid differences across architectures (ARM vs Intel).
        if (retang < 0 && IsNearZero(retang))
        {
            retang = 0.0;
        }

        if (retang < 0.0)
            retang += TWOPI; // Correct for negative angles

        if (retang >= TWOPI)
            retang -= TWOPI; // Correct for angles exceeding 2π

        return retang;
    }

    // Converts an angle in world coordinates to local coordinates
    // based on a given plane (defined by normal and UCS X-direction vectors).
    public static double UserToLocalAngle(Vector3d normal, Vector3d ucsXdir)
    {
        // Transformation matrix from World Coordinate System (WCS) to Local Coordinate System (LCS)
        var wcsToLcs = Matrix3d.WorldToPlane(normal);

        // Transform the UCS X-direction vector into the local coordinate system
        var xDir = ucsXdir;
        xDir.TransformBy(wcsToLcs);

        // Calculate the angle in the local plane using Atan2
        var angle = Math.Atan2(xDir.Y, xDir.X);

        // Normalize the angle using FixAngle to ensure it is within [0, 2π]
        return FixAngle(angle);
    }

    // Command method to test dimensioning of ordinates in AutoCAD
    [CommandMethod("TstDimOrdinate")]
    public static void TestDimOrdinate()
    {
        // Get the active AutoCAD document
        var doc = Application.DocumentManager.MdiActiveDocument;
        if (doc == null) return;

        var db = doc.Database; // Get the database of the active document
        var ed = doc.Editor;   // Get the editor (for user interaction)

        // Start a transaction to modify the database
        using (var tr = db.TransactionManager.StartTransaction())
        {
            // Open the block table and the model space block table record for writing
            var bt = (BlockTable)tr.GetObject(db.BlockTableId, OpenMode.ForRead);
            var btr = (BlockTableRecord)tr.GetObject(bt[BlockTableRecord.ModelSpace], OpenMode.ForWrite);

            // Create a new UCS based on specified vectors
            var ucs = new CoordinateSystem3d(Point3d.Origin, new Vector3d(1, 1, 0), new Vector3d(-1, 1, 0));

            // Open the UCS table for reading
            var ucsTbl = (UcsTable)tr.GetObject(db.UcsTableId, OpenMode.ForRead);
            UcsTableRecord ucstr;

            // Check if the UCS named "TestUcs" already exists, if not, create it
            if (!ucsTbl.Has("TestUcs"))
            {
                ucstr = new UcsTableRecord
                {
                    Name = "TestUcs" // Name the UCS "TestUcs"
                };

                // Open the UCS table for writing and add the new UCS
                tr.GetObject(db.UcsTableId, OpenMode.ForWrite);
                ucsTbl.Add(ucstr);
                tr.AddNewlyCreatedDBObject(ucstr, true);
            }
            else
            {
                // Retrieve the existing UCS if "TestUcs" already exists
                ucstr = (UcsTableRecord)tr.GetObject(ucsTbl["TestUcs"], OpenMode.ForWrite);
            }

            // Set UCS origin and axes
            ucstr.Origin = Point3d.Origin;
            ucstr.XAxis = new Vector3d(1, 1, 0);
            ucstr.YAxis = new Vector3d(-1, 1, 0);

            // Get the active viewport and configure the UCS icon to display at the origin
            var vptr = (ViewportTableRecord)tr.GetObject(doc.Editor.ActiveViewportId, OpenMode.ForWrite);
            vptr.IconAtOrigin = true;
            vptr.IconEnabled = true;

            // Set the current UCS to the newly created or retrieved UCS
            vptr.SetUcs(ucstr.ObjectId);
            doc.Editor.UpdateTiledViewportsFromDatabase();

            // Prompt the user to input two points
            PromptPointResult pPtRes;
            PromptPointOptions pPtOpts = new PromptPointOptions("");
            Point3d[] point3Ds = new Point3d[2];

            for (int i = 0; i < 2; i++)
            {
                pPtOpts.Message = $"\nEnter point {i + 1}: ";
                pPtRes = doc.Editor.GetPoint(pPtOpts);

                if (pPtRes.Status != PromptStatus.OK)
                {
                    doc.Editor.WriteMessage("\nPoint input was canceled or invalid.");
                    break;
                }

                point3Ds[i] = pPtRes.Value; // Store the entered points
            }

            // Transform the input points to the current UCS
            Matrix3d activeUCS = ed.CurrentUserCoordinateSystem;
            Point3d ucsDp = point3Ds[0].TransformBy(activeUCS);
            Point3d ucsLp = point3Ds[1].TransformBy(activeUCS);

            // Calculate the angle of rotation for the ordinate dimension
            double rotation = UserToLocalAngle(activeUCS.CoordinateSystem3d.Zaxis, activeUCS.CoordinateSystem3d.Xaxis);

            // Create a new Ordinate Dimension with the calculated properties
            OrdinateDimension ordDim = new OrdinateDimension
            {
                DefiningPoint = ucsDp,
                LeaderEndPoint = ucsLp,
                Normal = activeUCS.CoordinateSystem3d.Xaxis.CrossProduct(activeUCS.CoordinateSystem3d.Yaxis),
                UsingXAxis = false,
                DimensionStyle = db.Dimstyle,
                HorizontalRotation = -rotation,
                ColorIndex = 1

            };

            ordDim.SetDatabaseDefaults();
            btr.AppendEntity(ordDim);
            tr.AddNewlyCreatedDBObject(ordDim, true);

            // Commit the transaction to finalize changes
            tr.Commit();
        }
    }
Video
view raw
source.md hosted with ❤ by GitHub

