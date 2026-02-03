# This code attempts to find x in polynomial equations starting from an initial value entered
# Initially it will do so using Newton's Method
# In the future I plan to include possible solutions via the Rational Root Theorem (p/q), Briot-Ruffini, Bhaskara, and grouping factoring
# I also intend to add graphs and visual feedback of the process.

# Current state: initial, uses only Newton's Method, does not display anything visually
# Objective: find the value of x that solves the equation = 0

# Still haven't solved complex roots! I also haven't reviewed to ensure that the Newton method won't diverge (it will).

# Expected results and additional explanations are in the results.tex file



#########################################################################################

from typing import Dict, Union

parts: Dict[int, Union[int, float]] = {}

def parse_polynomial(polynomial: str) -> None:
    global parts
    polynomial_terms = polynomial.replace(" ", "").replace("-", "+-")
    if polynomial_terms.startswith("+"): 
        polynomial_terms = polynomial_terms[1:]

    polynomial_terms_full = polynomial_terms.split("+")

    for term in polynomial_terms_full:
        
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

if __name__ == "__main__":
    polynomial_input: str = input("Please enter the polynomial. Example: x^2−5x+6 ")
    unknown: float = float(input("Now enter the value to be tested as x "))

    parse_polynomial(polynomial_input)

    derivative: Dict[int, Union[int, float]] = generate_derivative(parts)
    
    for i in range(100):  
            current_result: float = test_result_polynomial(unknown, parts)

            if abs(current_result) < 0.000001:
                break
                
            unknown = use_newton_method(unknown, parts, derivative)
            print(f"Attempt {i+1}: x = {unknown:.4f}")

    print("Result found :)")
    print(f"Final result: {unknown:.2f}")