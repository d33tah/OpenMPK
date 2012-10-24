package pl.lodz.uni.math;

import java.util.LinkedList; //wybrana w skomplikowanym procesie losowania :P

public class Main {
	public static void main(String[] args) {

		Graph graph = new Graph();

		Stop s1 = new Stop();
		s1.setName("Legionów - Włókniarzy");

		Stop s2 = new Stop(); 
		s2.setName("Zielona - 1 Maja");

		Line line = new Line();
		line.setName("13");
		
		Connection c1 = new Connection();
		c1.setFrom(s1);
		c1.setTo(s2);
		c1.setLine(line);
		c1.setTime(2);

		LinkedList<Connection> l1 = new LinkedList<Connection>();
		l1.addLast(c1);

		Connection c2 = new Connection();
		c1.setFrom(s2);
		c1.setTo(s1);
		c1.setLine(line);
		c1.setTime(2);

		LinkedList<Connection> l2 = new LinkedList<Connection>();
		l2.addLast(c2);

		graph.addStop(s1,l1);
		graph.addStop(s2,l2);

		System.out.print("Program uruchomił się poprawnie.");

	}
}
