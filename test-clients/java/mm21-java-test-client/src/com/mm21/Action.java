package com.mm21;

import org.json.JSONArray;
import org.json.JSONObject;

/**
 * Represents a single turn of the game
 * @competitors You may modify this file, but you shouldn't need to
 */
public class Action {

    // Action types
    public enum ActionType { CLEAN, CONTROL, DDOS, IPS, PORTSCAN, ROOTKIT, SCAN, UPGRADE }

    // Property values (feel free to write to these, unless it's an ActionResult)
    public ActionType actionType;
    public int multiplier = 1;
    public int[] supplierIds = null;
    public int targetId;

    // Convert to JSON object
    public JSONObject toJSONObject() {

        JSONObject o = new JSONObject();

        // Simple properties
        o.put("action", this.actionType.toString());
        o.put("multiplier", this.multiplier);
        o.put("targetId", this.targetId);

        // Complex property #1 (Supplier IDs)
        JSONArray powerIds = new JSONArray();
        if (this.supplierIds != null) {
            for (int i = 0; i < this.supplierIds.length; i++) {
                powerIds.put(this.supplierIds[i]);
            }
        }
        o.put("supplierIds", supplierIds);

        // Done!
        return o;
    }
}
