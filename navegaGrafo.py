from hash import *
import sys, re

class NoLista():
	def __init__(self,tipo,simbolo,indice,alternativo,sucessor):
		self.tipo = tipo
		self.simbolo = simbolo
		self.indice = int(indice)
		self.indiceAlternativo = int(alternativo)
		self.indiceSucessor = int(sucessor)
		self.bloco = None
		
	def getProxNoBloco(self):
		return self.bloco.proxNoLista
	
	def printNoLista(self, msg):
		print(msg, " ",self.tipo, " ", self.simbolo, " ", self.indice, " ", self.indiceAlternativo, " ", self.indiceSucessor)

class Bloco():
	def __init__(self,simbolo):
		self.simbolo = simbolo
		self.nos = []

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
		if(self.topo >= 1):
			self.topo -= 1
			return self.pilha.pop()
		return None

class Grafo():
	def __init__(self, caminhoArq, hashIden, hashFunc):
		self.hashIden = hashIden
		self.hashFunc = hashFunc
		self.listaVar = []
		self.listaBlocos = []
		self.tamanho = 0

		a = open(caminhoArq,"Ur")
		texto = a.read().split("\n")
		for linha in texto:
			palavras = linha.split()
			if(palavras[0] == "C"):
				self.listaBlocos.append(Bloco(palavras[1]))
			else:
				noLista = NoLista(palavras[0],palavras[1],palavras[2],palavras[3],palavras[4])
				self.listaBlocos[-1].nos.append(noLista)

	def verificaPrograma(self, listaLex):
		titulo = ""
		pilhaSintatica = Pilha()
		pilhaBlocos = Pilha()
		pilhaAuxiliar = Pilha()
		pilhaAuxiliar.push((0, 1))

		idAtual = 1
		count = 2
		for item in listaLex:
			print(item)
			noAtual = self.getNoById(idAtual)
			analisa = self.semantico(item)
			print("Analisando ", analisa)
			while True:
				if analisa != None:
					if noAtual.simbolo == "idenParametro":
						if noAtual.indiceSucessor != 0:
							idAtual = noAtual.indiceSucessor
							pilhaSintatica.push(item)
							break
						else:
							#retorna para o bloco anterior
							no = pilhaAuxiliar.pop()
							while no != None and no[0] != 0:
								if self.getNoById(no[0]).indiceSucessor != 0:
									idAtual = self.getNoById(no[0]).indiceSucessor
									break
								no = pilhaAuxiliar.pop()
							if no == None:
								return False, "Programa invalido"
							else:
								if no[0] == 0:
										return True, "Programa Valido"
								else:
									break

					#e um simbolo
					if analisa == noAtual.simbolo:
						if noAtual.tipo == "N":
							#Empilha o no onde deixamos o bloco
							pilhaAuxiliar.push((noAtual.indice, count))
							noAtual = self.getBlocoByType(noAtual.simbolo)
							count += 1
							analisa = None
						elif noAtual.tipo == "T":
							#Nao e bloco e leu
							if noAtual.indiceSucessor != 0:
								idAtual = noAtual.indiceSucessor
								pilhaSintatica.push(item)
								break
							else:
								#retorna para o bloco anterior
								print("retorna bloco")
								no = pilhaAuxiliar.pop()
								while (no != None and no[0] != 0):
									if self.getNoById(no[0]).indiceSucessor != 0:
										idAtual = self.getNoById(no[0]).indiceSucessor
										break
									no = pilhaAuxiliar.pop()
								if no == None:
									return False, "Programa invalido"
								else:
									if no[0] == 0:
											return True, "Programa Valido"
									else:
										break
					else:
						if noAtual.simbolo == "Expressao":
							pilhaAuxiliar.push((noAtual.indice, count))
							count += 1
							noAtual = self.getBlocoByType(noAtual.simbolo)
						elif noAtual.simbolo == "OpLogica":
							if item == "!" or analisa == "atribuicao":
								pilhaAuxiliar.push((noAtual.indice, count))
								count += 1
								noAtual = self.getBlocoByType(noAtual.simbolo)
							else:
								return False, pilhaAuxiliar.pop()[0]
						elif noAtual.simbolo == "OpAritmetica":
							if analisa == "atribuicao":
								pilhaAuxiliar.push((noAtual.indice, count))
								count += 1
								noAtual = self.getBlocoByType(noAtual.simbolo)
							else:
								return False, pilhaAuxiliar.pop()[0]
						else:
							if noAtual.indiceAlternativo != 0:
								noAtual = self.getNoById(noAtual.indiceAlternativo)
							else:
								#Programa invalido
								return False, pilhaAuxiliar.pop()[0]
				#Quando o item nao e de acao semantica
				else:
					if noAtual.simbolo == "setParametro":
						if item not in self.listaVar:
							self.listaVar.append(item)
							if noAtual.indiceSucessor != 0:
								idAtual = noAtual.indiceSucessor
								pilhaSintatica.push(item)
								break
							else:
								#retorna para o bloco anterior
								no = pilhaAuxiliar.pop()
								if no != None:
									if no[0] == 0:
										return True, "Programa Valido"
									else:
										idAtual = self.getNoById(no[0]).indiceSucessor
										break

					if noAtual.simbolo == "Expressao":
						if noAtual.indiceSucessor != 0:
							idAtual = noAtual.indiceSucessor
							pilhaSintatica.push(item)
							break
						else:
							#retorna para o bloco anterior
							no = pilhaAuxiliar.pop()
							if no != None:
								if no[0] == 0:
									return True, "Programa Valido"
								else:
									idAtual = self.getNoById(no[0]).indiceSucessor
									break

					if item == noAtual.simbolo:
						if noAtual.tipo == "N":
							#Empilha o no onde deixamos o bloco
							pilhaAuxiliar.push((noAtual.indice, count))
							noAtual = self.getBlocoByType(noAtual.simbolo)
							count += 1
						elif noAtual.tipo == "T":
							#Nao e bloco e leu
							if noAtual.indiceSucessor != 0:
								idAtual = noAtual.indiceSucessor
								pilhaSintatica.push(item)
								break
							else:
								print("retorna bloco")
								#retorna para o bloco anterior
								no = pilhaAuxiliar.pop()
								while no != None and no[0] != 0:
									if self.getNoById(no[0]).indiceSucessor != 0:
										idAtual = self.getNoById(no[0]).indiceSucessor
										break
									no = pilhaAuxiliar.pop()
								if no == None:
									return False, "Programa invalido"
								else:
									if no[0] == 0:
											return True, "Programa Valido"
									else:
										break
					else:
						if noAtual.indiceAlternativo != 0:
							noAtual = self.getNoById(noAtual.indiceAlternativo)
						else:
							#Programa invalido
							return False, pilhaAuxiliar.pop()[0]


	def getBlocoByType(self, tipo):
		for b in self.listaBlocos:
			if b.simbolo == tipo:
				return b.nos[0]

	def getNoById(self, id):
		for b in self.listaBlocos:
			for n in b.nos:
				if id == n.indice:
					return n

	def semantico(self, palavra):
		if self.hashIden.consultarChave(palavra) != 0:
			return "Identificador"

		if self.hashFunc.consultarChave(palavra) != 0:
			return "funcao"

		if palavra in self.listaVar:
			return "atribuicao"

		if palavra == "fim":
			return "fim"

		return None



	def lexico(self, caminho):
		listaLex = []
		arq = open(caminho, "Ur")
		titulo = arq.readline().split()[1]
		texto = arq.read().replace("\t", "")
		for linha in texto.split("\n"):
			for palavra in linha.strip().split():
				if(palavra.isalnum()):
					listaLex.append(palavra)
					continue

				text = ""
				for c in palavra:
					if(c.isalnum()):
						text += c
					else:
						if len(text) > 0:
							listaLex.append(text)
							text = ""

						if len(c) > 0:
							listaLex.append(c)
		
		return titulo, listaLex