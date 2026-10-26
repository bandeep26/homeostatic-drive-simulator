import config


def clamp(value, low=0.0, high=1.0):
    """Clamps a numeric value strictly between low and high limits."""
    return max(low, min(value, high))


def detect_regime(drive):
    """
    Determines emotional state, valence, and arousal from a drive value.
    Thresholds:
    - drive > 0.75: overwhelmed (-1 valence, +1 arousal)
    - 0.25 <= drive <= 0.75: homeostatic (+1 valence, 0 arousal)
    - drive < 0.25: under-stimulated (-1 valence, -1 arousal)
    """
    if drive > config.UPPER_THRESHOLD:
        return "overwhelmed", -1, 1
    elif drive < config.LOWER_THRESHOLD:
        return "under-stimulated", -1, -1
    else:
        return "homeostatic", 1, 0


def run_simulation(stimulus_list):
    """
    Executes the homeostatic drive simulation across TOTAL_STEPS.
    Equation: A_drive(t+1) = A_drive(t) + stimulus(t) - (DECAY_RATE * DT)
    Returns: drive_values, regime_labels, valence_values, arousal_values
    """
    if len(stimulus_list) != config.TOTAL_STEPS:
        raise ValueError(
            f"stimulus_list must contain exactly {config.TOTAL_STEPS} values, "
            f"but got {len(stimulus_list)}."
        )

    # Initialize output lists
    drive_values = [0.0] * config.TOTAL_STEPS
    regime_labels = []
    valence_values = []
    arousal_values = []

    # Set initial drive state
    drive_values[0] = config.INITIAL_DRIVE

    # Compute regime for index 0
    regime, val, aro = detect_regime(drive_values[0])
    regime_labels.append(regime)
    valence_values.append(val)
    arousal_values.append(aro)

    # Calculate decay per step
    decay_per_step = config.DECAY_RATE * config.DT

    # Main simulation loop across timesteps 1 to TOTAL_STEPS - 1
    for i in range(1, config.TOTAL_STEPS):
        # Update drive using linear decay equation
        raw_drive = drive_values[i - 1] + stimulus_list[i] - decay_per_step

        # Clamp drive between 0.0 and 1.0
        drive_values[i] = clamp(raw_drive, 0.0, 1.0)

        # Detect regime, valence, and arousal for current step
        regime, val, aro = detect_regime(drive_values[i])
        regime_labels.append(regime)
        valence_values.append(val)
        arousal_values.append(aro)

    return drive_values, regime_labels, valence_values, arousal_values


if __name__ == "__main__":
    # Test 1: detect_regime threshold checks
    print("Testing detect_regime:")
    print("0.80 ->", detect_regime(0.80))  # Expected: ('overwhelmed', -1, 1)
    print("0.75 ->", detect_regime(0.75))  # Expected: ('homeostatic', 1, 0)
    print("0.50 ->", detect_regime(0.50))  # Expected: ('homeostatic', 1, 0)
    print("0.25 ->", detect_regime(0.25))  # Expected: ('homeostatic', 1, 0)
    print(
        "0.10 ->", detect_regime(0.10)
    )  # Expected: ('under-stimulated', -1, -1)

    # Test 2: 300 zero stimulus values (drive drops by 0.005 each step)
    zero_stimulus = [0.0] * config.TOTAL_STEPS
    drives, regimes, valences, arousals = run_simulation(zero_stimulus)

    print("\nTesting zero stimulus simulation:")
    print(f"Initial drive (index 0): {drives[0]}")  # Expected: 0.5
    print(f"Step 1 drive: {drives[1]:.3f}")  # Expected: 0.495
    print(f"Step 10 drive: {drives[10]:.3f}")  # Expected: 0.450
    print(f"Final drive (index 299): {drives[-1]}")  # Expected: 0.0 (clamped)
    print(f"Regime at step 0: {regimes[0]}")  # Expected: homeostatic
    print(
        f"Regime at step 51: {regimes[51]}"
    )  # Expected: under-stimulated (dropped below 0.25)

    # Test 3: Steady state stimulus matching decay (0.005 per step)
    steady_stimulus = [0.005] * config.TOTAL_STEPS
    drives_steady, _, _, _ = run_simulation(steady_stimulus)
    print(f"\nSteady stimulus final drive: {drives_steady[-1]:.3f}")  # 0.500