package pl.lodz.uni.math;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.PriorityQueue;

public class Algorithm {
	private static final int INF = 999999999;

	public static void main(String[] args) {
		Graph graf = new Graph();
		Stop a = new Stop("A");
		Stop b = new Stop("B");
		Stop c = new Stop("C");
		a.setId("A");
		b.setId("B");
		c.setId("C");
		a.addConnection(new Connection(b));
		b.addConnection(new Connection(c));
		a.addConnection(new Connection(c));

		graf.addStop("A", new Stop("A"));
		graf.addStop("B", new Stop("B"));
		graf.addStop("C", new Stop("C"));
		Map<String, Integer> odlegloscTab = new HashMap<String, Integer>();
		Map<String, String> poprzednikTab = new HashMap<String, String>();
		Comparable<Stop> comm = new Comparable<Stop>() {
			public static Map<String,Integer> odlegloscTab;

			public int compareTo(Stop o)
			{
				odlegloscTab.size(); //zeby sprawdzic zasieg
				return 0;
			}
		};
		}
	
		
		PriorityQueue<Stop> kolejkaPrzystankow = new PriorityQueue<Stop>(10, comm);
		/*
		 * Dijkstra(G,w,s): dla ka¿dego wierzcho³ka v w V[G] wykonaj d[v] :=
		 * nieskoñczonoœæ poprzednik[v] := niezdefiniowane d[s] := 0 Q := V
		 * dopóki Q niepuste wykonaj u := Zdejmij_Min(Q) dla ka¿dego wierzcho³ka
		 * v – s¹siada u wykonaj je¿eli d[v] > d[u] + w(u, v) to d[v] := d[u] +
		 * w(u, v) poprzednik[v] := u Dodaj(Q, v)
		 * 
		 * cout <<"Droga wynosi: "<<d[v];
		 */
		for (Entry<String, Stop> przystanek : graf.getStopsMap().entrySet()) {
//			odlegloscTab.put(przystanek.getKey(), INF);
//			poprzednikTab.put(przystanek.getKey(), "");
			przystanek.getValue().setLength(-1);
			przystanek.getValue().setPrevious("");
		}
//		odlegloscTab.put(a.getId(), 0);
		graf.getStopsMap().get(a.getId()).setLength(0);
		new PriorityQueue<Stop>();

	}
}
