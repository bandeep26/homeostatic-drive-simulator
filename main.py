import argparse
import api_handler
import config
import plotter
import simulator


def make_default_stimulus():
    """Generates a default 300-step stimulus list covering all 3 regimes."""
    stimulus = [0.0] * config.TOTAL_STEPS

    # Noisy burst: steps 40 to 119
    for i in range(40, 120):
        stimulus[i] = 0.012

    return stimulus


def compute_regime_percentages(regime_labels):
    """Calculates the percentage of simulation time spent in each regime."""
    total_steps = len(regime_labels)
    percentages = {}

    for regime in ["homeostatic", "overwhelmed", "under-stimulated"]:
        count = regime_labels.count(regime)
        percentages[regime] = round((count / total_steps) * 100, 2)

    return percentages


def parse_arguments():
    """Parses command line arguments for the simulator CLI."""
    parser = argparse.ArgumentParser(
        description="Homeostatic Drive Simulator CLI"
    )
    parser.add_argument(
        "--scenario",
        type=str,
        help="Name of scenario (e.g., 'noisy_workday', 'relax')",
    )
    parser.add_argument(
        "--level",
        type=str,
        choices=["none", "low", "medium", "high", "extreme"],
        help="Override stimulus level across burst phase",
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Force local mock scenario generation",
    )
    return parser.parse_args()


def main():
    """Main CLI entry point for the simulation tool."""
    args = parse_arguments()

    if args.scenario:
        print(f"--- Running Scenario Mode: '{args.scenario}' ---")
        scenario_data = api_handler.fetch_scenario_stimulus(
            args.scenario, use_mock=args.mock
        )
        stimulus = scenario_data["stimulus"]
        print(f"Description: {scenario_data.get('description', 'N/A')}")

        # Apply level override if specified by user
        if args.level:
            override_val = config.LEVEL_TO_STIMULUS[args.level]
            print(
                f"Applying custom level override: '{args.level}' ({override_val})"
            )
            for i in range(len(stimulus)):
                if stimulus[i] > 0.0:
                    stimulus[i] = override_val
    else:
        print("--- Running Default Baseline Mode ---")
        stimulus = make_default_stimulus()

    # Run simulation physics engine
    drives, regimes, valences, arousals = simulator.run_simulation(stimulus)

    # Compute and display percentages
    percentages = compute_regime_percentages(regimes)
    print("\n--- Regime Breakdown ---")
    for regime, pct in percentages.items():
        print(f"{regime.capitalize()}: {pct}%")

    # Generate visual plot output
    plot_name = (
        f"plot_{args.scenario}.png" if args.scenario else "drive_plot.png"
    )
    plotter.generate_plots(
        drives, regimes, valences, arousals, filename=plot_name
    )


if __name__ == "__main__":
    main()