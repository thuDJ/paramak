
import os
import unittest
from pathlib import Path

import paramak


class test_Plasma(unittest.TestCase):
    def test_plasma_attributes(self):
        """creates a plasma object using the Plasma parametric component and checks that
        its attributes can be set correctly"""

        test_plasma = paramak.Plasma()

        assert isinstance(test_plasma.elongation, float)

        def test_plasma_elongation_min_setting():
            """checks ValueError is raised when an elongation < 0 is specified"""

            test_plasma.elongation = -1

        self.assertRaises(ValueError, test_plasma_elongation_min_setting)

        def test_plasma_elongation_max_setting():
            """checks ValueError is raised when an elongation > 4 is specified"""

            test_plasma.elongation = 400

        self.assertRaises(ValueError, test_plasma_elongation_max_setting)

    def test_plasma_x_points(self):
        """creates several plasmas with different configurations using the Plasma parametric
        component and checks the location of the x point for each"""

        for (
            triangularity,
            elongation,
            minor_radius,
            major_radius,
            vertical_displacement,
        ) in zip(
            [-0.7, 0, 0.5],  # triangularity
            [1, 1.5, 2],  # elongation
            [100, 200, 300],  # minor radius
            [300, 400, 600],  # major radius
            [0, -10, 5],
        ):  # displacement

            for config in ["non-null", "single-null", "double-null"]:

                # Run
                test_plasma = paramak.Plasma(
                    configuration=config,
                    triangularity=triangularity,
                    elongation=elongation,
                    minor_radius=minor_radius,
                    major_radius=major_radius,
                    vertical_displacement=vertical_displacement,
                )

                # Expected
                expected_lower_x_point, expected_upper_x_point = None, None
                if config == "single-null" or config == "double-null":
                    expected_lower_x_point = (1 -
                                              (1 +
                                               test_plasma.x_point_shift) *
                                              triangularity *
                                              minor_radius, -
                                              (1 +
                                               test_plasma.x_point_shift) *
                                              elongation *
                                              minor_radius +
                                              vertical_displacement, )

                    if config == "double-null":
                        expected_upper_x_point = (
                            expected_lower_x_point[0],
                            (1 +
                             test_plasma.x_point_shift) *
                            elongation *
                            minor_radius +
                            vertical_displacement,
                        )

                # Check
                for point, expected_point in zip(
                    [test_plasma.lower_x_point, test_plasma.upper_x_point],
                    [expected_lower_x_point, expected_upper_x_point],
                ):
                    assert point == expected_point

    def test_plasma_x_points_plasmaboundaries(self):
        """creates several plasmas with different configurations using the PlasmaBoundaries
        parametric component and checks the location of the x point for each"""

        for A, triangularity, elongation, minor_radius, major_radius in zip(
            [0, 0.05, 0.05],  # A
            [-0.7, 0, 0.5],  # triangularity
            [1, 1.5, 2],  # elongation
            [100, 200, 300],  # minor radius
            [300, 400, 600],
        ):  # major radius

            for config in ["non-null", "single-null", "double-null"]:

                # Run
                test_plasma = paramak.PlasmaBoundaries(
                    configuration=config,
                    A=A,
                    triangularity=triangularity,
                    elongation=elongation,
                    minor_radius=minor_radius,
                    major_radius=major_radius,
                )

                # Expected
                expected_lower_x_point, expected_upper_x_point = None, None
                if config == "single-null" or config == "double-null":
                    expected_lower_x_point = (1 -
                                              (1 +
                                               test_plasma.x_point_shift) *
                                              triangularity *
                                              minor_radius, -
                                              (1 +
                                               test_plasma.x_point_shift) *
                                              elongation *
                                              minor_radius, )

                    if config == "double-null":
                        expected_upper_x_point = (
                            expected_lower_x_point[0],
                            -expected_lower_x_point[1],
                        )

                # Check
                for point, expected_point in zip(
                    [test_plasma.lower_x_point, test_plasma.upper_x_point],
                    [expected_lower_x_point, expected_upper_x_point],
                ):
                    assert point == expected_point
                assert test_plasma.solid is not None

    def test_export_plasma_source(self):
        """creates a plasma using the Plasma parametric component and checks an stp file
        of the shape can be exported using the export_stp method"""

        test_plasma = paramak.Plasma()

        os.system("rm plasma.stp")

        test_plasma.export_stp("plasma.stp")

        assert Path("plasma.stp").exists()
        os.system("rm plasma.stp")

    def test_export_plasma_from_points_export(self):
        """creates a plasma using the PlasmaFromPoints parametric component and checks an
        stp file of the shape can be exported using the export_stp method"""

        test_plasma = paramak.PlasmaFromPoints(
            outer_equatorial_x_point=500,
            inner_equatorial_x_point=300,
            high_point=(400, 200),
            rotation_angle=180,
        )

        os.system("rm plasma.stp")

        test_plasma.export_stp("plasma.stp")
        assert test_plasma.high_point[0] > test_plasma.inner_equatorial_x_point
        assert test_plasma.high_point[0] < test_plasma.outer_equatorial_x_point
        assert test_plasma.outer_equatorial_x_point > test_plasma.inner_equatorial_x_point
        assert Path("plasma.stp").exists()
        os.system("rm plasma.stp")
