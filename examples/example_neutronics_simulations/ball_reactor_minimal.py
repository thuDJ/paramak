"""This is a minimal example that obtains the TBR (Tritium Breeding Ratio)
for a parametric ball reactor"""

import paramak
from parametric_plasma_source import PlasmaSource, SOURCE_SAMPLING_PATH
import openmc

def make_model_and_simulate():
    """Makes a neutronics Reactor model and simulates the TBR"""

    # makes the 3d geometry from input parameters
    my_reactor = paramak.BallReactor(
        inner_bore_radial_thickness=50,
        inboard_tf_leg_radial_thickness=200,
        center_column_shield_radial_thickness=50,
        divertor_radial_thickness=50,
        inner_plasma_gap_radial_thickness=50,
        plasma_radial_thickness=100,
        outer_plasma_gap_radial_thickness=50,
        firstwall_radial_thickness=1,
        blanket_radial_thickness=100,
        blanket_rear_wall_radial_thickness=10,
        elongation=2,
        triangularity=0.55,
        number_of_tf_coils=16,
        rotation_angle=360,
    )

    my_plasma = PlasmaSource(
        elongation=1.557,
        ion_density_origin=1.09e20,
        ion_density_peaking_factor=1,
        ion_density_pedestal=1.09e20,
        ion_density_separatrix=3e19,
        ion_temperature_origin=45.9,
        ion_temperature_peaking_factor=8.06,
        ion_temperature_pedestal=6.09,
        ion_temperature_separatrix=0.1,
        major_radius=my_reactor.major_radius,
        minor_radius=my_reactor.minor_radius,
        pedestal_radius=0.8 * my_reactor.major_radius,
        plasma_id=1,
        shafranov_shift=0.44789,
        triangularity=0.270,
        ion_temperature_beta=6,
    )
    source = openmc.Source()
    source.library = SOURCE_SAMPLING_PATH
    source.parameters = str(my_plasma)

    # makes the neutronics model from the geometry and material allocations
    neutronics_model = paramak.NeutronicsModelFromReactor(
        reactor=my_reactor,
        source=source,
        materials={
            'inboard_tf_coils_mat': 'eurofer',
            'center_column_shield_mat': 'eurofer',
            'divertor_mat': 'eurofer',
            'firstwall_mat': 'eurofer',
            'blanket_rear_wall_mat': 'eurofer',
            'blanket_mat': 'Li4SiO4'},
        cell_tallies=['TBR', 'heat'],
        simulation_batches=5,
        simulation_particles_per_batch=1e4,
    )

    # simulate the neutronics model
    neutronics_model.simulate(method='trelis')
    print(neutronics_model.results)


if __name__ == "__main__":
    make_model_and_simulate()
