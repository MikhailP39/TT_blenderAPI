# Grouping objects using geometry nodes
## Purpose
The aim of the task is to verify the ability to use Blender.
## Task
Using version 3.1 of Blender, create a python script that:

* Will create 2 collections named "DISTRIBUTOR" and "CONTENTS"
* In the CONTENTS collection, it will create one primitive object - a cube, a sphere, a cone, a cylinder
* In the collection DISTRIBUTOR will create any object to which it will add the "Geometry Nodes" modifier, which should:
    * At the input in "Group Input" have the following fields:
        * Contents - allows you to select a collection
        * Min in group - The minimum number of objects in the group. Make sure that it is possible to give integer values ​​in the range 1-3
        * Max in group - The maximum number of objects in the group. Make sure that it is possible to give integer values ​​in the range 4-6
    * Objects from the collection that is set in the "Contents" field will be placed on a straight line
    * Objects should be arranged in groups, the size of which is randomly selected from the range "Min in group" - "Max in group", e.g. we place a cube, the size of the group is 3, so there will be 3 cubes next to each other, then we place the ball, the size of the group is 2, so there are 2 spheres next to each other, and so on. The way in which the objects to be set are selected is arbitrary, for example we can take objects from the collection one by one.

## Result
The result is a python script that, when run in Blender, will create the elements described above.