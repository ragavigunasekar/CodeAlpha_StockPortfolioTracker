"""Console-based stock portfolio tracker using illustrative sample prices."""

import csv
import math


STOCK_PRICES = {
    "AAPL": 180.00,
    "TSLA": 250.00,
    "GOOGL": 140.00,
    "MSFT": 420.00,
    "AMZN": 190.00,
    "NVDA": 120.00,
    "META": 500.00,
    "NFLX": 650.00,
}

CSV_FILENAME = "portfolio.csv"
CSV_HEADERS = ["Stock Symbol", "Quantity", "Unit Price", "Investment Value"]


def display_welcome():
    """Show the application title, purpose, and sample-price disclaimer."""
    print("=" * 64)
    print("           CODEALPHA STOCK PORTFOLIO TRACKER")
    print("=" * 64)
    print("Track estimated investment values using predefined sample prices.")
    print("Note: prices are illustrative hardcoded values, not live market data.\n")
    display_available_stocks()


def display_available_stocks():
    """Display every supported stock symbol and its predefined price."""
    print("Available stocks (illustrative sample prices):")
    print(f"{'Symbol':<12}{'Unit Price':>16}")
    print("-" * 28)
    for symbol, price in STOCK_PRICES.items():
        formatted_price = f"${price:,.2f}"
        print(f"{symbol:<12}{formatted_price:>16}")


def calculate_investment(symbol, quantity):
    """Return the investment value for a known stock and share quantity."""
    return round(STOCK_PRICES[symbol] * quantity, 2)


def calculate_total_investment(portfolio):
    """Return the total value of all positions in the portfolio."""
    return round(
        sum(calculate_investment(symbol, quantity) for symbol, quantity in portfolio.items()),
        2,
    )


def add_stock(portfolio, symbol=None, quantity=None):
    """Validate and add shares to a portfolio, combining existing positions.

    Optional symbol and quantity arguments make the function easy to test or
    reuse; when omitted, values are requested from the console.
    """
    if symbol is None:
        symbol = input("Enter a stock symbol: ")
    symbol = symbol.strip().upper()

    if symbol not in STOCK_PRICES:
        print(f"Sorry, '{symbol}' is not in the available stock list.")
        return False

    if quantity is None:
        quantity = input("Enter the quantity of shares: ")

    try:
        quantity = float(quantity)
    except (TypeError, ValueError):
        print("Quantity must be a positive number (for example, 5 or 2.5).")
        return False

    if not math.isfinite(quantity) or quantity <= 0:
        print("Quantity must be a positive number greater than zero.")
        return False

    portfolio[symbol] = portfolio.get(symbol, 0.0) + quantity
    investment_value = calculate_investment(symbol, quantity)
    print(
        f"Added {quantity:g} share(s) of {symbol} at "
        f"${STOCK_PRICES[symbol]:,.2f} each (${investment_value:,.2f})."
    )
    return True


def display_portfolio(portfolio):
    """Print a formatted portfolio table and its total investment value."""
    print("\nPortfolio Summary")
    print("-" * 72)
    print(f"{'Symbol':<12}{'Quantity':>14}{'Unit Price':>18}{'Investment':>20}")
    print("-" * 72)

    if not portfolio:
        print("Your portfolio is currently empty.")
    else:
        for symbol, quantity in portfolio.items():
            value = calculate_investment(symbol, quantity)
            formatted_price = f"${STOCK_PRICES[symbol]:,.2f}"
            formatted_value = f"${value:,.2f}"
            print(
                f"{symbol:<12}{quantity:>14g}"
                f"{formatted_price:>18}{formatted_value:>20}"
            )

    print("-" * 72)
    print(f"Total Investment: ${calculate_total_investment(portfolio):,.2f}\n")


def save_portfolio_to_csv(portfolio, filename=CSV_FILENAME):
    """Write portfolio positions and a consistent total row to a CSV file."""
    try:
        with open(filename, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(CSV_HEADERS)
            for symbol, quantity in portfolio.items():
                writer.writerow(
                    [
                        symbol,
                        f"{quantity:g}",
                        f"{STOCK_PRICES[symbol]:.2f}",
                        f"{calculate_investment(symbol, quantity):.2f}",
                    ]
                )
            writer.writerow(
                ["TOTAL", "", "", f"{calculate_total_investment(portfolio):.2f}"]
            )
        print(f"Portfolio saved successfully to '{filename}'.")
        return True
    except (OSError, csv.Error) as error:
        print(f"Unable to save the portfolio: {error}")
        return False


def display_menu():
    """Display the available portfolio actions."""
    print("\nMenu")
    print("1. View available stocks")
    print("2. Add stock to portfolio")
    print("3. View portfolio summary")
    print("4. Save portfolio to CSV")
    print("5. Exit")


def main():
    """Run the interactive menu until the user confirms that they want to exit."""
    portfolio = {}
    display_welcome()

    while True:
        display_menu()
        choice = input("Select an option (1-5): ").strip()

        if choice == "1":
            display_available_stocks()
        elif choice == "2":
            add_stock(portfolio)
        elif choice == "3":
            display_portfolio(portfolio)
        elif choice == "4":
            save_portfolio_to_csv(portfolio)
        elif choice == "5":
            confirmation = input("Are you sure you want to exit? (y/n): ").strip().lower()
            if confirmation in ("y", "yes"):
                print("Thank you for using the Stock Portfolio Tracker. Goodbye!")
                break
            print("Exit cancelled. Returning to the menu.")
        else:
            print("Invalid menu option. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nInput ended. Thank you for using the Stock Portfolio Tracker.")
