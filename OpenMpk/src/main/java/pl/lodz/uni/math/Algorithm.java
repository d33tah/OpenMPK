package pl.lodz.uni.math;

public class Algorithm {
	public static void main(String[] args) {
		Graph graf = new Graph();
		Stop A = new Stop("A");
		graf.addStop("A", new Stop("A"));
		graf.addStop("B", new Stop("B"));
		graf.addStop("C", new Stop("C"));

	}
}
