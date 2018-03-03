![alt text](https://github.com/dimven/SpringNodes/blob/master/spring%20nodes%20logo.jpg "Logo")

a.k.a. Springs for Dynamo, Dynamo Springs

Spring Nodes is a custom node package for [Dynamo](http://www.dynamobim.org) .

   Its main focus is to improve Dynamo's interaction with Revit. The wider goal is to explore any and all means that can help accelerate BIM focused work-flows. Many of the nodes use either IronPython or DesignScript and can be a good starting point for learning the specific syntax and finer points of both.

   The package repository is posted under the MIT license. You will find all the [sample files](https://github.com/dimven/SpringNodes/tree/master/Samples) and brief descriptions [here](https://github.com/dimven/SpringNodes/wiki/Node-Documentation), that can further demonstrate how some of the nodes work.

   Nobody likes squeaky springs. Therefore your recommendations and ideas on how to improve this package further are always welcome. Please be sure to report any [issues](https://github.com/dimven/SpringNodes/issues) or feedback directly to the repository.

   Some of the nodes provided in this package have been sprung by existing content, such as the wonderful SteamNodes, archi-lab.net, Clockwork and LunchBox, because every great mechanism could use a spare spring from time to time. The aim is to always improve upon the original content either by enabling additional functionality or opening up new uses. By giving it a new twist, we avoid affecting the original content's goals and direction.

### INSTALLATION

Installation is simple - just use Dynamo's built-in package manager and search for ```spring```.
   
### CHANGE LOG
------
#### 132.2.4 030318
- The ErrorReport.Parse and InterferenceCheck.Parse nodes got refactored and will now return integers instead of strings, when the "fetch elements" input is set to false or if the element is not found.
- A few new springlets:
	- Wall.IsCurtainWall is a simple node that quickly checks if a wall instance is a curtan wall
	- (Toolkit)Mesh.BoundingBox can be used to extract the bounding box representation of either a built in mesh or a toolkit mesh.
	- Geometry.DifferenciateDisplay is a basic CN wrapper around the built in Color Range node, used to quickly paint geometries or lists of geometries into easily distinguishable colours. 
	- Surface.TrimWithLoopsFix is my attemt at a workaround for issue #8600 in the Dynamo repo. It might fail with concave cutouts.

#### 132.2.3 210218
- New nodes:
	- List.ItemAtIndex+ is a just a basic custom node wrapper around the built-in design script sintax. Unlike the built-in GetItemAtIndex node, it works with negative indices.
	- Element.SetParameterToNone is useful when you need to set parameters such as View Template, Phase Demolished or Top Constraint to None / Unconstrained
	- BatchInstances.ByPointsLevels is similar to the built in node, however it uses the faster batch placement api method and can optionally avoid the element tracking mechanism, thus place instances on each run. Be sure to use manual run mode in such cases.
	
#### 132.2.2 180218
- The ElementsInView and LinkedInstanceElements collectors now use multi-category filters and return combined results. To revert to the old behaviour, apply a List.Chop(numbers=1) to the list of categories.
- The List.Randomise&Divide node's seed input now produces identical result for the same seeds.
- New nodes:
	- dsString.FromList converts a list of basic objects (numbers, strings, booleans, nulls) to a string that you can paste into a code block node. (use Clockwork's Clipboard.SendTo node to be able to paste it)
	- Voronoi2d.ByPoints is a simple workaround for the built in tessellation package when workigng with a set of planar points
	- List.FirstLast is a simple utility node to get just the head and tail of the list.

#### 132.2.1 010118
- Geometry/Point.BoxedDistanceTo is a quick way to numerically get the distance between the bounding box representations of two geometrical objects.
- Doc.CopyFromViewToView is useful when you need to copy over view-based elements such as tags, detail items, etc.
- Mesh.ToPolysurface refactored for readability and stability. This might have a slight negative effect on performance

#### 132.2.0 031217
- Some additions to the package:
	- Points.MinAreaRectangle builds up on the convex hull node and finds a rotated rectangle with the smallest point, that would fit all the points using a linear time algorithm
	- Quads.ByPointMatrix builds a list of quad points from nested lists of points
	- String.ReplaceIllegalChars is useful when you want to strip non-os characters from room and view names.
	- ToolkitMesh.Merge can be used to group many toolkit meshes into a single entity.
- The Revit selection nodes were revised and now include a linked transform
- Minor regression fixes.

#### 132.1.0 051017
- Most of the python nodes are set up to automatically promote their input to a list. The original idea behind this was to elliminate cases where we're starting multiple script scopes for a list of inputs. The scripts had a defined "output" function that could incorrectly demote the output to a singleton. For consistency reasons, the output functio has been removed and all affected nodes will always return a list. I realize this might break some existing workflows and apologise in advance, hopefully the added consistency will pay off in the long term. For graphs where you always worked with a singleton, add a List.FirstItem at the ned. And if you have any graphs where you worked with both single items and lists and wanted to preserve the old functionality, try using the newly added "RankOutput" node.
- Most of the design script nodes had a DS function inside even tho they took a single item as an input. That did not benefit us in any way and the additional function calls affected performance negatively (DS functions have a high cost in the Dynamo VM) and their names leaked into the main graph and were poluting the function lookup table. That lead to name clashes and undesired results. All DS nodes have been cleaned up and simplified.
- A few rarely used nodes have been depreciated (instance and type collectors). Check out the [depreciated page](https://github.com/dimven/SpringNodes/wiki/Depreciated-and-Changed-nodes-throughout-versions)
- I've added a few new additions, nothing major:
	- PolyCurve.ArcChamfer: similar to the chamfer node but tapers the curves with a variable radius arc instead of a line
	- PolyCurve.Fillet+ : a way to fillet both the CW and CCW sides of a polycurve.
	- BoundingBox.2dRectangle: a simple way to get a 2d rectangle from an element's boundign box
	- Polygon.3dArea: a numeric calculation to get the area of non intersecting polys in euclidean space
	- ViewInstance.ByPoint: similar in functionality with the Clockwork node but handles lists in a different way
	- RankOutput: a utility node to correctly rank puthon nodes' output based on their input
- Finally updated the node documentation on GitHub! :D

#### 121.1.1 170917
- Polygon.IsRectangular will tell you if any four points are square or rectangular.
- FamilyInstance.ByGeometry subcategory tweaks; now existing subcategories are assigned as expected
- other minor tweaks

#### 121.1.0 270817
- Geometry.ReadTag and Geometry.WriteTag are a pair of nodes that exploit the option to store custom information into any dynamo geometry.
- Doc.DeleteElement now has better null handling.

#### 121.0.3 190817
- Dictionary.ByKeysValues has an new optional default return. That means that if a  kay is not found, the default value will be used instead.
- The watch+ node can display information without writing the list indexes.
- The new FamilyTemplatePaths node simply points to the default templates folder and returns the mass and generic model templates.

#### 121.0.2 070817
- All namespace clashes with the List class from arch-lab.net should be fixed.
- Small bufgix in Element.SetLocation

#### 121.0.1 200617
- The DirectShape nodes now work in Revit 2018
- The Geometry.IndexByDistance node returns the distance between the elements


#### 121.0.0 170617
- All nodes that previously returned an empty list when an error occurs, return a null value instead. This is due to Dynamo's issues when processing empty lists. (like list rank reduction).
- The ElementType.Duplicate node now handles most element types. Previously the existing type detection was limited to floor, wall and instance types only.
- The File.Size and Number.ToString nodes now have additional functionality.
- The Polygon.ContainmentTest+ node now returns a list of bools (instead of a pair of in/out lists). This is to bring it more in line with Dynamo's other geometric nodes and provide easier coexistance with the core list management nodes.
- The Pt2Str and Ln2Str have been converted from DS to python for increased performance. (calling DS functions on thousands of elements has a big overhead) They also have additional rounding and trimming options.
- The Collector.ElementsInView now has an optional category input for when you'd like to get only the elements of a specific category.
- New nodes:
	- Doc.CentralPath: If the document is workshared, the node returns the path to the central document as a string. Otherwise a null value will be returned.
	- Doc.CopyFromLinkInstance: The node will use the total transformation of the link instance to copy the input elements into the local document.
	- Element.Unjoin: Unjoins the element(s) in the second list from the primary  input element.
	- ElementType.Instances: Fetches all instances of the input element type. (optimised for concurrent use with multiple types)
	- Geometry.IndexByDistance: Provides the index of the closest or farthest geometry. Should prove much faster than getting the geometry and finding its index in two separate operations.
	- ScopeBox.Geometry: Fetches the base curve and solid representation of a scope box element.
	- RevitProcess.EmptyWorkingSet: Use at your own risk! Removes as many pages as possible from the working set of the active Revit session. (I've seen some improvements in performance by doing this in cases where Dynamo has been running for a while and has accumulated a lot of memory and after closing it, fails to release that memory.)


#### 110.2.0 190217
- Minor bug fixes and two new nodes for working with 2d:
	- Polygon.2DArea, used to quickly get the 2d area of a polygon using simple numeric calculations.
	- Delaunay2D.ByPoints, is a fix for the built in node with the same name. It works with 2d collections of points.

#### 110.1.0 300117
- ErrorReport/InterferenceCheck.Parse get a big speed boost from improved iteration.
- BrepShape/DirectShape.ByGeometry have been revised in accordance with issue #25
- Collector.ElementSketch has been revised to improve performance (if elementid - 1 is a sketch, avoid an expensive sub-transaction)
- List management (like the Dictionary.ByKeysValues and List.MergeBuBoolMask) nodes's inputs have been revised so that they work better with nested lists and the new list@level functionality.
- Bugs in Feet2Fraction & Fraction2Feet fixed. However DesignScript functions have been behaving problematically. (VM failing to register the function inside a custom node).
- New Node: Elements.GroupByDistance provides a functionality very similar to the Geometry.GroupByDistance node. By pairing each element with a geometry, we cal quickly detect element groups.

#### 110.0.2 291116
- Fix for #20

#### 110.0.1 101116
- Fixed a regression in Element.SetLocation, that I created previously, when cleaning up old Revit2014 code.

#### 110.0.0 061116
- New nodes:
	- Springs.BrepShape.ByGeometry works only in Revit 2017 and later and implements the new BrepBuilder class to generate DirectShapes with materials. However, poly-surfaces and solids with periodic faces like spheres, cylinders and cones are not supported at thistime.
	- Springs.SelectFaces+ works in a similar manner to the built in node, with the exception that it provides a valid face reference for family instance elements and the global picl point during selection. You can use the pick point to easily identfy the correct face for planar surfaces with multiple loops.
	- Springs.BoundingBox.MidPoint is a simple utility node that can quickly compute the mid point between a BB's min and max extent.
	- Springs.Points.ConvexHull2D is an evolution of Clockwork's "UV.ConvexHull2D".
- The DirectShapeType implementation has been revised in an attempt to make it more robust between Revit sessions.
- All UI nodes now have an additional "CustomMsg" input to provide additional insight when using the nodes with DynamoPlayer.
- The serialization nodes now have an optional separator input to customize the output for use with some CSV files.
- The even/odd list utility node have been merged.

#### 100.0.1 140716
- Sheet.Views+ got a big speed boost
- Doc.DeleteElements now handles elements that could not be deleted and returns their ids as a chained string

#### 100.0.0 130716
- A lot of nodes provided duplicate functionality or needed refactoring and were removed / replaced. You can find a full list of the changes [here](https://github.com/dimven/SpringNodes/wiki/Depreciated-and-Changed-nodes-throughout-versions)
- The library organisation has been revised. Everything is now under the "Springs" tab. All nodes have a "Springs" prefix so that users don't have to wonder where that node comes from.
- As Dynamo 0.82 was the last version that supported Revit 2014, Spring Nodes no longer targets Revit 2014.
- New nodes:
	- Geometry.Extents fetches the W/L/H of a geometry object.
	- Mesh.ToToolkitMesh converts a dynamo mesh (like the one you'd get from a toposurface) to a mesh toolkit mesh
- Refactored nodes:
	- Geometry.GroupByDistance acts similarly to archi-lab's "Group Curves" node and the "Lines.GroupAndFixCorners" but works for all types of geometry
	- LineLoop.Merge replaces the "Lines.GroupAndFixCorners" after you've first grouped the lines with the "Geometry.GroupByDistance" node.
	- Mesh.ToPolySurface is now multithreaded and replaces the "Topography.ToPolySurface" node. This way you can also process meshes obtained through other means and still handle toposurfaces by first extracting their mesh with the built-in "Topography.Mesh" node.
	- ElementType.Duplicate is similar to Clockwork's node with the same name but can handle duplicate names. It will be merged with clockwork's node after Clockwork 1.0

#### 82.9.1 220516
- New nodes:
	- AdaptiveFamily.ByFacetedGeometry will genearate a new adaptive component family type from any solid or polysurface consisting of planar faces.
	- List.MergeByBoolMask will merge two lists by a third of true and false values.
	- List.Subpairs is similar in principle to the built-in Sublists node.
	- PolyCurve.Chamfer creates chamfered edges with the specified distance. Neeeds to be tweaked for 1.0
- Geometry.SplitRecursively(Dir) is an alternative of the node with the same name. It has an additional point.geometry input that defines the general direction of the split. The old node does not function as expexted when lines are used as the split tools.

#### 82.8.3 080516
- New node: PlanarFace.FixDomain fixes PointAtParameter for 3&4 corner planar revit faces.
- ClosedCurve.Offset+(0.90) merged into main node(alternative solution)
- Element.AddVoidCut now accepts a new integer based lacing input
- List.DropFirstLast also lists the removed items

#### 82.8.2 040416
- tiny bugfix

#### 82.8.1 040416
- AreaPlan.ByLevelName, "Select Linked Face" revised.

#### 82.8.1 030416
- Lots of tiny optimizations.
- New nodes:
	- AreaPlan.ByLevelName will generate new area plans.
	- Polygon.ContainmentTest+ should perform a bit faster than the built-in node at the cost of some accuracy
	- FamilyInsance.ByFacePoints will place multiple face based families on a target face
	- "Select Elements (ordered)" and "Select Linked Elements (ordered)" will preserve the order of selection of your elements.

#### 82.7.8 250216
- General bug cleaning and optimization.

#### 82.7.7 180216
- DirectShape.Transform added. (vector node renamed to DS.Translate)
- Topography.ToPolySurface(py) added. Should provide a 5-10% boost compared to the DS version.

#### 82.7.6 090216
- Element Collectors get a much needed maintenance.

#### 82.7.5 010216
- Even more general maintenance.
- FamilyInstance.ByGeometry and Form.ByGeometry now support localized versions of Revit.

#### 82.7.4 280116
- More general maintenance.
- All collector nodes now have a refresh toggle.
- Sheet.Views+ now collects schedules as well.

#### 82.7.4 280116
- Sheet.Views+ now lists schedules as well.

#### 82.7.3 270116
- General maintenance. Converted most for loops to xrange loops.
- All UI nodes now have an optional "names" input. This should make handling named objects such as views and sheets much easier.
- Watch+ is a new UI node that provides an alternative to the built-in watch node.

#### 82.7.2 140116
- Bug fixes:
	- FamilyInstance.ByGeometry was failing to assign a subcategory when no material was in use ( Thanks Jeremy)
	- HostedInstance.ByPoints did not work for non-active family types.
- New nodes:
	- ErrorReport.Parse is an awesome way of making sence of Revit errors and fetching the offending elements.
	- InterferenceCheck.Parse similar to the error report node but for interference checks.

#### 82.7.1 100116
- Bug fixes:
	- Element.SetLocation works in Revit 2014 once again
- New nodes:
	- Collector.ElementSketch: fetches the actual geometry curves used to generate the element; can optionally fetch the model curve equivalents - this opens the (dangerous) functionality of moving and deleting curve loops that represent openings for example.
	- Select Edges: Fetches multiple edges and converts them to Dynamo geometry.
	- List.DragDropReorder: My current pride and joy - a node that allows us to visually reorder the elements of a list.
	- Point.PullOntoPlane: Pulls a point along the plane normal. The Geom.ClosestTo was producing errors for some reason...
- New functionality/changes:
	- FamilyInstance.ByGeometry has a new optional Subcategory input. Also by popular demand, the newly generated geometry is now placed next to the family origin. The node is out of BETA (as long as it behaves) and can be found under SpringNodes>Revit>FamilyInstances
	- "Filter.BySelection" and "List.DropDown" are out of BETA as well and have been moved to SpringNodes>Lists. They've also received a new paint job and support nested lists.

#### 82.6.1 061215
- Bug fixes:
	- DirectShape.ByGeometry. The element was being offset from the origin.
	- SelectInRevit will now work in R16.
	- FamilyInstance.ByGeometry will now work in R16.
- New nodes:
	-Element.AddVoidCut, Element.RemoveVoidCut, Element.IsCut and Element.IsCutting for managing void cuts in a variety of ways. Works great in combination with FamilyInstance.ByGeometry.
	- Select Linked Face will enable face selection from linked files.
	- List.Split is a very simple but a time saving node for easy list management.
	- Line.StraightenXY and Line.StraightenZ can be used to axially align lines. Usefull with those pesky Revit errors.
	- Curve.Offset+ and ClosedCurve.Offset+(there's a special version for 0.9 due to name changes) improve the default offset functionality.

#### 82.5.0 171115
- Minor maintenance on "SelectInRevit" and "Collector.LinkedInstanceElements".
	- The collector was outputting vectors because I was only using it for links that were moved and were not mirrored or rotated/
	- The node now outputs coordinate systems that can be used to correctly relocate the geometry.
- New geometry node, "N-hedron.ByOriginVector", used to generate multi - sided polyhedrons. (pyramids)
- New _BETA_ features. These feateres may proove more unstable than usual:
	- "FamilyInstance.ByGeometry" generates a new family in the background of the currently open document and places an instance of that family.
	- "Filter.BySelection" and "List.DropDown" each provide a custom interface for object selection and management.

#### 82.4.0 121115
- DirectShape.ByGeometry and Form.ByGeometry have been completely revised
	- the (SAT) versions have been depreciated and merged into the main node
	- the node is now unitless
	- better error handling and error messages
- Sheet.Views+ now supports Revit 2014

#### 82.3.3 021115
- new List.EveryOther node added. As the name stipulates, it creates a new list for each list element and drops the corresponding element.
- new FamilyInstance.Rotation node added. It fetches a point based element's rotation around its insertion point.
- new CurveLoop.Simplify node added. Design script based. It attempts to merge continuous straight curves into a single line.

#### 82.3.2 021015
- Two nodes for converting Revit decimal colours to Dynamo colours and back added. ( Color2Decimal & Decimal2Color)

#### 82.3.1 021015
- Two new nodes for Converting between fractional and decimal feet added.

#### 82.3.0 021015
- Two new nodes for fetching elements from linked files added.

#### 82.2.3 011015
- Form.ByGeometry(SAT) added.

#### 82.2.2 011015
- New node BoundingBox.Scale added
- DirectShape.ByGeometry(SAT) added. It uses a more robust SAT import method.

#### 82.2.1 290915
- Form.ByGeometry improvements
- small bug fixes
#### 82.2.0 280915
- new Element.Copy and DirectShape.Translate nodes
- more robust DirectShape.ByGeometry node (had to downgrade back to 0.82 due to regression https://github.com/DynamoDS/Dynamo/issues/5371)
- Dictionary.ByKeysValues can handle search for missing keys

#### 82.1.2 270915
- Fixed bug in DirectShape.ByGeometry

#### 82.1.1 270915
- Initial release
