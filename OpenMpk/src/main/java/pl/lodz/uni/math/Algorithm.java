package pl.lodz.uni.math;

import java.util.Comparator;
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
		a.addConnection(new Connection(b, 2));
		b.addConnection(new Connection(c, 3));
		a.addConnection(new Connection(c, 7));

		graf.addStop("A", a);
		graf.addStop("B", b);
		graf.addStop("C", c);
		// final Map<String, Integer> odlegloscTab = new HashMap<String,
		// Integer>();
		// Map<String, String> poprzednikTab = new HashMap<String, String>();

		dijkstra(graf, "A");

	}

	public static void dijkstra(Graph graf, String startingPoint) {
		Comparator<Stop> comm = new Comparator<Stop>() {

			public int compare(Stop o1, Stop o2) {
				if (o1.getLength() <= o2.getLength()) {
					return -1;
				} else {
					return 1;
				}

			}
		};

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
			// odlegloscTab.put(przystanek.getKey(), INF);
			// poprzednikTab.put(przystanek.getKey(), "");
			przystanek.getValue().setLength(INF);
			przystanek.getValue().setPrevious(null);
		}
		graf.getStop(startingPoint).setLength(0);
		// odlegloscTab.put(a.getId(), 0);
		// graf.getStopsMap().get(a.getId()).setLength(0);
		// new PriorityQueue<Stop>();
		for (Stop stop : graf.getStopsMap().values()) {
//			stop.setLength(-1);
			kolejkaPrzystankow.add(stop);
		}
		System.out.println(kolejkaPrzystankow);
		Stop temp;
		while (!kolejkaPrzystankow.isEmpty()) {
			temp = kolejkaPrzystankow.poll();
			System.out.println("zdjalem "+temp.getId());
			for (Connection connection : temp.getConnections()) {
				System.out.println("odwiedzam "+connection.getTo().getId());
				if (connection.getTo().getLength() > temp.getLength() + connection.getTime(null)) {
					connection.getTo().setLength(temp.getLength() + connection.getTime(null));
					connection.getTo().setPrevious(temp);
					kolejkaPrzystankow.add(connection.getTo());
				}
			}

		}

		for (Stop stop : graf.getStopsMap().values()) {
			System.out.println("Odleg³oœæ: " + stop.getLength() + " Nazwa: " + stop.getId() + (stop.getPrevious() == null ? "" : " poprzednik: " + stop.getPrevious().getId()));
		}
	}
}
