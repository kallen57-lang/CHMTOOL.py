import math
import re
from fractions import Fraction


VALID_ELEMENTS = set(
    "H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn "
    "Ga Ge As Se Br Kr Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs Ba La "
    "Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po "
    "At Rn Fr Ra Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr Rf Db Sg Bh Hs Mt Ds Rg "
    "Cn Nh Fl Mc Lv Ts Og".split()
)


def parse_formula(formula):
    tokens = re.findall(r"[A-Z][a-z]?|\d+|[()]", formula)
    if not tokens or "".join(tokens) != formula:
        raise ValueError("Invalid chemical formula: " + formula)
    position = 0

    def parse_group(nested=False):
        nonlocal position
        counts = {}
        while position < len(tokens):
            token = tokens[position]
            position += 1
            if token == ")":
                if not nested:
                    raise ValueError("Unmatched closing parenthesis in " + formula)
                return counts
            if token == "(":
                group_counts = parse_group(True)
                multiplier = 1
                if position < len(tokens) and tokens[position].isdigit():
                    multiplier = int(tokens[position])
                    position += 1
            elif token in VALID_ELEMENTS:
                group_counts = {token: 1}
                multiplier = 1
                if position < len(tokens) and tokens[position].isdigit():
                    multiplier = int(tokens[position])
                    position += 1
            else:
                raise ValueError("Unexpected token in chemical formula: " + token)
            if multiplier <= 0:
                raise ValueError("Formula subscripts must be positive.")
            for element, amount in group_counts.items():
                counts[element] = counts.get(element, 0) + amount * multiplier

        if nested:
            raise ValueError("Unmatched opening parenthesis in " + formula)
        return counts

    counts = parse_group()
    if position != len(tokens):
        raise ValueError("Invalid chemical formula: " + formula)
    return counts


def balance_equation():
    equation = input("Enter equation (use ->, e.g. H2 + O2 -> H2O): ").replace(" ", "")
    sides = re.split(r"->|=", equation)
    if len(sides) != 2 or not sides[0] or not sides[1]:
        print("Enter one equation with reactants and products separated by -> or =.")
        return

    reactants = sides[0].split("+")
    products = sides[1].split("+")
    formulas = reactants + products
    try:
        compounds = [parse_formula(formula) for formula in formulas]
    except ValueError as error:
        print("Could not parse equation:", error)
        return

    elements = sorted({element for compound in compounds for element in compound})
    matrix = [
        [
            Fraction(compounds[column].get(element, 0) * (1 if column < len(reactants) else -1))
            for column in range(len(formulas))
        ]
        for element in elements
    ]

    pivot_columns = []
    pivot_row = 0
    for column in range(len(formulas)):
        selected_row = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][column]),
            None,
        )
        if selected_row is None:
            continue
        matrix[pivot_row], matrix[selected_row] = matrix[selected_row], matrix[pivot_row]
        pivot = matrix[pivot_row][column]
        matrix[pivot_row] = [value / pivot for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row != pivot_row and matrix[row][column]:
                factor = matrix[row][column]
                matrix[row] = [
                    value - factor * pivot_value
                    for value, pivot_value in zip(matrix[row], matrix[pivot_row])
                ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(matrix):
            break

    free_columns = [column for column in range(len(formulas)) if column not in pivot_columns]
    if len(free_columns) != 1:
        print("This equation does not have one unique set of balancing ratios.")
        return

    coefficients = [Fraction(0) for _ in formulas]
    free_column = free_columns[0]
    coefficients[free_column] = Fraction(1)
    for row, column in enumerate(pivot_columns):
        coefficients[column] = -matrix[row][free_column]
    if all(coefficient < 0 for coefficient in coefficients):
        coefficients = [-coefficient for coefficient in coefficients]
    if any(coefficient <= 0 for coefficient in coefficients):
        print("No positive balancing coefficients were found for this equation.")
        return

    denominator_lcm = 1
    for coefficient in coefficients:
        denominator = coefficient.denominator
        denominator_lcm = abs(denominator_lcm * denominator) // math.gcd(
            denominator_lcm, denominator
        )
    integer_coefficients = [
        coefficient.numerator * (denominator_lcm // coefficient.denominator)
        for coefficient in coefficients
    ]
    common_divisor = integer_coefficients[0]
    for coefficient in integer_coefficients[1:]:
        common_divisor = math.gcd(common_divisor, coefficient)
    integer_coefficients = [coefficient // common_divisor for coefficient in integer_coefficients]

    balanced = [
        ("" if coefficient == 1 else str(coefficient)) + formula
        for coefficient, formula in zip(integer_coefficients, formulas)
    ]
    print(
        "Balanced:",
        " + ".join(balanced[:len(reactants)]),
        "->",
        " + ".join(balanced[len(reactants):]),
    )