import paramak


class HTSTokamak(paramak.Reactor):
    """Creates geometry for a tokamak based on the Overview of SPARC paper
    DOI: https://doi.org/10.1017/S0022377820001257 as this is a fixed design
    the componets are not parametric and few inputs are required to produce
    the model.

    Arguments:
        rotation_angle (float): the angle of the sector that is desired

    Returns:
        a paramak shape object: a Reactor object that has generic functionality
    """

    def __init__(
        self,
        rotation_angle=360,
    ):

        super().__init__([])

        shapes_or_components = []

        # self.rotation_angle_check()
        # self.make_plasma(shapes_or_components)
        # self.make_inboard_tf_coils(shapes_or_components)
        self.make_pf_coils
        (shapes_or_components)
        # self.make_center_column_shield(shapes_or_components)
        # self.make_component_cuts(shapes_or_components)

        # self.shapes_and_components = shapes_or_components
    
# 2.0893854748603347, 1.0583126550868487
# 2.5214152700186214, 0.7307692307692307
# 1.9031657355679696, 0.403225806451613
# 1.4934823091247669, 0.6786600496277916
# 1.3891992551210426, 0.403225806451613
# 0.9795158286778394, 0.6786600496277916
# 0.8752327746741151, 0.403225806451613
# 0.055865921787709105, 0.6712158808933003
# -0.05586592178770955, 0.403225806451613
# -0.8752327746741155, 0.6712158808933003
# -0.9795158286778403, 0.403225806451613
# -1.389199255121043, 0.6712158808933003
# -1.4934823091247678, 0.403225806451613
# -1.9031657355679705, 0.6712158808933003
# -2.089385474860335, 0.7307692307692307
# -2.5065176908752322, 1.050868486352357
# -2.2309124767225326, 1.4081885856079404
# -2.543761638733706, 1.8920595533498759
# -2.089385474860335, 2.4354838709677415
# -2.3649906890130357, 2.859801488833747
# -1.1135940409683425, 3.55955334987593
# -1.4860335195530734, 3.931761786600496
# 1.4934823091247669, 3.5669975186104215
# 1.113594040968342, 3.939205955334988
# 2.0968342644320295, 2.859801488833747
# 2.3724394785847296, 2.4354838709677415
# 2.5512104283054, 1.400744416873449
# 2.230912476722532, 1.8995037220843671
