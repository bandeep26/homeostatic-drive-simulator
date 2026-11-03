# Homeostatic Drive Simulator

A modular Python CLI simulation modeling homeostatic drive dynamics, affective state mapping (valence & arousal), and regime classification, featuring a pluggable architecture designed for Groq API integration (`llama-3.1-8b-instant`) paired with dynamic network verification and a resilient local mock fallback.

---

## Technical Architecture

The project follows a multi-phase modular architecture:

- `config.py`: Simulation constants ($\Delta t$, decay rate, regime thresholds, Groq model parameters, and level mappings).
- `simulator.py`: Numerical update engine with lower/upper clamping $[0.0, 1.0]$.
- `api_handler.py`: Dynamic scenario provider with HTTPS REST network verification, Groq LLM integration, and deterministic hash fallback.
- `plotter.py`: 3-panel visual rendering suite (Drive timeline, affective step plots, regime strip).
- `main.py`: Command Line Interface entry point built with `argparse`.

---

## Installation & Setup

1. Clone the repository and navigate to the project directory:
   ```bash
   git clone [https://github.com/bandeep26/homeostatic-drive-simulator.git](https://github.com/bandeep26/homeostatic-drive-simulator.git)
   cd homeostatic-drive-simulator
