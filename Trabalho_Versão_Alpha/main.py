from sint import *
from lex import *

if __name__ == '__main__':
	auto = Automato("automato.txt")
	#Inicializando o objeto tabela de simbolos
	tabela = SymbolTable(47,"simbolos.txt")
	listaLex = auto.analiseLexica("./exemplos/teste1.txt")
	#print(listaLex)
	listaEntrada = []
	for i in listaLex:
		listaEntrada.append(i)
	teste = GrafoGramatica("minhaTabGrande.txt")
	teste.verificaFrase(listaEntrada, False)
