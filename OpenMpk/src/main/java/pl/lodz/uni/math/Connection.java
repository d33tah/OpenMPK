package pl.lodz.uni.math;

import java.util.Date;

public class Connection {
	// private Stop from;
	private Stop to;
	private int time;
	private Line line;

	/*
	 * Znamy przystanek poczatkowy public Connection(Stop from, Stop to) {
	 * 
	 * }
	 * 
	 * public Stop getFrom() { return from; }
	 * 
	 * public void setFrom(Stop from) { this.from = from; }
	 */
	public Connection(Stop to, int time) {
		this.to = to;
		this.time=time;
	}

	public Stop getTo() {
		return to;
	}

	public void setTo(Stop to) {
		this.to = to;
	}

	public int getTime(Date givenTime) {
		return time;
	}

	public void setTime(int time) {
		this.time = time;
	}

	public Line getLine() {
		return line;
	}

	public void setLine(Line line) {
		this.line = line;
	}

	@Override
	public String toString() {
		StringBuilder builder = new StringBuilder();
		builder.append("Connection [to=");
		builder.append(to);
		builder.append(", time=");
		builder.append(time);
		builder.append(", line=");
		builder.append(line);
		builder.append("]");
		return builder.toString();
	}
	
}
