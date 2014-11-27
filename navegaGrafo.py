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
		self.listaBlocos = []
		self.tamanho = 0

		a = open(caminhoArq,"Ur")
		texto = a.read().split("\n")
		for linha in texto:
			palavras = linha.split()
			if(palavras[0] == "C"):
				self.listaBlocos.append(Bloco(linha[1]))
			else:
				noLista = NoLista(linha[0],linha[1],linha[2],linha[3],linha[4])
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
			noAtual = getNoById(idAtual)
			analisa = self.semantico(item)

			while True:
				if analisa != None:
					if analisa == noAtual.simbolo:
						if noAtual.tipo == "N":
							noAtual = getBlocoByType(noAtual.simbolo)
						pilhaSintatica.push(item)
						pilhaAuxiliar.push((noAtual.indiceSucessor, count))
						if noAtual == :
							pass
						count += 1
						break
					
					if noAtual.indiceAlternativo != 0:
						noAtual = getNoById(noAtual.indiceAlternativo)
					else:
						return pilhaAuxiliar[-1]
				#Quando o item não é de ação semantica
				else:
					if item == noAtual.simbolo:
						pilhaSintatica.push(item)
						pilhaAuxiliar.push((noAtual.indiceSucessor, count))
						count += 1
						break
					
					if noAtual.indiceAlternativo != 0:
						noAtual = getNoById(noAtual.indiceAlternativo)
					else:
						return pilhaAuxiliar[-1]




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

		return None



	def lexico(self):
		listaLex = []
		arq = open(caminho, "Ur")
		titulo = arq.readline()
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
		
		return listaLex