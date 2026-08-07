# Optimized Flight Route Planning System

A graph-based flight planner that finds optimal routes between two cities under three different objectives, respecting real-world connection time constraints.

## What It Does

Given a start city, destination, and time window, it returns:
- **Fewest flights** (earliest arrival as tiebreaker)
- **Cheapest total fare**
- **Fewest flights** with cheapest fare as tiebreaker

## Key Design Decision

Rather than modeling cities as graph nodes, each **individual flight** is a node. Two flights are connected if the second departs at least 20 minutes after the first lands.

This matters because whether you can catch a connection depends on *when* you arrive, not just *where* — a city carries no timing information. Encoding the constraint into the edges means the search algorithms never have to reason about it.

## Algorithms

| Route Type | Algorithm | Complexity |
|---|---|---|
| Fewest flights | BFS | O(m) |
| Cheapest fare | Dijkstra | O(m log m) |
| Fewest flights, then cheapest | Priority queue ordered by (depth, cost) | O(m log m) |

Linear-time BFS is achievable because the problem guarantees at most 100 flights per city, bounding total edges at O(m).

## Implementation Notes

- Valid flight-to-flight connections are precomputed once at construction, so route queries don't recheck the time-gap rule
- Routes are reconstructed via parent pointers stored on each search node

## Files

- `Flight_Planner.cpp` — C++ implementation
- `planner.py`, `flight.py`, `main.py` — Python implementation
- `test_1.py`, `test_2.py`, `test_3.py`, `new_tc.py`, `kartik_tc.py` — test cases

## Tech Stack
Python, C++
