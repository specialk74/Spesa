import sqlite3

connection = sqlite3.connect('database.db')
with open('CreateTables.sql') as f:
	connection.executescript(f.read())
connection.commit()


with open("lista.txt", "r") as listaFile:
	lista = listaFile.readlines()
	for elements in lista:
		try:
			elements = elements.replace('[x]', '')
			elements = elements.replace('[]', '')
			elements = elements.replace('[ ]', '')
			element_list = elements.split()
			if len(element_list) < 3:
				raise Exception("Sorry, no numbers below zero")
			if element_list[0].isnumeric() == False:
				raise Exception("Sorry, no numbers below zero")
			if element_list[1].isnumeric() == False:
				raise Exception("Sorry, no numbers below zero")
			element_list = [element_list[0], element_list[1], ' '.join(element_list[2:])]
			connection.execute('INSERT INTO spesa (name, quantity, category, count, toTake) VALUES (?,?,?,0,0)', (element_list[2], element_list[0], element_list[1]))
			connection.commit()
			print (element_list)
		except:
			pass


connection.close()
