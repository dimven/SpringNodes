![Image](spring nodes logo.jpg)

Spring Nodes is a custom node package for [Dynamo](http://www.dynamobim.org) .

Every great mechanism could use a spring from time to time. Spring Nodes's goal is to fill a niche and keep things short and simple. It's main focus is on improving Dynamo's interaction with Revit and explore any means that can help accelerate BIM work-flows.

Some nodes provided in this package have been inspired by existing content, such as the wonderful "SteamNodes", "archi-lab.net", "Clockwork" and "LunchBox" packages. The aim is to improve upon the original content in one way or another, by giving it a new twist and open up new functionalists and uses, without affecting its direction in any way.

Your recommendations and ideas on how to improve this package are always welcome. Please be sure to report any issues.

CHANGE LOG

82.2.0 280915
- new Element.Copy and DirectShape.Translate nodes
- more robust DirectShape.ByGeometry node (had to downgrade back to 0.82 due to regression https://github.com/DynamoDS/Dynamo/issues/5371)
- Dictionary.ByKeysValues can handle search for missing keys

82.1.2	270915
- Fixed bug in DirectShape.ByGeometry

82.1.1	270915
-Initial release