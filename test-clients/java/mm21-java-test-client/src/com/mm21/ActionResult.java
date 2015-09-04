package com.mm21;

import org.json.JSONArray;
import org.json.JSONObject;

import java.util.ArrayList;

/**
 * Represents the results of a player's action
 * @competitors You may modify this file, but you shouldn't need to
 */
public class ActionResult {

    // Property values (private to prevent unintentional writing)
    private int m_id = -1;
    private boolean m_succeeded;
    private String m_status;
    private String m_message = "";
    private ArrayList<Node> m_powerSourceNodes;
    private Action m_action;

    // Property getters
    public int id() { return m_id; }
    public boolean succeeded() { return m_succeeded; }
    public String status() { return m_status; }
    public String message() { return m_message; }
    public ArrayList<Node> powerSourceNodes() { return m_powerSourceNodes; }
    public Action action() { return m_action; }

    // Constructor
    public ActionResult(JSONObject o) {

        // ActionResult properties
        this.m_status = o.getString("status");
        this.m_succeeded = m_status == "ok";
        this.m_message = o.getString("message");

        // Simple Action properties
        this.m_action = new Action(
                Action.ActionType.valueOf(o.getString("action")),
                o.getInt("targetId"),
                1);
        if (o.has("multiplier")) { this.m_action.multiplier = o.getInt("multiplier"); }
    }

    // Delayed property initializers - must not be used until all nodes have been parsed
    public void initPowerSourceNodes(Node[] map, JSONObject o) {
        m_powerSourceNodes = new ArrayList<Node>();
        JSONArray psIds = o.getJSONArray("powerSources");
        for (int i = 0; i < psIds.length(); i++) {
            m_powerSourceNodes.add(map[psIds.getInt(i)]);
        }
    }
}
