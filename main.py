# This code attempts to find x in polynomial equations (resulting in 0) starting from an initial value entered

# Objective: find the value of x that solves the equation = 0

# It still doesn't cover irrational roots!!!!!

# Expected results and additional explanations are in the notes.tex file, which are my supermemo brief notes (that doesn't cover everything as well).

#########################################################################################

from typing import Dict, Union
import argparse

parts: Dict[int, Union[int, float]] = {}

def parse_polynomial(polynomial: str) -> None:
    global parts
    polynomial = polynomial.replace(" ", "").replace("−", "-").replace("–", "-")
    
    import re
    terms = re.findall(r'[+-]?[^+-]+', polynomial)

    for term in terms:
        if term.startswith("+"):
            term = term[1:]
            
        coef: Union[int, float, str] = ""
        exponent: Union[int, str] = ""

        if "x" in term:
            if "^" in term:
                elements = term.split("x^")
                coef = elements[0]
                exponent = elements[1]
            else:
                elements = term.split("x")
                coef = elements[0]
                exponent = 1
            
            if coef == "" or coef == "+":
                coef = 1
            elif coef == "-":
                coef = -1
            else:
                coef = int(coef)

            exponent = int(exponent)

        else:
            exponent = 0
            if "^" in term:
                base_exp = term.split("^")
                coef = int(base_exp[0]) ** int(base_exp[1]) 
            else:
                coef = int(term)

        if isinstance(coef, (int, float, str)) and coef != "":
            final_coef = float(coef)
        else:
            final_coef = 0.0

        if exponent in parts:
            parts[int(exponent)] += final_coef
        else:
            parts[int(exponent)] = final_coef

# normalize
def polynomial_to_coeff_list(polynomial: Dict[int, Union[int, float]]) -> list[float]:
    degree = max(polynomial.keys())
    coeffs = []

    for d in range(degree, -1, -1):
        coeffs.append(float(polynomial.get(d, 0.0)))

    return coeffs


def test_result_polynomial(unknown: float, polynomial: Dict[int, Union[int, float]]) -> float:
    equation = []
    for exponent, coef in polynomial.items():
        if exponent > 0:
            x = unknown ** exponent
            equation.append(x * coef)
        else:
            equation.append(float(coef))

    return float(sum(equation))
              
def generate_derivative(parts_original: Dict[int, Union[int, float]]) -> Dict[int, Union[int, float]]:
    parts_derivative: Dict[int, Union[int, float]] = {}

    for exponent, coef in parts_original.items():
        if exponent > 0:
            new_coef = exponent * coef
            new_exponent = exponent - 1

            parts_derivative[new_exponent] = new_coef
    
    return parts_derivative

def use_newton_method(unknown: float, parts_original: Dict[int, Union[int, float]], parts_derivative: Dict[int, Union[int, float]]) -> float:

    original_poly_result = test_result_polynomial(unknown, parts_original)
    derivative_poly_result = test_result_polynomial(unknown, parts_derivative)

    method_result = unknown - (original_poly_result/derivative_poly_result)

    return float(method_result)

def use_rational_root_theorem(coeffs: list[float]) -> list[float]:
    leading_coefficient = abs(int(coeffs[0]))
    constant = abs(int(coeffs[-1]))

    leading_divs = find_divisors(leading_coefficient)
    const_divs = find_divisors(constant)

    possibilities = []

    for q in leading_divs:
        for p in const_divs:
            r = p / q
            possibilities.append(r)
            possibilities.append(-r)

    possibilities = list(set(possibilities))
    return possibilities



def find_divisors(number: int) -> list:
    divisor = number
    divisors: list[int] = []

    while divisor > 0:
        if number % divisor == 0:
            divisors.append(divisor)
        divisor -= 1

    return divisors

def use_briot_ruffini(root: Union[float, int], polynomial: Dict[int, Union[int, float]]) -> list[Union[int, float]]:

    degree = max(list(polynomial.keys()))

    full_coeffs = []
    for d in range(degree, -1, -1):
        full_coeffs.append(polynomial.get(d, 0.0))

    stored = []
    r_number = full_coeffs[0]
    stored.append(r_number)

    for i in range(1, len(full_coeffs)):
        r_number = (r_number * root) + full_coeffs[i]
        
        if i < len(full_coeffs) - 1:
            stored.append(r_number)

    return stored

def use_bhaskara(coefficients: list[float]) -> list[str]:
    a = coefficients[0]
    b = coefficients[1]
    c = coefficients[2]

    delta = (b**2) - (4 * a * c)
    
    roots = []

    if delta >= 0:
        x1 = (-b + (delta**0.5)) / (2 * a)
        x2 = (-b - (delta**0.5)) / (2 * a)
        roots.append(f"{x1:.2f}")

        if delta > 0:
            roots.append(f"{x2:.2f}")
    else:

        parte_real = -b / (2 * a)
        parte_imaginaria = (abs(delta)**0.5) / (2 * a)
        
        roots.append(f"{parte_real:.2f} + {parte_imaginaria:.2f}i")
        roots.append(f"{parte_real:.2f} - {parte_imaginaria:.2f}i")

    return roots

# x^2-3x+5 // esse tá difiço porque a raíz é irracional (vou precisar de outros métodos)
# 2x^3 - 5x^2 - 5 + 12
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PolyPocket ~ Polynomial Solver\n\n"
                                     "Enter the equation in the format: 2x^3 - 5x^2 - 5 + 12",
                                     formatter_class=argparse.RawTextHelpFormatter)

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-n", "--newton", type=str, help="Run Newton's method with the given equation")
    group.add_argument("-p", "--rational", type=str, help="Run the Rational Root Theorem with the given equation")

    parser.add_argument("-u", "--unknown", type=float, help="Initial guess for Newton's method (required with -n)", default=None)


    args = parser.parse_args()
    parts.clear()

    polynomial_input = args.newton if args.newton else args.rational
    parse_polynomial(polynomial_input)
    coeffs = polynomial_to_coeff_list(parts)

    if args.newton:
        if args.unknown is None:
            print("Error: Newton's method requires an initial guess (-u).")
        else:
            unknown = args.unknown
            derivative = generate_derivative(parts)
            found = False
            
            for i in range(500):
                current_result = test_result_polynomial(unknown, parts)
                if abs(current_result) < 0.000001:
                    found = True
                    break
                
                d_val = test_result_polynomial(unknown, derivative)
                if d_val == 0: break
                
                unknown = use_newton_method(unknown, parts, derivative)
                print(f"Attempt {i+1}: x = {unknown:.4f}")

            if found:
                print(f"\nRoot found using Newton's method: {unknown:.4f}")
            else:
                print("\nNewton's method failed to converge with this initial guess.")

    elif args.rational:
        possibilities = use_rational_root_theorem(coeffs)
        found_roots = []
        
        for possibility in possibilities:
            result = test_result_polynomial(float(possibility), parts)
            if abs(result) < 1e-5:
                if possibility not in found_roots:
                    found_roots.append(possibility)
        
        if found_roots:
            print(f"Rational roots found: {found_roots}")
            
            degree = max(parts.keys())
            current_coeffs = []
            for d in range(degree, -1, -1):
                current_coeffs.append(parts.get(d, 0.0))
            
 
            root_index = 0
            while len(current_coeffs) > 3 and root_index < len(found_roots):
                r = found_roots[root_index]
                print(f"Reducing degree {len(current_coeffs)-1} -> {len(current_coeffs)-2} using root: {r}")
                
                temp_dict = {len(current_coeffs)-1-i: c for i, c in enumerate(current_coeffs)}
                current_coeffs = use_briot_ruffini(r, temp_dict)
                root_index += 1

            if len(current_coeffs) == 3:
                print(f"Polynomial reduced to degree 2: {current_coeffs}")
                final_bhaskara = use_bhaskara(current_coeffs)
                print(f"Final roots via quadratic formula: {final_bhaskara}")
            else:
                print(f"Could not reduce further. Remaining coefficients: {current_coeffs}")
        else:
            print("No rational roots found using the Rational Root Theorem.")