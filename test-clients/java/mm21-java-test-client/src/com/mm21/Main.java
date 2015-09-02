package com.mm21;

import java.io.IOException;
import java.util.ArrayList;

/**
 * The entry-point class of the test client
 * @competitors Add your team name, but don't modify anything else
 * @competitors Your AI itself should go in AI.java
 */

public class Main {

    // @competitors Modify me
    private static final String TEAM_NAME = "YOUR_TEAM_NAME_HERE";

    /**
     * Run the game
     * @competitors Do not modify
     */
    public static void main(String[] args) {

        // Connect
        System.out.println("Connecting to server...");
        try {
            ServerConnection.connect(TEAM_NAME);
        } catch (IOException e) {
            System.out.println("!!! CONNECTION FAILED !!!");
            e.printStackTrace(System.out);
        }
        System.out.println("Successfully connected to server.");

        // Main game loop
        boolean gameOver = false;
        int turnCounter = 1;
        while (!gameOver) {
            try {

                // Execute turn
                // @competitors DO NOT PUT YOUR AI HERE - use AI.java instead!
                TurnResult serverResponse = ServerConnection.readTurn();
                System.out.println("Received turn.");
                ArrayList<Action> clientActions = AI.processTurn(serverResponse);
                System.out.println("Computed turn.");
                ServerConnection.sendTurn(clientActions);
                System.out.println("Sent turn.");

                // Update variables
                turnCounter++;

            } catch (IOException e) {
                System.out.println("!!! ERROR, SEE BELOW !!!");
                e.printStackTrace(System.out);
            }
        }
    }
}
