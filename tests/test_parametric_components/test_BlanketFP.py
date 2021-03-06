
import paramak
import unittest


class test_BlanketFP(unittest.TestCase):
    def test_BlanketFP_creation_plasma(self):
        """checks that a cadquery solid can be created by passing a plasma to the
        BlanketFP parametric component"""

        plasma = paramak.Plasma(
            major_radius=300, minor_radius=50, triangularity=0.5, elongation=2,
        )
        test_shape = paramak.BlanketFP(
            plasma=plasma,
            thickness=200,
            stop_angle=90,
            start_angle=270,
            offset_from_plasma=30,
            rotation_angle=180,
        )

        assert test_shape.solid is not None
        assert test_shape.volume > 1000

    def test_BlanketFP_creation_noplasma(self):
        """checks that a cadquery solid can be created using the BlanketFP parametric
        component when no plasma is passed"""

        test_shape = paramak.BlanketFP(
            major_radius=300,
            minor_radius=50,
            triangularity=0.5,
            elongation=2,
            thickness=200,
            stop_angle=360,
            start_angle=0,
            rotation_angle=180
        )

        assert test_shape.solid is not None
        assert test_shape.volume > 1000

    def test_BlanketFP_full_cov_full_rotation(self):
        """checks BlanketFP cannot have full coverage and 360 rotation at the same time"""
        def create_shape():
            test_shape = paramak.BlanketFP(
                major_radius=300,
                minor_radius=50,
                triangularity=0.5,
                elongation=2,
                thickness=200,
                stop_angle=360,
                start_angle=0,
                rotation_angle=360
            )
            test_shape.solid
        self.assertRaises(
            ValueError, create_shape)

    def test_BlanketFP_creation_variable_thickness_from_tuple(self):
        """checks that a cadquery solid can be created using the BlanketFP parametric
        component when a tuple of thicknesses is passed"""

        test_shape = paramak.BlanketFP(
            major_radius=300,
            minor_radius=50,
            triangularity=0.5,
            elongation=2,
            thickness=(100, 200),
            stop_angle=90,
            start_angle=270,
        )

        assert test_shape.solid is not None
        assert test_shape.volume > 1000

    def test_BlanketFP_creation_variable_thickness_from_2_lists(self):
        """checks that a cadquery solid can be created using the BlanketFP
        parametric component when a list of angles and a list of thicknesses
        are passed"""

        test_shape = paramak.BlanketFP(
            major_radius=300,
            minor_radius=50,
            triangularity=0.5,
            elongation=2,
            thickness=[(270, 90), [10, 30]],
            stop_angle=90,
            start_angle=270,
        )

        assert test_shape.solid is not None

    def test_BlanketFP_creation_variable_thickness_function(self):
        """checks that a cadquery solid can be created using the BlanketFP parametric
        component when a thickness function is passed"""

        def thickness(theta):
            return 100 + 3 * theta

        test_shape = paramak.BlanketFP(
            major_radius=300,
            minor_radius=50,
            triangularity=0.5,
            elongation=2,
            thickness=thickness,
            stop_angle=90,
            start_angle=270,
        )

        assert test_shape.solid is not None
        assert test_shape.volume > 1000

    def test_BlanketFP_creation_variable_offset_from_tuple(self):
        """checks that a cadquery solid can be created using the BlanketFP
        parametric component when a tuple of offsets is passed"""

        test_shape = paramak.BlanketFP(
            major_radius=300,
            minor_radius=50,
            triangularity=0.5,
            elongation=2,
            thickness=100,
            offset_from_plasma=(0, 10),
            stop_angle=90,
            start_angle=270,
        )

        assert test_shape.solid is not None
        assert test_shape.volume > 1000

    def test_BlanketFP_creation_variable_offset_from_2_lists(self):
        """checks that a cadquery solid can be created using the BlanketFP
        parametric component when a list of offsets and a list of angles are
        passed"""

        test_shape = paramak.BlanketFP(
            major_radius=300,
            minor_radius=50,
            triangularity=0.5,
            elongation=2,
            thickness=100,
            offset_from_plasma=[[270, 100, 90], [0, 5, 10]],
            stop_angle=90,
            start_angle=270,
        )

        assert test_shape.solid is not None

    def test_BlanketFP_creation_variable_offset_error(self):
        """checks that an error is raised when two lists with different
        lengths are passed in offset_from_plasma"""
        def test_different_lengths():
            test_shape = paramak.BlanketFP(
                major_radius=300,
                minor_radius=50,
                triangularity=0.5,
                elongation=2,
                thickness=100,
                offset_from_plasma=[[270, 100, 90], [0, 5, 10, 15]],
                stop_angle=90,
                start_angle=270,
            )
            test_shape.solid

        self.assertRaises(ValueError, test_different_lengths)

    def test_BlanketFP_creation_variable_offset_function(self):
        """checks that a cadquery solid can be created using the BlanketFP
        parametric component when a offset function is passed"""

        def offset(theta):
            return 100 + 3 * theta

        test_shape = paramak.BlanketFP(
            major_radius=300,
            minor_radius=50,
            triangularity=0.5,
            elongation=2,
            thickness=100,
            stop_angle=90,
            start_angle=270,
            offset_from_plasma=offset
        )

        assert test_shape.solid is not None
        assert test_shape.volume > 1000

    def test_BlanketFP_physical_groups(self):
        """creates a blanket using the BlanketFP parametric component and checks that
        physical groups can be exported using the export_physical_groups method"""

        test_shape = paramak.BlanketFP(100, stop_angle=90, start_angle=270,)
        test_shape.export_physical_groups("tests/blanket.json")

    def test_BlanketFP_full_cov_stp_export(self):
        """creates a blanket using the BlanketFP parametric component and checks that
        an stp file with full coverage can be exported using the export_stp method"""

        test_shape = paramak.BlanketFP(
            major_radius=300,
            minor_radius=50,
            triangularity=0.5,
            elongation=2,
            thickness=200,
            stop_angle=360,
            start_angle=0,
            rotation_angle=180,
        )

        test_shape.export_stp("tests/test_blanket_full_cov")
