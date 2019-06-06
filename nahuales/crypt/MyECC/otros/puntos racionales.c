#include <cstdlib>
#include <stdio.h>
#include <conio.h>

struct pareja
{
	int x;
	int y;     
};

struct pareja parejas[100000];

int main ()
{
	for(int k=0; k<100000; k++)
	{
		parejas[k].x=0;
		parejas[k].y=0;
	}
	
	parejas[0].x=-1;
	parejas[0].y=-1;
	
	int c_parejas=1;
	
	//int a=0;
	int a=1;
	int b=1;
	int z;
	
	//    int Zp=5;
	int Zp=10007;
	
	int x,y;
	for(x=0; x< Zp; x++)
	{
		//z = ((x*x*x) + (a*x) + b)%Zp;
		z = ((  (   ((x*x)%Zp) *x)%Zp) + ((a*x)%Zp) + b)%Zp;
		for(y=0; y< Zp; y++)
		{
			int y2 = (y*y);
			int y2_modulo = y2 % Zp;
			
			if(  y2_modulo == z )
			{
			//printf("(%d, %d)\n", x,y);     
			parejas[c_parejas].x=x;
			parejas[c_parejas].y=y;
			
			c_parejas++;
			}
			
		}
//		printf("f_x: %d\n", x);
	}

	struct pareja Punto;
	Punto.x = 7;
	Punto.y = 5300;
	
	for(int j=0; ; j++)
	{
		if(parejas[j].y == 0 && parejas[j].x == 0)
		break;
		
		//if(parejas[j].x == 7)                
		//{
		printf("%d\t",j+1);
		printf("(%d, %d)\n",parejas[j].x,parejas[j].y); 
		
		//struct pareja suma_eliptica( Punto , parejas[j]);
		//}
	}
	
	
	getch();
	return 0;
}