"""Offline direct-heal comparison; see README for model assumptions."""
import argparse
import json
import math


def number(value, name, *, positive=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a number")
    if not math.isfinite(value) or value < 0 or (positive and value == 0):
        raise ValueError(f"{name} must be finite and {'positive' if positive else 'nonnegative'}")
    return value


def expected_useful(low, high, missing):
    """E[min(uniform(low, high), missing)], continuous-roll approximation."""
    if missing <= low:
        return missing
    if missing >= high:
        return (low + high) / 2
    return ((missing**2 - low**2) / 2 + missing * (high - missing)) / (high - low)


def compare(spell, missing, budget):
    missing = number(missing, "missing HP")
    budget = number(budget, "mana budget")
    low = number(spell["min_heal"], "minimum heal")
    high = number(spell["max_heal"], "maximum heal")
    if high < low:
        raise ValueError("maximum heal must be >= minimum heal")
    mana = number(spell["mana"], "mana", positive=True)
    cast = number(spell["cast_seconds"], "cast time")
    gcd = number(spell["gcd_seconds"], "GCD", positive=True)
    mean = (low + high) / 2
    return {
        "name": spell["name"], "mean_heal": mean,
        "raw_hp_per_mana": mean / mana,
        "useful_hp_per_mana": expected_useful(low, high, missing) / mana,
        "raw_hp_per_second": mean / max(cast, gcd),
        "first_heal_seconds": cast,
        "casts_in_budget": int(budget // mana),
        "uncapped_healing_in_budget": int(budget // mana) * mean,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input")
    parser.add_argument("--missing-hp", type=float, required=True)
    parser.add_argument("--mana-budget", type=float, required=True)
    args = parser.parse_args()
    try:
        with open(args.input, encoding="utf-8") as handle:
            data = json.load(handle)
        if not data.get("source") or not data.get("build"):
            raise ValueError("source and build are required")
        rows = [compare(s, args.missing_hp, args.mana_budget) for s in data["spells"]]
        print(json.dumps({
            "source": data["source"], "build": data["build"],
            "attribution": data.get("attribution", data["source"]),
            "assumptions": "Uniform rolls; direct heals; no crit, regen or incoming damage. Raw burst healing is uncapped.",
            "missing_hp": args.missing_hp, "mana_budget": args.mana_budget,
            "results": rows,
        }, indent=2, ensure_ascii=False, allow_nan=False))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
