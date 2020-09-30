
"""
Example which creates a simple neutronics model using the CenterColumnStudyReactor
and finds the neutron spectra and current for different configurations
"""

import os

import openmc
from neutronics_material_maker import Material
import json
import paramak
import uuid
from skopt import dummy_minimize  # available via pip install scikit-optimize


def neutron_flux_in_center_column(params):

    inner_bore_radial_thickness = params[0]
    inboard_tf_leg_radial_thickness = params[1]
    center_column_shield_radial_thickness_mid = params[2]
    center_column_shield_radial_thickness_upper = params[3] * params[2]
    inboard_firstwall_radial_thickness = params[4]
    inner_plasma_gap_radial_thickness = params[5]
    divertor_radial_thickness = params[6]
    plasma_radial_thickness = params[7]
    outer_plasma_gap_radial_thickness = params[8]
    plasma_gap_vertical_thickness = params[9]
    center_column_arc_vertical_thickness = params[10]

    plasma_high_point_y = params[11]

    # plasma_high_point_x_factor is param[12]
    plasma_high_point_x = (params[7] * params[12]) + sum(params[0:6])
    plasma_high_point = (plasma_high_point_x, plasma_high_point_y)

    print(params)

    my_reactor = paramak.CenterColumnStudyReactor(
        inner_bore_radial_thickness=inner_bore_radial_thickness,
        inboard_tf_leg_radial_thickness=inboard_tf_leg_radial_thickness,
        center_column_shield_radial_thickness_mid=center_column_shield_radial_thickness_mid,
        center_column_shield_radial_thickness_upper=center_column_shield_radial_thickness_upper,
        inboard_firstwall_radial_thickness=inboard_firstwall_radial_thickness,
        inner_plasma_gap_radial_thickness=inner_plasma_gap_radial_thickness,
        divertor_radial_thickness=divertor_radial_thickness,
        plasma_radial_thickness=plasma_radial_thickness,
        outer_plasma_gap_radial_thickness=outer_plasma_gap_radial_thickness,
        plasma_gap_vertical_thickness=plasma_gap_vertical_thickness,
        center_column_arc_vertical_thickness=center_column_arc_vertical_thickness,
        plasma_high_point=plasma_high_point,
        rotation_angle=180)
    simulation_id = str(uuid.uuid4())
    my_reactor.export_neutronics_description(simulation_id + '/manifest.json')
    my_reactor.export_svg(simulation_id + '/image.png')
    my_reactor.export_stp(output_folder=simulation_id)

    cwd = os.getcwd()
    os.system('cp make_faceteted_neutronics_model.py ' + simulation_id)
    os.chdir(simulation_id)
    os.system('trelis -batch -nographics make_faceteted_neutronics_model.py')
    os.system('make_watertight dagmc_notwatertight.h5m -o dagmc.h5m')

    firstwall_mat = Material(
        material_name='eurofer',
        material_tag='firstwall_mat')

    inboard_tf_coils_mat = Material(
        material_name='WC',
        material_tag='inboard_tf_coils_mat')

    center_column_mat = Material(
        material_name='WC',
        material_tag='center_column_shield_mat')

    divertor_mat = Material(
        material_name='eurofer',
        material_tag='divertor_mat')

    blanket_mat = Material(
        material_name='Li4SiO4',
        enrichment=60,
        material_tag='blanket_mat')

    mats = openmc.Materials([
                            firstwall_mat.openmc_material,
                            inboard_tf_coils_mat.openmc_material,
                            center_column_mat.openmc_material,
                            divertor_mat.openmc_material,
                            blanket_mat.openmc_material,
                            ]
                        )

    # this is the underlying geometry container that is filled with the faceteted CAD model
    universe = openmc.Universe()
    geom = openmc.Geometry(universe)

    # settings for the number of neutrons to simulate
    settings = openmc.Settings()
    settings.batches = 10
    settings.inactive = 0
    settings.particles = 100
    settings.run_mode = 'fixed source'
    settings.dagmc = True 

    # details of the birth locations and energy of the neutronis
    source = openmc.Source()
    source.space = openmc.stats.Point((my_reactor.major_radius, 0, 0))
    source.angle = openmc.stats.Isotropic()
    source.energy = openmc.stats.Discrete([14e6], [1])
    settings.source = source

    # details about what neutrons interactions to keep track of (called a tally)
    tallies = openmc.Tallies()
    material_filter = openmc.MaterialFilter(center_column_mat)
    flux_tally = openmc.Tally(name='neutron_flux_in_center_column')
    flux_tally.filters = [material_filter]
    flux_tally.scores = ['flux']
    tallies.append(flux_tally)

    # make the model from gemonetry, materials, settings and tallies
    model = openmc.model.Model(geom, mats, settings, tallies)

    # run the simulation
    output_filename = model.run()

    # open the results file
    sp = openmc.StatePoint(output_filename)

    # access the tally
    flux_tally = sp.get_tally(name='neutron_flux_in_center_column')
    df = flux_tally.get_pandas_dataframe()
    flux_tally_result = df['mean'].sum()

    # print result
    print('The neutron flux was found, flux = ', flux_tally_result)
    # return flux_tally_result


    # input_and_output_data = {
    #     "inner_bore_radial_thickness": inner_bore_radial_thickness,
    #     "inboard_tf_leg_radial_thickness": inboard_tf_leg_radial_thickness,
    #     "center_column_shield_radial_thickness_mid": center_column_shield_radial_thickness_mid,
    #     "center_column_shield_radial_thickness_upper": center_column_shield_radial_thickness_upper,
    #     "inboard_firstwall_radial_thickness": inboard_firstwall_radial_thickness,
    #     "inner_plasma_gap_radial_thickness": inner_plasma_gap_radial_thickness,
    #     "divertor_radial_thickness": divertor_radial_thickness,
    #     "plasma_radial_thickness": plasma_radial_thickness,
    #     "outer_plasma_gap_radial_thickness": outer_plasma_gap_radial_thickness,
    #     "plasma_gap_vertical_thickness": plasma_gap_vertical_thickness,
    #     "center_column_arc_vertical_thickness": center_column_arc_vertical_thickness,
    #     "plasma_high_point_x": plasma_high_point[0],
    #     "plasma_high_point_y": plasma_high_point[1],
    # }

    # with open(simulation_id + ".json", 'w') as outfile:
    #     json.dump(input_and_output_data, outfile, indent=4)
    

    os.chdir(cwd)
    return 1


if __name__ == "__main__":
    res = dummy_minimize(neutron_flux_in_center_column,
                         [
                             (10., 50.),  # inner_bore_radial_thickness
                             (50., 100.),  # inboard_tf_leg_radial_thickness
                             # center_column_shield_radial_thickness_mid
                             (10., 150.),
                             (1., 1.5),  # center_column_shield_radial_thickness_upper
                             (2., 10.),  # inboard_firstwall_radial_thickness
                             (2., 20.),  # inner_plasma_gap_radial_thickness
                             (20., 50.),  # divertor_radial_thickness
                             (100., 300.),  # plasma_radial_thickness
                             (2., 20.),  # outer_plasma_gap_radial_thickness
                             (2., 20.),  # plasma_gap_vertical_thickness
                             (200., 500.),  # center_column_arc_vertical_thickness
                             (200., 500.),  # plasma_high_point_y
                             (0., 1.),  # plasma_high_point_x_factor
                         ],
                         n_calls=20  # this can be increased to perform more samples
                         )
