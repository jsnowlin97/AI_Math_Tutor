import re

class MistakeDetector:
    def __init__(self):
        self.common_mistakes = {
            'sign_error': {
                'pattern': r'[+-][^=]*=[^=]*[+-]',
                'description': 'Sign error when moving terms',
                'severity': 'high'
            },
            'distribution': {
                'pattern': r'\d+\([^)]+\)',
                'description': 'Check distribution of multiplication',
                'severity': 'medium'
            },
            'like_terms': {
                'pattern': r'\d+x\s*[+-]\s*\d+[^x]',
                'description': 'Combining unlike terms',
                'severity': 'medium'
            }
        }
    
    def analyze_solution(self, equation, student_steps):
        """Analyze student solution for mistakes"""
        mistakes = []
        
        for i, step in enumerate(student_steps):
            step_mistakes = self._check_step(equation, step, i+1)
            mistakes.extend(step_mistakes)
        
        return {
            'has_mistakes': len(mistakes) > 0,
            'mistakes': mistakes,
            'summary': self._generate_summary(mistakes)
        }
    
    def _check_step(self, original_eq, step, step_num):
        """Check individual step for mistakes"""
        mistakes = []
        
        # Check sign errors
        if self._detect_sign_error(step):
            mistakes.append({
                'step': step_num,
                'type': 'sign_error',
                'description': 'Possible sign error in term movement',
                'correction': 'When moving terms across equals sign, change the sign'
            })
        
        # Check distribution
        if self._detect_distribution_error(step):
            mistakes.append({
                'step': step_num,
                'type': 'distribution',
                'description': 'Check multiplication distribution',
                'correction': 'Multiply the term outside parentheses with EVERY term inside'
            })
        
        # Check arithmetic
        arithmetic_error = self._check_arithmetic(step)
        if arithmetic_error:
            mistakes.append({
                'step': step_num,
                'type': 'arithmetic',
                'description': arithmetic_error,
                'correction': 'Double-check your arithmetic calculation'
            })
        
        return mistakes
    
    def _detect_sign_error(self, step):
        """Detect sign errors"""
        # Pattern for sign changes
        patterns = [
            r'([+-]\s*\d+)\s*=\s*([^=]+)\s*([+-]\s*\d+)',  # Moving terms
            r'(\d+)\s*=\s*[^=]+\s*([+-]\s*\d+)'  # Sign on right side
        ]
        
        for pattern in patterns:
            if re.search(pattern, step):
                return True
        return False
    
    def _detect_distribution_error(self, step):
        """Detect distribution errors"""
        # Check for parentheses without proper distribution
        if '(' in step and ')' in step:
            # Extract multiplication before parentheses
            match = re.search(r'(\d+)\(', step)
            if match:
                return True
        return False
    
    def _check_arithmetic(self, step):
        """Check arithmetic calculations"""
        # Extract numbers and operations
        numbers = re.findall(r'\d+', step)
        operations = re.findall(r'[+-]', step)
        
        # Simple validation (can be enhanced)
        if len(numbers) >= 2:
            # Check for obviously wrong arithmetic
            try:
                # This is a simplified check
                pass
            except:
                return "Check your arithmetic"
        
        return None
    
    def _generate_summary(self, mistakes):
        """Generate summary of mistakes"""
        if not mistakes:
            return "No common mistakes detected. Good work!"
        
        summary = f"Found {len(mistakes)} potential issues:\n"
        for mistake in mistakes:
            summary += f"- Step {mistake['step']}: {mistake['description']}\n"
        
        return summary
    
    def provide_hints(self, equation, mistake_type):
        """Provide helpful hints based on mistake type"""
        hints = {
            'sign_error': [
                "Remember: When moving a term across the equals sign, its sign changes",
                "Think of adding the same quantity to both sides instead of 'moving'",
                "Check if you kept the sign consistent throughout"
            ],
            'distribution': [
                "Distribute means multiply with EVERY term inside parentheses",
                "Example: 3(x + 2) = 3x + 6, not 3x + 2",
                "Draw arrows to track distribution"
            ],
            'arithmetic': [
                "Take it step by step",
                "Write down intermediate calculations",
                "Double-check with estimation"
            ],
            'like_terms': [
                "You can only combine terms with the same variable and exponent",
                "3x and 5x can combine, but 3x and 5 cannot",
                "Sort terms before combining"
            ]
        }
        
        return hints.get(mistake_type, ["Review the step carefully"])