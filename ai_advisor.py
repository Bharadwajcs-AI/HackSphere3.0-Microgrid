"""
HackSphere 3.0 — AI Grid Reasoning & Advisory Engine
Powered by NVIDIA NIM Multi-Model Pool (DiffusionGemma / Nemotron)
with built-in Autonomous Edge Expert Reasoning Fallback.
Analyzes 24-hour demand forecasts, battery reserves, and emits
actionable grid management advisories for microgrid operators.
"""

import os
import requests
from pathlib import Path

# Load .env manually if dotenv is not present
ENV_FILE = Path(__file__).parent / ".env"
if ENV_FILE.exists():
    with open(ENV_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip().strip('"').strip("'")

NVIDIA_BASE_URL = os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")
NVIDIA_GENERAL_KEY = os.getenv("NVIDIA_GENERAL_KEY")
NVIDIA_GENERAL_MODEL = os.getenv("NVIDIA_GENERAL_MODEL", "google/diffusiongemma-26b-a4b-it")


def generate_expert_grid_advisory(summary: dict, hourly: list = None) -> dict:
    """
    Autonomous domain-expert grid dispatch advisory engine.
    Produces structured, high-level engineering analysis directly from microgrid simulation metrics.
    Guaranteed zero-failure local intelligence.
    """
    peak_kw = float(summary.get("peak_demand_kw", 0))
    avg_kw = float(summary.get("avg_demand_kw", 0))
    overloads = int(summary.get("overload_alerts", 0))
    ren_hrs = int(summary.get("hours_renewable", 0))
    grid_hrs = int(summary.get("hours_main_grid", 0))
    min_soc = float(summary.get("min_battery_soc_pct", 80))
    final_soc = float(summary.get("final_battery_soc_pct", 80))

    # 1. Executive Summary
    if overloads > 0:
        exec_summary = (
            f"CRITICAL DISPATCH NOTICE: Forecast projects {overloads} critical overload events (>= 200.0 kW) "
            f"with a maximum peak of {peak_kw:.2f} kW. Microgrid requires immediate reserve prioritization, "
            f"automated bus transfer to Renewable Storage, and strict battery depth-of-discharge monitoring."
        )
    elif peak_kw > 160:
        exec_summary = (
            f"ELEVATED LOAD PROFILE: Peak demand of {peak_kw:.2f} kW initiates Renewable Storage switching across "
            f"{ren_hrs} hours without violating the 200.0 kW critical overload boundary. Overall grid stability remains nominal."
        )
    else:
        exec_summary = (
            f"OPTIMAL STABILITY PROFILE: 24-hour demand curve remains benign with peak of {peak_kw:.2f} kW and average "
            f"demand of {avg_kw:.2f} kW. All operations reside safely within standard distribution thresholds."
        )

    # 2. Critical Anomalies & Overload Risks
    if overloads > 0:
        anomaly_analysis = (
            f"The microgrid experiences sustained severe loading exceeding the 200.0 kW critical safety threshold across "
            f"{overloads} discrete hourly intervals. Peak demand reaches {peak_kw:.2f} kW "
            f"({(peak_kw - 200.0):.1f} kW above safety threshold). "
            f"High-stress windows demand active load-shedding protocols and automated renewable battery discharge "
            f"to protect feeder substation transformers from thermal overstress."
        )
    elif peak_kw > 160:
        anomaly_analysis = (
            f"No critical overloads detected (0 hours >= 200 kW). However, {ren_hrs} hours surpass the 160.0 kW "
            f"transition threshold or fall within the evening peak window (18:00 to 22:00), requiring automated "
            f"transfer to Renewable Storage mode to avoid elevated peak-tariff grid surcharges."
        )
    else:
        anomaly_analysis = (
            f"Zero critical overload events detected. Demand remains well below both the 160.0 kW renewable trigger and "
            f"the 200.0 kW critical limit. Renewable mode activations ({ren_hrs}h) strictly correspond to mandatory "
            f"evening peak hours (18:00 - 22:00)."
        )

    # 3. Battery Dispatch Strategy
    if min_soc <= 10.5:
        battery_analysis = (
            f"Battery energy depleted to the mandatory 10.0% emergency reserve floor ({min_soc:.1f}% minimum reached). "
            f"Under HackSphere safety guidelines, discharge is automatically locked at 50.0 kWh (10% capacity) to prevent "
            f"irreversible lithium cell degradation. Subsequent demand is safely redirected to the Main Grid. "
            f"Replenish battery at maximum 50 kW rate during off-peak low-demand hours."
        )
    else:
        battery_analysis = (
            f"Storage reserves maintained in a secure operating window: minimum SOC reached is {min_soc:.1f}% "
            f"(comfortably above the 10.0% safety floor), concluding the 24-hour horizon at {final_soc:.1f}% SOC. "
            f"Battery charging at 50 kW during Main Grid mode ({grid_hrs} hours) provides robust reserve buffer."
        )

    # 4. Operator Action Checklist
    checklist = [
        f"Confirm automatic relay switching for all {ren_hrs} hours scheduled in Renewable Storage Mode (including 18:00-22:00 peak).",
        f"Verify emergency battery reserve protection lock is engaged at 10.0% SOC (50 kWh safety limit).",
        (
            f"Alert field staff to initiate auxiliary generator pre-start for {overloads} projected overload hours (>= 200 kW)."
            if overloads > 0
            else "Ensure 50 kW off-peak charging schedule proceeds during low-demand overnight intervals."
        ),
    ]

    text = (
        "1. EXECUTIVE SUMMARY:\n"
        f"{exec_summary}\n\n"
        "2. CRITICAL ANOMALIES & OVERLOAD RISKS:\n"
        f"{anomaly_analysis}\n\n"
        "3. BATTERY DISPATCH STRATEGY:\n"
        f"{battery_analysis}\n\n"
        "4. OPERATOR ACTION CHECKLIST:\n"
        f"• {checklist[0]}\n"
        f"• {checklist[1]}\n"
        f"• {checklist[2]}"
    )

    return {
        "success": True,
        "provider": "Autonomous Grid Reasoning Engine",
        "model": "Edge-Expert-RuleBased-v3.0",
        "advisory": text,
    }


def generate_ai_advisory(summary: dict, hourly: list = None) -> dict:
    """
    Generate real-time AI strategic guidance on power transitions and battery health.
    Uses NVIDIA NIM if configured; otherwise provides deterministic expert domain reasoning.
    """
    if not NVIDIA_GENERAL_KEY:
        # Fall back directly to the expert autonomous reasoning engine
        return generate_expert_grid_advisory(summary, hourly)

    # Extract key stats
    peak_kw = summary.get("peak_demand_kw", 0)
    avg_kw = summary.get("avg_demand_kw", 0)
    overloads = summary.get("overload_alerts", 0)
    ren_hrs = summary.get("hours_renewable", 0)
    grid_hrs = summary.get("hours_main_grid", 0)
    min_soc = summary.get("min_battery_soc_pct", 80)
    final_soc = summary.get("final_battery_soc_pct", 80)

    prompt = f"""You are the HackSphere 3.0 Autonomous Microgrid Advisory AI.
Analyze the following 24-hour forecast data and produce a structured, high-level engineering advisory.

Microgrid Forecast Metrics:
- Peak Demand: {peak_kw} kW (Thresholds: 160 kW Renewable switch, 200 kW Critical Overload)
- Average Demand: {avg_kw} kW
- Renewable Storage Hours: {ren_hrs} hours
- Main Grid Hours: {grid_hrs} hours
- Overload Alert Events (>= 200 kW): {overloads}
- Minimum Battery SOC Reached: {min_soc}% (Floor limit: 10%)
- Final Forecasted Battery SOC: {final_soc}%

Provide an engineering dispatch assessment formatted with these exact sections:
1. EXECUTIVE SUMMARY: (1-2 sentences on grid stability and transition health)
2. CRITICAL ANOMALIES & OVERLOAD RISKS: (Analyze overload count and peak hours)
3. BATTERY DISPATCH STRATEGY: (Recommendations for pre-charging, depth-of-discharge, or reserve protection)
4. OPERATOR ACTION CHECKLIST: (3 concise bullet points for the shift engineer)

Keep the response professional, concise, and focused on power stability."""

    headers = {
        "Authorization": f"Bearer {NVIDIA_GENERAL_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": NVIDIA_GENERAL_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are an expert power microgrid engineer and AI dispatch advisor.",
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
        "max_tokens": 500,
    }

    try:
        url = f"{NVIDIA_BASE_URL}/chat/completions"
        res = requests.post(url, headers=headers, json=payload, timeout=12)
        if res.status_code == 200:
            data = res.json()
            analysis_text = data["choices"][0]["message"]["content"]
            return {
                "success": True,
                "provider": "NVIDIA NIM",
                "model": NVIDIA_GENERAL_MODEL,
                "advisory": analysis_text,
            }
        else:
            # On API error, gracefully fall back to expert reasoning
            return generate_expert_grid_advisory(summary, hourly)
    except Exception:
        # On connection failure, gracefully fall back to expert reasoning
        return generate_expert_grid_advisory(summary, hourly)
