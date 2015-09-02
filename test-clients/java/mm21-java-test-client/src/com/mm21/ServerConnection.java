package com.mm21;
import org.json.JSONObject;
import org.json.JSONTokener;
import org.json.JSONArray;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.InetAddress;
import java.net.Socket;
import java.util.ArrayList;

/**
 * Handles connections to the game server
 * @competitors Do not modify
 */
public class ServerConnection {

    // Connection values
    private static InetAddress SERVER_ADDR;
    private static final int SERVER_PORT = 1337;
    private static Socket socket;
    private static OutputStreamWriter writer;
    private static InputStreamReader reader;

    // Initialize connection to server
    public static void connect(String TEAM_NAME) throws IOException {

        // Connect to server
        SERVER_ADDR = InetAddress.getLocalHost();
        Socket temp = new Socket(SERVER_ADDR, SERVER_PORT);
        writer = new OutputStreamWriter(socket.getOutputStream());

        // Send team data
        JSONObject teamData = new JSONObject();
        teamData.put("teamName", TEAM_NAME);
        teamData.write(writer);
        writer.flush();
    }

    // Convert JSON response from game into a Turn object
    public static TurnResult readTurn() throws IOException {

        // Get turn JSON
        JSONObject turnJson = (JSONObject) new JSONTokener(new BufferedReader(reader).readLine()).nextValue();

        // Convert turn JSON into a Turn object
        TurnResult turnObj = new TurnResult(turnJson);
        return turnObj;
    }

    // Send client's actions to server
    public static void sendTurn(ArrayList<Action> actions) throws IOException {

        // Convert actions to JSON
        JSONArray jsonActions = new JSONArray();
        for (int i = 0; i < actions.size(); i++) {
            JSONObject action = actions.get(i).toJSONObject();
            jsonActions.put(i, action);
        }

        // Send action JSON
        jsonActions.write(writer);
        writer.flush();
    }
}