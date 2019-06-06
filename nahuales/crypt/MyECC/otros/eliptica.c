/*
 * eliptica.c
 * 
 * Copyright 2013 Carlos Rodriguez <carlitos.oliva@gmail.com>
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

typedef int uint16_t;
typedef int bool;
#define TRUE  1
#define FALSE 0
#define PRM 10007

int num_pr = 0;

struct puntoRacional{
	uint16_t pX;
	uint16_t pY;
};

bool ecuacion_cubica(uint16_t, uint16_t);
void mostrar_puntos_racionales(void);
void calcular_sumas(uint16_t, uint16_t, uint16_t);
struct puntoRacional suma(uint16_t, uint16_t, uint16_t, uint16_t);
uint16_t inversoMul(uint16_t);
uint16_t inversoAdd(uint16_t);
uint16_t raiz(uint16_t);

uint16_t puntoX[PRM*PRM];
uint16_t puntoY[PRM*PRM];

int main(int argc, char **argv)
{
	int i = 0;
	int j = 0;
	int k = 1;
	puntoX[0] = -1;
	puntoY[0] = -1;
	for(i = 0;i<PRM;i++){
		for(j=0;j<PRM;j++){
			if(ecuacion_cubica(i,j)){
				puntoX[k] = i;
				puntoY[k] = j;
				k++;
			}
		}
	}
	num_pr = k;
	calcular_sumas(7, 5300, 12345%10065);
	calcular_sumas(7, 5300, 12345);
	//mostrar_puntos_racionales();
	return 0;
}

bool ecuacion_cubica(uint16_t x, uint16_t y){
	
	uint16_t resY = 0;
	uint16_t resX = 0;
	
	//Para y
	resY = (y*y)%PRM;
	
	//Para x
	resX = (x*x)%PRM;
	resX = (resX*x)%PRM;
	resX = (resX + x)%PRM;
	resX = (resX + 1)%PRM;
	
	if(resY == resX)
		return TRUE;
	return FALSE;
}

void mostrar_puntos_racionales(){
	int i = 0;
	for(i=0; i<num_pr;i++){
		printf("(%u,%u)\n",(unsigned int)puntoX[i], (unsigned int)puntoY[i]);
	}
}

void calcular_sumas(uint16_t puntox, uint16_t puntoy, uint16_t d){
	struct puntoRacional pr1;
	int i = 0;
	
	pr1.pX = -1;
	pr1.pY = -1;
	for(i = 0; i <= d; i++){
		pr1 = suma(pr1.pX, pr1.pY, puntox, puntoy);
	}
	printf("El resultado es:\nX:%d\nY:%d",pr1.pX, pr1.pY);
	if(ecuacion_cubica(pr1.pX, pr1.pY))
		printf("\nEl cual es un punto racional.");
	else
		printf("\nOh diablos!! No es un punto racional");
}

struct puntoRacional suma(uint16_t x0, uint16_t y0, uint16_t x1, uint16_t y1){
	int pend = 0;
	struct puntoRacional pR;
	pR.pX = 0;
	pR.pY = 0;
	int aux1 = 0;
	
	if(x0==x1 && y0==(PRM-y1)){
		pR.pX = -1;
		pR.pY = -1;
	}
	else if(x0==-1){
		pR.pX = x1;
		pR.pY = y1;
	}
	else if(x1==-1){
		pR.pX = x0;
		pR.pY = y0;
	}
	else if(x0==x1 && y0==y1){
		pend = ((3*x0*x0)%PRM+1)%PRM;
		pend = (pend * inversoMul((2*y0)%PRM))%PRM;
		pR.pX = (((pend*pend)%PRM) + inversoAdd((2*x0)%PRM))%PRM;
		//pR.pY = ((pend*pR.pX)%PRM + inversoAdd((x0*pend)%PRM)+y0)%PRM;
		aux1 = (pR.pX*pR.pX)%PRM;
		aux1 = (aux1*pR.pX)%PRM;
		pR.pY = inversoAdd(raiz((aux1 + pR.pX + 1)%PRM));
	}
	else{
		pend = (y1 + inversoAdd(y0))%PRM;
		pend = (pend * inversoMul((x1+inversoAdd(x0))%PRM))%PRM;
		pR.pX = (((pend*pend)%PRM) + inversoAdd((x0+x1)%PRM))%PRM;
		pR.pY = inversoAdd(((pend*pR.pX)%PRM + inversoAdd((x0*pend)%PRM)+y0)%PRM);
		aux1 = (pR.pX*pR.pX)%PRM;
		aux1 = (aux1*pR.pX)%PRM;
		//pR.pY = raiz((aux1 + pR.pX + 1)%PRM);
	}
	
	return pR;
}

uint16_t inversoMul(uint16_t valor){
	uint16_t resultado = 0;
	int i,j;
	/*int matA[4] = {1,0,0,1};
	int matB[4] = {0,1,1,0};
	int matV[4] = {0,0,0,0};
	int matI[4] = {0,0,0,0};
	uint16_t mcd = 0;
	uint16_t indice = 0;
	uint16_t b = PRM;
	uint16_t b1 = b;
	uint16_t a = valor;
	int q = 0;
	uint16_t tamV = 0;
	uint16_t tamA = 0;

	do{
		b1 = a%b;
		q = floor(a/b);
		matV[indice] = 0-q;
		indice++;
		if(b1==0){
			mcd = b;
			b = 0;
		}
		else{
			a = b;
			b = b1;
		}
	}while(b!=0);
	
	tamV = sizeof(matV)/sizeof(matV[0]);
	tamA = sizeof(matA)/sizeof(matA[0]);
	for(i = 0; i<tamV; i++){
		matB[0] = 0;
		matB[1] = 1;
		matB[2] = 1;
		matB[3] = matV[tamV-1-i];
		matI[0] = matA[0]*matB[0]+matA[1]*matB[2];
		matI[1] = matA[0]*matB[1]+matA[1]*matB[3];
		matI[2] = matA[2]*matB[0]+matA[3]*matB[2];
		matI[3] = matA[2]*matB[1]+matA[3]*matB[3];
		for(j = 0; j<tamA; j++){
			matA[j] = matI[j];
		}
	}
	//printf("=======>matA0: %d. matA1 %d matA2 %d matA3 %d",matA[0], matA[1], matA[2], matA[3]);
	if(matA[2]<0){
		matA[2] = 0 - matA[2];
	}
	resultado = matA[2];*/
	for(i=0;i<PRM;i++){
		resultado = (i*valor)%PRM;
		if(resultado==1)
			return i;
	}
	
	return 0;
}

uint16_t inversoAdd(uint16_t valor){
	uint16_t resultado = 0;
	
	resultado = PRM - valor;
	if(resultado == PRM)
		resultado = 0;
	return resultado;
}

uint16_t raiz(uint16_t valor){
	uint16_t resultado = 0;
	int i = 0;
	
	for(i=0;i<PRM;i++){
		resultado = (i*i)%PRM;
		if(resultado==valor)
			return i;
	}

	return 0;
}
