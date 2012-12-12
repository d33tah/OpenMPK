package pl.lodz.uni.math;

import java.io.*;
import java.util.LinkedList; //wybrana w skomplikowanym procesie losowania :P
import java.util.HashMap;

public class Main {

	public static void main(String[] args) {

		GraphLoader loader = new GraphLoader();
		Graph graph = loader.loadGraph();
		System.out.println("Program uruchomil sie poprawnie.");
		Algorithm algorithm=new Algorithm();
		algorithm.dijkstra(graph, "Strykowska");
		System.out.println(graph.getStop("Szczecińska").getLength());
	}
}
