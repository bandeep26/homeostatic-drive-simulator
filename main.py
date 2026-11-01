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


def main():
    """Executes default mode simulation, outputs percentages, and generates plot."""
    # 1. Generate stimulus list
    stimulus = make_default_stimulus()

    # 2. Run core simulation
    drives, regimes, valences, arousals = simulator.run_simulation(stimulus)

    # 3. Compute regime percentages
    percentages = compute_regime_percentages(regimes)

    # Print terminal output
    print("--- Simulation Summary ---")
    for regime, pct in percentages.items():
        print(f"{regime.capitalize()}: {pct}%")

    # 4. Generate 3-panel plot
    plotter.generate_plots(drives, regimes, valences, arousals)


if __name__ == "__main__":
    main()