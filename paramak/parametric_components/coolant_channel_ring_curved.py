
import numpy as np 

from paramak import SweepCircleShape


class CoolantChannelRingCurved(SweepCircleShape):
    """A ring of equally-spaced curved circular coolant channels with
    constant thickness.

    Arguments:
        height (float): height of each coolant channel in ring.
        channel_radius (float): radius of each coolant channel in ring.
        number_of_coolant_channels (float): number of coolant channels in ring.
        ring_radius (float): radius of coolant channel ring.
        stp_filename (str, optional): Defaults to
            "CoolantChannelRingCurved.stp".
        stl_filename (str, optional): Defaults to
            "CoolantChannelRingCurved.stl".
        material_tag (str, optional): Defaults to "coolant_channel_mat".
    """

    def __init__(
        self,
        height,
        channel_radius,
        number_of_coolant_channels,
        ring_radius,
        mid_offset,
        stp_filename="CoolantChannelRingCurved.stp",
        stl_filename="CoolantChannelRingCurved.stl",
        material_tag="coolant_channel_mat",
        **kwargs
    ):

        self.ring_radius = ring_radius
        self.mid_offset = mid_offset
        self.height = height
        self.channel_radius = channel_radius

        super().__init__(
            path_points=self.path_points,
            radius=channel_radius,
            material_tag=material_tag,
            stp_filename=stp_filename,
            stl_filename=stl_filename,
            **kwargs
        )

        self.number_of_coolant_channels = number_of_coolant_channels

    @property
    def azimuth_placement_angle(self):
        self.find_azimuth_placement_angle()
        return self._azimuth_placement_angle

    @azimuth_placement_angle.setter
    def azimuth_placement_angle(self, value):
        self._azimuth_placement_angle = value

    @property
    def path_points(self):
        self.find_path_points()
        return self._path_points 
    
    @path_points.setter
    def path_points(self, value):
        self._path_points = value

    def find_azimuth_placement_angle(self):
        """Calculates the azimuth placement angles based on the number of
        coolant channels"""

        angles = list(
            np.linspace(0, 360, self.number_of_coolant_channels, endpoint=False)
        )

        self.azimuth_placement_angle = angles

    def find_path_points(self):

        # for the moment, channels are centered about z=0
        path_points = [
            (self.ring_radius, -self.height / 2),
            (self.ring_radius + self.mid_offset, 0),
            (self.ring_radius, self.height / 2)
        ]

        self.path_points = path_points


    
