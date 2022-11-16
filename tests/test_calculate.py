import unittest

from calculate import explode


class TestExplode(unittest.TestCase):
    def setUp(self) -> None:
        self.origin_x = 0
        self.origin_y = 0
        self.background_color = (30, 30, 30)
        self.number_of_particles = 20
        self.max_ticks = 100
        return super().setUp()

    def test_base(self):
        explosion = explode(
            self.origin_x,
            self.origin_y,
            self.background_color,
            self.number_of_particles,
            self.max_ticks,
        )
        for particle in explosion:
            self.assertEqual(particle[1], (30, 30, 30))
        self.assertEqual(len(explosion), 20)

    def test_max_ticks(self):
        explosion = explode(
            self.origin_x,
            self.origin_y,
            self.background_color,
            self.number_of_particles,
            5,
        )
        for particle in explosion:
            self.assertEqual(particle[2], 5)

    def test_color(self):
        explosion = explode(
            self.origin_x,
            self.origin_y,
            (0, 0, 0),
            self.number_of_particles,
            self.max_ticks,
        )
        for particle in explosion:
            self.assertEqual(particle[1], (0, 0, 0))
