arq = open("teste.txt", "r")
texto = arq.read().replace("\t", "")
for linha in texto.split("\n"):
	for palavra in linha.strip().split():
		if(palavra.isalnum()):
			#analisa palavra
			print palavra
			continue

		text = ""
		for c in palavra:
			if(c.isalnum()):
				text += c
			else:
				if len(text) > 0:
					#analisa text
					print text
					text = ""

				if len(c) > 0:
					#analisa character
					print c