# CodeAlpha Stock Portfolio Tracker

**CodeAlpha Python Programming Internship — Task 2: Stock Portfolio Tracker**

## Project overview

A beginner-friendly, console-based Python application for recording stock positions and calculating their investment values. The tracker uses a small, predefined dictionary of sample stock prices; it does not connect to a market data service.

## Key features

- Displays the supported stock symbols and sample unit prices.
- Accepts stock symbols in uppercase or lowercase.
- Validates symbols and positive numeric share quantities, including fractional shares.
- Combines quantities when the same stock is added more than once.
- Displays a readable portfolio table and total investment value.
- Exports positions and a total row to `portfolio.csv` using Python's built-in `csv` module.
- Handles invalid input and CSV file errors without crashing.
- Confirms the user's choice before exiting.

## Available symbols and sample prices

| Symbol | Illustrative unit price |
| --- | ---: |
| AAPL | $180.00 |
| TSLA | $250.00 |
| GOOGL | $140.00 |
| MSFT | $420.00 |
| AMZN | $190.00 |
| NVDA | $120.00 |
| META | $500.00 |
| NFLX | $650.00 |

> **Price disclaimer:** These prices are hardcoded illustrative sample values for this learning project. They are not real-time, current, or investment advice. All calculations use only these predefined values.

## Python concepts used

- Dictionaries for stock prices and portfolio positions.
- Functions, variables, and loops.
- Conditional menu navigation with `if`/`elif`/`else`.
- Console input and output.
- Numeric validation and basic arithmetic.
- File handling, the built-in `csv` module, and exception handling.
- Automated tests with `unittest` and temporary directories.

## Technologies

- Python 3
- Python standard library only (`csv`, `math`, `unittest`, and related built-in modules)

No third-party packages are required. `requirements.txt` is intentionally empty of dependencies.

## Project structure

```text
CodeAlpha_StockPortfolioTracker/
├── stock_tracker.py
├── README.md
├── requirements.txt
├── .gitignore
└── tests/
    └── test_stock_tracker.py
```

## Installation

1. Install Python 3 (Python 3.8 or newer is recommended).
2. Download or clone this repository and open its project directory in a terminal.
3. No package installation is needed because the project uses only the standard library.

## Run the application

From the project directory, run:

```bash
python stock_tracker.py
```

On Windows, `py stock_tracker.py` can also be used if the Python launcher is installed.

## Example usage

Select **2** to add `AAPL` with quantity `5`, then add `TSLA` with quantity `2`. Select **3** to view the summary:

```text
Symbol          Quantity        Unit Price          Investment
------------------------------------------------------------------------
AAPL                   5          $180.00              $900.00
TSLA                   2          $250.00              $500.00
------------------------------------------------------------------------
Total Investment: $1,400.00
```

Select **4** to save the current positions. Select **5** and confirm with `y` to exit. If the same symbol is added again, its share quantity is combined with the existing position.

## CSV export

The export creates or overwrites `portfolio.csv` in the current working directory. It contains the columns **Stock Symbol**, **Quantity**, **Unit Price**, and **Investment Value**, followed by one row per position and a `TOTAL` row. File errors are reported in the console.

## Run tests

From the project directory, run:

```bash
python -m unittest discover -s tests -v
```

The tests cover stock display, investment calculations, repeated and lowercase symbols, invalid entries, empty summaries, CSV content and file errors, and menu/exit behavior.

## Learning outcomes

This project provides practice with breaking a small application into functions, validating user input, working with dictionaries and loops, formatting output, writing CSV files, handling common errors, and verifying behavior with automated unit tests.

## Internship and author

- **Program:** CodeAlpha Python Programming Internship
- **Task:** Task 2 — Stock Portfolio Tracker
- **Author:** Ragavi G.
- **GitHub repository name:** `CodeAlpha_StockPortfolioTracker`
