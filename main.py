"""EcoThread command-line interface."""

import argparse
from ecothread import analyze_file


def main():
    parser = argparse.ArgumentParser(description="Review Python code for possible repeated work.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    analyze = subparsers.add_parser("analyze", help="analyze a Python source file")
    analyze.add_argument("file", help="Python file to inspect")
    analyze.add_argument("--before-seconds", type=float, help="measured runtime before the change")
    analyze.add_argument("--after-seconds", type=float, help="measured runtime after the change")
    analyze.add_argument("--power-w", type=float, help="assumed/ measured average power in watts")
    analyze.add_argument(
        "--grid-intensity-g-per-kwh",
        type=float,
        help="electricity carbon intensity in grams CO2 per kWh",
    )
    args = parser.parse_args()

    measurement_options = (
        args.before_seconds,
        args.after_seconds,
        args.power_w,
        args.grid_intensity_g_per_kwh,
    )
    if any(value is not None for value in measurement_options) and not all(
        value is not None for value in measurement_options
    ):
        parser.error("CO2 estimation requires all four measurement options")

    analyze_file(
        args.file,
        before_seconds=args.before_seconds,
        after_seconds=args.after_seconds,
        power_w=args.power_w,
        grid_intensity_g_per_kwh=args.grid_intensity_g_per_kwh,
    )


if __name__ == "__main__":
    main()
