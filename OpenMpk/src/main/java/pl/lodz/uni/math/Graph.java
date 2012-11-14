package pl.lodz.uni.math;

import java.util.LinkedList;
import java.util.HashMap;
import java.util.Map;

public class Graph {
	private HashMap<Stop, LinkedList<Connection>> stops;
	private Map<String,Stop> stopsMap;
	
	public HashMap<Stop, LinkedList<Connection>> getStops() {
		return stops;
	}

	public Graph() {
		stops = new HashMap<Stop, LinkedList<Connection>>();
		stopsMap = new HashMap<String,Stop>();
	}


	public void addStop(String id, Stop stop) {
		stopsMap.put(id,stop);
	}

	public Stop getStop(String id) {
		return stopsMap.get(id);
	}

	public void addConnection(Stop stop, Connection connection) {
		if(!stops.containsKey(stop)) {
			LinkedList<Connection> list = new LinkedList<Connection>();
			list.addLast(connection);
			stops.put(stop,list);
		}
		else {
			LinkedList<Connection> list = stops.get(stop);
			list.addLast(connection);
			stops.put(stop,list);
		}
	}
}
