package pl.lodz.uni.math;

import java.util.LinkedList;
import java.util.HashMap;
import java.util.Map;

public class Graph {
	// private HashMap<Stop, LinkedList<Connection>> stops;
	private Map<String, Stop> stopsMap;

	/*
	 * public HashMap<Stop, LinkedList<Connection>> getStops() { return stops; }
	 */

	public Graph() {
		stopsMap = new HashMap<String, Stop>();
	}

	public void addStop(String id, Stop stop) {
		stopsMap.put(id, stop);
	}

	public Stop getStop(String id) {
		Stop ret = stopsMap.get(id);
		if(ret==null)
		{
			System.out.println("Nie znaleziono dla: "+id);
			return new Stop("(NIEZNANY)");
		}
			
		return ret;
	}

	public Map<String, Stop> getStopsMap() {
		return stopsMap;
	}

	public void setStopsMap(Map<String, Stop> stopsMap) {
		this.stopsMap = stopsMap;
	}

}
