import importlib.machinery
import importlib.util
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch
from types import SimpleNamespace


SCRIPT = Path(__file__).resolve().parents[1] / "EVOCHEM"


class EvochemTests(unittest.TestCase):
    def load_tool(self, ti_system):
        loader = importlib.machinery.SourceFileLoader("evochem", str(SCRIPT))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        module = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, {"ti_system": ti_system}):
            loader.exec_module(module)
        return module

    def test_evo_number_keys_need_no_enter(self):
        for key, option in [(102, 0), (92, 1), (93, 2), (94, 3), (82, 4), (83, 5), (45, 0)]:
            with self.subTest(key=key):
                ti_system = SimpleNamespace(get_key=lambda wait: key, disp_clr=lambda: None)
                module = self.load_tool(ti_system)
                with patch("builtins.input", side_effect=AssertionError("Unexpected input")), patch("builtins.print"):
                    self.assertEqual(module.show_menu(), option)

    def test_evo_ignores_unrelated_keys(self):
        key_stream = iter([105, 25, 0, 94])
        module = self.load_tool(SimpleNamespace(get_key=lambda wait: next(key_stream), disp_clr=lambda: None))
        with patch("builtins.input", side_effect=AssertionError("Unexpected input")), patch("builtins.print"):
            self.assertEqual(module.show_menu(), 3)

    def test_evo_submenus_ignore_unavailable_options(self):
        key_stream = iter([45, 102, 83, 92])
        module = self.load_tool(SimpleNamespace(get_key=lambda wait: next(key_stream), disp_clr=lambda: None))
        with patch("builtins.input", side_effect=AssertionError("Unexpected input")), patch("builtins.print"):
            self.assertEqual(module.menu_choice((1, 2), "Choice: "), 1)

    def test_evo_calculation_and_return_to_menu(self):
        from unittest.mock import Mock
        # Main menu 2, submenu 1, any key to leave result, then 0 to exit.
        get_key = Mock(side_effect=[93, 92, 105, 102])
        clear = Mock()
        module = self.load_tool(SimpleNamespace(get_key=get_key, disp_clr=clear))
        with patch("builtins.input", side_effect=["18", "18"]) as typed, patch("builtins.print") as output:
            module.main()
        self.assertEqual(typed.call_count, 2)
        output.assert_any_call("Moles:", 1.0, "mol")
        output.assert_any_call("Any key: menu")
        self.assertEqual(clear.call_count, 2)
        self.assertEqual(get_key.call_count, 4)
        self.assertTrue(all(call.args == (1,) for call in get_key.call_args_list))

    def run_tool(self, answers):
        result = subprocess.run(
            [sys.executable, str(SCRIPT)], input=answers,
            capture_output=True, text=True, timeout=5,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        return result.stdout

    def test_import_does_not_prompt(self):
        loader = importlib.machinery.SourceFileLoader("evochem", str(SCRIPT))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        module = importlib.util.module_from_spec(spec)
        with patch("builtins.input", side_effect=AssertionError("Unexpected prompt")):
            loader.exec_module(module)
        self.assertTrue(callable(module.main))

    def test_menu_exit(self):
        self.assertIn("CHEM TOOLKIT", self.run_tool("0\n"))

    def test_element_lookup(self):
        self.assertIn("Sodium", self.run_tool("1\n na \n0\n"))
        self.assertIn("Element not in quick-database.", self.run_tool("1\nXx\n0\n"))

    def test_moles_and_mass(self):
        for answers, expected in [
            ("2\n1\n18\n18\n0\n", "Moles: 1.0 mol"),
            ("2\n2\n2\n18\n0\n", "Mass: 36.0 g"),
        ]:
            with self.subTest(answers=answers):
                self.assertIn(expected, self.run_tool(answers))

    def test_all_gas_law_unknowns(self):
        for values, expected in [
            ("0\n24.618\n1\n300\n", "P = 1.0 atm"),
            ("1\n0\n1\n300\n", "V = 24.618 L"),
            ("1\n24.618\n0\n300\n", "n = 1.0 mol"),
            ("1\n24.618\n1\n0\n", "T = 300.0 K"),
        ]:
            with self.subTest(values=values):
                self.assertIn(expected, self.run_tool("3\n" + values + "0\n"))

    def test_gas_law_requires_one_unknown(self):
        for values in ["0\n1\n0\n300\n", "0\n0\n0\n0\n"]:
            with self.subTest(values=values):
                output = self.run_tool("3\n" + values + "0\n")
                self.assertIn("Enter exactly one unknown as 0.", output)
                self.assertNotIn("P =", output)
        self.assertIn("All values are known", self.run_tool("3\n1\n1\n1\n300\n0\n"))

    def test_ph_calculations(self):
        for values in ["1\n3\n", "2\n0.001\n"]:
            with self.subTest(values=values):
                output = self.run_tool("4\n" + values + "0\n")
                for expected in ["pH: 3.0", "pOH: 11.0", "[H+]: 1.00e-03", "[OH-]: 1.00e-11"]:
                    self.assertIn(expected, output)

    def test_thermochemistry(self):
        self.assertIn("Heat energy q = 418.4 J", self.run_tool("5\n10\n4.184\n10\n0\n"))

    def test_bad_input_recovers(self):
        for answers, expected in [
            ("oops\n0\n", "invalid numeric input"),
            ("99\n0\n", "Invalid choice."),
            ("2\n1\n18\n0\n0\n", "division by zero"),
            ("4\n2\n0\n0\n", "invalid numeric input"),
            ("4\n1\n-1000\n0\n", "number too large"),
        ]:
            with self.subTest(answers=answers):
                self.assertIn(expected, self.run_tool(answers))

    def test_end_of_input_exits(self):
        for answers in ["", "1\n", "3\n0\n"]:
            with self.subTest(answers=answers):
                self.assertIn("Goodbye.", self.run_tool(answers))


if __name__ == "__main__":
    unittest.main()
