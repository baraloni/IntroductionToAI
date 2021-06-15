
Comments:

Blokus Corners Problem Heuristic:
The Heuristic calculates the distance from the farthest point of the box created by the maximum values of
  0 1 2 3    the X and Y axises of covered tiles to the farthest corner + 1 for each horizontal and  
 ---------   vertical corner that is unfilled.
0|*| |*| |   The distance is calculated by chess distance (infinity norm)
 ---------   In this Example - the corner of the box is (2,1) the distance to the farthest corner is 2
1| |*| | |   and the both corners (0,2) and (3,0) are unfilled thus the heuristic value will be 4
 ---------
2| | | | |   The heuristic is consistent thus it is also admissible
 ---------

Blokus Cover Problem Heuristic:
The heuristic is the counting of unfilled targets. the heuristic is alco consistent and thus admissible.

Suboptimal Search Problem:
This search chooses each time the next closest target to the starting point or the filled targets.
At each step the search search for the best solution to cover the next target - greedy approach.

- PLEASE READ!-

Fixes:
1. Q4: We've omitted the 'return' from the return statement so we fixed that.
2. Q5: Wrong implementation, but we didn't fix that because we are not allowed to :(
3. Q7: We've replaced the (x,y) coordinates because of game board drawing, and as suggested
       in the forum. Obviously it wasn't the intention so we've switched it back (is_goal_state).
4. Q8: Wrong output, but we didn't fix that because we are not allowed to :(
5. Q9: We've sent 3 params to a function that gets only 2, we've adjusted it (line 258).

