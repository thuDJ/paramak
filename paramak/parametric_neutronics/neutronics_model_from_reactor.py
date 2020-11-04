import json
import os
import warnings
from collections import defaultdict
from pathlib import Path
from random import random

import matplotlib.pyplot as plt

try:
    from parametric_plasma_source import SOURCE_SAMPLING_PATH, PlasmaSource
except BaseException:
    warnings.warn('parametric_plasma_source not found distributed plasma \
            sources are not avaialbe in Neutronics simulations', UserWarning)

try:
    import openmc
except BaseException:
    warnings.warn('OpenMC not found, NeutronicsModelFromReactor.simulate \
            method not available', UserWarning)

try:
    import neutronics_material_maker as nmm
except BaseException:
    warnings.warn("neutronics_material_maker not found, \
            NeutronicsModelFromReactor.materials can't accept strings or \
            neutronics_material_maker objects", UserWarning)


class NeutronicsModelFromReactor():
    """Creates a neuronics model of the provided reactor geometry with assigned
    materials, plasma source and neutronics tallies.

    Arguments:
        reactor: (paramak.Reactor): The reactor object to convert to a
            neutronics model. e.g. reactor=paramak.BallReactor() or
            reactor=paramak.SubmersionReactor() .
        materials: (dict): Where the dictionary keys are the material tag
            and the dictionary values are either a string, openmc.Material,
            neutronics-material-maker.Material or
            neutronics-material-maker.MultiMaterial. All components within the
            Reactor() object must be accounted for. Material tags required
            for the reactor can be obtained with Reactor().material_tags.
        cell_tallies: (list of strings): the cell based tallies to calculate,
            options include TBR, heat and flux
        mesh_tallies_2D: (list of strings): the 2D mesh based tallies to
            calculate, options include TBR, heat and flux
        fusion_power: (float): the power in watts emitted by the fusion
            reaction recalling that each DT fusion reaction emitts 17.6 MeV or
            2.819831e-12 Joules
        method: (str): The method to use when making the imprinted and
            merged geometry. Options are 'trelis' or 'ppp'. Further details
            on imprinting and merging are available on the DAGMC homepage
            https://svalinn.github.io/DAGMC/usersguide/trelis_basics.html
            The Parallel-PreProcessor is an open-source tool available
            https://github.com/ukaea/parallel-preprocessor and can be used
            in conjunction with the OCC_faceter
            (https://github.com/makeclean/occ_faceter) to create imprinted
            and merged geometry while Trelis (also known as Cubit) is
            available from the CoreForm website https://www.coreform.com/
        simulation_batches: (int): the number of batch to simulate.
        simulation_particles_per_batch: (int): particles per batch.
        ion_density_origin: (float): 1.09e20,
        ion_density_peaking_factor: (float): 1,
        ion_density_pedestal: (float): 1.09e20,
        ion_density_separatrix: (float): 3e19,
        ion_temperature_origin: (float): 45.9,
        ion_temperature_peaking_factor: (float): 8.06,
        ion_temperature_pedestal: (float): 6.09,
        ion_temperature_separatrix: (float): 0.1,
        pedestal_radius: (float): 0.8 * 2.92258,
        shafranov_shift: (float): 0.44789,
        triangularity: (float): 0.270,
        ion_temperature_beta: (float): 6,
        merge_tolerance(float): the tolerance to use when merging surfaces.
            Defaults to 1e-4.
        faceting_tolerance(float): the tolerance to use when faceting surfaces.
            Defaults to 1e-1.
    """

    def __init__(
        self,
        reactor,
        materials,
        fusion_power=1e9,
        method='trelis',
        simulation_batches=100,
        simulation_particles_per_batch=10000,
        max_lost_particles=10,
        faceting_tolerance=1e-1,
        merge_tolerance=1e-4,
        cell_tallies=None,
        mesh_tallies_2D=None,
        source=None
    ):

        self.reactor = reactor
        self.materials = materials
        self.cell_tallies = cell_tallies
        self.mesh_tallies_2D = mesh_tallies_2D
        self.method = method
        self.simulation_batches = simulation_batches
        self.simulation_particles_per_batch = simulation_particles_per_batch
        self.max_lost_particles = max_lost_particles
        self.faceting_tolerance = faceting_tolerance
        self.merge_tolerance = merge_tolerance
        self.source = source
        self.fusion_power = fusion_power

        self.model = None

        # Only 360 degree models are supported for now as reflecting surfaces
        # are needed for sector models and they are not currently supported
        if reactor.rotation_angle != 360:
            reactor.rotation_angle = 360
            print('remaking reactor as it was not set to 360 degrees')
            reactor.solid
            # TODO make use of reactor.create_solids() here

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        self._source = value

    @property
    def faceting_tolerance(self):
        return self._faceting_tolerance

    @faceting_tolerance.setter
    def faceting_tolerance(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError(
                "NeutronicsModelFromReactor.faceting_tolerance should be a\
                number (floats or ints are accepted)")
        if value < 0:
            raise ValueError(
                "NeutronicsModelFromReactor.faceting_tolerance should be a\
                positive number")
        self._faceting_tolerance = value

    @property
    def merge_tolerance(self):
        return self._merge_tolerance

    @merge_tolerance.setter
    def merge_tolerance(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError(
                "NeutronicsModelFromReactor.merge_tolerance should be a\
                number (floats or ints are accepted)")
        if value < 0:
            raise ValueError(
                "NeutronicsModelFromReactor.merge_tolerance should be a\
                positive number")
        self._merge_tolerance = value

    @property
    def cell_tallies(self):
        return self._cell_tallies

    @cell_tallies.setter
    def cell_tallies(self, value):
        if value is not None:
            if not isinstance(value, list):
                raise ValueError(
                    "NeutronicsModelFromReactor.cell_tallies should be a\
                    list")
            output_options = ['TBR', 'heat', 'flux', 'fast flux', 'dose']
            for entry in value:
                if entry not in output_options:
                    raise ValueError(
                        "NeutronicsModelFromReactor.cell_tallies argument",
                        entry,
                        "not allowed, the following options are supported",
                        output_options)
        self._cell_tallies = value

    @property
    def materials(self):
        return self._materials

    @materials.setter
    def materials(self, value):
        if not isinstance(value, dict):
            raise ValueError("NeutronicsModelFromReactor.materials should be a\
                dictionary")
        self._materials = value

    @property
    def simulation_batches(self):
        return self._simulation_batches

    @simulation_batches.setter
    def simulation_batches(self, value):
        if isinstance(value, float):
            value = int(value)
        if not isinstance(value, int):
            raise ValueError(
                "NeutronicsModelFromReactor.simulation_batches should be an int")
        self._simulation_batches = value

    @property
    def simulation_particles_per_batch(self):
        return self._simulation_particles_per_batch

    @simulation_particles_per_batch.setter
    def simulation_particles_per_batch(self, value):
        if isinstance(value, float):
            value = int(value)
        if not isinstance(value, int):
            raise ValueError(
                "NeutronicsModelFromReactor.simulation_particles_per_batch\
                    should be an int")
        self._simulation_particles_per_batch = value

    def create_materials(self):
        # checks all the required materials are present
        for reactor_material in self.reactor.material_tags:
            if reactor_material not in self.materials.keys():
                raise ValueError(
                    "material included by the reactor model has not \
                    been added", reactor_material)

        # checks that no extra materials we added
        for reactor_material in self.materials.keys():
            if reactor_material not in self.reactor.material_tags:
                raise ValueError(
                    "material has been added that is not needed for this \
                    reactor model", reactor_material)

        openmc_materials = {}
        for material_tag, material_entry in self.materials.items():
            if isinstance(material_entry, str):
                material = nmm.Material(
                    material_entry, material_tag=material_tag)
                openmc_materials[material_tag] = material.openmc_material
            elif isinstance(material_entry, openmc.Material):
                # sets the material name in the event that it had not been set
                material_entry.name = material_tag
                openmc_materials[material_tag] = material_entry
            elif isinstance(material_entry, (nmm.Material, nmm.MultiMaterial)):
                # sets the material tag in the event that it had not been set
                material_entry.material_tag = material_tag
                openmc_materials[material_tag] = material_entry.openmc_material
            else:
                raise ValueError("materials must be either a str, \
                    openmc.Material, nmm.MultiMaterial or nmm.Material object \
                    not a ", type(material_entry), material_entry)

        self.openmc_materials = openmc_materials

        self.mats = openmc.Materials(list(self.openmc_materials.values()))

        return self.mats

    def create_neutronics_geometry(self, method=None):
        """Produces a dagmc.h5m neutronics file compatable with DAGMC
        simulations. This is done by first exporting the stp files for the
        whole reactor, then exporting the neutronics description of the reactor
        , then there are two methods available for producing the imprinted and
        merged h5m geometry. The next step is to make the geometry watertight
        which uses make_watertight from DAGMC. If using the Trelis option you
        must have the make_faceteted_neutronics_model.py in the same directory
        as your Python script.

        Arguments:
            method: (str): The method to use when making the imprinted and
                merged geometry. Options are PPP or Trelis. Defaults to
                NeutronicsModelFromReactor.method. where options ae further
                described.
        """

        os.system('rm dagmc_not_watertight.h5m')
        os.system('rm dagmc.h5m')

        self.reactor.export_stp()
        self.reactor.export_neutronics_description()

        if method is None:
            method = self.method
            if method not in ['ppp', 'trelis']:
                raise ValueError(
                    "the method using in create_neutronics_geometry \
                    should be either ppp or trelis not", method)

        if method == 'ppp':
            # as the installer connects to the system python not the conda python
            # this full path is needed for now
            if os.system(
                    '/usr/bin/python3 /usr/bin/geomPipeline.py manifest.json') != 0:
                raise ValueError(
                    "geomPipeline.py failed, check PPP is installed")

            # TODO allow tolerance to be user controlled
            if os.system(
                    'occ_faceter manifest_processed/manifest_processed.brep') != 0:
                raise ValueError(
                    "occ_faceter failed, check occ_faceter is install and the \
                    occ_faceter/bin folder is in the path directory")

        elif method == 'trelis':

            if not Path("make_faceteted_neutronics_model.py").is_file():
                raise ValueError("The make_faceteted_neutronics_model.py was \
                    not found in the directory")
            os.system("trelis -batch -nographics make_faceteted_neutronics_model.py \"faceting_tolerance='" +
                      str(self.faceting_tolerance) + "'\" \"merge_tolerance='" + str(self.merge_tolerance) + "'\"")

            if not Path("dagmc_not_watertight.h5m").is_file():
                raise ValueError("The dagmc_not_watertight.h5m was not found \
                    in the directory, the Trelis stage has failed")

        if not Path("dagmc_not_watertight.h5m").is_file():
            raise ValueError(
                "The" +
                method +
                "failed to create a dagmc_not_watertight.h5m file")

        if os.system(
                "make_watertight dagmc_not_watertight.h5m -o dagmc.h5m") != 0:
            raise ValueError(
                "make_watertight failed, check DAGMC is install and the \
                    DAGMC/bin folder is in the path directory")

        print('neutronics model saved as dagmc.h5m')

    def plot_neutronics_geometry(self):

        plt.show(self.universe.plot(width=(1200, 1200), basis='xz'))
        plt.show(self.universe.plot(width=(1200, 1200), basis='xy'))
        plt.show(self.universe.plot(width=(1200, 1200), basis='xy'))

        # TODO use colors already assigned to reactor components, like this ...
        # plt.show(self.universe.plot(width=(1200, 1200), basis='xy', colors={cell_1: 'blue'}))

    def create_neutronics_model(self, method=None):
        """Uses OpenMC python API to make a neutronics model, including tallies
        (cell_tallies), simulation settings (batches, particles per batch)

        Arguments:
            method: (str): The method to use when making the imprinted and
                merged geometry. Options are PPP or Trelis. Defaults to
                NeutronicsModelFromReactor.method. where options ae further
                described.
        """

        self.create_materials()
        self.create_neutronics_geometry(method=method)
        self.create_tallies()

        # this is the underlying geometry container that is filled with the
        # faceteted DGAMC CAD model
        self.universe = openmc.Universe()
        geom = openmc.Geometry(self.universe)

        # settings for the number of neutrons to simulate
        settings = openmc.Settings()
        settings.batches = self.simulation_batches
        settings.inactive = 0
        settings.particles = self.simulation_particles_per_batch
        settings.run_mode = "fixed source"
        settings.dagmc = True
        settings.photon_transport = True
        settings.source = self.source
        settings.max_lost_particles = self.max_lost_particles

        # make the model from gemonetry, materials, settings and tallies
        self.model = openmc.model.Model(geom, self.mats, settings, self.tallies)

    def create_tallies(self):
        # details about what neutrons interactions to keep track of (tally)
        tallies = openmc.Tallies()

        if self.mesh_tallies_2D is not None:
            # Create mesh which will be used for tally
            mesh = openmc.RegularMesh()
            mesh_height = 100
            mesh_width = mesh_height
            mesh.dimension = [mesh_width, mesh_height]
            mesh.lower_left = [0, -1200, -1200]  # hard coded for now
            mesh.upper_right = [0, 1200, 1200]  # should be obtained from the geometry

            if 'tritium_production' in self.mesh_tallies_2D:
                mesh_filter = openmc.MeshFilter(mesh)
                mesh_tally = openmc.Tally(name='tritium_production_on_2D_mesh')
                mesh_tally.filters = [mesh_filter]
                mesh_tally.scores = ["(n,Xt)"]
                tallies.append(mesh_tally)

        if self.cell_tallies is not None:
            if 'TBR' in self.cell_tallies:
                blanket_mat = self.openmc_materials['blanket_mat']
                material_filter = openmc.MaterialFilter(blanket_mat)
                tally = openmc.Tally(name="TBR")
                tally.filters = [material_filter]
                tally.scores = ["(n,Xt)"]  # where X is a wild card
                tallies.append(tally)

            if 'heat' in self.cell_tallies:
                for key, value in self.openmc_materials.items():
                    if key != 'DT_plasma':
                        material_filter = openmc.MaterialFilter(value)
                        tally = openmc.Tally(name=key + "_heat")
                        tally.filters = [material_filter]
                        tally.scores = ["heating"]
                        tallies.append(tally)

            if 'flux' in self.cell_tallies:
                for key, value in self.openmc_materials.items():
                    if key != 'DT_plasma':
                        material_filter = openmc.MaterialFilter(value)
                        tally = openmc.Tally(name=key + "_flux")
                        tally.filters = [material_filter]
                        tally.scores = ["flux"]
                        tallies.append(tally)

        self.tallies = tallies

    def simulate(self, verbose=True, method=None):
        """Run the OpenMC simulation. Deletes exisiting simulation output
        (summary.h5) if files exists.

        Arguments:
            verbose: (Boolean, optional): Print the output from OpenMC (true)
                to the terminal and don't print the OpenMC output (false).
                Defaults to True.
            method: (str): The method to use when making the imprinted and
                merged geometry. Options are PPP or Trelis. Defaults to
                NeutronicsModelFromReactor.method.

        Returns:
            dict: the simulation output filename
        """

        if self.model is None:
            self.create_neutronics_model(method=method)

        # Deletes summary.h5m if it already exists.
        # This avoids permission problems when trying to overwrite the file
        os.system('rm summary.h5')

        self.output_filename = self.model.run(output=verbose)
        self.results = self.get_results()

        return self.output_filename

    def get_results(self):
        """Reads the output file from the neutronics simulation
        and prints the TBR tally result to screen

        Returns:
            dict: a dictionary of the simulation results
        """

        # open the results file
        sp = openmc.StatePoint(self.output_filename)

        results = defaultdict(dict)

        # access the tallies
        for key, tally in sp.tallies.items():

            df = tally.get_pandas_dataframe()
            tally_result = df["mean"].sum()
            tally_std_dev = df['std. dev.'].sum()

            if tally.name == 'TBR':

                results[tally.name] = {
                    'result': tally_result,
                    'std. dev.': tally_std_dev,
                }

            if tally.name.endswith('heat'):

                results[tally.name]['MeV per source particle'] = {
                    'result': tally_result / 1e6,
                    'std. dev.': tally_std_dev / 1e6,
                }
                results[tally.name]['Watts'] = {
                    'result': tally_result * 1.602176487e-19 * (self.fusion_power / ((17.58 * 1e6) / 6.2415090744e18)),
                    'std. dev.': tally_std_dev * 1.602176487e-19 * (self.fusion_power / ((17.58 * 1e6) / 6.2415090744e18)),
                }

            if tally.name.endswith('flux'):

                results[tally.name]['Flux per source particle'] = {
                    'result': tally_result,
                    'std. dev.': tally_std_dev,
                }

        self.results = json.dumps(results, indent=4, sort_keys=True)

        return results
