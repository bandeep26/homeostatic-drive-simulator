import os
import matplotlib.pyplot as plt
import numpy as np
import config


def generate_plots(
    drive_values,
    regime_labels,
    valence_values,
    arousal_values,
    filename="drive_plot.png",
):
    """
    Generates and saves a 3-panel visualization chart:
    - Panel 1: Drive trajectory timeline with threshold bands.
    - Panel 2: Valence and Arousal step curves.
    - Panel 3: Colored regime timeline blocks.
    """
    # Generate time array (0.0 to 29.9 seconds)
    time = np.arange(config.TOTAL_STEPS) * config.DT

    # Color mapping for consistency across panels
    colors = {
        "overwhelmed": "red",
        "homeostatic": "green",
        "under-stimulated": "gold",
    }

    fig, axes = plt.subplots(3, 1, figsize=(10, 10), sharex=True)

    # --- Panel 1: Drive Timeline ---
    ax1 = axes[0]
    ax1.plot(time, drive_values, color="blue", linewidth=2, label="Drive Level")

    # Threshold background bands
    ax1.fill_between(
        time,
        config.UPPER_THRESHOLD,
        1.0,
        color=colors["overwhelmed"],
        alpha=0.2,
        label="Overwhelmed Zone",
    )
    ax1.fill_between(
        time,
        config.LOWER_THRESHOLD,
        config.UPPER_THRESHOLD,
        color=colors["homeostatic"],
        alpha=0.2,
        label="Homeostatic Zone",
    )
    ax1.fill_between(
        time,
        0.0,
        config.LOWER_THRESHOLD,
        color=colors["under-stimulated"],
        alpha=0.2,
        label="Under-stimulated Zone",
    )

    # Threshold lines
    ax1.axhline(
        config.UPPER_THRESHOLD, color="red", linestyle="--", alpha=0.7
    )
    ax1.axhline(
        config.LOWER_THRESHOLD, color="orange", linestyle="--", alpha=0.7
    )

    ax1.set_ylim(0, 1.05)
    ax1.set_ylabel("Drive Level")
    ax1.set_title("Homeostatic Drive Simulation Timeline")
    ax1.legend(loc="upper right")
    ax1.grid(True, linestyle=":", alpha=0.6)

    # --- Panel 2: Valence & Arousal ---
    ax2 = axes[1]
    ax2.step(
        time, valence_values, where="post", color="purple", label="Valence"
    )
    ax2.step(
        time, arousal_values, where="post", color="darkorange", label="Arousal"
    )

    ax2.set_yticks([-1, 0, 1])
    ax2.set_ylim(-1.2, 1.2)
    ax2.set_ylabel("State Value")
    ax2.set_title("Affective State (Valence & Arousal)")
    ax2.legend(loc="upper right")
    ax2.grid(True, linestyle=":", alpha=0.6)

    # --- Panel 3: Regime Strip ---
    ax3 = axes[2]

    # Group consecutive identical regime labels into runs
    runs = []
    current_label = regime_labels[0]
    start_idx = 0

    for idx in range(1, len(regime_labels)):
        if regime_labels[idx] != current_label:
            runs.append((start_idx, idx - 1, current_label))
            current_label = regime_labels[idx]
            start_idx = idx
    runs.append((start_idx, len(regime_labels) - 1, current_label))

    # Draw colored blocks for each regime run
    for start_i, end_i, label in runs:
        start_t = start_i * config.DT
        end_t = (end_i + 1) * config.DT
        ax3.axvspan(
            start_t,
            end_t,
            color=colors.get(label, "gray"),
            alpha=0.6,
            label=label,
        )

    # Avoid duplicate labels in panel 3 legend
    handles, labels = ax3.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax3.legend(
        by_label.values(), by_label.keys(), loc="upper right"
    )

    ax3.set_yticks([])
    ax3.set_xlabel("Time (s)")
    ax3.set_ylabel("Regime")
    ax3.set_title("Regime Classification Strip")

    # Ensure output folder exists and save plot
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(config.OUTPUT_DIR, filename)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.show()

    print(f"Plot successfully saved to: {output_path}")