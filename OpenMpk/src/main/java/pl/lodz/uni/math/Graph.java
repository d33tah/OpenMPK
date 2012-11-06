package pl.lodz.uni.math;

import java.util.List;
import java.util.Map;

/**
 * Klasa reprezentujaca graf
 * @author pt12ol
 *
 */
public class Graph {
	private Map<Stop, List<Connection>> stops;
	
	public Map<Stop, List<Connection>> getStops() {
		return stops;
	}

	public void setStops(Map<Stop, List<Connection>> stops) {
		this.stops = stops;
	}
	
	public void addStop(Stop stop) {
		stops.put(stop, null);
	}
}
