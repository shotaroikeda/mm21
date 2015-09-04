package com.mm21;

import java.util.ArrayList;
import java.util.Arrays;

/**
 * A file containing a competitor's AI
 * @competitors Modify this file to your heart's content, including the helper functions
 */
public class AI {

    // Global test client variables
    // @competitors Put your global/between-turn variables here
    public static int MY_PLAYER_ID = -1; // Your client's player ID

    // Determine what actions to do, given the server response
    public static ArrayList<Action> processTurn(TurnResult result) {

        // List of actions to execute
        ArrayList<Action> actions = new ArrayList<Action>();

        // Compute actions
        // @competitors reject our AI and substitute your own.
        ArrayList<Node> allNodes = new ArrayList(Arrays.asList(result.nodes()));
        ArrayList<Node> myNodes = filterMyNodes(allNodes);
        for (Node n : myNodes) {

            // Attempt to infiltrate nearby nodes
            Action a = n.adjacentNodes().get(0).doControl(500);
            actions.add(a);
        }

        // Done!
        return actions;
    }

    // Helper function to remove nodes you own from a node list
    private static ArrayList<Node> filterMyNodes(ArrayList<Node> inNodes) {
        return filterNodesByOwner(inNodes, MY_PLAYER_ID);
    }

    // Helper function to filter nodes you don't own from a node list
    private static ArrayList<Node> filterOthersNodes(ArrayList<Node> inNodes) {
        ArrayList<Node> outNodes = new ArrayList<Node>();
        for (Node n : inNodes) {
            if (n.ownerId() != MY_PLAYER_ID) {
                outNodes.add(n);
            }
        }
        return outNodes;
    }

    // Helper function to filter a node list by player ID
    private static ArrayList<Node> filterNodesByOwner(ArrayList<Node> inNodes, int playerId) {
        ArrayList<Node> outNodes = new ArrayList<Node>();
        for (Node n : inNodes) {
            if (n.ownerId() == playerId) {
                outNodes.add(n);
            }
        }
        return outNodes;
    }
}
