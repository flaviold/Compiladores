# -*- coding: latin-1 -*-

# UFES
# Gilberto Ewald Filho, Mauricio Carvalho de Oliveira
# Compiladores - 2014/1
import sys, re

#Definindo a classe que representa o no da lista
class NoLista():
	def __init__(self,tipo,simbolo,indice,alternativo,sucessor,semantico):
		self.tipo = tipo
		self.simbolo = simbolo
		self.indice = int(indice)
		self.indiceAlternativo = int(alternativo)
		self.indiceSucessor = int(sucessor)
		self.semantico = semantico
		self.bloco = None
		
	def getProxNoBloco(self):
		return self.bloco.proxNoLista
	
	def reconheceItemLex(self, itemLex, listaVar):
		# vendo se eh variavel
		if(self.simbolo == "palavraReservadaVar" and itemLex.palavra in listaVar):
			return True
		if(itemLex.tipo[:9] == "operador"):
			#print("		comparando ", self.simbolo, " com ", itemLex.palavra)
			return self.simbolo == itemLex.palavra
		else:
			#print("		comparando ", self.simbolo, " com ", itemLex.tipo)
			return self.simbolo == itemLex.tipo
	
	def printNoLista(self, msg):
		print(msg, " ",self.tipo, " ", self.simbolo, " ", self.indice, " ", self.indiceAlternativo, " ", self.indiceSucessor)

class Bloco():
	def __init__(self,simbolo):
		self.simbolo = simbolo
		self.proxNoLista = None
		
#Definindo a classe que representa a tabela dos simbolos terminais
#class tabelaSimbolosTerminais():
#    def __init__(self):
#        self.tabelaTerminais=[]

#Definindo a classe que representa o item da tabela de simbolos nao terminais
#class itemTabelaNaoTerminais():
#    def __init__(self,simboloNaoTerminal,numero):
#        self.simboloNaoTerminal = simboloNaoTerminal
#        self.numero = numero

#Funcao que representa um item da pilha que trabalha junto com a pilha sintatica
class itemPilhaAuxiliar():
    def __init__(self,topoPilha,voltar):
        #Comeca apontando para o topo igual a 1
        self.topoPilha = topoPilha
        #primeiro elemento igual a zero
        self.voltar = voltar

class Arvore():
	def __init__(self, raiz):
		self.raiz = raiz
		self.filhos = []
		
class Pilha():
	def __init__(self):
		self.pilha = [None]
		self.topo = 0
	
	def push(self, objeto):
		if(self.topo >= len(self.pilha)):
			self.pilha.append(None)
		self.pilha[self.topo] = objeto
		self.topo = self.topo + 1
	
	def pop(self):
		#print(self.topo)
		if(self.topo >= 1):
			self.topo = self.topo - 1
			return self.pilha[self.topo]
		return None
	
	def popAte(self, topoVar):
		while(self.topo > topoVar):
			self.pop()
			

#Definindo a classe que representa a tabela dos simbolos nao terminais:
class GrafoGramatica():
	def __init__(self, caminhoArq):
		#self.funcoesPrimitivas = 
		#	{"leia": "input()"
		self.listaSimbolos = []
		self.listaBlocos = []
		self.tamanho = 0
		
		listaNaoTerminais = []
		
		# Flag pra dizer que proximo NoLista comeca bloco:
		proxComecaBloco = False
		
		a = open(caminhoArq,"Ur")
		linha = a.readline().split()
		while(len(linha)>0):
			if(linha[0] == "C"):
				self.listaBlocos.append(Bloco(linha[1]))
				proxComecaBloco = True
				#listaBlocos.append(noLista)
			else:
				noLista = NoLista(linha[0],linha[1],linha[2],linha[3],linha[4],linha[5])
				self.adicionaNo(noLista, int(linha[2]))
				if(proxComecaBloco):
					self.listaBlocos[-1].proxNoLista = noLista
					proxComecaBloco = False
					
				if(linha[0] == "N"):
					listaNaoTerminais.append(noLista)
			linha = a.readline().split()
			
		for noNT in listaNaoTerminais:
			for bloco in self.listaBlocos:
				if(noNT.simbolo == bloco.simbolo):
					noNT.bloco = bloco
					break
	
	def getNoListaSucessor(self, noLista):
		proxIndice = noLista.indiceSucessor-1
		if(proxIndice < 0):
			return None
		return self.listaSimbolos[noLista.indiceSucessor-1]
	
	def getNoListaAlternativo(self, noLista):
		proxIndice = noLista.indiceAlternativo-1
		if(proxIndice < 0):
			return None
		return self.listaSimbolos[noLista.indiceAlternativo-1]
		
	def adicionaNo(self,simbolo,numero):
		while(len(self.listaSimbolos) < numero):
			self.listaSimbolos.append(0)
		#print(numero)
		self.listaSimbolos[numero-1] = simbolo
	
    #Procurando se o simbolo esta na tabela de simbolos nao terminais
	def procurarSimbolo(self,simbolo):
		if(simbolo.indice < len(self.listaSimbolos)):
			if(self.listaSimbolos[simbolo.indice] == simbolo):
				return True
		return False
	
	def imprimaGrafo(self):
		for i in self.listaSimbolos:
			print("**************************\n")
			print("Minha representacao = ",i.simbolo,"\n")
			print("Tipo: ",i.tipo,"\n")
			print("Semantico: ",i.semantico,"\n")
			print("Alternativo: ",i.alternativo,"\n")
			print("Sucessor: ",i.sucessor,"\n")
			
	#Funcao que verifica se a palavra pertence a gramatica
	def verificaFrase(self, frase, debug):
		pilhaSintatica = Pilha()
		pilhaAuxiliar = Pilha()
		pilhaAuxiliar.push( (0,1,len(frase)-1) )
		listaVar = []
		
		noLista = self.listaSimbolos[0]
				
		if(debug): noLista.printNoLista("Comecou em ")
		
		codigoFinal = """class Inteiro(object):
        def __init__(self, val=0) :
                self._val = int(val)

        def __add__(self, val) :
                return self._val + val
        def __radd__(self, val) :
                return self._val + val

        def __sub__(self, val) :
                return self._val - val
        def __rsub__(self, val) :
                return self._val - val
        
        def __mul__(self, val):
                return self._val * val
        def __rmul__(self, val):
                return self._val * val

        def __div__(self, val):
                return self._val / val
        def __rdiv__(self, val):
                return self._val / val
        
        def __str__(self) :
                return str(self._val)

        def __repr__(self) :
                return 'int(%s)' %self._val

        def __gt__(self, val):
                return int(self._val) > val

        def __lt__(self, val):
                return int(self._val) < val

class Cadeia():
	def __init__(self, tam):
		self.tamanho = tam
		self._val = [None]*tam

	def __repr__(self):
		return '%s' %self._val

def leia(param):
	if(isinstance(param, Inteiro)):
		param._val = int(input())
	else:
		param._val = input()

def imprima(param):
	print(param)
\n"""
		tabCount = 0
		i = 0
		itemLex = frase[0]
		while(i < len(frase)):
			itemLex = frase[i]
			if(debug): print("\nAnalisando ", itemLex.palavra)
			if(pilhaAuxiliar.topo == 0):
				print("Erro! Programa invalido!")
				print(codigoFinal)
				break
			while(True):
				if(pilhaAuxiliar.topo == 0):
					break
				if(debug): print("# PilhaAuxiliar = ", pilhaAuxiliar.pilha, " at ", pilhaAuxiliar.topo)
				if(noLista.tipo == "T"): # Item terminal - verificar se reconhece item lexico
					# Manejando identacao:
					if("10" in noLista.semantico):
						tabCount -= 1
					if("9" in noLista.semantico):
						tabCount += 1
					if("8" in noLista.semantico):
						tabCount += 1
					if(noLista.reconheceItemLex(itemLex, listaVar)):	# Verifica se reconhece item lexico
						# Item lexico reconhecido.
						
						# Adicionando identacao:
						codigoFinal += self.trataSemantico(noLista, itemLex)
						if("11" in noLista.semantico):
							listaVar.append(itemLex.palavra)
						if("12" in noLista.semantico):
							if(itemLex.palavra not in listaVar and '"' not in itemLex.palavra):
								print("ERRO - variavel " + itemLex.palavra + " nao declarada")
							#if(itemLex.palavra in listaVar):
								#codigoFinal += "._val"
						if("3" in noLista.semantico or "8" in noLista.semantico or "9" in noLista.semantico or "10" in noLista.semantico):	# passou por uma quebra de linha, poe a identacao
							codigoFinal += tabCount * "\t"
							
						# Vai para o no sucessor:
						noLista = self.getNoListaSucessor(noLista)
						if(noLista == None):	# Se não houver sucessor, bloco reconhecido. Vai desempilhar:
							(topoPilhaSint, indiceListaSimbolos, iNovo) = pilhaAuxiliar.pop()
							pilhaSintatica.popAte(topoPilhaSint)
							noLista = self.listaSimbolos[indiceListaSimbolos]
							if(debug): print("	Desempilhou ", indiceListaSimbolos)
							
						# Poe o noLista na pilha sintatica
						pilhaSintatica.push(noLista)
						if(debug): noLista.printNoLista("	SUCESSO, Foi para ")
						break
					else:	# Item lexico nao reconhecido:
						noLista = self.getNoListaAlternativo(noLista)	# Pega no alternativo.
						if(noLista == None):	# Se não houver alternativo, desempilha
							(topoPilhaSint, indiceListaSimbolos, iNovo) = pilhaAuxiliar.pop()
							pilhaSintatica.popAte(topoPilhaSint)
							noLista = self.listaSimbolos[indiceListaSimbolos]
							#i = iNovo-1
							#itemLex = frase[i]
							if(debug): print("	Desempilhou ", indiceListaSimbolos)
						if(debug): noLista.printNoLista("	FALHA, Foi para ")
				elif(noLista.tipo == "N"):
					# Item nao terminal - abre o proximo bloco
					
					# Manuseio de identacao:
					if("4" in noLista.semantico): # ao abrir um bloco, aumenta a identacao
						tabCount += 1
						codigoFinal += "\t"
					if("4" in noLista.semantico): # ao abrir um bloco, aumenta a identacao
						tabCount += 1
						codigoFinal += "\t"
					
					# Abre blocos:
					while(noLista.tipo == "N"):
						pilhaAuxiliar.push( (pilhaSintatica.topo,noLista.indice, i) )
						noLista = noLista.getProxNoBloco()
						if(debug): noLista.printNoLista("	BLOCO, Foi para ")
			i += 1
		else:
			if(pilhaAuxiliar.topo == 0):
				print("\nPrograma valido!")
				print(codigoFinal)
				print(frase[1].palavra + "()")
			else:
				print("\nPrograma invalido!")
				print(codigoFinal)
			arquivo = open(frase[1].palavra+'.py', 'w')
			arquivo.write(codigoFinal + "\n" + frase[1].palavra + "()")
			
	
	def trataSemantico(self, noLista, itemLex):
		# Semanticos:
		# 0 - faz nada
		# 1 - pega nome do identificador
		# 2 - pega nome do identificador + ():\n
		# 3 - quebra de linha
		# 4 - tab
		# 6 - começa a tratar cadeia
		# 7 - numero
		# 8 - faca do enquanto
		# 11 - pega identificador e guarda var
		# 12 - pega identificador e verifica se var existe
		# 99 - pega identificador + ._val
		if(noLista == None):
			return ""
		sem = noLista.semantico
		#print("SEMANTICO: " + sem)
		if(not sem.isdigit()):
			return sem + " "
		elif(int(sem) == 1):
			return itemLex.palavra + " "
		elif(int(sem) == 2):
			return itemLex.palavra + "():"
		elif(int(sem) == 3):
			return "\n"
		elif(int(sem) == 4):
			return "\t"
		elif(int(sem) == 6):
			return "[None] * "
		elif(int(sem) == 7):
			return itemLex.palavra + " "
		elif(int(sem) == 8):
			return ":\n"
		elif(int(sem) == 9):
			return "else:\n"
		elif(int(sem) == 10):
			return "\n"
		elif(int(sem) == 11):
			return itemLex.palavra + " "
		elif(int(sem) == 12):
			return itemLex.palavra
		else:
			return ""
