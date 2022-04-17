from sqlalchemy import false


class Automaton():

	def __init__(self, config_file):
		self.config_file = config_file
		print("Hi, I'm an automaton!")

	def get_start_state(self):
		"""Return a String
		"""
		for state in self.automaton["States"].keys():
			if self.automaton["States"][state] == "S":
				return state
		return ""

	def is_final_state(self, state):
		return self.automaton["States"].get(state) == "F"

	def validate(self):
		"""Return a Boolean

		Returns true if the config file is valid,
		and raises a ValidationException if the config is invalid.
		"""

		f = open(self.config_file)
		input_str = f.read()

		# parsez input-ul
		sections = ["Sigma", "States", "Transitions"]
		self.automaton = dict()
		self.automaton["Sigma"] = list()
		self.automaton["States"] = dict()
		self.automaton["Transitions"] = dict()

		inside_section = False
		current_section = ''

		for line_index, line in enumerate(input_str.split('\n'), 1):
			# linia nu va avea spatii la inceput si la sfarsit
			line = line.strip()

			if len(line) == 0 or line[0] == '#':
				# linie goala sau comentarii
				continue
			else:
				# linie de cod
				if not inside_section:
					if line[-1] == ':':
						# inceput de sectiune
						line = line[:-1]
						line = line.strip()
						line = line.split()
						if len(line) != 1:
							raise Exception(f'{line_index}: Inceputul sectiunii nu respecta formatul "Sectiune :"')

						# inceputul sectiunii respecta formatul
						line = line[0]
						if line not in sections:
							print(line)
							raise Exception(f'{line_index}: Sectiune necunoscuta: ${line}')

						# incepe o sectiune valida
						inside_section = True
						current_section = line
					else:
						# eroare
						raise Exception(f'{line_index}: Codul trebuie sa fie continut intr-o sectiune')
				else:
					if line == 'End':
						inside_section = False
					else:
						# sunt intr-o sectiune
						# impart linia in cuvinte separate prin virgula
						line = [token.strip() for token in line.split(',')]
						for token in line:
							if len(token.split()) > 1:
								raise Exception(f'{line_index}: Cuvintele trebuie sa fie separate prin virgula')

						if current_section == "Sigma":
							if len(line) > 1:
								raise Exception(f'{line_index}: Cuvintele din Sigma trebuie sa fie pe linii diferite')
							self.automaton["Sigma"].append(line[0])
						elif current_section == "States":
							if len(line) == 1:
								# stare simpla
								self.automaton["States"][line[0]] = ""
							elif len(line) == 2:
								# stare speciala
								if line[1] != "F" and line[1] != "S":
									raise Exception(f'{line_index}: Starile speciale trebuie sa fie initiale (S) sau finale (F)')
								self.automaton["States"][line[0]] = line[1]
							else:
								raise Exception(f'{line_index}: Liniile din sectiunea States trebuie sa contina maxim 2 cuvinte')
						elif current_section == 'Transitions':
							if len(line) != 3:
								raise Exception(f'{line_index}: Liniile din sectiunea Transitions trebuie sa contina fix 3 cuvinte')

							start_state, word, end_state = line
							if start_state not in self.automaton["Transitions"]:
								self.automaton["Transitions"][start_state] = dict()
							self.automaton["Transitions"][start_state][word] = end_state

		# verific sa existe o unica stare initiala
		initial_states = 0
		for state in self.automaton["States"].keys():
			initial_states += (self.automaton["States"][state] == "S")
			if initial_states > 1:
				raise Exception('Prea multe stari initiale')
		if initial_states == 0:
			raise Exception('Nu exista nicio stare initiala')

		# starile care nu au tranzitii vor avea un dictionar gol
		for state in self.automaton["States"].keys():
			if self.automaton["Transitions"].get(state) is None:
				self.automaton["Transitions"][state] = dict()

		# validez tranzitiile
		for state in self.automaton["Transitions"].keys():
			if state not in self.automaton["States"].keys():
				raise Exception(f'Starea "{state}" nu apare in States')

			for token in self.automaton["Transitions"][state].keys():
				if token not in self.automaton["Sigma"]:
					raise Exception(f'Cuvantul "{token}" nu apare in Sigma')
				
				end_state = self.automaton["Transitions"][state][token]
				if end_state not in self.automaton["States"].keys():
					raise Exception(f'Starea "{end_state}" nu apare in States')

		return True

	def accepts_input(self, input_str):
		"""Return a Boolean

		Returns True if the input is accepted,
		and it returns False if the input is rejected.
		"""
		pass

	def read_input(self, input_str):
		"""Return the self.automaton's final configuration
		
		If the input is rejected, the method raises a
		RejectionException.
		"""
		pass

if __name__ == "__main__":
	a = Automaton('my_config.txt')
	print(a.validate())
