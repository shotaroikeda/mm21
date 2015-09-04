package com.mm21;

import org.json.JSONArray;
import org.json.JSONObject;

/**
 * Represents the results of a game turn
 * @competitors You may modify this file, but you shouldn't need to
 */
public class TurnResult {

    // Property values (private to prevent unintentional writing)
    private Node[] m_nodes;
    private String[] m_players;
    private ActionResult[] m_actionResults;

    // Property getters
    public Node[] nodes() { return m_nodes; }
    public String[] players() { return m_players; }
    public ActionResult[] actionResults() { return m_actionResults; }

    // Constructor
    public TurnResult(JSONObject serverResponse) {

        // Serialize map
        JSONArray mapNodes = serverResponse.getJSONArray("map");
        this.m_nodes = new Node[mapNodes.length()];
        for (int i = 0; i < mapNodes.length(); i++) {
            this.m_nodes[i] = new Node(mapNodes.getJSONObject(i));
        }

        // Initialize adjacent nodes
        for (int i = 0; i < mapNodes.length(); i++) {
            this.m_nodes[i].initAdjacentNodes(this.m_nodes, mapNodes.getJSONObject(i));
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

        // Initialize power source nodes
        for (int i = 0; i < actionResults.length(); i++) {
            this.m_actionResults[i].initPowerSourceNodes(this.m_nodes, actionResults.getJSONObject(i));
        }
    }
}
