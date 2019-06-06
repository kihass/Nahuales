/* DemoRC2.h - Demo para RC2.

   Universidad Nacional Autonoma de Mexico,
        Dr. Gerardo Vega Hernández
              Abril del 2003.
*/
#include <stdio.h>
#include "RC2.h"

B8 Key[8] = {0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00};
B8 Ptx[8] = {0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00};

main()
{
    FILE *archivo;
    int i, nbytes, longSal;
    B8 *ap;
    B16 Ky[64];
    B8 buffer[65536];

    ExpandeLlave(Ky,Key,8,63);
    RC2_CifraBloque((B16 *)Ptx,Ky);
    ap = Ptx;
    for(i=0;i<8;i++) {
      if(!(i%4)) printf(" ");
      printf("%02x",ap[i]);
    }
    RC2_DescifraBloque((B16 *)Ptx,Ky);
    ap = Ptx;
    for(i=0;i<8;i++) {
      if(!(i%4)) printf(" ");
      printf("%02x",ap[i]);
    }
}

/* Rutina para el cifrado de un bloque de datos de
   longitud variable.
   Entrada:
	EntySal, un buffer de bytes de longuitud longEnt.
	K, La llave expandida que se usara en el cifrado.
   Salida:
        EntySal, un buffer de bytes de longuitud longSal.
   Observacion: El archivo de entrada y salida es el mismo.
*/
void RC2_Cifra(EntySal,longEnt,longSal,K)
B8 EntySal[];
int longEnt, *longSal;
B16 K[];
{
    int i, longPad=8-(longEnt%8), numBloques;
    unsigned char *Ptx;

    /* Agregamos el padding antes de cifrar. */
    for(i=0;i<longPad;i++) EntySal[longEnt+i] = (unsigned char) longPad;
    *longSal = longEnt + longPad;  /* La longitud del buffer por cifrar. */
    numBloques = (*longSal) >> 3;  /* Núm. de bloques por cifrar. */
    /* ¡A cifrar! */
    for(i=0,Ptx=EntySal;i<numBloques;i++,Ptx+=8)
        RC2_CifraBloque((B16 *)Ptx,K);
}

/* Rutina para el descifrado de un bloque de datos de
   longitud variable.
   Entrada:
        EntySal, un buffer de bytes de longuitud longEnt.
        K, La llave expandida que se usara en el descifrado.
   Salida:
        EntySal, un buffer de bytes de longuitud longSal.
   Observacion: El archivo de entrada y salida es el mismo.
*/
void RC2_Descifra(EntySal,longEnt,longSal,K)
B8 EntySal[];
int longEnt, *longSal;
B16 K[];
{
    int i, numBloques;
    unsigned char *Ptx;

    numBloques = longEnt >> 3;  /* Núm. de bloques por descifrar. */
    /* ¡A descifrar! */
    for(i=0,Ptx=EntySal;i<numBloques;i++,Ptx+=8)
        RC2_DescifraBloque((B16 *)Ptx,K);
    *longSal = longEnt - (unsigned int) *(Ptx-1);  /* Quitamos padding. */
}

/* Rutina de expancion de la llave;
   salida: EKey, la llave expandida.
   entrada: Key, la llave por expander.
            t, número de bytes en la llave.
            t1, número de bits efectivos en la llave.
*/
void ExpandeLlave(EKey,Key,t,t1)
B16 *EKey;
B8 *Key;
int t, t1;
{
    int i, T8=((t1+7)/8);
    int TM=(255 % (1 << (8+t1-8*T8)));
    B8 *Ly = (B8 *) EKey;

    memcpy(Ly,Key,t);   /* Inicializa EKey */
    /* Primer loop, ver RFC2268 p. 3. */
    for(i=t;i<128;i++) Ly[i] = PITABLE[(Ly[i-1]+Ly[i-t])&0xff];
    /* Paso intermedio. */
    Ly[128-T8] = PITABLE[Ly[128-T8]&TM];
    /* Segundo loop. */
    for(i=127-T8;i>=0;i--) Ly[i] = PITABLE[Ly[i+1]^Ly[i+T8]];
}

/* Rutina para cifrar un bloque usando RC2.
   parámetros: R el bloque de 64 bits a cifrar y la llave
   expandida K que habrá de usarse. La salida i.e. el bloque
   cifrado estará en R.
*/
void RC2_CifraBloque(R,K)
B16 R[],K[];
{
    int j=0,cnr,im;
    B8 S[4]={0x01,0x02,0x03,0x05};

    Mix(R,K,j,5);
    Mash(R,K);
    Mix(R,K,j,6);
    Mash(R,K);
    Mix(R,K,j,5);
}

/* Rutina para descifrar un bloque usando RC2.
   parámetros: R el bloque de 64 bits a descifrar y la llave
   expandida K que habrá de usarse. La salida i.e. el bloque
   descifrado estará en R.
*/
void RC2_DescifraBloque(R,K)
B16 R[],K[];
{
    int j=63,cnr,im;
    B8 S[4]={0x01,0x02,0x03,0x05};

    R_Mix(R,K,j,5);
    R_Mash(R,K);
    R_Mix(R,K,j,6);
    R_Mash(R,K);
    R_Mix(R,K,j,5);
}

