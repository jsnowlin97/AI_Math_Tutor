import os
import google.generativeai as genai
from dotenv import load_dotenv
import PIL.Image
import io

load_dotenv()

class GeminiClient:
    def __init__(self):
        """Initialize Gemini client with API key"""
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.model_name = os.getenv('MODEL_NAME', 'gemini-2.5-flash')
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)
        
    def image_to_latex(self, image):
        """Convert image to LaTeX equation"""
        prompt = """
        Extract the mathematical equation from this image and convert it to LaTeX format.
        Rules:
        1. Output ONLY the LaTeX code, no explanations
        2. Use proper LaTeX syntax: for fractions use \frac{}{}
        3. For exponents use ^
        4. For square roots use \sqrt{}
        5. Include proper brackets
        6. If multiple equations, separate with \\
        """
        
        try:
            response = self.model.generate_content([prompt, image])
            return self._clean_latex(response.text)
        except Exception as e:
            return f"Error: {str(e)}"
    
    def solve_step_by_step(self, equation):
        """Generate step-by-step solution"""
        prompt = f"""
        Solve this equation step by step: {equation}
        
        Format your response as:
        Step 1: [explanation]
        Step 2: [explanation]
        ...
        Final Answer: x = [value]
        
        Include mathematical reasoning and show all algebraic manipulations.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return self._parse_solution_steps(response.text)
        except Exception as e:
            return {"error": str(e)}
    
    def detect_mistakes(self, equation, student_solution):
        """Identify common algebraic mistakes"""
        prompt = f"""
        Analyze this equation: {equation}
        Student's solution attempt: {student_solution}
        
        Identify any mistakes:
        1. Sign errors
        2. Distribution errors  
        3. Like term combination errors
        4. Arithmetic errors
        
        For each mistake, explain:
        - What was wrong
        - Why it's wrong
        - How to fix it
        """
        
        try:
            response = self.model.generate_content(prompt)
            return self._parse_mistakes(response.text)
        except Exception as e:
            return {"error": str(e)}
    
    def _clean_latex(self, text):
        """Clean and format LaTeX output"""
        # Remove markdown code blocks if present
        text = text.replace('```latex', '').replace('```', '')
        return text.strip()
    
    def _parse_solution_steps(self, text):
        """Parse solution into structured steps"""
        steps = []
        lines = text.split('\n')
        
        for line in lines:
            if line.lower().startswith('step'):
                steps.append(line)
            elif line.lower().startswith('final answer'):
                final_answer = line
        
        return {
            'steps': steps,
            'final_answer': final_answer if 'final_answer' in locals() else ''
        }
    
    def _parse_mistakes(self, text):
        """Parse mistake analysis"""
        return {'analysis': text}