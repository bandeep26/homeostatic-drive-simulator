import config
import plotter
import simulator


def make_default_stimulus():
    """Generates a default 300-step stimulus list covering all 3 regimes."""
    stimulus = [0.0] * config.TOTAL_STEPS

    for i in range(40, 120):
        stimulus[i] = 0.012

    return stimulus


if __name__ == "__main__":
    stim = make_default_stimulus()
    drives, regimes, valences, arousals = simulator.run_simulation(stim)

    # Draw and save the 3-panel plot
    plotter.generate_plots(drives, regimes, valences, arousals)