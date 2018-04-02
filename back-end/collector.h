#ifndef COLLECTOR_H
#define COLLECTOR_H
#define COUNT_MAX 20
#define ENCRYPT_MAX 20
#define ADDR_MAX 20

class Collector{
private:
	char address[ADDR_MAX];
	int state; 
		// 0: idle state
		// 1: family loggin
		// 2: collector loggin
		// 3: repair max loggin
	int space; 
		// since our simulation is only on software
		// the space is defined by the number of garbage
		// actually, it can be implemented by 
	int used_space;
	float threshlod; // range from 0 to 1
public:
	// the consruction
	Collector(); 
	// connect to the database to validate the log-in information
	void logIn(char usrName[COUNT_MAX], char password[ENCRYPT_MAX]);
	// generate QT (the throwing behaviour in the family view) (only family)
	void QTgenerate(int type);
	// go idle after certain time after the last reaction
	void goIdle(void);
	// call the corresponding car to collect when reach threshold
	void callCar(int type);
	// change the space (only repair man)
	void spaceSet(int type, int newSpace);
	// change the threshold (only repair man)
	void thresholdSet(float newThreshold);
	// collect the garbage (only collector)
	void collectGarbage(int type)
}

#endif