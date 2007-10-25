module nn.testing;

import std.math;
import std.stdio;

import algo.nnindex;
import dataset.features;
import util.resultset;
import util.timer;
import util.logger;
import util.profiler;
import output.console;
import output.report;


const float SEARCH_EPS = 0.10;

template search(bool withOutput) {
float search(int checks, out float time) 
{
	int correct = 0;
	time = profile( {
	for (int i = 0; i < testData.count; i++) {
		resultSet.init(testData.vecs[i]);
		index.findNeighbors(resultSet,testData.vecs[i], checks);			
		int nn_index = resultSet.getPointIndex(0+skipMatches);
		
		if (nn_index == testData.match[i]) {
			correct++;
		}
	}
	});
	
	float performance = 100*cast(float)correct/testData.count;
	
	static if (withOutput) {
		Logger.log(Logger.INFO,"  %5d     %6.2f      %6.2f      %6.3f\n",
				checks, performance,
				time, 1000.0 * time / testData.count);
		Logger.log(Logger.SIMPLE,"%d %f %f %f\n",
				checks, correct * 100.0 / cast(float) testData.count,
				time, 1000.0 * time / testData.count);
	}
	
	return performance;
}
}



void testNNIndex(bool withOutput)(NNIndex index, Features!(float) testData, int nn, int checks, uint skipMatches)
{
	
	static if (withOutput)
		Logger.log(Logger.INFO,"Searching... \n");
	
	ResultSet resultSet = new ResultSet(nn+skipMatches);
	
	mixin search!(false);
	
	float time;
	float precision = search(checks,time);

	static if (withOutput) {
		Logger.log(Logger.INFO,"  Nodes    %% correct    Time     Time/vector\n"
				" checked   neighbors   (seconds)      (ms)\n"
				" -------   ---------   ---------  -----------\n");
		Logger.log(Logger.INFO,"  %5d     %6.2f      %6.2f      %6.3f\n",
				checks, precision,
				time, 1000.0 * time / testData.count);
		Logger.log(Logger.SIMPLE,"%d %f %f %f\n",
				checks, precision,
				time, 1000.0 * time / testData.count);
	}

}


void testNNIndexPrecision(bool withOutput, bool withReporting)(NNIndex index, Features!(float) testData, int nn, float precision, uint skipMatches)
{	
	static if (withOutput) {
		Logger.log(Logger.INFO,"Searching... \n");
		Logger.log(Logger.INFO,"  Nodes    %% correct    Time     Time/vector\n"
				" checked   neighbors   (seconds)      (ms)\n"
				" -------   ---------   ---------  -----------\n");
	}
	ResultSet resultSet = new ResultSet(nn+skipMatches);
	
	mixin search!(true);

	int c2 = 1;
	float p2;
	
	int c1;
	float p1;
	
	float time;
	
	
	p2 = search(c2,time);
	while (p2<precision) {
		c1 = c2;
		p1 = p2;
		c2 *=2;
		p2 = search(c2,time);
	}
	
	int cx;
	float realPrecision;
	if (abs(p2-precision)>SEARCH_EPS) {
		writefln("Start linear estimation");
		// after we got to values in the vecibity of the desired precision
		// use linear approximation get a better estimation
			
		cx = lround(c1+(precision-p1)*(c2-c1)/(p2-p1));
		realPrecision = search(cx,time);
		while (abs(realPrecision-precision)>SEARCH_EPS) {
			if (p2!=realPrecision) {
				c1 = c2; p1 = p2;
			}
			c2 = cx; p2 = realPrecision;
			cx = lround(c1+(precision-p1)*(c2-c1)/(p2-p1));
			if (c2==cx) {
				cx += precision>realPrecision?1:-1;
			}
			if (cx==c1) {
				writefln("Got as close as I can");
				break;
			}
			realPrecision = search(cx,time);
		}
		
	} else {
		writefln("No need for linear estimation");
		cx = c2;
		realPrecision = p2;
	}
}

float testNNIndexExactPrecision(bool withOutput, bool withReporting)(NNIndex index, Features!(float) testData, int nn, 
												float precision, uint skipMatches)
{
	static if (withOutput) {
		Logger.log(Logger.INFO,"Searching... \n");
		Logger.log(Logger.INFO,"  Nodes    %% correct    Time     Time/vector\n"
				" checked   neighbors   (seconds)      (ms)\n"
				" -------   ---------   ---------  -----------\n");
 	}

	ResultSet resultSet = new ResultSet(nn+skipMatches);
	
	mixin search!(true);

	int estimate(int[] checks, float[] precision, int count, float desiredPrecision) {
		
		float[2][2] A;
		float[2] b;
		
		b[] = 0;
		A[0][] = 0;
		A[1][] = 0;
		
		for (int i=0;i<count;++i) {
			float c = log(checks[i]);
			float p = 100 - precision[i];
			A[1][1] += c*c;
			A[0][1] -= c;
			b[0] += c*p;
			b[1] += p;
		}
		A[1][0] = A[0][1];
		A[0][0] = count;
		
		float d = A[0][0]*A[1][1]-A[0][1]*A[1][0];
		
		float x[2];
		x[0] = (A[0][0]*b[0]+A[0][1]*b[1])/d;
		x[1] = (A[1][0]*b[0]+A[1][1]*b[1])/d;
		
		float cx = exp((100-desiredPrecision-x[1])/x[0]);
		
		return lround(cx);
	}

	
	const int MAX_CHECKS = 20;
	const float VECINITY_INTERVAL = 2;
	float SLOPE_EPS = tan(5*PI/180);
	
	int[MAX_CHECKS] c;
	float[MAX_CHECKS] p;	
	float time;
	int count;
	
	// get two samples of numbet_of_checks-precision dependencies
	count = 0;
	c[count] = 1;	
	p[count] = search(c[count],time);
	count++;
	
	c[count] = 5;	
	p[count] = search(c[count],time);
	count++;
	
	c[count] = 	estimate(c,p,count, 60);
	p[count] = search(c[count],time);
	count++;
	
	c[count] = 	estimate(c,p,count, 70);
	p[count] = search(c[count],time);
	count++;
	
	c[count] = 	estimate(c,p,count, 80);
	p[count] = search(c[count],time);
	count++;
	
	c[count] = 	estimate(c,p,count, precision);
	p[count] = search(c[count],time);
	count++;
	
	// use least square to estimate checks no. to obtain something close to
	// desired precision
	
	float m1 = (p[count-2]-p[count-3])/(c[count-2]-c[count-3]);
	float m2 = (p[count-1]-p[count-2])/(c[count-1]-c[count-2]);	
	float alpha = abs((m1-m2)/(1+m1*m2));
 	static if (withOutput) writefln("m1=%g, m2=%g, alpha = %g",m1,m2,alpha);	
	
	while (alpha>SLOPE_EPS && abs(p[count-1]-precision)>SEARCH_EPS) {
		c[count] = estimate(c,p,count, precision);
		p[count] = search(c[count],time);
		if (abs(p[count]-p[count-1])<0.001) {
			break;
		}
		count++;
		m1 = m2;
		m2 = (p[count-1]-p[count-2])/(c[count-1]-c[count-2]);
		alpha = abs((m1-m2)/(1+m1*m2));
	 	static if (withOutput) writefln("m1=%g, m2=%g, alpha = %g",m1,m2,alpha);	
	}
	
	int cx;
	float realPrecision;
	if (abs(p[count-1]-precision)>SEARCH_EPS) {
		static if (withOutput) writefln("Start linear estimation");
		// after we got to values in the vecibity of the desired precision
		// use linear approximation get a better estimation
		int c1 = c[count-2], c2 = c[count-1];
		float p1 = p[count-2], p2 = p[count - 1];
			
		cx = lround(c1+(precision-p1)*(c2-c1)/(p2-p1));
		realPrecision = search(cx,time);
		while (abs(realPrecision-precision)>SEARCH_EPS) {
			if (p2!=realPrecision) {
				c1 = c2; p1 = p2;
			}
			c2 = cx; p2 = realPrecision;
			cx = lround(c1+(precision-p1)*(c2-c1)/(p2-p1));
			if (c2==cx) {
				cx += precision>realPrecision?1:-1;
			}
			if (cx==c1) {
				static if (withOutput) writefln("Got as close as I can");
				break;
			}
			realPrecision = search(cx,time);
		}
		
	} else {
		static if (withOutput) writefln("No need for linear estimation");
		cx = c[count-1];
		realPrecision = p[count-1];
	}
	
	static if (withReporting) {
		reportedValues["checks"] = cx;
		reportedValues["match"] = cast(double)realPrecision;
		reportedValues["search_time"] = cast(double)time;
		flush_reporters();
	}

	static if (withOutput) {
		Logger.log(Logger.SIMPLE,"  %5d     %6.2f      %6.2f      %6.3f\n",
					cx, realPrecision,
					time, 1000.0 * time / testData.count);
	}

	return time;
}
