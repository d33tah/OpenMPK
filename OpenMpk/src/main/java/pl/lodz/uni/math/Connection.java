package pl.lodz.uni.math;

import java.util.Date;

public class Connection {
	private Stop from;
	private Stop to;
	private long time;	
	private Line line;
	
	public Stop getFrom() {
		return from;
	}
	public void setFrom(Stop from) {
		this.from = from;
	}
	public Stop getTo() {
		return to;
	}
	public void setTo(Stop to) {
		this.to = to;
	}
	public long getTime(Date givenTime) {
		return time;
	}
	public void setTime(long time) {
		this.time = time;
	}
	public Line getLine()
	{
		return line;
	}
	public void setLine(Line line)
	{
		this.line = line;
	}
}
