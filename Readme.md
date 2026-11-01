# Homeostatic Drive Simulator

A modular Python CLI simulation modeling homeostatic drive dynamics, affective state mapping (valence & arousal), and regime classification, featuring a pluggable architecture designed for LLM integration (e.g., OpenAI GPT-4o, Google Gemini) paired with a resilient local mock fallback.

---

## Technical Architecture

The project follows a multi-phase modular architecture:

- `config.py`: Simulation constants ($\Delta t$, decay rate, regime thresholds, affective vectors).
- `simulator.py`: Numerical update engine with lower/upper clamping $[0.0, 1.0]$.
- `api_handler.py`: Pluggable scenario provider with dual-mode API key checks and local mock generation.
- `plotter.py`: 3-panel visual rendering suite (Drive timeline, affective step plots, regime strip).
- `main.py`: Command Line Interface entry point built with `argparse`.

---

## Installation & Setup

1. Clone the repository and navigate to the project directory:
   ```bash
   git clone <repository-url>
   cd homeostatic-drive-simulator