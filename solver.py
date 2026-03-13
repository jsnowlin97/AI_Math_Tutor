import sympy as sp
import re

def solve_equation(latex_eq):
    """Solve algebraic equation step by step"""
    
    # Clean LaTeX
    equation = latex_eq.replace('$$', '').strip()
    
    # Parse equation
    if '=' in equation:
        left, right = equation.split('=')
        
        # Convert to sympy expression
        x = sp.symbols('x')
        
        try:
            # Parse expressions
            left_expr = sp.sympify(left)
            right_expr = sp.sympify(right)
            
            # Create equation
            eq = sp.Eq(left_expr, right_expr)
            
            # Solve
            solutions = sp.solve(eq, x)
            
            # Generate steps
            steps = [
                {
                    'number': 1,
                    'explanation': 'Original equation:',
                    'equation': equation
                },
                {
                    'number': 2,
                    'explanation': 'Rearranging terms:',
                    'equation': f'{left} - {right} = 0'
                },
                {
                    'number': 3,
                    'explanation': 'Solving for x:',
                    'equation': f'x = {solutions[0] if solutions else "No solution"}'
                }
            ]
            
            return {
                'steps': steps,
                'answer': f'x = {solutions[0]}' if solutions else 'No solution found'
            }
            
        except:
            return {
                'steps': [{'number': 1, 'explanation': 'Could not parse equation'}],
                'answer': 'Unable to solve'
            }
    
    return {
        'steps': [{'number': 1, 'explanation': 'Invalid equation format'}],
        'answer': 'Please provide an equation with = sign'
    }