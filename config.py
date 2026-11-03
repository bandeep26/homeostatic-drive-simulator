# Thresholds for drive regimes
UPPER_THRESHOLD = 0.75  # Above this is Overwhelmed
LOWER_THRESHOLD = 0.25  # Below this is Under-stimulated

# Simulation parameters
DECAY_RATE = 0.05       # Linear decay subtraction coefficient per second
DT = 0.1                # Timestep size in seconds
TOTAL_STEPS = 300       # 300 steps * 0.1s = 30 total seconds of simulation
INITIAL_DRIVE = 0.5     # Starting drive value (Homeostatic)

# File and API configurations
OUTPUT_DIR = "outputs"
GROQ_MODEL_NAME = "llama-3.1-8b-instant"  # Standard high-speed Groq model
REST_ENDPOINT_URL = "https://jsonplaceholder.typicode.com/posts/1"

# Stimulus mapping for scenario mode
LEVEL_TO_STIMULUS = {
    "none": 0.000,
    "low": 0.005,       # Balances decay (0.05 * 0.1 = 0.005)
    "medium": 0.010,
    "high": 0.020,
    "extreme": 0.030,
}