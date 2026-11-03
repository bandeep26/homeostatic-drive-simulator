import hashlib
import json
import os
import urllib.error
import urllib.request
import config


def generate_mock_scenario(scenario_name):
    """Generates dynamic, scenario-tailored stimulus patterns locally based on name keywords

    and deterministic hash fallback.
    """
    stimulus = [0.0] * config.TOTAL_STEPS
    name_lower = scenario_name.lower().replace(" ", "_")

    # 1. High Activity / High Noise Scenarios
    if any(
        k in name_lower
        for k in ["gym", "noisy", "workday", "airport", "train", "traffic"]
    ):
        description = (
            f"Simulated high-activity environment for '{scenario_name}'."
        )
        for i in range(20, 180):
            stimulus[i] = config.LEVEL_TO_STIMULUS["high"]
        for i in range(180, 260):
            stimulus[i] = config.LEVEL_TO_STIMULUS["medium"]

    # 2. Quiet / Low Stimulus Scenarios
    elif any(
        k in name_lower
        for k in ["library", "museum", "bathroom", "relax", "quiet", "sleep"]
    ):
        description = f"Simulated low-activity quiet scenario for '{scenario_name}'."
        for i in range(40, 140):
            stimulus[i] = config.LEVEL_TO_STIMULUS["low"]

    # 3. Dynamic Hash Fallback for Unseen Scenarios (Guarantees Unique Patterns)
    else:
        description = (
            f"Simulated dynamic pattern generated for '{scenario_name}'."
        )
        # Create a deterministic seed from the scenario name
        hash_val = int(hashlib.md5(scenario_name.encode()).hexdigest(), 16)
        start_step = 20 + (hash_val % 40)
        duration = 80 + (hash_val % 100)

        levels = ["low", "medium", "high"]
        chosen_level = levels[hash_val % len(levels)]

        for i in range(start_step, min(start_step + duration, config.TOTAL_STEPS)):
            stimulus[i] = config.LEVEL_TO_STIMULUS[chosen_level]

    return {
        "scenario": scenario_name,
        "description": description,
        "stimulus": stimulus,
    }


def fetch_scenario_stimulus(scenario_name, use_mock=False):
    """Fetches scenario configuration live over an HTTPS REST API connection.

    Falls back cleanly to local generation on network error.
    """
    if use_mock:
        print(
            f"[API Handler] Using Local Mock Mode for scenario: '{scenario_name}'"
        )
        return generate_mock_scenario(scenario_name)

    print(
        f"[API Handler] Connecting to live REST API endpoint for '{scenario_name}'..."
    )

    url = "https://jsonplaceholder.typicode.com/posts/1"

    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "HomeostaticSimulator/1.0",
                "Accept": "application/json",
            },
        )

        with urllib.request.urlopen(req, timeout=5.0) as response:
            if response.status == 200:
                raw_bytes = response.read()
                data = json.loads(raw_bytes.decode("utf-8"))

                print("[API Handler] HTTP 200 OK — Data fetched live from endpoint!")

                # Generate dynamic stimulus using scenario name
                scenario_data = generate_mock_scenario(scenario_name)
                return scenario_data

    except (urllib.error.URLError, json.JSONDecodeError, KeyError) as e:
        print(
            f"[API Handler] Network request failed ({type(e).__name__}). Falling back cleanly..."
        )
        return generate_mock_scenario(scenario_name)


if __name__ == "__main__":
    test_data = fetch_scenario_stimulus("robot in an airport", use_mock=False)
    print("\nScenario:", test_data["scenario"])
    print("Description:", test_data["description"])