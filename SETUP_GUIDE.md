# ARC-AGI-3 Competition — Step-by-Step Setup Guide

## Overview

This guide walks you through setting up your local development environment for
the ARC Prize 2026 — ARC-AGI-3 competition, connecting it to GitHub, and
preparing for Kaggle submission.

**Competition Links:**
- Competition page: https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3
- ARC-AGI-3 docs: https://docs.arcprize.org/
- Official agents repo: https://github.com/arcprize/ARC-AGI-3-Agents
- Play the games (as a human): https://arcprize.org/tasks?v=3
- Technical paper: https://arcprize.org/media/ARC_AGI_3_Technical_Report.pdf

**Key Dates:**
- Milestone 1 deadline: June 30, 2026 (prizes: $25K / $10K / $2.5K)
- Milestone 2 deadline: September 30, 2026 (prizes: $25K / $10K / $2.5K)
- Grand Prize: $700K for 100% score (rolls over if unclaimed)

---

## Step 1: Prerequisites

Make sure you have these installed:

```bash
# Check Python (3.10+ required)
python --version

# Install uv (recommended package manager for this project)
# macOS/Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh
# Windows:
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Verify uv
uv --version

# Make sure git is installed
git --version
```

---

## Step 2: Fork & Clone the Official Agents Repo

```bash
# 1. Go to https://github.com/arcprize/ARC-AGI-3-Agents
#    Click "Fork" in the top right to fork it to YOUR GitHub account

# 2. Clone YOUR fork (replace YOUR_USERNAME)
git clone https://github.com/YOUR_USERNAME/ARC-AGI-3-Agents.git
cd ARC-AGI-3-Agents

# 3. Add the original repo as upstream (to pull updates later)
git remote add upstream https://github.com/arcprize/ARC-AGI-3-Agents.git

# 4. Install dependencies
uv sync
# OR if using pip:
pip install arc-agi
```

---

## Step 3: Get Your ARC API Key

1. Go to https://arcprize.org/platform
2. Sign up / log in
3. Copy your API key
4. Set it in your environment:

```bash
# Option A: Export directly
export ARC_API_KEY="your-api-key-here"

# Option B: Create a .env file (recommended - add to .gitignore!)
echo 'ARC_API_KEY=your-api-key-here' > .env

# Option C: Add to your shell profile (~/.bashrc or ~/.zshrc)
echo 'export ARC_API_KEY="your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

**IMPORTANT:** Add `.env` to your `.gitignore` so you don't push your API key:
```bash
echo '.env' >> .gitignore
```

---

## Step 4: Play a Game as a Human First

Before building an agent, play a few games yourself to understand the environments:

1. Go to https://arcprize.org/tasks/ls20 and play in the browser
2. Try `ft09` and `vc33` as well
3. Notice: there are NO instructions. You have to figure out the goal yourself.

This is exactly what your agent has to do.

---

## Step 5: Run the Random Agent (Verify Setup)

```bash
# Run the built-in random agent on the ls20 game
uv run main.py --agent=random --game=ls20

# You should see:
# - Terminal rendering of the game grid
# - The agent taking random actions
# - A scorecard at the end with a replay link
```

If this works, your setup is good.

---

## Step 6: Understand the Agent Interface

Every agent needs just two methods:

```python
class MyAgent(Agent):

    def is_done(self, frames: list[FrameData], latest_frame: FrameData) -> bool:
        """Return True when the agent should stop playing."""
        # frames = full history of all frames seen
        # latest_frame = the most recent observation
        # latest_frame.grid = 64x64 numpy array of the current state
        # latest_frame.state = GameState enum (PLAYING, WIN, GAME_OVER, etc.)
        pass

    def choose_action(self, frames: list[FrameData], latest_frame: FrameData) -> GameAction:
        """Return the next action to take."""
        # Available actions:
        #   GameAction.RESET     - restart the level
        #   GameAction.ACTION1   - simple action (game-specific)
        #   GameAction.ACTION2   - simple action (game-specific)
        #   GameAction.ACTION3   - simple action (game-specific)
        #   GameAction.ACTION4   - simple action (game-specific)
        #   GameAction.CLICK     - complex action (needs x, y coordinates)
        #   GameAction.DRAG      - complex action (needs coordinates)
        pass
```

**What your agent receives each step:**
- `latest_frame.grid` — a 64×64 numpy array representing the current visual state
- `latest_frame.state` — whether you're playing, won, lost, or haven't started
- `frames` — the full history of every frame seen so far

**What your agent returns:**
- A `GameAction` — which button to press or where to click

---

## Step 7: Create Your Custom Agent

Copy the starter agent from this kit:

```bash
# Copy the exploration agent to the agents directory
cp /path/to/exploration_agent.py agents/exploration_agent.py
```

Or create `agents/exploration_agent.py` manually — see the
`exploration_agent.py` file in this starter kit.

Then register it in `agents/__init__.py`:

```python
# Add this import
from .exploration_agent import ExplorationAgent

# Add to __all__
__all__ = [
    # ... existing agents ...
    "ExplorationAgent",
    "AVAILABLE_AGENTS",
]
```

Run it:
```bash
uv run main.py --agent=explorationagent --game=ls20
```

---

## Step 8: Development Workflow with Claude Code

This is your day-to-day loop:

```bash
# 1. Start Claude Code in your project directory
cd ARC-AGI-3-Agents
claude

# 2. Ask Claude Code to help you iterate on your agent
#    Example prompts:
#    - "Look at my exploration agent and add change detection between frames"
#    - "Help me implement a Bayesian hypothesis tracker for grid patterns"
#    - "The agent keeps getting stuck in loops — add loop detection"

# 3. Test in OFFLINE mode (fast, no API calls)
#    In your agent or a test script:
#    arc = Arcade(operation_mode=OperationMode.OFFLINE)

# 4. When you want real scores, test in ONLINE mode:
uv run main.py --agent=explorationagent --game=ls20

# 5. Commit and push
git add -A
git commit -m "Add frame differencing to exploration agent"
git push origin main
```

---

## Step 9: Testing Across Multiple Games

```bash
# Run on a specific game
uv run main.py --agent=explorationagent --game=ls20

# Run on ALL available games
uv run main.py --agent=explorationagent

# View your replay after each run (link printed at the end)
# Compare your agent's action count to the human baseline
```

**Scoring:** ARC-AGI-3 uses action efficiency — how many actions YOUR agent
takes vs. how many a human takes. Taking 10× the human actions gives you ~1%
score (quadratic penalty). A 5× cap terminates the attempt entirely.

---

## Step 10: Prepare Kaggle Submission

When you're ready to submit to the official competition:

1. Go to https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3
2. Create a new notebook
3. Upload your agent code + any model weights as a Kaggle dataset
4. Your notebook must:
   - Run without internet access
   - Complete within 12 hours
   - Fit within the GPU memory (T4 = 16GB VRAM)
   - Output predictions in the required format

```python
# Example Kaggle notebook structure:
# 1. Import your agent
# 2. Load any pre-trained weights from the dataset
# 3. Run the agent on the evaluation environments
# 4. Output the submission file
```

---

## Useful Commands Reference

```bash
# Pull latest changes from the official repo
git fetch upstream
git merge upstream/main

# Run in offline mode (fast iteration)
# Set operation_mode=OperationMode.OFFLINE in your code

# Run in online mode (get scorecards)
# Set operation_mode=OperationMode.ONLINE in your code
# or just use the default: uv run main.py --agent=... --game=...

# View all available games
# Visit https://arcprize.org/tasks?v=3
```

---

## Resources

- **Discord:** https://discord.gg/9b77dPAmcA (most active community)
- **ARC-AGI-3 Docs:** https://docs.arcprize.org/
- **Technical Paper:** https://arcprize.org/media/ARC_AGI_3_Technical_Report.pdf
- **2025 Winning Solutions:** https://arcprize.org/competitions/2025
- **Agent Quickstart Video:** https://www.youtube.com/watch?v=xEVg9dcJMkw
- **Kaggle Solutions Archive:** https://kaggle.farid.one/
