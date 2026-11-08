# forever-ever

Reproducible theorycrafting for World of Warcraft: Forever. A personal, non-commercial project exploring **mathematically correct builds under explicit assumptions**, starting with priest healing.

## Status

Early prototype: an offline direct-heal comparator works with user-supplied JSON. The included example is **synthetic**, not game data or a build recommendation. ForeverDB API access has not yet been requested or approved. There is no live API integration or talent optimizer yet.

## Run

Python 3.11+ and [uv](https://docs.astral.sh/uv/):

```sh
uv run compare_heals.py examples/synthetic-heals.json --missing-hp 250 --mana-budget 300
uv run python -m unittest discover -s tests -v
```

No credentials or third-party Python packages are needed for this prototype.

## What “mathematically correct” means here

A build can only be optimal for a defined objective and constraints. We intend to compare useful healing per mana, healing throughput, response time and survival across specified encounters, gear, talents and levels. We will report trade-offs rather than claim one universally best build.

The current script is deliberately narrower: repeated identical **direct heals**, static missing HP, no incoming damage, no crits, no regeneration, no movement, no talents or gear simulation. Cast throughput uses the larger of cast time and GCD; first-heal delay is cast time. Expected useful healing assumes a uniform continuous roll between the supplied minimum and maximum, clipping each possible result to missing HP. The burst budget column reports uncapped expected healing, not useful healing on that static target. Input must already contain the desired character-adjusted values. It does not model HoTs, shields, channels or rotations.

## Data and attribution

Planned API source: **[Data from ForeverDB.net](https://foreverdb.net)** — [API documentation](https://foreverdb.net/developers). Integration pending approval; this repository currently distributes no ForeverDB dataset. Generated reports always include the source's attribution and game build. A README credit does not replace report-level credit.

Every imported record must retain source URL, retrieval date, game build, provenance and uncertainty (client data, in-game observation, or Classic fallback). Client records do not by themselves establish live availability. Game text and artwork belong to Blizzard Entertainment. This project is unofficial and unaffiliated with Blizzard or ForeverDB.

For API access: local read-only analysis of spell ranks, healing efficiency, talents and eventually builds; visible attribution in every displayed report; no resale or republishing of bulk data. Use only necessary endpoints within the provider's quotas and caching rules.

## Secrets and boundaries

Keep any future `FOREVERDB_API_KEY` in Infisical, injected at runtime. Never commit it, store it in an example, or expose it in a browser. No scripts control the game client, cast spells, move characters, or perform auction-house transactions.

## Next

- Obtain API access and validate priest spell and talent records against the live client.
- Compare spell ranks with explicit equipment and talent modifiers.
- Add incoming-damage timelines and mana regeneration before optimizing rotations.
- Search legal talent allocations under defined objectives, with sensitivity analysis and reproducible tests.

Changes to formulas should include boundary-case tests; changes to data should identify the source build. Synthetic fixtures must stay clearly labeled.
