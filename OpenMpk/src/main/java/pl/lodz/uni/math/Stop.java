package pl.lodz.uni.math;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

public class Stop{
	private String name;
	private String id;
	private String previous;
	public String getPrevious() {
		return previous;
	}

	public void setPrevious(String previous) {
		this.previous = previous;
	}

	public int getLength() {
		return length;
	}

	public void setLength(int length) {
		this.length = length;
	}

	private int length;
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

	public String getId() {
		return id;
	}

	public void setId(String id) {
		this.id = id;
	}

}
