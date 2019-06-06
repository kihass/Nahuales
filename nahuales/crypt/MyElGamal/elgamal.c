/*
 * elgamal.c
 * 
 * Copyright 2013 Carlos Rodriguez <carlos@carlos-N53SM>
 * 
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 * MA 02110-1301, USA.
 * 
 * 
 */


#include <stdio.h>
#include <math.h>

unsigned int potencia(int);

#define desborde 0x10000
#define mascara 0xffff
#define polprim 0x2841

int main(int argc, char **argv)
{
	unsigned int respuesta = 0;
	int i = 1;
	/*do{
		respuesta = potencia(i++);
		printf("%d\n",respuesta);
	}while(respuesta!=1);
	printf("\n i:%d",i);*/
	printf("\n%d",potencia(12345));
	printf("\n%d",potencia(51585)); 
	printf("\n%d",potencia(48603));
	printf("\n%d",potencia(34653));
	return 0;
}

unsigned int potencia(int pot){
	unsigned int res = 1;
	int i = 0;
	for(i=0;i<pot;i++){
		res = res<<1;
		if((res & desborde) == desborde){
			res = ((res&mascara)^polprim);
		}
	}
	return res;
}
