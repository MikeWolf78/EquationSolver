import re
import math

class EquationSolver:
    def __init__(self, equation_str):
        self.equation_str = equation_str.replace(" ", "").lower()

    def parse(self):
        if self.equation_str.blank():
            exit("No input provided. Exiting.")
        # Normalize the equation to the form ax^2 + bx + c = 0
        if "=" not in self.equation_str:
            raise ValueError("Invalid equation: missing '='")
        
        left, right = self.equation_str.split("=")
        
        # Combine everything on the left side
        # To do this easily, we can parse terms on both sides
        coeffs_left = self._get_coefficients(left)
        coeffs_right = self._get_coefficients(right)
        
        a = coeffs_left.get(2, 0) - coeffs_right.get(2, 0)
        b = coeffs_left.get(1, 0) - coeffs_right.get(1, 0)
        c = coeffs_left.get(0, 0) - coeffs_right.get(0, 0)
        
        return a, b, c

    def _get_coefficients(self, expression):
        # Match terms like: +2x^2, -x, 5, -3x^2, x^2
        # regex to find terms: ([+-]?\d*\.?\d*)(x(\^2)?)?
        # We need to ensure we don't just match empty strings.
        # Replacing x^2 with something unique to avoid 'x' matching 'x' in 'x^2'
        temp_expr = expression.replace("x^2", "U")
        pattern = r'([+-]?\d*\.?\d*)([xU])?'
        matches = re.finditer(pattern, temp_expr)
        
        coeffs = {2: 0, 1: 0, 0: 0}
        
        for match in matches:
            coeff_str = match.group(1)
            variable_part = match.group(2)
            
            if not coeff_str and not variable_part:
                continue
            
            # Determine the value of the coefficient
            if coeff_str == "+" or coeff_str == "":
                val = 1.0
            elif coeff_str == "-":
                val = -1.0
            else:
                try:
                    val = float(coeff_str)
                except ValueError:
                    continue
            
            # Determine the degree
            if not variable_part:
                coeffs[0] += val
            elif variable_part == "x":
                coeffs[1] += val
            elif variable_part == "U":
                coeffs[2] += val
                
        return coeffs

    def solve(self):
        try:
            a, b, c = self.parse()
        except ValueError as e:
            return [str(e)]

        steps = [f"Equation simplified to: {a}x^2 + {b}x + {c} = 0"]

        if a == 0:
            # Linear equation bx + c = 0
            steps.append("This is a linear equation.")
            if b == 0:
                if c == 0:
                    steps.append("0 = 0. The equation has infinitely many solutions.")
                else:
                    steps.append(f"{c} = 0. This is a contradiction. No solution.")
            else:
                steps.append(f"Step 1: Subtract {c} from both sides: {b}x = {-c}")
                x = -c / b
                steps.append(f"Step 2: Divide by {b}: x = {-c} / {b} = {x}")
                steps.append(f"Result: x = {x}")
        else:
            # Quadratic equation ax^2 + bx + c = 0
            steps.append("This is a quadratic equation.")
            steps.append(f"Using the quadratic formula: x = (-b ± √Δ) / 2a")
            steps.append(f"Where a = {a}, b = {b}, c = {c}")
            
            discriminant = b**2 - 4*a*c
            steps.append(f"Step 1: Calculate the discriminant Δ = b^2 - 4ac ")
            steps.append(f"Δ = ({b})^2 - 4 * ({a}) * ({c})")
            steps.append(f"Δ = {b**2} - {4*a*c}")
            steps.append(f"Δ = {discriminant}")
            
            if discriminant > 0:
                steps.append("The discriminant is positive, so there are two real roots.")
                sqrt_d = math.sqrt(discriminant)
                steps.append(f"Step 2: Calculate square root of D: √{discriminant} = {sqrt_d}")
                x1 = (-b + sqrt_d) / (2 * a)
                x2 = (-b - sqrt_d) / (2 * a)
                steps.append(f"Step 3: Solve for x = (-b ± √D) / 2a")
                steps.append(f"x1 = (-({b}) + {sqrt_d}) / (2 * {a}) = {x1}")
                steps.append(f"x2 = (-({b}) - {sqrt_d}) / (2 * {a}) = {x2}")
                steps.append(f"Results: x1 = {x1}, x2 = {x2}")
            elif discriminant == 0:
                steps.append("The discriminant is zero, so there is one real root.")
                x = -b / (2 * a)
                steps.append(f"Step 2: Solve for x = -b / 2a")
                steps.append(f"x = -({b}) / (2 * {a}) = {x}")
                steps.append(f"Result: x = {x}")
            else:
                steps.append("The discriminant is negative, so there are two complex roots.")
                real_part = -b / (2 * a)
                imag_part = math.sqrt(-discriminant) / (2 * a)
                steps.append(f"Step 2: Calculate the real and imaginary parts:")
                steps.append(f"Real part = -b / 2a = -({b}) / (2 * {a}) = {real_part}")
                steps.append(f"Imaginary part = √(abs(D)) / 2a = √{abs(discriminant)} / (2 * {a}) = {abs(imag_part)}")
                steps.append(f"Results: x1 = {real_part} + {abs(imag_part)}i, x2 = {real_part} - {abs(imag_part)}i")
        
        return steps

def main():
    print("Welcome to the Equation Solver!")
    print("Please enter an equation in terms of x (e.g., 'x^2 + 2x + 1 = 0' or '2x - 4 = 0').")
    
    while True:
        try:
            equation_input = input("\nEnter equation (or 'quit' to exit): ")
            if equation_input.lower() == 'quit':
                break
            
            solver = EquationSolver(equation_input)
            steps = solver.solve()
            
            print("\nSteps to solve:")
            for step in steps:
                print(f"- {step}")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
