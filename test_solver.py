import unittest
from solver import EquationSolver

class TestEquationSolver(unittest.TestCase):
    def test_linear_equation(self):
        solver = EquationSolver("2x - 4 = 0")
        steps = solver.solve()
        self.assertIn("Result: x = 2.0", steps[-1])

    def test_quadratic_two_roots(self):
        solver = EquationSolver("x^2 - 5x + 6 = 0")
        steps = solver.solve()
        self.assertTrue(any("x1 = 3.0" in s for s in steps))
        self.assertTrue(any("x2 = 2.0" in s for s in steps))

    def test_quadratic_one_root(self):
        solver = EquationSolver("x^2 - 4x + 4 = 0")
        steps = solver.solve()
        self.assertIn("Result: x = 2.0", steps[-1])

    def test_quadratic_complex_roots(self):
        solver = EquationSolver("x^2 + 1 = 0")
        steps = solver.solve()
        self.assertTrue(any("x1 = -0.0 + 1.0i" in s or "x1 = 0.0 + 1.0i" in s for s in steps))

    def test_mixed_sides(self):
        solver = EquationSolver("x^2 + 2x = -1")
        steps = solver.solve()
        self.assertIn("Equation simplified to: 1.0x^2 + 2.0x + 1.0 = 0", steps[0])
        self.assertIn("Result: x = -1.0", steps[-1])

    def test_subtraction_no_spaces(self):
        solver = EquationSolver("x^2-x=0")
        steps = solver.solve()
        self.assertIn("Equation simplified to: 1.0x^2 + -1.0x + 0.0 = 0", steps[0])
        self.assertTrue(any("x1 = 1.0" in s for s in steps))
        self.assertTrue(any("x2 = 0.0" in s for s in steps))

    def test_decimal_coefficients(self):
        solver = EquationSolver("0.5x^2 + 1.5x + 1.0 = 0")
        steps = solver.solve()
        self.assertIn("Equation simplified to: 0.5x^2 + 1.5x + 1.0 = 0", steps[0])
        self.assertTrue(any("x1 = -1.0" in s for s in steps))
        self.assertTrue(any("x2 = -2.0" in s for s in steps))

    def test_expression_coefficients(self):
        solver = EquationSolver("(1+1)x^2 + (3/2)x - 1 = 0")
        steps = solver.solve()
        self.assertIn("Equation simplified to: 2.0x^2 + 1.5x + -1.0 = 0", steps[0])
        self.assertTrue(any("x1 = 0.42539" in s for s in steps))
        self.assertTrue(any("x2 = -1.17539" in s for s in steps))

if __name__ == "__main__":
    unittest.main()
