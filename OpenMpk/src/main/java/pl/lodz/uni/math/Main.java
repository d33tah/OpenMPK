package pl.lodz.uni.math;

import java.io.*;
import java.util.LinkedList; //wybrana w skomplikowanym procesie losowania :P
import java.util.HashMap;
import java.util.Map.Entry;

public class Main {

	public static void main(String[] args) {

		System.out.println(new File(".").getAbsolutePath()); 
		GraphLoader loader = new GraphLoader();
		Graph graph = loader.loadGraph();
		System.out.println("Program uruchomil sie poprawnie.");
		/*for (String stop : graph.getStopsMap().keySet()) {
			System.out.println(stop);
		}*/
		
		
//		Stop stryko = graph.getStop("0364");
//		System.out.println(stryko.getConnections());
		
		Algorithm algorithm=new Algorithm();
		algorithm.dijkstra(graph, "0954");
//		System.out.println(graph.getStop("1501").getLength());
		System.out.println("\n\n\nWYNIKI");
		
		Stop stop = graph.getStop("1501");
		while(stop.getPrevious()!=null) {
			System.out.println(stop.getName());
			stop = stop.getPrevious();
		}
	}
}
