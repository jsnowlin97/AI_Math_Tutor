from sympy import symbols, Eq, solve, simplify, latex, parse_expr
from sympy.parsing.latex import parse_latex
import re

class EquationSolver:
    def __init__(self):
        self.x = symbols('x')
        
    def parse_equation(self, equation_str):
        """Parse equation string to SymPy equation"""
        try:
            # Handle LaTeX input
            if '\\' in equation_str:
                return self._parse_latex(equation_str)
            
            # Handle plain text
            return self._parse_text(equation_str)
        except Exception as e:
            return {'error': f"Parse error: {str(e)}"}
    
    def _parse_latex(self, latex_str):
        """Parse LaTeX equation"""
        try:
            # Remove LaTeX math mode delimiters
            latex_str = latex_str.replace('$$', '').replace('$', '')
            
            # Parse to SymPy expression
            expr = parse_latex(latex_str)
            
            # Convert to equation (assuming expr = 0)
            if isinstance(expr, Eq):
                return expr
            else:
                return Eq(expr, 0)
        except:
            return None
    
    def _parse_text(self, text_str):
        """Parse plain text equation"""
        try:
            # Remove spaces
            text_str = text_str.replace(' ', '')
            
            # Check if it's an equation
            if '=' in text_str:
                left, right = text_str.split('=')
                expr = parse_expr(f'({left}) - ({right})')
                return Eq(expr, 0)
            else:
                # Assume expression = 0
                expr = parse_expr(text_str)
                return Eq(expr, 0)
        except:
            return None
    
    def solve_linear(self, equation):
        """Solve linear equations"""
        try:
            solution = solve(equation, self.x)
            return {
                'type': 'linear',
                'solutions': solution,
                'steps': self._generate_linear_steps(equation)
            }
        except:
            return None
    
    def solve_quadratic(self, equation):
        """Solve quadratic equations"""
        try:
            # Get polynomial form
            poly = equation.lhs.as_poly()
            
            if poly and poly.degree() == 2:
                a, b, c = poly.all_coeffs()
                solution = solve(equation, self.x)
                
                return {
                    'type': 'quadratic',
                    'solutions': solution,
                    'coefficients': {'a': a, 'b': b, 'c': c},
                    'steps': self._generate_quadratic_steps(equation, a, b, c)
                }
        except:
            return None
    
    def solve_equation(self, equation_str):
        """Main solving function"""
        # Parse equation
        equation = self.parse_equation(equation_str)
        
        if not equation:
            return {'error': 'Could not parse equation'}
        
        # Try linear
        result = self.solve_linear(equation)
        if result:
            return result
        
        # Try quadratic
        result = self.solve_quadratic(equation)
        if result:
            return result
        
        # Generic solve
        try:
            solution = solve(equation, self.x)
            return {
                'type': 'generic',
                'solutions': solution,
                'steps': ['Solving equation...']
            }
        except:
            return {'error': 'Could not solve equation'}
    
    def _generate_linear_steps(self, equation):
        """Generate step-by-step for linear equations"""
        steps = []
        
        # Original equation
        steps.append({
            'step': 1,
            'description': 'Start with the original equation',
            'equation': latex(equation)
        })
        
        # Isolate x term
        lhs = equation.lhs
        rhs = equation.rhs
        
        # Add steps based on operations
        steps.append({
            'step': 2,
            'description': 'Move constant terms to the right side',
            'equation': f'{latex(lhs)} = {latex(rhs)}'
        })
        
        # Solve for x
        solution = solve(equation, self.x)
        steps.append({
            'step': 3,
            'description': 'Divide both sides by the coefficient',
            'equation': f'x = {latex(solution[0])}'
        })
        
        return steps
    
    def _generate_quadratic_steps(self, equation, a, b, c):
        """Generate step-by-step for quadratic equations"""
        steps = []
        
        # Step 1: Identify coefficients
        steps.append({
            'step': 1,
            'description': 'Identify coefficients',
            'equation': f'a = {a}, b = {b}, c = {c}'
        })
        
        # Step 2: Apply quadratic formula
        discriminant = b**2 - 4*a*c
        steps.append({
            'step': 2,
            'description': 'Calculate discriminant',
            'equation': f'Δ = b² - 4ac = {b}² - 4({a})({c}) = {discriminant}'
        })
        
        # Step 3: Find solutions
        steps.append({
            'step': 3,
            'description': 'Apply quadratic formula',
            'equation': f'x = [-{b} ± √({discriminant})] / (2×{a})'
        })
        
        return steps
    
    def validate_solution(self, equation, solution):
        """Validate if solution satisfies equation"""
        try:
            lhs = equation.lhs.subs(self.x, solution)
            rhs = equation.rhs.subs(self.x, solution)
            return abs(lhs - rhs) < 1e-10
        except:
            return False