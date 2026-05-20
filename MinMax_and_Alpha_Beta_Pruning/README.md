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

### Quantitative Efficiency Metrics
When evaluating both engines from a completely vacant board state (Turn 1), the absolute choice of move remains completely unchanged, but the reduction in computational overhead is significant:

| Metric Evaluation | Standard Minimax | Alpha-Beta Pruning | Performance Optimization |
| :--- | :--- | :--- | :--- |
| **Nodes Checked (Turn 1)** | **549,946** | **18,297** | **~96.7% reduction** in search space |
| **Move Decision Accuracy** | 100% Optimal | 100% Optimal | Zero loss in precision |

---

## 2. Advanced Decision-Making Frameworks

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

## 3. Structural Comparison Matrix

| Feature | Minimax / Alpha-Beta | Monte Carlo Tree Search (MCTS) | Markov Decision Process (MDP) |
| :--- | :--- | :--- | :--- |
| **Environment Profile** | Deterministic, Perfect Info, 2-Player, Zero-Sum. | Deterministic or Stochastic, Perfect/Imperfect Info. | Stochastic (Probabilistic), Single Agent vs Environment. |
| **Search Framework** | Complete Depth-First Search tree traversal. | Stochastic Sampling & Randomized simulations. | Global Dynamic Programming (Iterative value adjustment). |
| **Heuristic Dependency**| High (Requires evaluation functions if depth cutoffs are used). | None (Relies entirely on actual win/loss metrics from full rollouts). | High (Requires designing a continuous reward function $R$). |
| **Scalability Matrix** | Low ($O(b^d)$ explodes quickly on complex games). | High (Can be stopped at any time limit; scales well to high factors). | Moderate (Suffers from the "curse of dimensionality" as states multiply). |
| **Core Computation Output** | Single best move for the exact current state. | Single best move backed by maximum win statistics. | A complete Policy ($\pi$) mapping actions for every possible state. |
| **Primary Domain** | Tic-Tac-Toe, Chess, Checkers, Connect Four. | Go, complex real-time strategy games, card games. | Robotic pathfinding, industrial automation, financial options. |