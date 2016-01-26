def get_list(nombrearchivo):
	with open(nombrearchivo,"r") as f:

		list_of_file = list(f)

	##### LISTA HOUR_LIST #####

	hour_first_index = 5

	hour_list = [list_of_file[hour_first_index].split()]

	#obtener cantidad de satelites medidos: bf_index = indice de la linea anterior
	def get_nos(bf_index):
		nos = hour_list[int(bf_index)][1]
		return int(nos)

	#indice del proximo elemento para hour_list
	hour_next_index = hour_first_index + 1 + get_nos(-1)

	while len(list_of_file) > hour_next_index:
		hour_list.append(list_of_file[hour_next_index].split())
		hour_next_index = hour_next_index + get_nos(-1) + 1

	##### FIN LISTA HOUR_LIST #####

	##### LISTA SATELITES #####

	sat_list = []

	for row in list_of_file[6:]:
		if row.split() not in hour_list:
			sat_list.append(row.split())
			sat_list[-1][-3] = float(sat_list[-1][-3])

	##### FIN LISTA SATELITES #####

	##### MERGE #####

	merge_list = []

	for row in sat_list[0:7]:
		merge_list.append(hour_list[0] + row)

	last = 7
	num = 7+int(hour_list[1][1])

	for row in sat_list[last:num]:
		merge_list.append(hour_list[1] + row)

	i = 2

	while i < len(hour_list):
		last = num
		num = num+int(hour_list[i][1])

		for row in sat_list[last:num]:
			merge_list.append(hour_list[i] + row)
		i = i + 1

	##### FIN MERGE #####

	year, month, day, hour, minute = list_of_file[3].split()

	for row in merge_list:
		row.insert(0,day)
		row.insert(0,month)
		row.insert(0,year)

	return merge_list
