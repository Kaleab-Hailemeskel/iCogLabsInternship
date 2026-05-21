# Lab Assignment: AI Game-Playing Engine (Minimax vs. Alpha-Beta Pruning)

This repository contains the implementation, performance metrics, and a comparative theoretical analysis of foundational game-playing AI algorithms tested on a $3 \times 3$ Tic-Tac-Toe environment.

---

## 1. Code Review & Architecture

The project contains two variations of a state-space search algorithm designed for two-player, turn-based, zero-sum games of perfect information. 

Both scripts utilize **backtracking state management**. Instead of copying the board layout at every step, a single reference to the grid array is modified (`grid[r][c] = symbol`) before making a recursive dive, and then immediately restored (`grid[r][c] = empty`) upon returning. This configuration maintains a memory footprint of $O(n^2)$ space complexity.

### Standard Minimax (`minimax`)
* **Mechanism:** Executes an exhaustive, brute-force, depth-first traversal of the entire game tree. It checks every permutation of legal moves until it encounters a terminal state (win, loss, or draw).
* **Limitation:** Suffers from exponential time complexity ($O(b^d)$), where $b$ is the branching factor and $d$ is the depth. It repeatedly spends processing cycles evaluating sub-trees that an optimal opponent would mathematically never let the game drift into.

### Optimized Alpha-Beta Pruning (`minimax_alphabeta`)
* **Mechanism:** Enhances the depth-first search by tracking two dynamic mathematical boundary constraints:
  * **$\alpha$ (Alpha):** The lower bound—the maximum score the Maximizer (AI) is already assured of.
  * **$\beta$ (Beta):** The upper bound—the minimum score the Minimizer (Opponent) is already assured of.
* **Pruning Logic:** Whenever a branch returns a value where $\beta \le \alpha$, the loop executes an immediate `break` statement. This truncates the remaining search paths safely, because an optimal opponent would avoid this branch entirely.

---

## 2. Empirical Performance Optimization Analysis

To measure the real-world efficiency gains of Alpha-Beta Pruning over plain Minimax, both algorithms were executed from an empty root board state ($3 \times 3$ grid) on Turn 1 to track the total number of states visited (`node_count`).

While both algorithms are mathematically guaranteed to return the **exact same optimal move vector**, Alpha-Beta Pruning introduces a massive computational reduction by dynamically eliminating irrelevant branches.

### Node Evaluation Comparison

| Performance Metric | Standard Minimax | Alpha-Beta Pruning | Empirical Savings / Reduction |
| :--- | :--- | :--- | :--- |
| **Total Nodes Evaluated (Turn 1)** | **549,946** | **18,297** | **531,649 nodes skipped** |
| **Search Space Traversed** | 100% | ~3.33% | **96.67% of tree pruned** |
| **Execution Accuracy** | 100% Optimal | 100% Optimal | No loss in precision |

### Why the Optimization is Crucial
Standard Minimax operates at a computational complexity of $O(b^d)$. In a simple game like Tic-Tac-Toe, a modern CPU can handle half a million node evaluations in a fraction of a second. However, as the branching factor $b$ and depth $d$ scale upward (e.g., Chess or Connect Four), the state-space size scales exponentially. 

By dropping the total nodes visited on the very first turn from over **549,000 down to just 18,297**, Alpha-Beta Pruning demonstrates how effective boundary logic is at containing state-space explosions without reducing the intelligence or accuracy of the AI.

---

## 3. Advanced Decision-Making Frameworks

While Minimax and Alpha-Beta Pruning function exceptionally well within small, deterministic environments, they fail to scale when games feature hidden information, random elements, or massive branching factors (such as Chess or Go). Below is an analysis of alternative search frameworks.

### A. Monte Carlo Tree Search (MCTS)
Unlike Minimax, which explores states uniformly layer-by-layer, MCTS relies on **statistical sampling** and randomized rollouts. It constructs an asymmetric tree, prioritizing computing power toward highly favorable moves while balancing raw exploration.

MCTS runs continuously through four distinct recursive steps:
1. **Selection:** Starting at the root, the engine navigates down existing child nodes using a selection policy formula, typically **UCB1 (Upper Confidence Bound)**. This equation balances *exploitation* (choosing paths with high known win rates) against *exploration* (visiting rarely checked states).
2. **Expansion:** Upon reaching a leaf node that is not a terminal game state, the engine expands the tree structure by adding one or more legal child nodes.
3. **Simulation (Rollout):** From the newly opened node, the engine simulates a fast-paced game all the way to completion. Moves during this phase are picked randomly or via lightweight heuristics. No tree nodes are saved here.
4. **Backpropagation:** The outcome of the simulated game ($1$ for a win, $0$ for a draw/loss) is passed back up the path to the root. Every node along that path increments its tracking metrics (`total_wins` and `total_visits`), updating the statistical weights for the next selection loop.

### B. Markov Decision Process (MDP)
Minimax and MCTS both operate under the assumption that actions are entirely deterministic—if the AI moves to a space, it occupies that space with 100% certainty. A **Markov Decision Process (MDP)** provides a mathematical framework for environments where outcomes are **probabilistic and partially stochastic** (involving chance).

An MDP is defined formally as a 4-tuple $(S, A, P, R)$:
* **$S$ (States):** The complete set of all environmental configurations.
* **$A$ (Actions):** The set of moves or choices available to the agent.
* **$P(s' \mid s, a)$ (Transition Probability):** The probability that taking action $a$ while in state $s$ successfully leads to state $s'$. For example, due to environmental noise or rolling dice, an action might succeed 85% of the time and fail or drift 15% of the time.
* **$R(s, a, s')$ (Reward Function):** The immediate feedback score returned to the agent after executing a transition.

Instead of outputting a single string of specific moves, solving an MDP calculates a comprehensive **Policy ($\pi$)**. A policy maps every single state in the system to its absolute best possible action. This is computed globally using dynamic programming methods like **Value Iteration** or **Policy Iteration**.

---

## 4. Structural Comparison Matrix

| Feature | Minimax / Alpha-Beta | Monte Carlo Tree Search (MCTS) | Markov Decision Process (MDP) |
| :--- | :--- | :--- | :--- |
| **Environment Profile** | Deterministic, Perfect Info, 2-Player, Zero-Sum. | Deterministic or Stochastic, Perfect/Imperfect Info. | Stochastic (Probabilistic), Single Agent vs Environment. |
| **Search Framework** | Complete Depth-First Search tree traversal. | Stochastic Sampling & Randomized simulations. | Global Dynamic Programming (Iterative value adjustment). |
| **Heuristic Dependency**| High (Requires evaluation functions if depth cutoffs are used). | None (Relies entirely on actual win/loss metrics from full rollouts). | High (Requires designing a continuous reward function $R$). |
| **Scalability Matrix** | Low ($O(b^d)$ explodes quickly on complex games). | High (Can be stopped at any time limit; scales well to high factors). | Moderate (Suffers from the "curse of dimensionality" as states multiply). |
| **Core Computation Output** | Single best move for the exact current state. | Single best move backed by maximum win statistics. | A complete Policy ($\pi$) mapping actions for every possible state. |
| **Primary Domain** | Tic-Tac-Toe, Chess, Checkers, Connect Four. | Go, complex real-time strategy games, card games. | Robotic pathfinding, industrial automation, financial options. |