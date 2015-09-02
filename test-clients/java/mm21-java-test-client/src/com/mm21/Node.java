package com.mm21;

import org.json.JSONArray;
import org.json.JSONObject;
import java.util.Iterator;
/**
 * Represents a node in the game
 * @competitors You may modify this file, but you shouldn't need to.
 */
public class Node {

    // Enum
    public class NodeType {
        public static final int SMALL_CITY = 0;
        public static final int MEDIUM_CITY = 1;
        public static final int LARGE_CITY = 2;
        public static final int ISP = 3;
        public static final int DATACENTER = 5;
    }

    // Property values (private to prevent unintentional writing)
    private int m_id;
    private int m_ownerId;
    private int m_processing;
    private int m_networking;
    private int m_upgradeLevel;
    private boolean m_isDDoSed;
    private boolean m_isIPSed;
    private int[] m_infiltration;
    private int[] m_rootkitIds;
    private NodeType m_nodeType;

    // Property getters
    public int id() { return m_id; }
    public int ownerId() { return m_ownerId; }
    public int processing() { return m_processing; }
    public int networking() { return m_networking; }
    public int upgradeLevel() { return m_upgradeLevel; }
    public boolean isDDoSed() { return m_isDDoSed; }
    public boolean isIPSed() { return m_isIPSed; }
    public int[] infiltration() { return m_infiltration; }
    public int[] rootkitIds() { return m_rootkitIds; }
    public NodeType nodeType() { return m_nodeType; }

    // Helper methods
    public int totalPower() {
        return m_networking + m_processing;
    }

    // Constructor
    public Node(JSONObject o) {

        // Simple properties
        this.m_id = o.getInt("id");
        this.m_ownerId = o.getInt("ownerId");
        this.m_processing = o.getInt("processingPower");
        this.m_networking = o.getInt("networkingPower");
        this.m_upgradeLevel = o.getInt("upgradeLevel");
        this.m_isDDoSed = o.getBoolean("isDDoSed");
        this.m_isIPSed = o.getBoolean("isIPSed");
        this.m_nodeType = (NodeType) o.get("nodetype");

        // Complex property #1 (Infiltration)
        JSONObject iObj = o.getJSONObject("infiltration");
        Iterator<String> iKeys = iObj.keys();
        m_infiltration = new int[iObj.length()];
        while (iKeys.hasNext()) {
            String iKey = iKeys.next();
            m_infiltration[Integer.parseInt(iKey)] = iObj.getInt(iKey);
        }

        // Complex property #2 (Rootkit IDs)
        JSONArray rArr = o.getJSONArray("rootkitIds");
        m_rootkitIds = new int[rArr.length()];
        for (int i = 0; i < rArr.length(); i++) {
            m_rootkitIds[i] = rArr.getInt(i);
        }
    }
}