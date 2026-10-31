"""Automated tests for the CodeAlpha stock portfolio tracker."""

import csv
import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import stock_tracker


class StockTrackerTests(unittest.TestCase):
    def setUp(self):
        self.portfolio = {}

    def capture_output(self, function, *args, **kwargs):
        output = io.StringIO()
        with redirect_stdout(output):
            result = function(*args, **kwargs)
        return result, output.getvalue()

    def test_available_stocks_are_displayed(self):
        _, output = self.capture_output(stock_tracker.display_available_stocks)
        for symbol in stock_tracker.STOCK_PRICES:
            self.assertIn(symbol, output)
        self.assertIn("$180.00", output)

    def test_add_aapl_quantity_five_and_calculate_value(self):
        self.assertTrue(stock_tracker.add_stock(self.portfolio, "AAPL", 5))
        self.assertEqual(self.portfolio["AAPL"], 5)
        self.assertEqual(stock_tracker.calculate_investment("AAPL", 5), 900.00)

    def test_add_tsla_quantity_two_and_calculate_value(self):
        self.assertTrue(stock_tracker.add_stock(self.portfolio, "TSLA", 2))
        self.assertEqual(stock_tracker.calculate_investment("TSLA", 2), 500.00)

    def test_total_for_aapl_and_tsla_is_1400(self):
        stock_tracker.add_stock(self.portfolio, "AAPL", 5)
        stock_tracker.add_stock(self.portfolio, "TSLA", 2)
        self.assertEqual(stock_tracker.calculate_total_investment(self.portfolio), 1400.00)

    def test_repeated_stock_quantities_are_combined(self):
        stock_tracker.add_stock(self.portfolio, "AAPL", 5)
        stock_tracker.add_stock(self.portfolio, "AAPL", 2)
        self.assertEqual(self.portfolio, {"AAPL": 7})

    def test_lowercase_symbol_is_accepted(self):
        self.assertTrue(stock_tracker.add_stock(self.portfolio, "aapl", 1))
        self.assertEqual(self.portfolio, {"AAPL": 1})

    def test_unknown_symbol_is_rejected(self):
        result, output = self.capture_output(
            stock_tracker.add_stock, self.portfolio, "NOPE", 1
        )
        self.assertFalse(result)
        self.assertIn("not in the available stock list", output)
        self.assertEqual(self.portfolio, {})

    def test_zero_quantity_is_rejected(self):
        self.assertFalse(stock_tracker.add_stock(self.portfolio, "AAPL", 0))
        self.assertEqual(self.portfolio, {})

    def test_negative_quantity_is_rejected(self):
        self.assertFalse(stock_tracker.add_stock(self.portfolio, "AAPL", -2))
        self.assertEqual(self.portfolio, {})

    def test_non_numeric_quantity_is_rejected(self):
        result, output = self.capture_output(
            stock_tracker.add_stock, self.portfolio, "AAPL", "many"
        )
        self.assertFalse(result)
        self.assertIn("Quantity must be a positive number", output)
        self.assertEqual(self.portfolio, {})

    def test_non_finite_quantity_is_rejected(self):
        self.assertFalse(stock_tracker.add_stock(self.portfolio, "AAPL", "NaN"))
        self.assertFalse(stock_tracker.add_stock(self.portfolio, "AAPL", "inf"))
        self.assertEqual(self.portfolio, {})

    def test_empty_portfolio_summary_is_clear_and_zero(self):
        _, output = self.capture_output(stock_tracker.display_portfolio, {})
        self.assertIn("portfolio is currently empty", output)
        self.assertIn("Total Investment: $0.00", output)

    def test_csv_export_contains_positions_and_total(self):
        stock_tracker.add_stock(self.portfolio, "AAPL", 5)
        stock_tracker.add_stock(self.portfolio, "TSLA", 2)
        with tempfile.TemporaryDirectory() as directory:
            filename = os.path.join(directory, "portfolio.csv")
            result, _ = self.capture_output(
                stock_tracker.save_portfolio_to_csv, self.portfolio, filename
            )
            self.assertTrue(result)
            with open(filename, newline="", encoding="utf-8") as csv_file:
                rows = list(csv.reader(csv_file))

        self.assertEqual(rows[0], stock_tracker.CSV_HEADERS)
        self.assertEqual(rows[1], ["AAPL", "5", "180.00", "900.00"])
        self.assertEqual(rows[2], ["TSLA", "2", "250.00", "500.00"])
        self.assertEqual(rows[3], ["TOTAL", "", "", "1400.00"])

    def test_csv_export_handles_file_errors(self):
        result, output = self.capture_output(
            stock_tracker.save_portfolio_to_csv,
            self.portfolio,
            os.path.join("missing-directory-for-test", "portfolio.csv"),
        )
        self.assertFalse(result)
        self.assertIn("Unable to save the portfolio", output)

    def test_menu_navigation_and_exit_confirmation(self):
        user_input = "1\n2\naapl\n5\n3\n5\ny\n"
        with patch("builtins.input", side_effect=user_input.splitlines()):
            _, output = self.capture_output(stock_tracker.main)
        self.assertIn("AAPL", output)
        self.assertIn("Added 5 share(s) of AAPL", output)
        self.assertIn("Total Investment: $900.00", output)
        self.assertIn("Goodbye!", output)

    def test_exit_can_be_cancelled_before_confirming(self):
        user_input = "5\nn\n5\ny\n"
        with patch("builtins.input", side_effect=user_input.splitlines()):
            _, output = self.capture_output(stock_tracker.main)
        self.assertIn("Exit cancelled", output)
        self.assertIn("Goodbye!", output)

    def test_invalid_menu_option_does_not_end_program(self):
        user_input = "invalid\n5\ny\n"
        with patch("builtins.input", side_effect=user_input.splitlines()):
            _, output = self.capture_output(stock_tracker.main)
        self.assertIn("Invalid menu option", output)
        self.assertIn("Goodbye!", output)


if __name__ == "__main__":
    unittest.main()
