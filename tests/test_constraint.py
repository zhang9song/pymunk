import pymunk as p
from pymunk.vec2d import Vec2d
import unittest

####################################################################
class UnitTestConstraint(unittest.TestCase):
    def setUp(self):
        p.reset_shapeid_counter()

    def testA(self):
        a,b = p.Body(10,10), p.Body(10,10)
        j = p.PivotJoint(a, b, (0,0))
        self.assertEqual(j.a, a)

    def testB(self):
        a,b = p.Body(10,10), p.Body(10,10)
        j = p.PivotJoint(a, b, (0,0))
        self.assertEqual(j.b, b)

    def testMaxForce(self):
        a,b = p.Body(10,10), p.Body(10,10)
        j = p.PivotJoint(a, b, (0,0))
        self.assertEqual(j.max_force, p.inf)
        j.max_force = 10
        self.assertEqual(j.max_force, 10)

    def testErrorBias(self):
        a,b = p.Body(10,10), p.Body(10,10)
        j = p.PivotJoint(a, b, (0,0))
        self.assertAlmostEqual(j.error_bias, pow(1.0 - 0.1, 60.0))
        j.error_bias = 0.3
        self.assertEqual(j.error_bias, 0.3)

    def testMaxBias(self):
        a,b = p.Body(10,10), p.Body(10,10)
        j = p.PivotJoint(a, b, (0,0))
        self.assertEqual(j.max_bias, p.inf)
        j.max_bias = 10
        self.assertEqual(j.max_bias, 10)

    def testCollideBodies(self):
        a,b = p.Body(10,10), p.Body(10,10)
        j = p.PivotJoint(a, b, (0,0))
        self.assertEqual(j.collide_bodies, True)
        j.collide_bodies = False
        self.assertEqual(j.collide_bodies, False)

    def testImpulse(self):
        a,b = p.Body(10,10), p.Body(10,10)
        b.position = 0,10
        j = p.PivotJoint(a, b, (0,0))

        s = p.Space()
        s.gravity = 0,10
        s.add(b, j)
        self.assertEqual(j.impulse, 0)
        s.step(1)
        self.assertAlmostEqual(j.impulse, 50)

    def testActivate(self):
        a,b = p.Body(), p.Body(10,10)
        j = p.PivotJoint(a,b,(0,0))
        s = p.Space()
        s.sleep_time_threshold = 0.01
        s.add(a,b)
        a.sleep()
        b.sleep()

        j.activate_bodies()
        self.assertFalse(a.is_sleeping)
        self.assertFalse(b.is_sleeping)

class UnitTestPinJoint(unittest.TestCase):
    def testAnchor(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.PinJoint(a, b, (1,2), (3,4))
        self.assertEqual(j.anchor_a, (1,2))
        self.assertEqual(j.anchor_b, (3,4))
        j.anchor_a = (5,6)
        j.anchor_b = (7,8)
        self.assertEqual(j.anchor_a, (5,6))
        self.assertEqual(j.anchor_b, (7,8))

    def testDistane(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.PinJoint(a, b, (0,0), (10,0))
        self.assertEqual(j.distance, 10)
        j.distance = 20
        self.assertEqual(j.distance, 20)

class UnitTestSlideJoint(unittest.TestCase):
    def testAnchor(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.SlideJoint(a, b, (1,2), (3,4), 0, 10)
        self.assertEqual(j.anchor_a, (1,2))
        self.assertEqual(j.anchor_b, (3,4))
        j.anchor_a = (5,6)
        j.anchor_b = (7,8)
        self.assertEqual(j.anchor_a, (5,6))
        self.assertEqual(j.anchor_b, (7,8))

    def testMin(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.SlideJoint(a, b, min=1)
        self.assertEqual(j.min, 1)
        j.min = 2
        self.assertEqual(j.min, 2)

    def testMax(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.SlideJoint(a, b, max=1)
        self.assertEqual(j.max, 1)
        j.max = 2
        self.assertEqual(j.max, 2)

class UnitTestPivotJoint(unittest.TestCase):
    def testPivotjoint(self):
        a,b = p.Body(10,10), p.Body(20,20)
        a.position = (-10,0)
        b.position = (10,0)
        s = p.Space()
        j1 = p.PivotJoint(a, b, (0,0))
        j2 = p.PivotJoint(a, b, (-10,0), (10,0))
        s.add(a,b,j1,j2)
        s.step(1)
        self.assertEqual(j1.anchr1, j2.anchr2)
        self.assertEqual(j2.anchr1, j1.anchr2)

    def testDampedSpring(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.DampedSpring(a,b,(1,0), (10,0), 7, 12,5)
        self.assertEqual(j.rest_length, 7)
        self.assertEqual(j.stiffness, 12)
        self.assertEqual(j.damping, 5)

    def testDampedRotarySpring(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.DampedRotarySpring(a,b, 0.4, 12,5)
        self.assertEqual(j.rest_angle, 0.4)
        self.assertEqual(j.stiffness, 12)
        self.assertEqual(j.damping, 5)

    def testDampedRotarySpringCallback(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.DampedRotarySpring(a,b, 0.4, 12,5)
        def f(self, relative_angle):
            return 1
        j.torque_func = f
        s = p.Space()
        s.add(a,b,j)
        a.apply_impulse((10,0), (0,10))
        a.apply_impulse((-10,0), (0,-10))
        for x in range(100):
            s.step(0.1)
        self.assertAlmostEqual(a.angle-b.angle,-29.3233997)

    def testRotaryLimitJoint(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.RotaryLimitJoint(a, b, 0.1, 0.2)
        self.assertEqual(j.max, 0.2)
        self.assertEqual(j.min, 0.1)

    def testRatchetJoint(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.RatchetJoint(a, b, 0.3, 0.2)
        self.assertEqual(j.angle, 0.0)
        self.assertEqual(j.phase, 0.3)
        self.assertEqual(j.ratchet, 0.2)

    def testGearJoint(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.GearJoint(a, b, 0.3, 0.2)
        self.assertEqual(j.phase, 0.3)
        self.assertEqual(j.ratio, 0.2)

    def testSimpleMotor(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.SimpleMotor(a, b, 0.3)
        self.assertEqual(j.rate, 0.3)
        j.rate = 0.4
        self.assertEqual(j.rate, 0.4)
        j.max_bias = 30
        j.bias_coef = 40
        j.max_force = 50
        self.assertEqual(j.max_bias, 30)
        self.assertEqual(j.bias_coef, 40)
        self.assertEqual(j.max_force, 50)

    def testGrooveJoint(self):
        a,b = p.Body(10,10), p.Body(20,20)
        a.position = 10,10
        b.position = 20,20
        j = p.GrooveJoint(a,b, (5,0), (7,7), (3,3))

        self.assertEqual(j.anchr2, (3,3))
        self.assertEqual(j.groove_a, (5,0))
        self.assertEqual(j.groove_b, (7,7))

####################################################################
if __name__ == "__main__":
    print ("testing pymunk version " + p.version)
    unittest.main()
