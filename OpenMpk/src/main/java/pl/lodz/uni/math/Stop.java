package pl.lodz.uni.math;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

public class Stop{
	@Override
	public String toString() {
		return "Stop [name=" + name + ", id=" + id + ", previous=" + (null== previous ? "null" : previous.name) + ", length=" + length + "]";
	}
	

	private String name;
	/*@Override
	public String toString() {
		StringBuilder builder = new StringBuilder();
		builder.append("Stop [name=");
		builder.append(name);
		builder.append(", id=");
		builder.append(id);
		builder.append(", previous=");
		builder.append(null== previous ? "null" : previous.name);
		builder.append(", length=");
		builder.append(length);
		builder.append("]");
		return builder.toString();
	}*/

	private String id;
	private Stop previous;
	private int length;
	private List<Connection> connections;
	
	public Stop getPrevious() {
		return previous;
	}

	public void setPrevious(Stop previous) {
		this.previous = previous;
	}

	@Override
	public int hashCode() {
		final int prime = 31;
		int result = 1;
		result = prime * result + ((id == null) ? 0 : id.hashCode());
		result = prime * result + ((name == null) ? 0 : name.hashCode());
		return result;
	}

	@Override
	public boolean equals(Object obj) {
		System.out.println("equals()");
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if (getClass() != obj.getClass())
			return false;
		Stop other = (Stop) obj;
		if (id == null) {
			if (other.id != null)
				return false;
		} else if (!id.equals(other.id))
			return false;
		if (name == null) {
			if (other.name != null)
				return false;
		} else if (!name.equals(other.name))
			return false;
		return true;
	}

	/**
	 * 
	 * @return Odleglosc od poczatku mierzona w czasie
	 */
	public int getLength() {
		return length;
	}

	/**
	 * 
	 * @param length Odleglosc od poczatku mierzona w czasie
	 */
	public void setLength(int length) {
		this.length = length;
	}


	public List<Connection> getConnections() {
		return connections;
	}

	public void setConnections(List<Connection> connections) {
		this.connections = connections;
	}

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
//		System.out.println("dodaje polaczenie dla przystanku "+name+", laczacy z "+connection.getTo().name);
//		System.out.println("connections "+connections);
//		System.out.println("connections.containt "+connections.contains(connection));
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
