import math


CONVERSION_UNITS = {
    "Mass": {
        "ug": (1e-6, 0), "mg": (1e-3, 0), "g": (1, 0), "kg": (1000, 0),
        "oz": (28.349523125, 0), "lb": (453.59237, 0),
    },
    "Volume": {
        "uL": (1e-6, 0), "mL": (1e-3, 0), "L": (1, 0), "m3": (1000, 0),
        "US fl oz": (0.0295735295625, 0), "US gal": (3.785411784, 0),
    },
    "Pressure": {
        "Pa": (1, 0), "kPa": (1000, 0), "MPa": (1e6, 0), "bar": (1e5, 0),
        "atm": (101325, 0), "torr": (101325 / 760, 0),
        "mmHg": (133.322387415, 0), "psi": (6894.757293168, 0),
    },
    "Temperature": {
        "C": (1, 273.15), "F": (5 / 9, 255.3722222222), "K": (1, 0),
    },
    "Energy": {
        "J": (1, 0), "kJ": (1000, 0), "cal": (4.184, 0), "kcal": (4184, 0),
        "eV": (1.602176634e-19, 0),
    },
    "Length": {
        "nm": (1e-9, 0), "um": (1e-6, 0), "mm": (1e-3, 0), "cm": (1e-2, 0),
        "m": (1, 0), "km": (1000, 0), "in": (0.0254, 0), "ft": (0.3048, 0),
    },
    "Amount": {
        "umol": (1e-6, 0), "mmol": (1e-3, 0), "mol": (1, 0), "kmol": (1000, 0),
        "particles": (1 / 6.02214076e23, 0),
    },
    "Concentration (amount/volume)": {
        "umol/L": (1e-6, 0), "mmol/L": (1e-3, 0), "mol/L": (1, 0),
        "mol/m3": (1e-3, 0),
    },
    "Concentration (mass/volume)": {
        "ug/L": (1e-6, 0), "mg/L": (1e-3, 0), "g/L": (1, 0),
        "kg/m3": (1, 0),
    },
    "Time": {
        "ms": (1e-3, 0), "s": (1, 0), "min": (60, 0), "h": (3600, 0),
    },
}


def unit_conversion():
    categories = list(CONVERSION_UNITS)
    print("\nConversion categories:")
    for index, category in enumerate(categories, 1):
        print("{}: {}".format(index, category))
    category_choice = int(input("Choose category: "))
    if not 1 <= category_choice <= len(categories):
        print("Invalid category.")
        return

    units = CONVERSION_UNITS[categories[category_choice - 1]]
    print("Units: " + ", ".join(units))
    value = float(input("Value to convert: "))
    if not math.isfinite(value):
        print("Value must be finite.")
        return
    from_unit = input("Convert from: ").strip()
    to_unit = input("Convert to: ").strip()
    if from_unit not in units or to_unit not in units:
        print("Choose units from the list above.")
        return

    base_value = value * units[from_unit][0] + units[from_unit][1]
    converted_value = (base_value - units[to_unit][1]) / units[to_unit][0]
    print("{} {} = {:.8g} {}".format(value, from_unit, converted_value, to_unit))