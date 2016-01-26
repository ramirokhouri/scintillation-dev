from dev import get_list
from PyQt4 import QtGui, QtCore
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

writer = pd.ExcelWriter('pandas_simple.xlsx')

def procesar_sum(sum_file_name):

	#obtener el .sum y convertirlo en data frame
	lista = []
	lista = get_list(sum_file_name)
	df = pd.DataFrame(lista)

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

	#contar eventos
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
	# result.plot(kind='bar')

	return result

class Window(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        layout = QtGui.QVBoxLayout(self)
        self.button = QtGui.QPushButton('Select Files', self)
        layout.addWidget(self.button)
        self.button.clicked.connect(self.handleButton)

    def handleButton(self):
    	i = 1
    	title = self.button.text()
    	for path in QtGui.QFileDialog.getOpenFileNames(self, title):
    		print path
        	result = procesar_sum(path)
        	result.to_excel(writer,'hoja'+ str(i))
        	i = i+1
        	# plt.savefig(str(path)+'.png')
        	
        writer.save()

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())