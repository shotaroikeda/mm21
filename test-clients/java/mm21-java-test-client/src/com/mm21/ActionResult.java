package com.mm21;

import org.json.JSONArray;
import org.json.JSONObject;

/**
 * Represents the results of a player's action
 * @competitors You may modify this file, but you shouldn't need to
 */
public class ActionResult extends Action {

    // Property values (private to prevent unintentional writing)
    private boolean m_succeeded;
    private String m_status;
    private String m_message = "";

    // Property getters
    public boolean succeeded() { return m_succeeded; }
    public String status() { return m_status; }
    public String message() { return m_message; }

    // Constructor
    public ActionResult(JSONObject o) {

        // ActionResult properties
        this.m_status = o.getString("status");
        this.m_succeeded = m_status == "ok";
        this.m_message = o.getString("message");

        // Simple Action properties
        this.actionType = ActionType.valueOf(o.getString("action"));
        this.targetId = o.getInt("targetId");
        if (o.has("multiplier")) { this.multiplier = o.optInt("multiplier"); }

        // Complex Action property #1 (Power sources)
        JSONArray powerIds = o.getJSONArray("powerSources");
        this.supplierIds = new int[powerIds.length()];
        for (int i = 0; i < powerIds.length(); i++) {
            this.supplierIds[i] = powerIds.getInt(i);
        }
    }
}
