package pl.lodz.uni.math;

import static org.junit.Assert.*;

import org.junit.Before;
import org.junit.Test;

public class AlgorithmCase {

	@Before
	public void setUp() throws Exception {
	}

	@Test
	public void test() {
		Algorithm algorithm=new Algorithm();
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

		algorithm.dijkstra(graf, "A");
		assertEquals(0, graf.getStop("A").getLength());
		assertEquals(2, graf.getStop("B").getLength());
		assertEquals(5, graf.getStop("C").getLength());
		assertEquals("A", graf.getStop("B").getPrevious().getName());
		assertEquals("B", graf.getStop("C").getPrevious().getName());
		
		
	}

}
