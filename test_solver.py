import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from equation_solver import EquationSolver

class TestEquationSolver(unittest.TestCase):
    def setUp(self):
        self.solver = EquationSolver()
    
    def test_linear_equation(self):
        """Test solving linear equations"""
        result = self.solver.solve_equation("2x + 3 = 7")
        self.assertIn('solutions', result)
        self.assertEqual(result['solutions'][0], 2)
    
    def test_quadratic_equation(self):
        """Test solving quadratic equations"""
        result = self.solver.solve_equation("x^2 - 5x + 6 = 0")
        self.assertIn('solutions', result)
        self.assertEqual(set(result['solutions']), {2, 3})
    
    def test_invalid_equation(self):
        """Test handling of invalid equations"""
        result = self.solver.solve_equation("invalid")
        self.assertIn('error', result)

if __name__ == '__main__':
    unittest.main()