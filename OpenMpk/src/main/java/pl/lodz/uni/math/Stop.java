package pl.lodz.uni.math;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

public class Stop {
	private String name;

	private List<Connection> connections;

	public Stop(String name) {
		this();
		this.name = name;
	}

	public Stop() {
		connections = new ArrayList<Connection>();
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public void addConnection(Connection connection) {
		if (!connections.contains(connection)) {
			connections.add(connection);
		}

	}
}
