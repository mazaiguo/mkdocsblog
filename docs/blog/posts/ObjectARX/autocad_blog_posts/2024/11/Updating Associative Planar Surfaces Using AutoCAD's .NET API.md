---
title: "Updating Associative Planar Surfaces Using AutoCAD's .NET API"
date: 2024-11-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - Selection
  - Surface
description: "Associative surfaces in AutoCAD offer robust capabilities for maintaining dynamic links between geometric objects. Updating these surfaces programm..."
author: Autodesk
---
# Updating Associative Planar Surfaces Using AutoCAD's .NET API

发布日期: 2024-11-01

原始链接: https://adndevblog.typepad.com/autocad/2024/11/updating-associative-planar-surfaces-using-autocads-net-api.html

## 文章内容

By Madhukar Moogala
Associative surfaces in AutoCAD offer robust capabilities for maintaining dynamic links between geometric objects. Updating these surfaces programmatically requires careful handling of associated entities and profile curves. In this blog, we’ll explore how to automate the process of updating an associative planar surface with a new profile curve using AutoCAD .NET API.
Scenario Overview
The primary goal of this method is to update the profile curve of a planar surface while preserving its associative behavior. We assume the user selects a planar surface with a rectangular profile curve. If the surface is associative, the existing profile is replaced with a modified version.

Key Highlights
Surface Selection: Ensures the selected entity is a valid surface.
Associativity Check: Identifies whether the surface has an associated AssocActionBody.
Profile Extraction: Extracts edges from the associative surface and processes them as AutoCAD entities.
Profile Transformation: Demonstrates scaling the extracted profile using its centroid.
Input Path Update: Updates the planar surface with a transformed profile.
1. Surface Selection
The method starts by prompting the user to select a surface. It validates the selection to ensure the entity is a DBSurface.
   
      PromptEntityOptions surfaceSelectionPrompt = new PromptEntityOptions("\nSelect a surface: ");
      surfaceSelectionPrompt.SetRejectMessage("Must be a Surface!");
      surfaceSelectionPrompt.AddAllowedClass(typeof(DBSurface), exactMatch: false);
      PromptEntityResult selectionResult = documentEditor.GetEntity(surfaceSelectionPrompt);
   
2. Associativity Check
To determine if the surface is associative, the code checks for a valid AssocActionBody.
   
      var surfaceCreationActionId = selectedSurface.CreationActionBodyId;
      bool isSurfaceAssociative = false;
   
      if (surfaceCreationActionId != ObjectId.Null)
      {
          AssocActionBody associatedActionBody = transaction.GetObject(surfaceCreationActionId, OpenMode.ForRead) as AssocActionBody;
          isSurfaceAssociative = associatedActionBody != null;
      }      
   
3. Extracting and Transforming the Profile
If the surface is associative, its input paths are processed. The extracted edges are converted into entities, modified (e.g., scaled), and used to update the surface.
   
      planeActionBody.GetInputPaths(out EdgeRef[][][] edgeReferenceLayers);
      foreach (var edgeReferences in edgeReferenceLayers.SelectMany(layer => layer))
      {
          foreach (var edgeReference in edgeReferences)
          {
              Entity extractedEntity = edgeReference.CreateEntity();
              extractedEntity.ColorIndex = 1;
              extractedEntity.SetDatabaseDefaults();
              ents.Add(extractedEntity);
          }
      }
      if (ents[0] is Polyline pl)
      {
          var center = GetCentroid(pl);
          profile.TransformBy(Matrix3d.Scaling(10, center));
          planeActionBody.UpdateInputPath(0, new PathRef(new EdgeRef[] { new EdgeRef(profile) }));
      }
   
4. Evaluating the Associative Network
Once the profile is updated, AssocManager.EvaluateTopLevelNetwork ensures all dependencies are recalculated.
   
      AssocManager.EvaluateTopLevelNetwork(activeDatabase, null, 0);
   

Conclusion
This approach offers a structured way to programmatically update associative planar surfaces in AutoCAD, making it a valuable tool for design automation. Whether you’re scaling a profile curve, transforming it, or replacing it entirely, understanding the associative network and leveraging the .NET API unlocks a wealth of possibilities for automation.

```csharp
/// <summary>
/// Updates the profile curve of an associative planar surface in AutoCAD.
/// Assumes the user has selected a planar surface with a rectangular profile curve.
/// Demonstrates the workflow for:
/// - Verifying surface associativity
/// - Extracting and transforming the profile
/// - Updating the surface with a modified profile
/// </summary>
[CommandMethod("UpdateAssociatePlanarSurface")]
public static void UpdateAssociatePlanarSurface()
{
    // Get the active AutoCAD database
    Database activeDatabase = HostApplicationServices.WorkingDatabase;
    // Prompt the user to select a surface
    PromptEntityOptions surfaceSelectionPrompt = new PromptEntityOptions("\nSelect a surface: ");
    surfaceSelectionPrompt.SetRejectMessage("Must be a Surface!"); // Reject non-surface entities
    surfaceSelectionPrompt.AddAllowedClass(typeof(DBSurface), exactMatch: false);
    Editor documentEditor = Application.DocumentManager.MdiActiveDocument.Editor;
    PromptEntityResult selectionResult = documentEditor.GetEntity(surfaceSelectionPrompt);
    // Exit if selection is canceled or invalid
    if (selectionResult.Status != PromptStatus.OK)
        return;
    // Begin a transaction to handle database changes
    using Transaction transaction = selectionResult.ObjectId.Database.TransactionManager.StartTransaction();
    try
    {
        // Access the selected surface
        DBSurface selectedSurface = transaction.GetObject(selectionResult.ObjectId, OpenMode.ForWrite) as DBSurface;
        if (selectedSurface == null)
            return;
        // Check if the surface is associative by verifying the CreationActionBodyId
        var surfaceCreationActionId = selectedSurface.CreationActionBodyId;
        bool isSurfaceAssociative = false;
        if (surfaceCreationActionId != ObjectId.Null)
        {
            AssocActionBody associatedActionBody = transaction.GetObject(surfaceCreationActionId, OpenMode.ForRead) as AssocActionBody;
            isSurfaceAssociative = associatedActionBody != null;
        }
        if (isSurfaceAssociative)
        {
            // Retrieve the associated action body for the planar surface
            AssocPlaneSurfaceActionBody planeActionBody = transaction.GetObject(surfaceCreationActionId, OpenMode.ForWrite) as AssocPlaneSurfaceActionBody;
            // Retrieve the input path parameters for the action body
            planeActionBody.GetInputPaths(out EdgeRef[][][] edgeReferenceLayers);
            // List to store extracted entities from edge references
            var ents = new List<Entity>();
            // Extract entities from the nested edge reference layers
            for (int layerIndex = 0; layerIndex < edgeReferenceLayers.Length; layerIndex++)
            {
                EdgeRef[][] edgeReferenceRows = edgeReferenceLayers[layerIndex];
                for (int rowIndex = 0; rowIndex < edgeReferenceRows.Length; rowIndex++)
                {
                    EdgeRef[] edgeReferences = edgeReferenceRows[rowIndex];
                    for (int referenceIndex = 0; referenceIndex < edgeReferences.Length; referenceIndex++)
                    {
                        // Convert edge references to entities and store them
                        Entity extractedEntity = edgeReferences[referenceIndex].CreateEntity();
                        extractedEntity.ColorIndex = 1; // Optional: Set the color for visual distinction
                        extractedEntity.SetDatabaseDefaults();
                        ents.Add(extractedEntity);
                        SubEntityUtilities.PostToDataBase(extractedEntity); // Add the entity to the database
                    }
                }
            }
            // Clone the first extracted profile and apply a transformation
            var profile = ents[0].Clone() as Entity;
            if (profile is Polyline pl)
            {
                // Calculate the centroid of the polyline for transformation
                var center = GetCentroid(pl);
                // Apply a scaling transformation to the profile
                profile.TransformBy(Matrix3d.Scaling(10, center));
                // Update the input path with the modified profile
                var edges = new List<EdgeRef> { new EdgeRef(profile) };
                planeActionBody.UpdateInputPath(0, new PathRef(edges.ToArray()));
            }
            // Reevaluate the associative network to apply the changes
            AssocManager.EvaluateTopLevelNetwork(activeDatabase, null, 0);
        }
        // Commit the transaction to save changes
        transaction.Commit();
    }
    catch (System.Exception ex)
    {
        // Handle errors and abort the transaction if necessary
        documentEditor.WriteMessage($"\nError: {ex.Message}");
        transaction.Abort();
    }
}
/// <summary>
/// Calculates the centroid of a closed polyline.
/// Throws an exception if the polyline is not closed.
/// </summary>
/// <param name="polyline">The closed polyline for which the centroid is calculated.</param>
/// <returns>The centroid of the polyline as a Point3d.</returns>
public static Point3d GetCentroid(Polyline polyline)
{
    if (!polyline.Closed)
        throw new Exception(ErrorStatus.InvalidInput, "Polyline must be closed");
    double area = 0, cx = 0, cy = 0;
    int numVertices = polyline.NumberOfVertices;
    // Apply the Shoelace formula for centroid and area calculation
    for (int i = 0; i < numVertices; i++)
    {
        Point2d p1 = polyline.GetPoint2dAt(i);
        Point2d p2 = polyline.GetPoint2dAt((i + 1) % numVertices);
        double temp = p1.X * p2.Y - p2.X * p1.Y;
        area += temp;
        cx += (p1.X + p2.X) * temp;
        cy += (p1.Y + p2.Y) * temp;
    }
    area *= 0.5;
    cx /= (6 * area);
    cy /= (6 * area);
    // Return the calculated centroid
    return new Point3d(cx, cy, 0);
}
```
view raw
UpdateAssociatePlanarSurface.cs hosted with ❤ by GitHub

## 评论

**内容**: poppy playtime said...
Commentary may be valuable if it contains a compelling conversation. Although it is possible that this is not a taboo subject, I believe that you should write about it. In general, there are not enough people to converse on topics like this. One more time. Salutations!
Reply
12/12/2024 at 12:33 AM

---
