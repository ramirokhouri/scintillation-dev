import pandas as pd

class SUMProcessor(object):
	"""docstring for SUMProcessor"""
	def __init__(self, sums):
		super(SUMProcessor, self).__init__()
		self.sums = sums

class SUM(object):
	"""docstring for SUM"""
	def __init__(self, path):
		super(SUM, self).__init__()
		self.path = path
		self.load_file() 							# metodos con _ y minuscula
		self.parse_hours()
		self.parse_sats()
		self.get_merge_list()

	def load_file(self):
		with open(self.path, "r") as f:
			self.list_of_file = list(f)

	def parse_hours(self):
		"""hour_row_list"""
		list_of_file = self.list_of_file
		HOUR_FIRST_INDEX = 5						# CONSTANTES CON MAYUSCULA
		hour_row_list = [list_of_file[HOUR_FIRST_INDEX].split()]

		#indice del proximo elemento para hour_row_list
		hour_next_index = HOUR_FIRST_INDEX + 1 + int(hour_row_list[-1][1])

		while len(list_of_file) > hour_next_index:
			hour_row_list.append(list_of_file[hour_next_index].split())
			hour_next_index = hour_next_index + 1 + int(hour_row_list[-1][1])

		self.hour_row_list = hour_row_list

	def parse_sats(self):
		"""sat_row_list"""
		sat_row_list  = []
		hour_row_list = self.hour_row_list
		list_of_file  = self.list_of_file

		for row in list_of_file[6:]:
			if row.split() not in hour_row_list:
				sat_row_list.append(row.split())
				sat_row_list[-1][-3] = float(sat_row_list[-1][-3])

		self.sat_row_list = sat_row_list

	def get_merge_list(self):
		"""merge_list"""
		merge_list 	  = []
		hour_row_list = self.hour_row_list
		sat_row_list  = self.sat_row_list
		list_of_file  = self.list_of_file

		LAST = 7		
		for row in sat_row_list[0:LAST]:
			merge_list.append(hour_row_list[0] + row)

		num = LAST + int(hour_row_list[1][1])

		for row in sat_row_list[LAST:num]:
			merge_list.append(hour_row_list[1] + row)

		i = 2 	# indice de la posicion del elemento de la lista hour_row_list

		while i < len(hour_row_list):
			LAST = num
			num = num + int(hour_row_list[i][1])

			for row in sat_row_list[LAST:num]:
				merge_list.append(hour_row_list[i] + row)
			i = i + 1

		year, month, day, hour, minute = list_of_file[3].split()

		for row in merge_list:
			row.insert(0,day)
			row.insert(0,month)
			row.insert(0,year)

		return merge_list

	def sum_to_dataframe(self):
		merge_list = self.get_merge_list()
		df = pd.DataFrame(merge_list)

		#eliminar las columnas innecesarias y dar nombre a las columnas
		del df[4]
		del df[5]
		del df[7]
		del df[8]
		del df[9]
		del df[10]
		del df[11]
		del df[12]
		del df[14]
		del df[15]

		df.columns=['year','month','day','hour','sat','s4']
		df = df.set_index('hour')

		return df


sum = SUM('/home/kuori/Documents/CIASuR dev/sums/120901A0.SUM')
df = sum.sum_to_dataframe()
print df.info()