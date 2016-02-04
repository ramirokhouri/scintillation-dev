import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from core import SUM
from PyQt4 import QtGui, QtCore

writer = pd.ExcelWriter('S4count_excel_test.xlsx')
workbook  = writer.book

class SUMProcessor(object):
	"""docstring for SUMProcessor"""
	def __init__(self, sums_paths):
		super(SUMProcessor, self).__init__()
		self.sums_paths = sums_paths

		df_list = []
		for sum_path in sums_paths:
			sum_ = SUM(sum_path)
			df = sum_.sum_to_dataframe()
			result = self.event_count(df)
			self.excel(sum_, result)
			df_list.append(result)

		df_result = pd.merge(df_list, how='inner')
		self.excel(sum_, df_result)
		writer.save()

	
	def event_count(self, df):
		#contar evento
		resultado_evt1 = dict()
		resultado_evt2 = dict()

		for hora in range(2100,3500,100):
			df_hora = df.loc[str(hora):str(hora + 59)]
			resultado_evt1[hora] = df_hora[df_hora.s4 > 0.1]["s4"].count()
			resultado_evt2[hora] = df_hora[df_hora.s4 > 0.5]["s4"].count()

		df_evt1 = pd.DataFrame.from_dict(resultado_evt1,orient='index')
		df_evt2 = pd.DataFrame.from_dict(resultado_evt2,orient='index')

		df_evt1.columns=['evt1']
		df_evt1 = df_evt1.sort_index()
		df_evt2.columns=['evt2']
		df_evt2 = df_evt2.sort_index()

		result = df_evt1.join(df_evt2, how='inner')

		return result

	def excel(self, sum_, result):
		result.to_excel(writer, sheet_name = sum_.name)
		worksheet = writer.sheets[sum_.name]
		# Create a chart object.
		chart = workbook.add_chart({'type': 'column'})
		# Configure the series of the chart from the dataframe data.
		chart.add_series({
			'name': '=' + 'Evento 1',
			'categories': '=' + sum_.name + '!$A$2:$A$15',
			'values': '=' + sum_.name + '!$B$2:$B$15'
			})
		chart.add_series({
			'name': '=' + 'Evento 2',
			'categories': '=' + sum_.name + '!$A$2:$A$15',
			'values': '=' + sum_.name + '!$C$2:$C$15'
			})

		chart.set_title({
		    'name': sum_.name,
		    'name_font': {
		        'name': 'Calibri',
		        'color': 'black',
		    },
		})
		
		chart.set_size({'width': 720, 'height': 576})

		# Chart labels
		chart.set_x_axis({'name': 'Horas'})
		chart.set_y_axis({'name': 'Cantidad'})
		# Insert the chart into the worksheet.
		worksheet.insert_chart('E2', chart)


path_list = ['/home/kuori/Documents/CIASuR dev/sums/120901A0.SUM',
'/home/kuori/Documents/CIASuR dev/sums/120902A0.SUM',
'/home/kuori/Documents/CIASuR dev/sums/120903A0.SUM',
'/home/kuori/Documents/CIASuR dev/sums/120904A0.SUM',
'/home/kuori/Documents/CIASuR dev/sums/120905A1.SUM',
'/home/kuori/Documents/CIASuR dev/sums/120906A0.SUM',
'/home/kuori/Documents/CIASuR dev/sums/120907A0.SUM']

sum_processor = SUMProcessor(path_list)