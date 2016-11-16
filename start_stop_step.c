#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv)
{
	int start = atoi(argv[1]);
	int stop = atoi(argv[2]);
	int step = atoi(argv[3]);
	printf("start %d, stop %d, step %d\n", start, stop, step);

	int i, j = 0;

	if (step > 0)
	{
	    	for (i = start; i < stop; i += step)
	    	{
	    		printf("%d ", i);
	    	}
		printf("\n");
	}
	else if(step < 0)
	{
	    	for (i = start; i > stop; i += step)
	    	{
	    		printf("%d ", i);
	    	}
		printf("\n");
		
	}
	else
	{
		printf("step value cannot be zero!\n");
	}
	return 0;
}
