# http://es.wikipedia.org/wiki/Data_Encryption_Standard
# http://en.wikipedia.org/wiki/DES_supplementary_material
# http://es.wikipedia.org/wiki/Operador_a_nivel_de_bits
# http://docs.python.org/2/extending/extending.html
# http://stackoverflow.com/questions/145270/calling-c-c-from-python
# http://www.tero.co.uk/des/test.php
# http://docs.python.org/3.3/library/struct.html
# http://docs.python.org/3.3/library/binascii.html

##1 <= a <= 7

##Operador 	Descripci\'on 	Ejemplo
##& 	and 	r = 3 & 2 # r es 2
##| 	or 	r = 3 | 2 # r es 3
##^ 	xor 	r = 3 ^ 2 # r es 1
##~ 	not 	r = ~3 # r es -4
##<< 	Desplazamiento a la izquierda 	r = 3 << 1 # r es 6
##>> 	Desplazamiento a la derecha 	r = 3 >> 1 # r es 1

# Listas circulares
#  data.hex(x)  Convert an integer number (of any size) to a hexadecimal string. The result is a valid Python expression.
# 0x17 hexadecimal = 23 en base 10
# 027 octal = 23 en base 10
##entero = type(23)  # type(entero) dar\'a int
##entero = Type(23L) # type(entero) dar\'a long
# print bin(desplaza_derecha)
#x = int("deadbeef", 16)
#print int("0xdeadbeef", 0)
# print("{0:b}".format(0b10101010))


##		tmpE = (((argData >> 31) & 0b1) << 47) \
##				| ((argData & 0b11111) << 42) \
##				| (((argData >>  3) & 0b111111) << 37) \
##				| ((argData & 0b1) )


def main():
    pass

if __name__ == '__main__':
    main()
