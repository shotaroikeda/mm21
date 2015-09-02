package com.mm21;

import java.io.IOException;
import java.util.ArrayList;

/**
 * @competitors You'll probably need to modify this file, unless you're happy with our dumb test client
 */

public class Main {

    /**
     * @competitors Modify me
     * User settings (team name + any global variables your test client needs)
     */
    private static final String TEAM_NAME = "YOUR_TEAM_NAME_HERE";
    // @competitors Put any additional variables here.

    /***
     * @competitors Modify me
     * Determine what actions to do, given the server response
     */
    private static ArrayList<Action> processTurn(TurnResult result) {

        // List of actions to execute
        ArrayList<Action> actions = new ArrayList<Action>();

        // @competitors Put your AI here.
        // NOTE: result is NULL on the first turn, so don't forget to null check!


        // Done!
        return actions;
    }

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
                TurnResult serverResponse = ServerConnection.readTurn();
                System.out.println("Received turn.");
                ArrayList<Action> clientActions = processTurn(serverResponse);
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
