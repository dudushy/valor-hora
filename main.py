import argparse
import sys

DEFAULT_DAYS_PER_MONTH = 21
DEFAULT_HOURS_PER_DAY = 8
CURRENCY = "R$"


def get_positive_float(prompt, default=None):
    while True:
        if default is not None:
            user_input = input(f"{prompt} [{default}]: ").strip()
            if user_input == "":
                return float(default)
        else:
            user_input = input(f"{prompt}: ").strip()
        try:
            value = float(user_input)
            if value <= 0:
                print("Please enter a positive number.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a numeric value.")


def ask_work_details():
    days = get_positive_float("Days worked per month", DEFAULT_DAYS_PER_MONTH)
    hours = get_positive_float("Hours worked per day", DEFAULT_HOURS_PER_DAY)
    return days, hours


def calculate_hourly(monthly_salary, days, hours):
    return monthly_salary / (days * hours)


def calculate_monthly(hourly_rate, days, hours):
    return hourly_rate * days * hours


def interactive_mode():
    print("=== Salary Calculator ===")
    print("What do you want to calculate?")
    print("  1 - Hourly rate from monthly salary")
    print("  2 - Monthly salary from hourly rate")

    while True:
        choice = input("Enter your choice (1 or 2): ").strip()
        if choice in ("1", "2"):
            break
        print("Invalid choice. Please enter 1 or 2.")

    if choice == "1":
        monthly_salary = get_positive_float("Monthly salary")
        days, hours = ask_work_details()
        hourly = calculate_hourly(monthly_salary, days, hours)
        print(f"\nHourly rate: {CURRENCY} {hourly:.2f}/h")
    else:
        hourly_rate = get_positive_float("Hourly rate")
        days, hours = ask_work_details()
        monthly = calculate_monthly(hourly_rate, days, hours)
        print(f"\nMonthly salary: {CURRENCY} {monthly:.2f}/month")


def main():
    parser = argparse.ArgumentParser(
        description="Calculate salary per hour or per month.",
        add_help=False,
    )
    parser.add_argument(
        "--help",
        action="help",
        default=argparse.SUPPRESS,
        help="Show this help message and exit",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-m",
        type=float,
        metavar="MONTHLY_SALARY",
        help="Monthly salary to calculate the hourly rate",
    )
    group.add_argument(
        "-h",
        type=float,
        metavar="HOURLY_RATE",
        help="Hourly rate to calculate the monthly salary",
    )

    args = parser.parse_args()

    if args.m is not None:
        if args.m <= 0:
            print("Monthly salary must be a positive number.")
            sys.exit(1)
        days, hours = ask_work_details()
        hourly = calculate_hourly(args.m, days, hours)
        print(f"\nHourly rate: {CURRENCY} {hourly:.2f}/h")
    elif args.h is not None:
        if args.h <= 0:
            print("Hourly rate must be a positive number.")
            sys.exit(1)
        days, hours = ask_work_details()
        monthly = calculate_monthly(args.h, days, hours)
        print(f"\nMonthly salary: {CURRENCY} {monthly:.2f}/month")
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
