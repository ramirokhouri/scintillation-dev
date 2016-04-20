# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from core import SUM
from PyQt4 import QtGui, QtCore

writer = pd.ExcelWriter('S4count_excel_test_200416.xlsx')
workbook  = writer.book

class SUMProcessor(object):
	"""docstring for SUMProcessor"""
	def __init__(self, sums_paths):
		super(SUMProcessor, self).__init__()
		self.sums_paths = sums_paths

		for sum_path in sums_paths:
			sum_ = SUM(sum_path)
			df = sum_.sum_to_dataframe()
			result = self.event_count(df)
			if sum_path == sums_paths[0]:
				result_all = result
				first_sum_name = sum_.name
			else: 
				result_all += result

			if sum_path == sums_paths[-1]:
				last_sum_name = sum_.name		

			title = sum_.name[-2:] + '-' + sum_.name[2:4] + '-' + sum_.name[0:2]
			self.excel(title, result)
		
		first_sum_name =  first_sum_name[-2:] + '-' + first_sum_name[2:4] + '-' + first_sum_name[0:2]
		last_sum_name =  last_sum_name[-2:] + '-' + last_sum_name[2:4] + '-' + last_sum_name[0:2]

		title = first_sum_name + ' to ' + last_sum_name
		self.excel(title, result_all)
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

	def excel(self, name, result):
		result.to_excel(writer, sheet_name = name)
		worksheet = writer.sheets[name]
		# Create a chart object.
		chart = workbook.add_chart({'type': 'column'})
		# Configure the series of the chart from the dataframe data.
		chart.add_series({
			'name': '=' + 'Evento 1',
			'categories': '=' + name + '!$A$2:$A$15',
			'values': '=' + name + '!$B$2:$B$15'
			})
		chart.add_series({
			'name': '=' + 'Evento 2',
			'categories': '=' + name + '!$A$2:$A$15',
			'values': '=' + name + '!$C$2:$C$15'
			})

		chart.set_title({
		    'name': name,
		    'name_font': {
		        'name': 'Calibri',
		        'color': 'black',
		    },
		})
		
		chart.set_size({'width': 720, 'height': 576})

		# Chart labels
		chart.set_x_axis({'name': 'Horas'})
		chart.set_y_axis({
			'name': 'Cantidad',
			'min': 0, 'max': 5000
			})
		# Insert the chart into the worksheet.
		worksheet.insert_chart('E2', chart)