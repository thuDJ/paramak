
import paramak
import unittest


class test_PoloidalSegments(unittest.TestCase):

    def test_PoloidalSegments_solid_count_with_incorect_input(self):
        """checks the segmenter does not take a float as an input"""
        def create_shape():
            test_shape_to_segment = paramak.PoloidalFieldCoil(
                height=100,
                width=100,
                center_point=(500, 500)
            )

            paramak.PoloidalSegments(
                shape_to_segment=test_shape_to_segment,
                center_point=(500, 500),
                number_of_segments=22.5,
            )

        self.assertRaises(
            ValueError, create_shape)

    def test_PoloidalSegments_solid_count_with_incorect_inputs2(self):
        """checks the segmenter does not take a negative int as an input"""
        def create_shape():
            test_shape_to_segment = paramak.PoloidalFieldCoil(
                height=100,
                width=100,
                center_point=(500, 500)
            )

            paramak.PoloidalSegments(
                shape_to_segment=test_shape_to_segment,
                center_point=(500, 500),
                number_of_segments=-5,
            )

        self.assertRaises(
            ValueError, create_shape)

    def test_PoloidalSegments_solid_count(self):
        """creates a rotated hollow ring and segments it into poloidal sections"""

        pf_coil = paramak.PoloidalFieldCoil(
            height=100,
            width=100,
            center_point=(500, 500)
        )

        test_shape_to_segment = paramak.PoloidalFieldCoilCaseFC(
            pf_coil=pf_coil,
            casing_thickness=100
        )

        test_shape = paramak.PoloidalSegments(
            shape_to_segment=test_shape_to_segment,
            center_point=(500, 500),
            number_of_segments=22,
        )

        assert test_shape.solid is not None
        assert len(test_shape.solid.Solids()) == 22

    def test_PoloidalSegments_solid_count2(self):
        """creates a rotated ring and segments it into poloidal sections"""

        test_shape_to_segment = paramak.PoloidalFieldCoil(
            height=100,
            width=100,
            center_point=(500, 500)
        )

        test_shape = paramak.PoloidalSegments(
            shape_to_segment=test_shape_to_segment,
            center_point=(500, 500),
            number_of_segments=22,
        )

        assert test_shape.solid is not None
        assert len(test_shape.solid.Solids()) == 22
