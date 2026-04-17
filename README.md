# ARC-AGI-3 Agent — ARC Prize 2026

My submission for the [ARC Prize 2026 — ARC-AGI-3 Competition](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3).

## What is ARC-AGI-3?

ARC-AGI-3 drops an AI agent into interactive game-like environments with **no instructions, no rules, and no stated goals**. The agent must explore, discover the rules, figure out what "winning" means, and execute — all from scratch.

- Humans score **100%**
- Best frontier AI (Gemini 3.1 Pro) scores **0.37%**
- Best algorithmic agent (RL + graph search) scores **12.58%**

Prize pool: **$2M+** across three tracks.

## My Approach

**Architecture:** [Describe your approach here as you develop it]

**Core ideas:**
- Systematic exploration with change detection
- [Your approach: Bayesian world modeling / program synthesis / RL / etc.]
- Action-efficiency optimization (quadratic scoring penalty)

## Setup

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/ARC-AGI-3-Agents.git
cd ARC-AGI-3-Agents

# Install
uv sync
# or: pip install arc-agi

# Set API key
export ARC_API_KEY="your-key"

# Run the exploration agent
uv run main.py --agent=explorationagent --game=ls20

# Run on all games
uv run main.py --agent=explorationagent
```

## Project Structure

```
ARC-AGI-3-Agents/
├── agents/
│   ├── __init__.py              # Agent registry
│   ├── agent.py                 # Base Agent class
│   ├── structs.py               # FrameData, GameAction, GameState
│   ├── exploration_agent.py     # My custom agent
│   └── templates/
│       └── random_agent.py      # Reference: random baseline
├── main.py                      # Entry point
├── notebooks/
│   ├── analysis.ipynb           # Grid analysis & visualization
│   └── kaggle_submission.ipynb  # Kaggle submission notebook
├── experiments/
│   └── experiment_log.md        # Track what works / doesn't
├── SETUP_GUIDE.md               # Detailed setup instructions
└── README.md                    # This file
```

## Development Workflow

1. **Develop locally** with Claude Code in OFFLINE mode (~2K FPS, no rate limits)
2. **Test ONLINE** for real scorecards and replays
3. **Push to GitHub** for version control
4. **Submit to Kaggle** when ready for official evaluation

## Experiment Log

| Date | Experiment | Game | Score | Notes |
|------|-----------|------|-------|-------|
| YYYY-MM-DD | Random baseline | ls20 | ~0% | Baseline measurement |
| YYYY-MM-DD | Exploration agent v1 | ls20 | TBD | Systematic action cycling + change detection |

## Key Constraints

- **No internet** during Kaggle evaluation
- **T4 GPU** (16GB VRAM) + 12hr runtime limit
- **Action efficiency scoring** — 10× human actions ≈ 1% score, 5× cap terminates
- **Must open-source** to be prize-eligible (MIT-0 or CC0 license)

## Resources

- [ARC-AGI-3 Docs & SDK](https://docs.arcprize.org/)
- [Technical Paper](https://arcprize.org/media/ARC_AGI_3_Technical_Report.pdf)
- [2025 Winning Solutions](https://arcprize.org/competitions/2025)
- [Discord Community](https://discord.gg/9b77dPAmcA)
- [Agent Quickstart Video](https://www.youtube.com/watch?v=xEVg9dcJMkw)

## License

MIT-0 (required for ARC Prize eligibility)
