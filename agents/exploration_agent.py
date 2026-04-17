"""
ExplorationAgent — A systematic exploration agent for ARC-AGI-3.

Strategy:
1. EXPLORE phase: Systematically try each action and observe what changes
2. MODEL phase: Build a state-transition model of the environment
3. PLAN phase: Use the model to find action sequences that move toward "winning" states

This is a starting scaffold. The real intelligence you'll build goes into
the MODEL and PLAN phases — this is where Bayesian reasoning, program synthesis,
or learned world models would plug in.

Author: Sparsh
Competition: ARC Prize 2026 — ARC-AGI-3
"""

import random
from collections import defaultdict
from typing import Any

import numpy as np
from arcengine import FrameData, GameAction, GameState

from .agent import Agent


class ExplorationAgent(Agent):
    """
    A systematic exploration agent that:
    - Tries each action and tracks what changes in the grid
    - Detects loops and avoids repeating unproductive sequences
    - Builds a simple state-action-outcome memory
    - Uses that memory to make increasingly informed decisions
    """

    MAX_ACTIONS = 200

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        # --- Exploration state ---
        self.action_history: list[GameAction] = []
        self.grid_history: list[np.ndarray] = []
        self.state_action_outcomes: dict = defaultdict(list)

        # --- Phase management ---
        self.phase = "EXPLORE"  # EXPLORE -> MODEL -> PLAN
        self.explore_step = 0
        self.max_explore_steps = 50   # actions dedicated to pure exploration
        self.max_total_steps = 200    # hard cap to avoid 5x penalty

        # --- Loop detection ---
        self.seen_grid_hashes: dict[int, int] = {}  # hash -> count
        self.consecutive_no_change = 0

        # --- Simple actions to cycle through during exploration ---
        self.simple_actions = [
            GameAction.ACTION1,
            GameAction.ACTION2,
            GameAction.ACTION3,
            GameAction.ACTION4,
        ]

    # ------------------------------------------------------------------ #
    #  Core interface methods
    # ------------------------------------------------------------------ #

    def is_done(self, frames: list[FrameData], latest_frame: FrameData) -> bool:
        """Stop when we win or exhaust our action budget."""
        if latest_frame.state is GameState.WIN:
            return True
        if len(self.action_history) >= self.max_total_steps:
            return True
        return False

    def choose_action(self, frames: list[FrameData], latest_frame: FrameData) -> GameAction:
        """Main decision loop — dispatches to the current phase."""

        # Handle game-over / not-started states
        if latest_frame.state in [GameState.NOT_PLAYED, GameState.GAME_OVER]:
            self._reset_state()
            action = GameAction.RESET
            action.reasoning = "Starting/restarting the game"
            return action

        # Record the current grid (FrameData.frame is a list of 2D layers; take the last one)
        current_grid = latest_frame.frame[-1] if latest_frame.frame else None
        if current_grid is not None and len(current_grid) > 0:
            grid_array = np.asarray(current_grid)
            self.grid_history.append(grid_array.copy())
            self._update_loop_detection(grid_array)

        # Dispatch to phase
        if self.phase == "EXPLORE":
            action = self._explore_phase(frames, latest_frame)
        elif self.phase == "MODEL":
            action = self._model_phase(frames, latest_frame)
        else:
            action = self._plan_phase(frames, latest_frame)

        self.action_history.append(action)
        return action

    # ------------------------------------------------------------------ #
    #  Phase 1: EXPLORE — Systematically try actions, observe changes
    # ------------------------------------------------------------------ #

    def _explore_phase(self, frames: list[FrameData], latest_frame: FrameData) -> GameAction:
        """
        Try each simple action in sequence and record what changes.
        Also try clicking on "interesting" grid locations (non-background pixels).
        """
        self.explore_step += 1

        # Transition to MODEL phase after exploration budget
        if self.explore_step > self.max_explore_steps:
            self.phase = "MODEL"
            return self._model_phase(frames, latest_frame)

        # If we're stuck in a loop, try something different
        if self.consecutive_no_change > 3:
            self.consecutive_no_change = 0
            return self._try_click_interesting_pixel(latest_frame)

        # Cycle through simple actions systematically
        action_idx = (self.explore_step - 1) % len(self.simple_actions)
        action = self.simple_actions[action_idx]
        action.reasoning = f"EXPLORE: Trying {action.value} (step {self.explore_step}/{self.max_explore_steps})"
        return action

    # ------------------------------------------------------------------ #
    #  Phase 2: MODEL — Analyze what we've learned
    # ------------------------------------------------------------------ #

    def _model_phase(self, frames: list[FrameData], latest_frame: FrameData) -> GameAction:
        """
        Analyze the exploration data and build a model of the environment.

        TODO: This is where your real intelligence goes. Ideas:
        - Bayesian hypothesis testing over candidate rules
        - Program synthesis to find grid transformation programs
        - Neural network that predicts next state given action
        - Graph search over the state space
        """
        # For now, analyze which actions caused the most grid changes
        best_actions = self._rank_actions_by_impact()

        self.phase = "PLAN"
        return self._plan_phase(frames, latest_frame)

    # ------------------------------------------------------------------ #
    #  Phase 3: PLAN — Use the model to act purposefully
    # ------------------------------------------------------------------ #

    def _plan_phase(self, frames: list[FrameData], latest_frame: FrameData) -> GameAction:
        """
        Use learned knowledge to take purposeful actions.

        TODO: This is where planning/search goes. Ideas:
        - Monte Carlo Tree Search over the state space
        - Beam search with learned value function
        - Active inference (minimize expected free energy)
        """
        # Simple heuristic: prefer actions that caused the most change
        best_actions = self._rank_actions_by_impact()

        if best_actions:
            action = best_actions[0]
            action.reasoning = f"PLAN: Using highest-impact action {action.value}"
            return action

        # Fallback: try clicking on interesting pixels
        return self._try_click_interesting_pixel(latest_frame)

    # ------------------------------------------------------------------ #
    #  Helper methods
    # ------------------------------------------------------------------ #

    def _grid_hash(self, grid: np.ndarray) -> int:
        """Fast hash of a grid for loop detection."""
        return hash(grid.tobytes())

    def _update_loop_detection(self, grid: np.ndarray):
        """Track how many times we've seen each grid state."""
        h = self._grid_hash(grid)
        self.seen_grid_hashes[h] = self.seen_grid_hashes.get(h, 0) + 1

        # Check if the grid changed from the previous step
        if len(self.grid_history) >= 2:
            prev_grid = self.grid_history[-2]
            if np.array_equal(grid, prev_grid):
                self.consecutive_no_change += 1
            else:
                self.consecutive_no_change = 0

    def _compute_grid_diff(self, grid_a: np.ndarray, grid_b: np.ndarray) -> int:
        """Count the number of pixels that changed between two grids."""
        if grid_a is None or grid_b is None:
            return 0
        if grid_a.shape != grid_b.shape:
            return int(max(grid_a.size, grid_b.size))
        return int(np.sum(grid_a != grid_b))

    def _rank_actions_by_impact(self) -> list[GameAction]:
        """
        Look at the history of (action, grid_change) pairs and rank
        actions by how much change they tend to cause.
        """
        action_impact: dict[GameAction, list[int]] = defaultdict(list)

        for i, action in enumerate(self.action_history):
            if i + 1 < len(self.grid_history) and i < len(self.grid_history):
                diff = self._compute_grid_diff(
                    self.grid_history[i],
                    self.grid_history[i + 1] if i + 1 < len(self.grid_history) else self.grid_history[i]
                )
                action_impact[action].append(diff)

        # Sort by average impact (descending)
        ranked = sorted(
            action_impact.keys(),
            key=lambda a: np.mean(action_impact[a]) if action_impact[a] else 0,
            reverse=True,
        )

        return ranked

    def _try_click_interesting_pixel(self, latest_frame: FrameData) -> GameAction:
        """
        Find non-background pixels and click on one of them.
        "Interesting" = pixels that differ from the most common color.
        """
        raw = latest_frame.frame[-1] if latest_frame.frame else None
        if raw is None or len(raw) == 0:
            # Fallback to random action
            action = random.choice(self.simple_actions)
            action.reasoning = "Fallback: random action (no grid available)"
            return action

        grid = np.asarray(raw)

        # Find the background color (most common)
        unique, counts = np.unique(grid, return_counts=True)
        bg_color = unique[np.argmax(counts)]

        # Find non-background pixel locations
        interesting = np.argwhere(grid != bg_color)

        if len(interesting) > 0:
            # Pick a random interesting pixel
            idx = random.randint(0, len(interesting) - 1)
            coords = interesting[idx]
            # Grid may be 2D (H,W) or higher-dim — take the last two as (y, x)
            y, x = int(coords[-2]), int(coords[-1])

            action = GameAction.ACTION6  # ACTION6 is the click/complex action in ARC-AGI-3
            action.set_data({"x": x, "y": y})
            action.reasoning = f"Clicking interesting pixel at ({x}, {y})"
            return action
        else:
            # Grid is uniform — try a random simple action
            action = random.choice(self.simple_actions)
            action.reasoning = "No interesting pixels found, trying random action"
            return action

    def _find_clusters(self, grid: np.ndarray, bg_color: int) -> list[dict]:
        """
        Find connected clusters of non-background pixels.
        Returns list of dicts with 'color', 'pixels', 'center'.

        TODO: Use this for object-level reasoning.
        """
        visited = np.zeros_like(grid, dtype=bool)
        clusters = []

        for y in range(grid.shape[0]):
            for x in range(grid.shape[1]):
                if grid[y, x] != bg_color and not visited[y, x]:
                    # BFS to find connected component
                    cluster_pixels = []
                    color = grid[y, x]
                    queue = [(y, x)]
                    visited[y, x] = True

                    while queue:
                        cy, cx = queue.pop(0)
                        cluster_pixels.append((cx, cy))

                        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            ny, nx = cy + dy, cx + dx
                            if (0 <= ny < grid.shape[0] and 0 <= nx < grid.shape[1]
                                    and not visited[ny, nx] and grid[ny, nx] == color):
                                visited[ny, nx] = True
                                queue.append((ny, nx))

                    center_x = np.mean([p[0] for p in cluster_pixels])
                    center_y = np.mean([p[1] for p in cluster_pixels])
                    clusters.append({
                        "color": int(color),
                        "pixels": cluster_pixels,
                        "center": (center_x, center_y),
                        "size": len(cluster_pixels),
                    })

        return clusters

    def _reset_state(self):
        """Reset internal state for a new game / level."""
        self.action_history = []
        self.grid_history = []
        self.state_action_outcomes = defaultdict(list)
        self.phase = "EXPLORE"
        self.explore_step = 0
        self.seen_grid_hashes = {}
        self.consecutive_no_change = 0
