import json
import os

import config
from openai import OpenAI


def generate_mock_scenario(scenario_name):
    """
    Generates structured scenario stimulus patterns locally without making live API calls.
    Returns a dictionary with 'scenario', 'description', and a 300-step 'stimulus' array.
    """
    stimulus = [0.0] * config.TOTAL_STEPS

    name_lower = scenario_name.lower().replace(" ", "_")

    if "noisy" in name_lower or "workday" in name_lower:
        # High noise burst scenario
        description = "Simulated high-activity workday with heavy stimulus bursts."
        for i in range(30, 150):
            stimulus[i] = config.LEVEL_TO_STIMULUS["high"]
        for i in range(150, 220):
            stimulus[i] = config.LEVEL_TO_STIMULUS["medium"]

    elif "relax" in name_lower or "quiet" in name_lower:
        # Low stimulus scenario
        description = "Simulated low-activity relaxation scenario."
        for i in range(50, 120):
            stimulus[i] = config.LEVEL_TO_STIMULUS["low"]

    else:
        # Default scenario pattern
        description = f"Simulated default stimulus pattern for '{scenario_name}'."
        for i in range(40, 120):
            stimulus[i] = config.LEVEL_TO_STIMULUS["medium"]

    return {
        "scenario": scenario_name,
        "description": description,
        "stimulus": stimulus,
    }


def fetch_scenario_stimulus(scenario_name, use_mock=False):
    """
    Fetches scenario stimulus data.
    If use_mock is True or live API fails (e.g. missing credits/key),
    it cleanly falls back to local mock scenario generation.
    """
    if use_mock:
        print(f"[API Handler] Using Mock Mode for scenario: '{scenario_name}'")
        return generate_mock_scenario(scenario_name)

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print(
            "[API Handler] No API key detected. Falling back to Mock Mode..."
        )
        return generate_mock_scenario(scenario_name)

    try:
        print(
            f"[API Handler] Calling OpenAI GPT-4o for scenario: '{scenario_name}'..."
        )
        client = OpenAI(api_key=api_key)

        prompt = f"""
        Generate a JSON object for a homeostatic drive simulation scenario named '{scenario_name}'.
        The JSON must contain:
        - "scenario": string
        - "description": brief summary string
        - "stimulus": array of exactly 300 float values representing stimulus per timestep (0.1s each).
        Use levels: none (0.0), low (0.005), medium (0.01), high (0.02), extreme (0.03).
        """

        response = client.chat.completions.create(
            model=config.MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
        )

        data = json.loads(response.choices[0].message.content)

        # Validate stimulus length
        if (
            "stimulus" in data
            and len(data["stimulus"]) == config.TOTAL_STEPS
        ):
            return data
        else:
            print(
                "[API Handler] Invalid stimulus length from API response. Falling back to Mock Mode..."
            )
            return generate_mock_scenario(scenario_name)

    except Exception as e:
        print(
            f"[API Handler] API call unfulfilled ({type(e).__name__}). Falling back cleanly to Mock Mode..."
        )
        return generate_mock_scenario(scenario_name)


if __name__ == "__main__":
    # Unit test for api_handler.py
    test_data = fetch_scenario_stimulus("noisy_workday", use_mock=True)
    print("Scenario Name:", test_data["scenario"])
    print("Description:", test_data["description"])
    print("Stimulus Array Length:", len(test_data["stimulus"]))
    print("Sample Stimulus (step 50):", test_data["stimulus"][50])