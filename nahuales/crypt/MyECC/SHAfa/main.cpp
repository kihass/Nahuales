#include <cstdlib>
#include <iostream>
#include <stdio.h>

using namespace std;


int SHAfa(char *archivo)
{
	FILE *fpe;
	unsigned char text, suma[2]={0,0};
	if((fpe = fopen(archivo,"r"))==NULL) {
		printf("Error: no puedo abrir %s\n",archivo);
		exit(1);
	}
	while(1) {
		if(fread(&text,1,1,fpe)!=1)
			break;
		suma[0]+=text;
		if(fread(&text,1,1,fpe)!=1)
			break;
		suma[1]+=text;
	}
	fclose(fpe); 
	suma[0]*=suma[1];
	suma[1]*=suma[0];
	printf("%d %d\n",suma[1],suma[0]);
	printf("Kike\t%d %d\n", 256*suma[1], suma[0]);
		return(256*suma[1]+suma[0]);
}


int main(int argc, char *argv[])
{
    printf("%d",  SHAfa("Documento") );
//    cout << "\nPress the enter key to continue ...";
//    cin.get();
    return EXIT_SUCCESS;
}
