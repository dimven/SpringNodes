![Image](spring nodes logo.jpg)

Spring Nodes is a custom node package for [Dynamo](http://www.dynamobim.org) .

Every great mechanism could use a spring from time to time. Spring Nodes's goal is to fill a niche and keep things short and simple. It's main focus is on improving Dynamo's interaction with Revit and explore any means that can help accelerate BIM work-flows.

Some nodes provided in this package have been inspired by existing content, such as the wonderful "SteamNodes", "archi-lab.net", "Clockwork" and "LunchBox" packages. The aim is to improve upon the original content in one way or another, by giving it a new twist and open up new functionalists and uses, without affecting its direction in any way.

Your recommendations and ideas on how to improve this package are always welcome. Please be sure to report any issues.

CHANGE LOG

82.6.1 061215
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

82.5.0 171115
- Minor maintenance on "SelectInRevit" and "Collector.LinkedInstanceElements".
	- The collector was outputting vectors because I was only using it for links that were moved and were not mirrored or rotated/
	- The node now outputs coordinate systems that can be used to correctly relocate the geometry.
- New geometry node, "N-hedron.ByOriginVector", used to generate multi - sided polyhedrons. (pyramids)
- New _BETA_ features. These feateres may proove more unstable than usual:
	- "FamilyInstance.ByGeometry" generates a new family in the background of the currently open document and places an instance of that family.
	- "Filter.BySelection" and "List.DropDown" each provide a custom interface for object selection and management.

82.4.0 121115
- DirectShape.ByGeometry and Form.ByGeometry have been completely revised
	- the (SAT) versions have been depreciated and merged into the main node
	- the node is now unitless
	- better error handling and error messages
- Sheet.Views+ now supports Revit 2014

82.3.3 021115
- new List.EveryOther node added. As the name stipulates, it creates a new list for each list element and drops the corresponding element.
- new FamilyInstance.Rotation node added. It fetches a point based element's rotation around its insertion point.
- new CurveLoop.Simplify node added. Design script based. It attempts to merge continuous straight curves into a single line.

82.3.2 021015
- Two nodes for converting Revit decimal colours to Dynamo colours and back added. ( Color2Decimal & Decimal2Color)

82.3.1 021015
- Two new nodes for Converting between fractional and decimal feet added.

82.3.0 021015
- Two new nodes for fetching elements from linked files added.

82.2.3 011015
- Form.ByGeometry(SAT) added.

82.2.2 011015
- New node BoundingBox.Scale added
- DirectShape.ByGeometry(SAT) added. It uses a more robust SAT import method.

82.2.1 290915
- Form.ByGeometry improvements
- small bug fixes
82.2.0 280915
- new Element.Copy and DirectShape.Translate nodes
- more robust DirectShape.ByGeometry node (had to downgrade back to 0.82 due to regression https://github.com/DynamoDS/Dynamo/issues/5371)
- Dictionary.ByKeysValues can handle search for missing keys

82.1.2	270915
- Fixed bug in DirectShape.ByGeometry

82.1.1	270915
-Initial release