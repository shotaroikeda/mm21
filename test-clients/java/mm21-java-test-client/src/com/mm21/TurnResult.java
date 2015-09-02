package com.mm21;

import org.json.JSONArray;
import org.json.JSONObject;

import javax.swing.plaf.ActionMapUIResource;

/**
 * Represents the results of a game turn
 * @competitors You may modify this file, but you shouldn't need to
 */
public class TurnResult {

    // Property values (private to prevent unintentional writing)
    private Node[] m_map;
    private String[] m_players;
    private ActionResult[] m_actionResults;

    // Property getters
    public Node[] map() { return m_map; }
    public String[] players() { return m_players; }
    public ActionResult[] actionResults() { return m_actionResults; }

    // Constructor
    public TurnResult(JSONObject serverResponse) {

        // Serialize map
        JSONArray mapNodes = serverResponse.getJSONArray("map");
        this.m_map = new Node[mapNodes.length()];
        for (int i = 0; i < mapNodes.length(); i++) {
            this.m_map[i] = new Node(mapNodes.getJSONObject(i));
        }

        // Serialize player list
        JSONObject playerInfos = serverResponse.getJSONObject("playerInfos");
        for (int i = 0; i < playerInfos.length(); i++) {
            this.m_players[i] = playerInfos.getString(Integer.toString(i));
        }

        // Serialize action results
        JSONArray actionResults = serverResponse.getJSONArray("turnResults");
        for (int i = 0; i < actionResults.length(); i++) {
            this.m_actionResults[i] = new ActionResult(actionResults.getJSONObject(i));
        }
    }
}
