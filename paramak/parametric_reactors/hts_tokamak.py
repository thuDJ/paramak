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
        # self.make_center_column_shield(shapes_or_components)
        # self.make_component_cuts(shapes_or_components)

        # self.shapes_and_components = shapes_or_components
