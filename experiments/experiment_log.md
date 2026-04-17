# Experiment Log — ARC-AGI-3

Track every iteration so you know what works and what doesn't.

---

## Experiment 001: Random Baseline
**Date:** [TBD]
**Agent:** `random_agent.py`
**Games tested:** ls20, ft09, vc33
**Results:**

| Game | Score | Actions Taken | Human Baseline | Notes |
|------|-------|---------------|----------------|-------|
| ls20 | | | | |
| ft09 | | | | |
| vc33 | | | | |

**Observations:**
- [What did the random agent do? Did it ever stumble onto anything useful?]

---

## Experiment 002: Exploration Agent v1
**Date:** [TBD]
**Agent:** `exploration_agent.py`
**Changes:** Systematic action cycling, change detection, click on interesting pixels
**Games tested:** ls20, ft09, vc33
**Results:**

| Game | Score | Actions Taken | Human Baseline | Notes |
|------|-------|---------------|----------------|-------|
| ls20 | | | | |
| ft09 | | | | |
| vc33 | | | | |

**Observations:**
- Which actions caused grid changes?
- Did clicking on non-background pixels do anything?
- Were there detectable patterns in how the grid changed?

**Next steps:**
- [ ] Add frame differencing to detect which regions changed
- [ ] Track state transitions as a graph
- [ ] Try drag actions between colored objects

---

## Experiment 003: [Your Next Idea]
**Date:**
**Agent:**
**Hypothesis:** [What do you think will improve performance and why?]
**Changes:**
**Results:**
**Observations:**
**Next steps:**

---

## Architecture Ideas Backlog

- [ ] **Bayesian world model** — Maintain distribution over candidate rules,
      update after each action-observation pair. Prior: uniform over simple
      grid transformations. Likelihood: how well the rule predicts the observed
      grid change.

- [ ] **Graph search over state space** — Hash each grid state, build a graph
      of (state, action) → next_state transitions. Use BFS/DFS to find paths
      to novel states.

- [ ] **Program synthesis** — Generate candidate programs (small DSLs for grid
      transformations) and test them against observed transitions. Evolve
      programs using genetic programming.

- [ ] **Neural state encoder** — Train a small CNN to embed 64×64 grids into
      a latent space. Use the latent distance as a reward signal for
      exploration (curiosity-driven RL).

- [ ] **Active inference** — Formalize as free energy minimization. The agent
      acts to reduce uncertainty about the environment dynamics AND to reach
      preferred (winning) states.

- [ ] **Object-centric representations** — Detect clusters/objects in the grid
      and reason about relationships between them rather than raw pixels.
