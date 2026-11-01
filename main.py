import config
import simulator


def make_default_stimulus():
    """
    Generates a default 300-step stimulus list that forces the simulation
    to traverse all three regimes (Homeostatic, Overwhelmed, Under-stimulated).
    """
    stimulus = [0.0] * config.TOTAL_STEPS

    # Steps 0 to 39: Quiet start (0.0)

    # Steps 40 to 119: Noisy burst (0.012 per step)
    for i in range(40, 120):
        stimulus[i] = 0.012

    # Steps 120 to 299: Quiet recovery (0.0)

    return stimulus


if __name__ == "__main__":
    # Test block to verify Phase 3
    stim = make_default_stimulus()
    drives, regimes, valences, arousals = simulator.run_simulation(stim)

    print("Unique regimes present:", set(regimes))
    print(f"Drive at step 39: {drives[39]:.3f} ({regimes[39]})")
    print(f"Peak drive (step 119): {drives[119]:.3f} ({regimes[119]})")
    print(f"Drive at step 243: {drives[243]:.3f} ({regimes[243]})")
    print(f"Final drive (step 299): {drives[299]:.3f} ({regimes[299]})")