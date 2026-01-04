import math
from sympy import parse_expr, Poly, symbols, Eq, solve as sympy_solve

class EquationSolver:
    def __init__(self, equation_str):
        self.equation_str = equation_str

    def parse(self):
        if not self.equation_str.strip():
            exit("No input provided. Exiting.")


        if "=" not in self.equation_str:
            raise ValueError("Invalid equation: missing '='")
        
        # Replace ^ with ** for sympy if user used ^, although convert_xor handles it.
        # But let's be safe. Actually convert_xor is enough.
        
        left_str, right_str = self.equation_str.split("=")
        
        x = symbols('x')
        try:
            from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
            transformations = (standard_transformations + (implicit_multiplication_application,) + (convert_xor,))
            
            # Handle empty sides
            if not left_str.strip(): left_str = "0"
            if not right_str.strip(): right_str = "0"
            
            left_expr = parse_expr(left_str, transformations=transformations)
            right_expr = parse_expr(right_str, transformations=transformations)
            
            full_expr = left_expr - right_expr
            
            # Ensure it's a polynomial in x
            poly = Poly(full_expr, x)
            
            # Check degree
            if poly.degree() > 2:
                raise ValueError("Equation degree is higher than 2.")
            
            # Get coefficients for ax^2 + bx + c
            a = poly.coeff_monomial(x**2)
            b = poly.coeff_monomial(x)
            c = poly.coeff_monomial(1)
            
            return a, b, c
        except Exception as e:
            raise ValueError(f"Error parsing equation: {e}")

    def solve(self):
        try:
            a_sym, b_sym, c_sym = self.parse()
        except ValueError as e:
            return [str(e)]

        # Convert to float for numerical steps, but keep SymPy objects for potential symbolic steps
        # For now, let's keep it simple and convert to float where appropriate
        try:
            a = float(a_sym)
            b = float(b_sym)
            c = float(c_sym)
        except:
            # If we can't convert to float (e.g. they are purely symbolic constants like 'pi'), 
            # we might need to handle it differently. But the issue says "expression parsing for coefficients".
            a, b, c = a_sym, b_sym, c_sym

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
                sqrt_d = math.sqrt(float(discriminant))
                steps.append(f"Step 2: Calculate square root of D: √{discriminant} = {sqrt_d}")
                x1 = (-b + sqrt_d) / (2 * a)
                x2 = (-b - sqrt_d) / (2 * a)
                steps.append(f"Step 3: Solve for x = (-b ± √Δ) / 2a")
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
                steps.append("The discriminant Δ is negative, so there are two complex roots.")
                real_part = -b / (2 * a)
                imag_part = math.sqrt(float(-discriminant)) / (2 * a)
                steps.append(f"Step 2: Calculate the real and imaginary parts:")
                steps.append(f"Real part = -b / 2a = -({b}) / (2 * {a}) = {real_part}")
                steps.append(f"Imaginary part = √(abs(Δ)) / 2a = √{abs(discriminant)} / (2 * {a}) = {abs(imag_part)}")
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
