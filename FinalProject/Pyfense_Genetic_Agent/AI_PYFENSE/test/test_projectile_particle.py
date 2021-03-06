"""
Test Projectile Particle class.
"""

import unittest
from cocos.director import director

from Pyfense import projectileParticle
from Pyfense import tower
from Pyfense import enemy
from Pyfense import game

settings = {
    "window": {
        "width": 1920,
        "height": 1080,
        "caption": "PyFense",
        "vsync": True,
        "fullscreen": False,
        "resizable": True
    },
    "player": {
        "currency": 200
    },
    "general": {
        "showFps": True
    }
}


class TestProjectileParticle(unittest.TestCase):
    """
    Test projectile particle class.
    """

    director.init(**settings['window'])

    def initiate_projectile(self):
        self.testGame = game.PyFenseGame(1)
        self.testPath = self.testGame.movePath
        self.testTower = tower.PyFenseTower(0, (50, 70))
        self.testEnemy = enemy.PyFenseEnemy(
            (50, 40), 0, 1, 1, self.testPath, 2)
        self.testProjectile = projectileParticle.PyFenseProjectileSlow(
            self.testTower, self.testEnemy, 1, 45,
            1000, 50, 'normal', 5, 1)

    def test_distance(self):
        """
        Test distance between Tower and Enemy.
        """

        self.initiate_projectile()
        result = self.testProjectile.distance
        actualResult = 30
        self.assertAlmostEqual(result, actualResult)

    def test_dispatch_event(self):
        """
        Test whether dispatching of event works.
        If test doesnt fail, then event has been dispatched.
        """

        self.initiate_projectile()
        self.testProjectile._dispatch_hit_event(
            0, self.testEnemy, 1, 'normal', 1, 1)


if __name__ == '__main__':
    unittest.main()
