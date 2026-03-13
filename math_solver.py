
import easyocr
import sympy as sp
import cv2
import numpy as np
from PIL import Image


# -------- OCR DETECTION --------
def detect_equation(image_path):

    reader = easyocr.Reader(['en'])

    image = cv2.imread(image_path)

    results = reader.readtext(image)

    equation = ""

    for (_, text, confidence) in results:
        equation += text + " "

    equation = equation.strip()

    print("\nDetected Equation:", equation)

    return equation


# -------- SOLVE EQUATION --------
def solve_equation(equation):

    try:

        x = sp.symbols('x')

        left, right = equation.split("=")

        expr = sp.Eq(sp.sympify(left), sp.sympify(right))

        print("\nParsed Equation:")
        print(expr)

        solution = sp.solve(expr, x)

        print("\nStep-by-step solving:")

        print("1. Move constants to other side")
        print("2. Simplify equation")
        print("3. Solve for x")

        print("\nFinal Solution:")

        for s in solution:
            print("x =", s)

    except Exception as e:
        print("Error solving equation:", e)


# -------- MAIN PROGRAM --------
def main():

    image_path = input("Enter image path: ")

    equation = detect_equation(image_path)

    if equation:
        solve_equation(equation)
    else:
        print("No equation detected.")


if __name__ == "__main__":
    main()

