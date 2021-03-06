Paramak
=======

The Paramak python package allows rapid production of 3D CAD models of fusion
reactors. The purpose of the Paramak is to provide geometry for parametric
studies. It is possible to use the created geometry in engineering and
neutronics studies as the STP files produced can be automatically converted to
DAGMC compatible neutronics models or meshed and used in finite element
analysis codes.

Features have been added to address particular needs and the software is by no
means a finished product. Contributions are welcome. CadQuery functions provide
the majority of the features, and incorporating additional capabilities is
straightforward for developers with Python knowledge.

.. toctree::
   :maxdepth: 1

   paramak.parametric_shapes
   paramak.parametric_components
   paramak.parametric_reactors
   paramak.core_modules
   example_parametric_shapes
   example_parametric_components
   example_parametric_reactors
   example_neutronics_simulations
   tests

Prerequisites
-------------

To use the paramak tool you will need Python 3 and Cadquery 2.0 or newer
installed.

* `Python 3 <https://www.python.org/downloads/>`_

* `CadQuery 2.0 <https://github.com/CadQuery/cadquery>`_

Cadquery 2.0 must be installed in a conda environment via conda-forge.
Conda environments are activated using Anaconda or Miniconda. 

* `Anaconda <https://www.anaconda.com/>`_
* `Miniconda <https://docs.conda.io/en/latest/miniconda.html>`_

Once you have activated a conda environment, Cadquery 2.0 can be installed
using the command:

.. code-block:: python

   conda install -c conda-forge -c cadquery cadquery=2

A more detailed description of installing Cadquery 2.0 can be found here:

* `Cadquery 2.0 installation <https://cadquery.readthedocs.io/en/latest/installation.html>`_


Installation
------------

The quickest way to install the Paramak is to use pip. In the terminal type...

.. code-block:: python

   pip install paramak

Alternatively you can download the repository using the `download link <https://github.com/ukaea/paramak/archive/develop.zip>`_ or clone the repository using:

.. code-block:: python

   git clone https://github.com/Shimwell/paramak.git

Navigate to the paramak repository and within the terminal install the paramak
package and the dependencies using pip3.

.. code-block:: python

   pip install .

Alternatively you can install the paramak with the following command.

.. code-block:: python

   python setup.py install

Docker
------

The paramak is availabie as a Docker image and can be downloaded using Docker
commands.

.. code-block:: bash

   docker build -t openmcworkshop/paramak . 

   docker run -it openmcworkshop/paramak

Presentations
-------------

Currently we just have one presentation that covers the Paramak.

`Link to presentation <https://github.com/ukaea/paramak/files/5260982/UKAEA_Paramak_shimwell.pdf>`_


Features
--------

In general the Paramak takes points and connection information in 2D space
(x,z) and performs operations on them to create 3D volumes. The points and
connections can be provided by the user or when using parametric_shapes the
points and connections are calculated by the software.

Once points and connections between the points are provided, the user has
options to perform CAD operations (rotate or extrude) to create a 3D volume and
boolean operations like cut, union or intersect.

The different families of shapes that can be made with the Paramak are shown in
the table below. The CadQuery objects created can be combined and modified
using CadQuery's powerful filtering capabilties to create more complex models
(e.g. a Tokamak).


.. |rotatestraight| image:: https://user-images.githubusercontent.com/56687624/87055469-4f070180-c1fc-11ea-9679-a29e37a90e15.png
                          :height: 200px

.. |extrudestraight| image:: https://user-images.githubusercontent.com/56687624/87055493-56c6a600-c1fc-11ea-8c58-f5b62ae72e0e.png
                          :height: 200px

.. |rotatespline| image:: https://user-images.githubusercontent.com/56687624/87055473-50382e80-c1fc-11ea-95dd-b4932b1e78d9.png
                          :height: 200px

.. |extrudespline| image:: https://user-images.githubusercontent.com/56687624/87055500-58906980-c1fc-11ea-879c-9f1845be3b57.png
                          :height: 200px

.. |rotatecircle| image:: https://user-images.githubusercontent.com/56687624/87055489-54fce280-c1fc-11ea-9545-a61582aea20a.png
                          :height: 200px

.. |extrudecircle| image:: https://user-images.githubusercontent.com/56687624/87055517-5b8b5a00-c1fc-11ea-83ef-d4329c6815f7.png
                          :height: 200px

.. |rotatemixed| image:: https://user-images.githubusercontent.com/56687624/87055483-53cbb580-c1fc-11ea-878d-92835684c8ff.png
                          :height: 200px

.. |extrudemixed| image:: https://user-images.githubusercontent.com/56687624/87055511-59c19680-c1fc-11ea-8740-8c7987745c45.png
                          :height: 200px



+-----------------------------------------------------------+-----------------------------------------------------------+------------------------------------------------------------+
|                                                           | Rotate                                                    | Extrude                                                    |
+===========================================================+===========================================================+============================================================+
| Points connected with straight lines                      | |rotatestraight|                                          | |extrudestraight|                                          |
|                                                           |                                                           |                                                            |
|                                                           |                                                           |                                                            |
|                                                           |                                                           |                                                            |
|                                                           |                                                           |                                                            |
|                                                           | ::                                                        | ::                                                         |
|                                                           |                                                           |                                                            |
|                                                           |     RotateStraightShape()                                 |     ExtrudeStraightShape()                                 |
+-----------------------------------------------------------+-----------------------------------------------------------+------------------------------------------------------------+
| Points connected with spline curves                       | |rotatespline|                                            | |extrudespline|                                            |
|                                                           |                                                           |                                                            |
|                                                           |                                                           |                                                            |
|                                                           |                                                           |                                                            |
|                                                           |                                                           |                                                            |
|                                                           | ::                                                        | ::                                                         |
|                                                           |                                                           |                                                            |
|                                                           |     RotateSplineShape()                                   |     ExtrudeSplineShape()                                   |
+-----------------------------------------------------------+-----------------------------------------------------------+------------------------------------------------------------+
| Points connected with a circle                            | |rotatecircle|                                            | |extrudecircle|                                            |
|                                                           |                                                           |                                                            |
|                                                           |                                                           |                                                            |
|                                                           |                                                           |                                                            |
|                                                           |                                                           |                                                            |
|                                                           | ::                                                        | ::                                                         |
|                                                           |                                                           |                                                            |
|                                                           |     RotateCircleShape()                                   |     ExtrudeCircleShape()                                   |
+-----------------------------------------------------------+-----------------------------------------------------------+------------------------------------------------------------+
| Points connected with a mixture                           | |rotatemixed|                                             | |extrudemixed|                                             |
|                                                           |                                                           |                                                            |
| ::                                                        |                                                           |                                                            |
|                                                           |                                                           |                                                            |
| (splines, straights and circles)                          |                                                           |                                                            |
|                                                           | ::                                                        | ::                                                         |
|                                                           |                                                           |                                                            |
|                                                           |     RotateMixedShape()                                    |     ExtrudeMixedShape()                                    |
+-----------------------------------------------------------+-----------------------------------------------------------+------------------------------------------------------------+


Usage - Parametric Shapes
-------------------------

There are a collection of Python scripts in the example folder that demonstrate
simple shape construction and visualisation. However here is a quick example of
a RotateStraightShape.

After importing the class the user then sets the points. By default, points
should be a list of (x,z) points. In this case the points are connected with
straight lines.

.. code-block:: python

   import paramak

   my_shape = paramak.RotateStraightShape(points = [(20,0), (20,100), (100,0)])

Once these properties have been set then users can write 3D volumes in CAD STP
or STL formats.

.. code-block:: python

   my_shape.export_stp('example.stp')

   my_shape.export_stl('example.stl')

.. image:: https://user-images.githubusercontent.com/56687624/88935761-ff0ae000-d279-11ea-8848-de9b486840d9.png
   :width: 350
   :height: 300
   :align: center

Usage - Parametric Components
-----------------------------

Parametric components are wrapped versions of the eight basic shapes where
parameters drive the construction of the shape. There are numerous parametric
components for a variety of different reactor components such as center columns,
blankets, poloidal field coils. This example shows the construction of a
plasma. Users could also construct a plasma by using a RotateSplineShape()
combined with coordinates for the points. However a parametric component called
Plasma can construct a plasma from more convenient parameters. Parametric
components also inherit from the Shape object so they have access to the same
methods like export_stp() and export_stl().

.. code-block:: python

   import paramak

   my_plasma = paramak.Plasma(major_radius=620, minor_radius=210, triangularity=0.33, elongation=1.85)

   my_plasma.export_stp('plasma.stp')

.. image:: https://user-images.githubusercontent.com/56687624/88935871-1ea20880-d27a-11ea-82e1-1afa55ff9ba8.png
   :width: 350
   :height: 300
   :align: center

Usage - Parametric Reactors
---------------------------

Parametric Reactors() are wrapped versions of a combination of parametric
shapes and components that comprise a particular reactor design. Some
parametric reactors include a ball reactor and a submersion ball reactor. These
allow full reactor models to be constructed by specifying a series of simple
parameters. This example shows the construction of a simple ball reactor
without the optional outer pf and tf coils.

.. code-block:: python

   import paramak

   my_reactor = paramak.BallReactor(
      inner_bore_radial_thickness = 50,
      inboard_tf_leg_radial_thickness = 50,
      center_column_shield_radial_thickness= 50,
      divertor_radial_thickness = 100,
      inner_plasma_gap_radial_thickness = 50,
      plasma_radial_thickness = 200,
      outer_plasma_gap_radial_thickness = 50,
      firstwall_radial_thickness = 50,
      blanket_radial_thickness = 100,
      blanket_rear_wall_radial_thickness = 50,
      elongation = 2,
      triangularity = 0.55,
      number_of_tf_coils = 16,
      rotation_angle = 180
   )

   my_reactor.name = 'BallReactor'
   
   my_reactor.export_stp()

.. image:: https://user-images.githubusercontent.com/56687624/89203299-465fdc00-d5ac-11ea-8663-a5b7eecfb584.png
   :width: 350
   :height: 300
   :align: center

Usage - Reactor Object
----------------------

A reactor object provides a container object for all Shape objects created, and
allows operations to be performed on the whole collection of Shapes.

.. code-block:: python

   import paramak

Initiate a Reactor object and pass a list of all Shape objects to the
shapes_and_components parameter.

.. code-block:: python

   my_reactor = paramak.Reactor(shapes_and_components = [my_shape, my_plasma])

A html graph of the combined Shapes can be created.

.. code-block:: python

   my_reactor.export_html('reactor.html')


Usage - Neutronics Model Creation
---------------------------------

First assign stp_filenames to each of the Shape objects that were created
earlier on.

.. code-block:: python

   my_shape.stp_filename = 'my_shape.stp'

   my_plasma.stp_filename = 'my_plasma.stp'

Then assign material_tags to each of the Shape objects.

.. code-block:: python

   my_shape.material_tag = 'steel'

   my_plasma.material_tag = 'DT_plasma'

Note - Tetrahedral meshes can also be assigned to Shape objects.

Now add the Shape objects to a freshly created reactor object.

.. code-block:: python

   new_reactor = Reactor([my_shape, my_plasma])

The entire reactor can now be exported as step files. This also generates a
DAGMC graveyard automatically.

.. code-block:: python

   my_reactor.export_stp()

A manifest.json file that contains all the step filenames and materials can now
be created.

.. code-block:: python

   my_reactor.export_neutronics_description()

Once you step files and the neutronics description has been exported then `Trelis <https://www.csimsoft.com/trelis>`_ can be used to generate a DAGMC geometry in the usual manner. There is also a convenient script included in task 12 of the UKAEA openmc workshop which can be used in conjunction with the neutronics description json file to automatically create a DAGMC geometry. Download `this script <https://github.com/ukaea/openmc_workshop/blob/master/tasks/task_12/make_faceteted_neutronics_model.py>`_ and place it in the same directory as the manifest.json and step files. Then run the following command from the terminal. You will need to have previously installed the `DAGMC plugin <https://github.com/svalinn/Trelis-plugin>`_ for Trelis.

::

   trelis make_faceteted_neutronics_model.py

Alternatively, run this without the GUI in batch mode using:

::

   trelis -batch -nographics make_faceteted_neutronics_model.py

This should export a h5m file for use in DAGMC.

Further information on DAGMC neutronics can be found `here <https://svalinn.github.io/DAGMC/>`_ and information on OpenMC can be found `here <https://openmc.readthedocs.io/>`_ . The two codes can be used together to simulate neutron transport on the h5m file created. The UKAEA openmc workshop also has two tasks that might be of interest `task 10 <https://github.com/ukaea/openmc_workshop/tree/master/tasks/task_10>`_ and `task 12 <https://github.com/ukaea/openmc_workshop/tree/master/tasks/task_12>`_ .


Example Scripts
---------------

There are several example scripts in the `examples folder <https://github.com/ukaea/paramak/blob/develop/examples/>`_ . A good one to start with is `make_CAD_from_points <https://github.com/ukaea/paramak/blob/develop/examples/make_CAD_from_points.py>`_ which makes simple examples of the different types of shapes (extrude, rotate) with different connection methods (splines, straight lines and circles).
