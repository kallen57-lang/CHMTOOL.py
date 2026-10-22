import math


GAS_CONSTANT = 0.08206
ELEMENTS = {
    "H": ("Hydrogen", 1.008, "1s1"),
    "He": ("Helium", 4.003, "1s2"),
    "C": ("Carbon", 12.011, "[He] 2s2 2p2"),
    "N": ("Nitrogen", 14.007, "[He] 2s2 2p3"),
    "O": ("Oxygen", 15.999, "[He] 2s2 2p4"),
    "Na": ("Sodium", 22.990, "[Ne] 3s1"),
    "Mg": ("Magnesium", 24.305, "[Ne] 3s2"),
    "Cl": ("Chlorine", 35.45, "[Ne] 3s2 3p5"),
    "K": ("Potassium", 39.098, "[Ar] 4s1"),
    "Ca": ("Calcium", 40.078, "[Ar] 4s2"),
    "Sc": ("Scandium", 44.956, "[Ar] 3d1 4s2"),
    "Ti": ("Titanium", 47.867, "[Ar] 3d2 4s2"),
    "V": ("Vanadium", 50.942, "[Ar] 3d3 4s2"),
    "Cr": ("Chromium", 51.996, "[Ar] 3d5 4s1"),
    "Mn": ("Manganese", 54.938, "[Ar] 3d5 4s2"),
    "Fe": ("Iron", 55.845, "[Ar] 3d6 4s2"),
    "Co": ("Cobalt", 58.933, "[Ar] 3d7 4s2"),
    "Ni": ("Nickel", 58.693, "[Ar] 3d8 4s2"),
    "Cu": ("Copper", 63.546, "[Ar] 3d10 4s1"),
    "Zn": ("Zinc", 65.38, "[Ar] 3d10 4s2"),
}


def element_data():
    symbol = input("Enter Element Symbol (e.g. O, Na): ").strip().title()
    if symbol in ELEMENTS:
        name, mass, config = ELEMENTS[symbol]
        print("\n" + name)
        print("Mass:", mass, "g/mol")
        print("Config:", config)
    else:
        print("Element not in quick-database.")


def get_molar_mass():
    value = input("Enter Element Symbol (e.g. O, Na) or molar mass (g/mol): ").strip()
    try:
        molar_mass = float(value)
    except ValueError:
        molar_mass = None
    else:
        if not math.isfinite(molar_mass) or molar_mass <= 0:
            print("Molar mass must be a finite number greater than zero.")
            return None
        print("Using molar mass:", molar_mass, "g/mol")
        return molar_mass

    element = ELEMENTS.get(value.title())
    if element is None:
        print("Enter a valid element symbol or positive molar mass.")
        return None

    name, molar_mass, _ = element
    print("Using", name, "molar mass:", molar_mass, "g/mol")
    return molar_mass


def moles_mass():
    print("\n1: Solve moles (n = mass / molar mass)")
    print("2: Solve mass (mass = n * molar mass)")
    print("3: Solve molar mass (molar mass = mass / n)")
    choice = int(input("Choice: "))
    if choice == 1:
        mass = float(input("Enter Mass (g): "))
        molar_mass = get_molar_mass()
        if molar_mass is None:
            return
        print("Moles:", round(mass / molar_mass, 4), "mol")
    elif choice == 2:
        moles = float(input("Enter Moles (mol): "))
        molar_mass = get_molar_mass()
        if molar_mass is None:
            return
        print("Mass:", round(moles * molar_mass, 4), "g")
    elif choice == 3:
        mass = float(input("Enter Mass (g): "))
        moles = float(input("Enter Moles (mol): "))
        if moles == 0:
            print("Moles must be nonzero to solve molar mass.")
            return
        print("Molar mass:", round(mass / moles, 4), "g/mol")
    else:
        print("Invalid choice.")


def gas_laws():
    print("\nSolve for missing value (Enter 0 for unknown)")
    pressure = float(input("P (atm): "))
    volume = float(input("V (L): "))
    moles = float(input("n (mol): "))
    temperature = float(input("T (K): "))

    unknown_count = sum(value == 0 for value in (pressure, volume, moles, temperature))
    if unknown_count != 1:
        print("Enter exactly one unknown as 0; all known values must be nonzero.")
        return

    if pressure == 0:
        print("P =", round((moles * GAS_CONSTANT * temperature) / volume, 4), "atm")
    elif volume == 0:
        print("V =", round((moles * GAS_CONSTANT * temperature) / pressure, 4), "L")
    elif moles == 0:
        print("n =", round((pressure * volume) / (GAS_CONSTANT * temperature), 4), "mol")
    elif temperature == 0:
        print("T =", round((pressure * volume) / (moles * GAS_CONSTANT), 2), "K")


def ph_calc():
    print("\nSolve the related values from one known value (at 25 C).")
    print("1: Given pH\n2: Given pOH\n3: Given [H+]\n4: Given [OH-]")
    choice = int(input("Choice: "))

    if choice == 1:
        ph = float(input("Enter pH: "))
        poh = 14.0 - ph
    elif choice == 2:
        poh = float(input("Enter pOH: "))
        ph = 14.0 - poh
    elif choice == 3:
        hydrogen_ion = float(input("Enter [H+] (e.g. 1e-3): "))
        if hydrogen_ion <= 0:
            raise ValueError("Hydrogen concentration must be positive.")
        ph = -math.log10(hydrogen_ion)
        poh = 14.0 - ph
    elif choice == 4:
        hydroxide_ion = float(input("Enter [OH-] (e.g. 1e-3): "))
        if hydroxide_ion <= 0:
            raise ValueError("Hydroxide concentration must be positive.")
        poh = -math.log10(hydroxide_ion)
        ph = 14.0 - poh
    else:
        print("Invalid choice.")
        return

    hydrogen_ion = 10 ** (-ph)
    hydroxide_ion = 10 ** (-poh)
    print("pH:", round(ph, 2))
    print("pOH:", round(poh, 2))
    print("[H+]:", "{:.2e}".format(hydrogen_ion))
    print("[OH-]:", "{:.2e}".format(hydroxide_ion))


def thermo():
    print("\nSpecific Heat: q = m * c * dT")
    print("1: Solve heat q\n2: Solve mass m\n3: Solve specific heat c\n4: Solve temperature change dT")
    choice = int(input("Choice: "))
    if choice == 1:
        mass = float(input("Mass m (g): "))
        specific_heat = float(input("Specific heat c (J/gC): "))
        temperature_change = float(input("Temp change dT (C): "))
        print("Heat energy q =", round(mass * specific_heat * temperature_change, 2), "J")
    elif choice == 2:
        heat = float(input("Heat q (J): "))
        specific_heat = float(input("Specific heat c (J/gC): "))
        temperature_change = float(input("Temp change dT (C): "))
        denominator = specific_heat * temperature_change
        if denominator == 0:
            print("Specific heat and temperature change must have a nonzero product.")
            return
        print("Mass m =", round(heat / denominator, 4), "g")
    elif choice == 3:
        heat = float(input("Heat q (J): "))
        mass = float(input("Mass m (g): "))
        temperature_change = float(input("Temp change dT (C): "))
        denominator = mass * temperature_change
        if denominator == 0:
            print("Mass and temperature change must have a nonzero product.")
            return
        print("Specific heat c =", round(heat / denominator, 4), "J/gC")
    elif choice == 4:
        heat = float(input("Heat q (J): "))
        mass = float(input("Mass m (g): "))
        specific_heat = float(input("Specific heat c (J/gC): "))
        denominator = mass * specific_heat
        if denominator == 0:
            print("Mass and specific heat must have a nonzero product.")
            return
        print("Temp change dT =", round(heat / denominator, 4), "C")
    else:
        print("Invalid choice.")