package pl.lodz.uni.math;

import java.io.*;
import java.util.LinkedList; //wybrana w skomplikowanym procesie losowania :P
import java.util.HashMap;
/*
public class GraphLoader {

	Graph graph;

	private void loadStops()
	{

		try {
			FileInputStream fstream = new FileInputStream(
					"przetworzone/nazwy_przystankow.txt");
			DataInputStream in = new DataInputStream(fstream);
			BufferedReader br = new BufferedReader(
					new InputStreamReader(in));
			String strLine;

			while ((strLine = br.readLine()) != null) {
				String[] commaSeparated = strLine.split(",");
				Stop stop = new Stop();
				stop.setName(commaSeparated[1]);
				graph.addStop(commaSeparated[0],stop);
			}
			in.close();
			
		}
		catch (IOException e) {
			System.err.println("Error: " + e.getMessage());
		}

	}

	private void parseDirection(String lineName, int numerKierunku, 
			Line line) {
		try {
			FileInputStream fstream = new FileInputStream(
					"przetworzone/lista_przystankow/"+
					lineName+"/"+
					Integer.toString(numerKierunku)+
					".csv");

			DataInputStream in = new DataInputStream(fstream);
			BufferedReader br = new BufferedReader(
					new InputStreamReader(in));
			String strLine;
			Stop stop = null;
			while ((strLine = br.readLine()) != null) {
				if(stop!=null) {
					Connection conn = new Connection();
					conn.setFrom(stop);
					conn.setTo(graph.getStop(strLine));
					conn.setLine(line);
					conn.setTime(1);
					graph.addConnection(stop,conn);

				}
				stop = graph.getStop(strLine);
			}
			in.close();

		}

		catch (IOException e) {
			System.err.println("Error: " + e.getMessage());
		}
	}

	private void parseLine(String lineName) {

		Line line = new Line();
		line.setName(lineName); 

		try {
			FileInputStream fstream = new FileInputStream(
					"przetworzone/lista_przystankow/"+
					lineName+"/il_kier.csv");

			DataInputStream in = new DataInputStream(fstream);
			BufferedReader br = new BufferedReader(
					new InputStreamReader(in));
			String strLine;

			while ((strLine = br.readLine()) != null) {
				for(int i=0; i<Integer.parseInt(strLine); i++)
				{
				parseDirection(lineName,i,line);
				}
			}
			in.close();

		}

		catch (IOException e) {
			System.err.println("Error: " + e.getMessage());
		}
	}

	private void loadLines() {
		try {
			FileInputStream fstream = new FileInputStream(
					"przetworzone/lista_linii.txt");
			DataInputStream in = new DataInputStream(fstream);
			BufferedReader br = new BufferedReader(
					new InputStreamReader(in));
			String strLine;

			while ((strLine = br.readLine()) != null) {
				System.out.println("Parsing: " + strLine);
				parseLine(strLine);
			}
			in.close();

		}

		catch (IOException e) {
			System.err.println("Error: " + e.getMessage());
		}

	}

	public Graph loadGraph() {
		graph = new Graph();
		loadStops();
		loadLines();
		return graph;
	}
}
*/