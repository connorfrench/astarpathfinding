# A* Pathfinding Visualization

This is an A* Pathfinding Algorithm implemented in Python that utilizes the Pygame library for real time visualization of the algorithms steps. I created this as a learning exercise to practice Python and familiarize myself with Pygame, as well as gain more experience implementing algorithms.

## Algorithm

This program uses the A* Algorithm to find the shortest possible path, which works like so:

The cost of a path is found with the function:

### f(n) = g(n) + h(n)
* g(n) = cost so far to reach this node
* h(n) = heuristic function applied to this node
   * The heuristic function used in this algorithm is Manhattan Distance, which is:         
     >h(n) = ∣ x<sub>n</sub>  ​− x<sub>end</sub> ​∣ + ∣ y<sub>n</sub>​− y<sub>end</sub> ​∣

### Starting at the selected start node:
1. Create a priority queue and add the start node.
2. Create a list of g values, initialized to infinity.
3. Create a list of f values, initialized to infinity.
4. Set g[start] to 0 and f[start] to h(start).
5. Set the current node to the node at the front of the queue.
6. If the current node at the front of the queue is the destination, the algorithm is complete, if the queue is empty, there is no possible path.
7. For each neighbor of the current node:
    * If the g value for reaching this neighbor is lower than the g value of this node in the list of g values, update the g value and f value.
    * If the neighbor is not in the queue, add it to the queue.
8. Remove the current node from the queue and return to step 5.



## Usage

Left mouse button: Place start point, end point, and barriers.

Right mouse button: Remove start point, end point, and barriers.

Spacebar: Start the algorithm (must have start point and end point placed).

C: Clear the board back to its original state.

## Color Meanings

* Orange: start node
* Blue: end node
* Black: barrier
* Purple: optimal path found
* Red: node discarded by algorithm
* Green: node still being considered by algorithm

## Examples

### Simple path with no barriers:

![pathfinding example 1](https://lh3.googleusercontent.com/pw/ACtC-3fixipWix7G9h10psWeCB2jqhgh4fIZhRo6fDnhH5ITRq4B-4KDEtXBcCaO2CcTUnCCDxXW1tdXgcFVrYMWDhy6m2KNDXcy7lfTyrrCWXeVSQtTuvVvGoUyz7OBjth2d-V4VEIR-TFzKF8nLRWwYB94=w798-h802-no)

### Path with barriers:

![pathfinding example 2](https://lh3.googleusercontent.com/pw/ACtC-3ewSEX6lCwuVAh3puhtQcBLjLdgg7MmsxFn3EEsSNWIQfou4y1ZTFyzDuC7ubBqe4FKl5IBkg6SWlEuORfgKIAbQe6_uZt_BvvOd20u7QZBesglm_clHxhpmfWSNGhOFW9K3z2m-hWp-D7tESZ4Ixpe=w799-h801-no?authuser=0)