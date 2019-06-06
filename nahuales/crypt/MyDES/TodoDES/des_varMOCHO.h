/*

	des_var.h

	Declaracion de variables para el des.c

	14 de febrero de 1997

	M. en C. Gerardo Vega H.

	Nota: Este archivo contiene una serie de tablas que fueron creadas con el
	programa tablas.c el cual aparece al final de este archivo.

*/

FILE *fpe, *fps;
B32 subllaves[ITER][2];
B32 llave[2];
BOOLEAN cifrar = TRUE;
BOOLEAN pantalla = FALSE;
BOOLEAN borrar = TRUE;
char ent[128], sal[128];                      /* Nombres de los archivos de E/S */
int LS[] = {1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1};

	 	/* tabla que efectua el trabajo de las cajas S's y la permutacion P */
B32 S_P[8][64]={
0x00808200,0x00000000,0x00008000,0x00808202,0x00808002,0x00008202,0x00000002,0x00008000,
0x00000200,0x00808200,0x00808202,0x00000200,0x00800202,0x00808002,0x00800000,0x00000002,
0x00000202,0x00800200,0x00800200,0x00008200,0x00008200,0x00808000,0x00808000,0x00800202,
0x00008002,0x00800002,0x00800002,0x00008002,0x00000000,0x00000202,0x00008202,0x00800000,
0x00008000,0x00808202,0x00000002,0x00808000,0x00808200,0x00800000,0x00800000,0x00000200,
0x00808002,0x00008000,0x00008200,0x00800002,0x00000200,0x00000002,0x00800202,0x00008202,
0x00808202,0x00008002,0x00808000,0x00800202,0x00800002,0x00000202,0x00008202,0x00808200,
0x00000202,0x00800200,0x00800200,0x00000000,0x00008002,0x00008200,0x00000000,0x00808002,

0x40084010,0x40004000,0x00004000,0x00084010,0x00080000,0x00000010,0x40080010,0x40004010,
0x40000010,0x40084010,0x40084000,0x40000000,0x40004000,0x00080000,0x00000010,0x40080010,
0x00084000,0x00080010,0x40004010,0x00000000,0x40000000,0x00004000,0x00084010,0x40080000,
0x00080010,0x40000010,0x00000000,0x00084000,0x00004010,0x40084000,0x40080000,0x00004010,
0x00000000,0x00084010,0x40080010,0x00080000,0x40004010,0x40080000,0x40084000,0x00004000,
0x40080000,0x40004000,0x00000010,0x40084010,0x00084010,0x00000010,0x00004000,0x40000000,
0x00004010,0x40084000,0x00080000,0x40000010,0x00080010,0x40004010,0x40000010,0x00080010,
0x00084000,0x00000000,0x40004000,0x00004010,0x40000000,0x40080010,0x40084010,0x00084000,

0x00000104,0x04010100,0x00000000,0x04010004,0x04000100,0x00000000,0x00010104,0x04000100,
0x00010004,0x04000004,0x04000004,0x00010000,0x04010104,0x00010004,0x04010000,0x00000104,
0x04000000,0x00000004,0x04010100,0x00000100,0x00010100,0x04010000,0x04010004,0x00010104,
0x04000104,0x00010100,0x00010000,0x04000104,0x00000004,0x04010104,0x00000100,0x04000000,
0x04010100,0x04000000,0x00010004,0x00000104,0x00010000,0x04010100,0x04000100,0x00000000,
0x00000100,0x00010004,0x04010104,0x04000100,0x04000004,0x00000100,0x00000000,0x04010004,
0x04000104,0x00010000,0x04000000,0x04010104,0x00000004,0x00010104,0x00010100,0x04000004,
0x04010000,0x04000104,0x00000104,0x04010000,0x00010104,0x00000004,0x04010004,0x00010100,

0x80401000,0x80001040,0x80001040,0x00000040,0x00401040,0x80400040,0x80400000,0x80001000,
0x00000000,0x00401000,0x00401000,0x80401040,0x80000040,0x00000000,0x00400040,0x80400000,
0x80000000,0x00001000,0x00400000,0x80401000,0x00000040,0x00400000,0x80001000,0x00001040,
0x80400040,0x80000000,0x00001040,0x00400040,0x00001000,0x00401040,0x80401040,0x80000040,
0x00400040,0x80400000,0x00401000,0x80401040,0x80000040,0x00000000,0x00000000,0x00401000,
0x00001040,0x00400040,0x80400040,0x80000000,0x80401000,0x80001040,0x80001040,0x00000040,
0x80401040,0x80000040,0x80000000,0x00001000,0x80400000,0x80001000,0x00401040,0x80400040,
0x80001000,0x00001040,0x00400000,0x80401000,0x00000040,0x00400000,0x00001000,0x00401040,

0x00000080,0x01040080,0x01040000,0x21000080,0x00040000,0x00000080,0x20000000,0x01040000,
0x20040080,0x00040000,0x01000080,0x20040080,0x21000080,0x21040000,0x00040080,0x20000000,
0x01000000,0x20040000,0x20040000,0x00000000,0x20000080,0x21040080,0x21040080,0x01000080,
0x21040000,0x20000080,0x00000000,0x21000000,0x01040080,0x01000000,0x21000000,0x00040080,
0x00040000,0x21000080,0x00000080,0x01000000,0x20000000,0x01040000,0x21000080,0x20040080,
0x01000080,0x20000000,0x21040000,0x01040080,0x20040080,0x00000080,0x01000000,0x21040000,
0x21040080,0x00040080,0x21000000,0x21040080,0x01040000,0x00000000,0x20040000,0x21000000,
0x00040080,0x01000080,0x20000080,0x00040000,0x00000000,0x20040000,0x01040080,0x20000080,

0x10000008,0x10200000,0x00002000,0x10202008,0x10200000,0x00000008,0x10202008,0x00200000,
0x10002000,0x00202008,0x00200000,0x10000008,0x00200008,0x10002000,0x10000000,0x00002008,
0x00000000,0x00200008,0x10002008,0x00002000,0x00202000,0x10002008,0x00000008,0x10200008,
0x10200008,0x00000000,0x00202008,0x10202000,0x00002008,0x00202000,0x10202000,0x10000000,
0x10002000,0x00000008,0x10200008,0x00202000,0x10202008,0x00200000,0x00002008,0x10000008,
0x00200000,0x10002000,0x10000000,0x00002008,0x10000008,0x10202008,0x00202000,0x10200000,
0x00202008,0x10202000,0x00000000,0x10200008,0x00000008,0x00002000,0x10200000,0x00202008,
0x00002000,0x00200008,0x10002008,0x00000000,0x10202000,0x10000000,0x00200008,0x10002008,

0x00100000,0x02100001,0x02000401,0x00000000,0x00000400,0x02000401,0x00100401,0x02100400,
0x02100401,0x00100000,0x00000000,0x02000001,0x00000001,0x02000000,0x02100001,0x00000401,
0x02000400,0x00100401,0x00100001,0x02000400,0x02000001,0x02100000,0x02100400,0x00100001,
0x02100000,0x00000400,0x00000401,0x02100401,0x00100400,0x00000001,0x02000000,0x00100400,
0x02000000,0x00100400,0x00100000,0x02000401,0x02000401,0x02100001,0x02100001,0x00000001,
0x00100001,0x02000000,0x02000400,0x00100000,0x02100400,0x00000401,0x00100401,0x02100400,
0x00000401,0x02000001,0x02100401,0x02100000,0x00100400,0x00000000,0x00000001,0x02100401,
0x00000000,0x00100401,0x02100000,0x00000400,0x02000001,0x02000400,0x00000400,0x00100001,

0x08000820,0x00000800,0x00020000,0x08020820,0x08000000,0x08000820,0x00000020,0x08000000,
0x00020020,0x08020000,0x08020820,0x00020800,0x08020800,0x00020820,0x00000800,0x00000020,
0x08020000,0x08000020,0x08000800,0x00000820,0x00020800,0x00020020,0x08020020,0x08020800,
0x00000820,0x00000000,0x00000000,0x08020020,0x08000020,0x08000800,0x00020820,0x00020000,
0x00020820,0x00020000,0x08020800,0x00000800,0x00000020,0x08020020,0x00000800,0x00020820,
0x08000800,0x00000020,0x08000020,0x08020000,0x08020020,0x08000000,0x00020000,0x08000820,
0x00000000,0x08020820,0x00020020,0x08000020,0x08020000,0x08000800,0x08000820,0x00000000,
0x08020820,0x00020800,0x00020800,0x00000820,0x00000820,0x00020020,0x08000000,0x08020800
};

						/* Tablas para la permutacion PC2 */
B32 PC2_Tab_0[16]={
0x00000000,0x00000400,0x00200000,0x00200400,0x00000001,0x00000401,0x00200001,0x00200401,
0x02000000,0x02000400,0x02200000,0x02200400,0x02000001,0x02000401,0x02200001,0x02200401
};

B32 PC2_Tab_1[256]={
0x00000000,0x00000800,0x08000000,0x08000800,0x00010000,0x00010800,0x08010000,0x08010800,
0x00000000,0x00000800,0x08000000,0x08000800,0x00010000,0x00010800,0x08010000,0x08010800,
0x00000100,0x00000900,0x08000100,0x08000900,0x00010100,0x00010900,0x08010100,0x08010900,
0x00000100,0x00000900,0x08000100,0x08000900,0x00010100,0x00010900,0x08010100,0x08010900,
0x00000010,0x00000810,0x08000010,0x08000810,0x00010010,0x00010810,0x08010010,0x08010810,
0x00000010,0x00000810,0x08000010,0x08000810,0x00010010,0x00010810,0x08010010,0x08010810,
0x00000110,0x00000910,0x08000110,0x08000910,0x00010110,0x00010910,0x08010110,0x08010910,
0x00000110,0x00000910,0x08000110,0x08000910,0x00010110,0x00010910,0x08010110,0x08010910,
0x00040000,0x00040800,0x08040000,0x08040800,0x00050000,0x00050800,0x08050000,0x08050800,
0x00040000,0x00040800,0x08040000,0x08040800,0x00050000,0x00050800,0x08050000,0x08050800,
0x00040100,0x00040900,0x08040100,0x08040900,0x00050100,0x00050900,0x08050100,0x08050900,
0x00040100,0x00040900,0x08040100,0x08040900,0x00050100,0x00050900,0x08050100,0x08050900,
0x00040010,0x00040810,0x08040010,0x08040810,0x00050010,0x00050810,0x08050010,0x08050810,
0x00040010,0x00040810,0x08040010,0x08040810,0x00050010,0x00050810,0x08050010,0x08050810,
0x00040110,0x00040910,0x08040110,0x08040910,0x00050110,0x00050910,0x08050110,0x08050910,
0x00040110,0x00040910,0x08040110,0x08040910,0x00050110,0x00050910,0x08050110,0x08050910,
0x01000000,0x01000800,0x09000000,0x09000800,0x01010000,0x01010800,0x09010000,0x09010800,
0x01000000,0x01000800,0x09000000,0x09000800,0x01010000,0x01010800,0x09010000,0x09010800,
0x01000100,0x01000900,0x09000100,0x09000900,0x01010100,0x01010900,0x09010100,0x09010900,
0x01000100,0x01000900,0x09000100,0x09000900,0x01010100,0x01010900,0x09010100,0x09010900,
0x01000010,0x01000810,0x09000010,0x09000810,0x01010010,0x01010810,0x09010010,0x09010810,
0x01000010,0x01000810,0x09000010,0x09000810,0x01010010,0x01010810,0x09010010,0x09010810,
0x01000110,0x01000910,0x09000110,0x09000910,0x01010110,0x01010910,0x09010110,0x09010910,
0x01000110,0x01000910,0x09000110,0x09000910,0x01010110,0x01010910,0x09010110,0x09010910,
0x01040000,0x01040800,0x09040000,0x09040800,0x01050000,0x01050800,0x09050000,0x09050800,
0x01040000,0x01040800,0x09040000,0x09040800,0x01050000,0x01050800,0x09050000,0x09050800,
0x01040100,0x01040900,0x09040100,0x09040900,0x01050100,0x01050900,0x09050100,0x09050900,
0x01040100,0x01040900,0x09040100,0x09040900,0x01050100,0x01050900,0x09050100,0x09050900,
0x01040010,0x01040810,0x09040010,0x09040810,0x01050010,0x01050810,0x09050010,0x09050810,
0x01040010,0x01040810,0x09040010,0x09040810,0x01050010,0x01050810,0x09050010,0x09050810,
0x01040110,0x01040910,0x09040110,0x09040910,0x01050110,0x01050910,0x09050110,0x09050910,
0x01040110,0x01040910,0x09040110,0x09040910,0x01050110,0x01050910,0x09050110,0x09050910
};

B32 PC2_Tab_2[256]={
0x00000000,0x00000004,0x00001000,0x00001004,0x00000000,0x00000004,0x00001000,0x00001004,
0x10000000,0x10000004,0x10001000,0x10001004,0x10000000,0x10000004,0x10001000,0x10001004,
0x00000020,0x00000024,0x00001020,0x00001024,0x00000020,0x00000024,0x00001020,0x00001024,
0x10000020,0x10000024,0x10001020,0x10001024,0x10000020,0x10000024,0x10001020,0x10001024,
0x00080000,0x00080004,0x00081000,0x00081004,0x00080000,0x00080004,0x00081000,0x00081004,
0x10080000,0x10080004,0x10081000,0x10081004,0x10080000,0x10080004,0x10081000,0x10081004,
0x00080020,0x00080024,0x00081020,0x00081024,0x00080020,0x00080024,0x00081020,0x00081024,
0x10080020,0x10080024,0x10081020,0x10081024,0x10080020,0x10080024,0x10081020,0x10081024,
0x20000000,0x20000004,0x20001000,0x20001004,0x20000000,0x20000004,0x20001000,0x20001004,
0x30000000,0x30000004,0x30001000,0x30001004,0x30000000,0x30000004,0x30001000,0x30001004,
0x20000020,0x20000024,0x20001020,0x20001024,0x20000020,0x20000024,0x20001020,0x20001024,


