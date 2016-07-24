import requests
import time
import datetime

class CityList(object): #object to hold dictionary of city info and IDs
	def __init__(self, name, city_dict = {}):
		self.name = name
		self.city_dict = {}
		
	def create_list(self):
		self.city_dict = {
			1: ['London', 2643743],
			2: ['Paris', 6455259],
			3: ['San Juan', 3929520],
			4: ['Bangkok', 1609350],
			5: ['Melbourne', 7839805],
			6: ['Albany', 4670094],
			7: ['Omaha', 4716696],
			8: ['Memphis', 5001644],
			9: ['Havana', 3553478],
			10: ['Saint Thomas Island', 7267904]
			}
		print 'test'
		print 'test again'
#test for commit
#test2
	def set_city(self):
		self.create_list()
		for city in self.city_dict:
			print str(city) + ': ' + self.city_dict[city][0]
		print '************************'
		print 'Please enter the ID above to select the city'
		choosing = True
		while choosing:
			try:
				choice = int(raw_input('? '))
				if choice in self.city_dict:
					request_param.city_ID = self.city_dict[choice][1]
					request_param.city_name = self.city_dict[choice][0]
					print 'You have selected ' + self.city_dict[choice][0]
					choosing = False
				else:
					print 'Please only enter an ID from the list above'
			except ValueError:
				print 'Please only enter an integer from the list above'
			
class TestData(object):
	def __init__(self, name, data):
		self.name = name
		self.data = {}

class RequestParam(object):
	#setting parameters for pulling data
	def __init__(self, name, city_name, city_ID, AAPID):
		self.name = name
		self.city_name = 'London'
		self.city_ID = 2643743 #setting default city ID
		self.APPID = '0ea823f0dd4547879b33ceaaad52a60e' #default API key
		
class WeatherData(object):
	def __init__(self, name, all_data = {}, noon_data = {}, date_dict = {}, sum_data = {}, weekday_dict = {}):
		self.name = name
		self.all_data = {} #dict for all api data returned
		self.noon_data = {} #dict for all weather data at noon
		self.date_dict = {} #dict for formatted dates and times
		self.sum_data = {} #dict for all summary weather data [date, time, temp hi, temp lo, temp, weather description]
		self.weekday_dict = {} #dict for formatted dates and weekday
		
	def get_data(self):
	#for pulling data
		data = {'id': request_param.city_ID, 'APPID': request_param.APPID, 'units': 'metric'}
		get_weather = requests.get("http://api.openweathermap.org/data/2.5/forecast/city", params=data)
		if get_weather.status_code == 200:
			pass
		else:
			print 'API error'
			print get_weather.status_code
			return
		self.all_data = get_weather.json()
		print 'data retrieved'
		#self.all_data = test_data.data #for testing
	
	def date_manage(self):
	#to reformat yyyy-mm-dd dates, get day names, and split out times
		a = 0 #this increment can be used as a key consistent across dictionaries
		for x in self.all_data['list']:
			ddd = [self.all_data['list'][a]['dt_txt'].split(' ')]
			r1 = ddd[0][0]
			r = r1.split('-')
			new_date_obj = datetime.date(int(r[0]), int(r[1]), int(r[2]))
			new_date_data = (new_date_obj.strftime('%A'), new_date_obj.strftime('%x')) #makes a tuple of weekday (%A) and formatted date (%x)
			#new_date = datetime.datetime.strptime(r, '%Y-%m-%d').strftime('%m/%d/%y')
			ddd.append(new_date_data)
			self.date_dict[a] = ddd # list ... 0 = yyyy-mm-dd, 1 = time 06:00:00, 2 = tuple (weekday, formatted date)
			if new_date_data[1] in self.weekday_dict:
				pass
			else:
				z = new_date_data[1]
				self.weekday_dict[z] = [new_date_data][0]
			a += 1
		
	def assign_data(self):
	#to populate dictionaries
	# can add data to dictionary with value as a list using append.  Example ap_dict[1] = [1,2,3] ...then... ap_dict[1].append(4) gives [1,2,3,4]
		self.date_manage()
		a = 0
		for x in self.all_data['list']:
			weather_description = self.all_data['list'][a]['weather'][0]['description']
			temp_max = self.all_data['list'][a]['main']['temp_max']
			temp_min = self.all_data['list'][a]['main']['temp_min']
			temp = self.all_data['list'][a]['main']['temp']
			self.sum_data[a] = [self.date_dict[a][1], self.date_dict[a][0][1], [weather_description, temp_max, temp_min, temp]]
			a += 1
		for y in self.date_dict:
			if self.date_dict[y][0][1] == '12:00:00':
				self.noon_data[y] = [self.date_dict[y][1], self.date_dict[y][0][1], self.sum_data[y][2]] # list ... 0 = tuple (weekday, formatted date), 1 = time, 2 = list 0 = weather description, 1 = temp max, 2 = temp min, 3 = temp
			else:
				pass			

class DisplayData(object):
	#displaying data
	def __init__(self, name, all_temp_dict = {}, avg_temp_dict = {}, descrip_rank = {}, descrip_dict = {}, descrip_processing = {}, descrip_avg = {}):
		self.name = name
		self.all_temp_dict = {}
		self.avg_temp_dict = {}
		self.descrip_rank = {}
		self.descrip_dict = {} #for all descriptions
		self.descrip_processing = {} #to append rank info
		self.descrip_avg = {} #for the final descriptions to be used
		
	def descrip_populate(self):
		self.descrip_rank = {
			0: ['thunder', 'storm', 'hail', 'tornado', 'hurricane', 'flood'],
			1: ['rain', 'shower'],
			2: ['heavy', 'high', 'strong', 'wind']
			}
		
	def easy_print(self): #prints data at noon every day
		noon_list = []
		print 'data at noon'
		for r in weather_data.noon_data:
			noon_list.append(r)
		noon_list.sort()
		for x in noon_list:
			print weather_data.noon_data[x][0][0], weather_data.noon_data[x][0][1] #weekday, date
			print 'weather description:', weather_data.noon_data[x][2][0], '|| Avg temp:', weather_data.noon_data[x][2][3] #sum data
			print '******************************************************************************'
			
	def compute_avg_temp(self):
		self.all_temp_dict = {} #all high and low temps for each 3 hour block, grouped by day, using 'dd-mm-yy' as the dict key
		self.avg_temp_dict = {} #dict for daily averages
		for x in weather_data.sum_data:
			block_date = weather_data.sum_data[x][0][1] 
			if block_date in self.all_temp_dict:
				self.all_temp_dict[block_date].append(weather_data.sum_data[x][2][1])
				self.all_temp_dict[block_date].append(weather_data.sum_data[x][2][2])
			else:
				self.all_temp_dict[block_date] = [weather_data.sum_data[x][2][1], weather_data.sum_data[x][2][2]]
		for day in self.all_temp_dict:
			day_avg_list = self.all_temp_dict[day]
			day_avg = sum(day_avg_list) / float(len(day_avg_list))
			self.avg_temp_dict[day] = [day_avg] #key: date 'mm/dd/yy' value: temp avg
			for g in weather_data.noon_data:
				g_date = weather_data.noon_data[g][0][1]
				if g_date in self.avg_temp_dict: #need to get rid of duplicate descriptions
					self.avg_temp_dict[g_date].append(weather_data.noon_data[g][2][0])
				else:
					pass
		
		
	def avg_descrip(self): #takes descriptions for each 3 hour block and decides which description should be the day summary
		from collections import Counter
		self.descrip_populate() #populates the directory that has priority keywords
		#first gather all descriptions in a dict[day] = [description list]
		#then see if any descriptions have the priority strings in self.descrip_rank. If so, take the description that contains the highest priority string 
		#(multiple descriptions are ok for one day if they are in the same priority rank)
		#If no descriptions have priority strings then take the description which appears the most throughout the day
		for x in weather_data.sum_data: #building the dictionary of {date: [description, description,etc]}
			x_date = weather_data.sum_data[x][0][1]
			if x_date in self.descrip_dict:
				self.descrip_dict[x_date].append(weather_data.sum_data[x][2][0])
			else:
				self.descrip_dict[x_date] = [weather_data.sum_data[x][2][0]]
		for y in self.descrip_dict: #going date by date
			for g in self.descrip_dict[y]: #going description by description in each date
				for d in self.descrip_rank: #going rank by rank in descrip_rank
					rank = d
					position = 0
					for e in self.descrip_rank[d]: #going keyword by keyword for each rank in descrip_rank
						priority_str = self.descrip_rank[d][position]
						if priority_str in g: #looking for the priority string in each description 
							#store the priority string somewhere and its rank (key)
							priority_dict = {}
							priority_dict[rank] = g #if keyword is found this dict is populated with [rank] = [string]. It is emptied again every time through the loop
							self.descrip_processing[y] = []
							self.descrip_processing[y].append(priority_dict) #descrip_processing dict[date] is appended with priority dict inside a list [date] = [{rank: 'string'}, {etc}]
							position += 1
						else:
							position += 1
		#that should cover the priority words. Next step is to assign any date without a priority description to whichever description appears the most often through the day
		for b in self.descrip_dict:
			if b in self.descrip_processing: #if the date already exists in the dict we don't want to add anything else
				pass
			else: #if not we want to find the most common description
				descrip_list = []
				descrip_list = self.descrip_dict[b]
				b_descrip = Counter(descrip_list)
				highest_descrip = b_descrip.most_common(1) #work this into the dict add
				self.descrip_processing[b] = [{3: highest_descrip[0][0]}]
		'''print self.descrip_dict
		print self.avg_temp_dict
		print self.descrip_processing
		raw_input()'''
		

	def display_day_avg(self):
		# self.avg_temp_dict is dict for temps. Uses {'date': [avg temp, 'descriptions'], etc}
		# self.descrip_processing Uses {'date': [{rank: 'description'}, {rank: 'description'}, etc], etc}
		print_dict = {} # {'date': ['day name', avg temp, [description, description]]}
		for x in self.avg_temp_dict:
			print_dict[x] = [weather_data.weekday_dict[x][0], self.avg_temp_dict[x][0]] # 'date' : ['day name', avg temp]
		for y in self.descrip_processing:
			temp_descrip_list = []
			rank_list = []
			description_location_count = len(self.descrip_processing[y]) #self.description_processing[y] is [{rank: 'description}, etc]
			for d in range(description_location_count):
				pos = d-1
				rank_key_list = self.descrip_processing[y][pos].keys()
				rank_list.append(rank_key_list[0])
			top_rank = rank_list[0]
			for item in range(description_location_count):
				check_rank = self.descrip_processing[y][item].keys()[0]
				if check_rank == top_rank:
					if self.descrip_processing[y][item][check_rank] in print_dict[y]:
						pass
					else:
						print_dict[y].append(self.descrip_processing[y][item][check_rank]) 
		print_date_list = print_dict.keys()
		print_date_list.sort()
		for print_date in print_date_list:
			print '******************************************************************************'
			print print_dict[print_date][0] + ' ' + print_date
			print 'Average Temperature: ' + str(print_dict[print_date][1])
			print print_dict[print_date][2]
			print '******************************************************************************'
						
		

class FlowManage(object):
	#to manage the workflow
	def __init__(self, name):
		self.name = name
		
	def flow(self):
		print '************************************'
		print 'Welcome to the weather portal!'
		print 'The selected city is ' + request_param.city_name
		print '************************************'
		choosing = True
		while choosing:
			choice = raw_input('Would you like to change the city (Y/N)? ')
			if choice.upper() == 'Y':
				city_list.set_city()
				choosing = False
			elif choice.upper() == 'N':
				choosing = False
			else:
				 print 'Please only enter Y or N'
				 choosing = True
		weather_data.get_data()
		weather_data.assign_data()
		print 'Daily weather data for ' + str(request_param.city_name)
		#display_data.easy_print()
		#print weather_data.noon_data
		#print display_data.avg_temp_dict
		display_data.compute_avg_temp()
		display_data.avg_descrip()
		display_data.display_day_avg()		
	
def main():
	running = True
	while running:
		flow_manage.flow()
		choice = raw_input('would you like to run it again? Y/N ')
		if choice.upper() == 'Y':
			running = True
		elif choice.upper() == 'N':
			running = False
		else:
			print 'please only enter Y or N'
			running = True
	print 'Goodbye'

city_list = CityList('city', {})
test_data = TestData('test', {})
weather_data = WeatherData('Weather', {}, {}, {}, {}, {})
flow_manage = FlowManage('Flow Manage')
display_data = DisplayData('Display Data', {}, {}, {}, {}, {}, {})
request_param = RequestParam('request', 'city_name', 111, 'AAPID')
test_data.data = {u'city': {u'name': u'London', u'country': u'GB', u'coord': {u'lat': 51.50853, u'lon': -0.12574}, u'sys': {u'population': 0}, u'id': 2643743, u'population': 0}, u'message': 0.3365, u'list': [{u'clouds': {u'all': 44}, u'rain': {u'3h': 0.005}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2016-07-12 18:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10d', u'description': u'light rain'}], u'dt': 1468346400, u'main': {u'temp_kf': -0.22, u'temp': 290.68, u'grnd_level': 1017.85, u'temp_max': 290.908, u'sea_level': 1025.36, u'humidity': 70, u'pressure': 1017.85, u'temp_min': 290.68}, u'wind': {u'speed': 2.41, u'deg': 324.004}}, {u'clouds': {u'all': 88}, u'rain': {u'3h': 0.035}, u'sys': {u'pod': u'n'}, u'dt_txt': u'2016-07-12 21:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10n', u'description': u'light rain'}], u'dt': 1468357200, u'main': {u'temp_kf': -0.15, u'temp': 288, u'grnd_level': 1019.03, u'temp_max': 288.145, u'sea_level': 1026.39, u'humidity': 77, u'pressure': 1019.03, u'temp_min': 288}, u'wind': {u'speed': 2.77, u'deg': 305.502}}, {u'clouds': {u'all': 88}, u'rain': {u'3h': 0.39}, u'sys': {u'pod': u'n'}, u'dt_txt': u'2016-07-13 00:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10n', u'description': u'light rain'}], u'dt': 1468368000, u'main': {u'temp_kf': -0.07, u'temp': 286.89, u'grnd_level': 1019.63, u'temp_max': 286.965, u'sea_level': 1027.13, u'humidity': 81, u'pressure': 1019.63, u'temp_min': 286.89}, u'wind': {u'speed': 3.37, u'deg': 332.003}}, {u'clouds': {u'all': 68}, u'rain': {u'3h': 0.1}, u'sys': {u'pod': u'n'}, u'dt_txt': u'2016-07-13 03:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10n', u'description': u'light rain'}], u'dt': 1468378800, u'main': {u'temp_kf': 0, u'temp': 284.346, u'grnd_level': 1020.26, u'temp_max': 284.346, u'sea_level': 1027.8, u'humidity': 79, u'pressure': 1020.26, u'temp_min': 284.346}, u'wind': {u'speed': 3.48, u'deg': 327.501}}, {u'clouds': {u'all': 56}, u'rain': {}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2016-07-13 06:00:00', u'weather': [{u'main': u'Clouds', u'id': 803, u'icon': u'04d', u'description': u'broken clouds'}], u'dt': 1468389600, u'main': {u'temp_kf': 0, u'temp': 284.451, u'grnd_level': 1021.31, u'temp_max': 284.451, u'sea_level': 1028.84, u'humidity': 80, u'pressure': 1021.31, u'temp_min': 284.451}, u'wind': {u'speed': 3.57, u'deg': 318.501}}, {u'clouds': {u'all': 44}, u'rain': {}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2016-07-13 09:00:00', u'weather': [{u'main': u'Clouds', u'id': 802, u'icon': u'03d', u'description': u'scattered clouds'}], u'dt': 1468400400, u'main': {u'temp_kf': 0, u'temp': 288.397, u'grnd_level': 1022.03, u'temp_max': 288.397, u'sea_level': 1029.56, u'humidity': 77, u'pressure': 1022.03, u'temp_min': 288.397}, u'wind': {u'speed': 3.66, u'deg': 323.003}}, {u'clouds': {u'all': 20}, u'rain': {}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2016-07-13 12:00:00', u'weather': [{u'main': u'Clouds', u'id': 801, u'icon': u'02d', u'description': u'few clouds'}], u'dt': 1468411200, u'main': {u'temp_kf': 0, u'temp': 290.63, u'grnd_level': 1022.83, u'temp_max': 290.63, u'sea_level': 1030.28, u'humidity': 69, u'pressure': 1022.83, u'temp_min': 290.63}, u'wind': {u'speed': 4.21, u'deg': 311.506}}, {u'clouds': {u'all': 88}, u'rain': {}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2016-07-13 15:00:00', u'weather': [{u'main': u'Clouds', u'id': 804, u'icon': u'04d', u'description': u'overcast clouds'}], u'dt': 1468422000, u'main': {u'temp_kf': 0, u'temp': 290.652, u'grnd_level': 1023.52, u'temp_max': 290.652, u'sea_level': 1030.96, u'humidity': 59, u'pressure': 1023.52, u'temp_min': 290.652}, u'wind': {u'speed': 4.93, u'deg': 308.504}}, {u'clouds': {u'all': 68}, u'rain': {}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2016-07-13 18:00:00', u'weather': [{u'main': u'Clouds', u'id': 803, u'icon': u'04d', u'description': u'broken clouds'}], u'dt': 1468432800, u'main': {u'temp_kf': 0, u'temp': 290.176, u'grnd_level': 1024.65, u'temp_max': 290.176, u'sea_level': 1032.14, u'humidity': 56, u'pressure': 1024.65, u'temp_min': 290.176}, u'wind': {u'speed': 4.57, u'deg': 310.504}}, {u'clouds': {u'all': 0}, u'rain': {}, u'sys': {u'pod': u'n'}, u'dt_txt': u'2016-07-13 21:00:00', u'weather': [{u'main': u'Clear', u'id': 800, u'icon': u'01n', u'description': u'clear sky'}], u'dt': 1468443600, u'main': {u'temp_kf': 0, u'temp': 287.804, u'grnd_level': 1026.28, u'temp_max': 287.804, u'sea_level': 1033.84, u'humidity': 60, u'pressure': 1026.28, u'temp_min': 287.804}, u'wind': {u'speed': 4, u'deg': 314.005}}, {u'clouds': {u'all': 0}, u'rain': {}, u'sys': {u'pod': u'n'}, u'dt_txt': u'2016-07-14 00:00:00', u'weather': [{u'main': u'Clear', u'id': 800, u'icon': u'01n', u'description': u'clear sky'}], u'dt': 1468454400, u'main': {u'temp_kf': 0, u'temp': 285.09, u'grnd_level': 1027.41, u'temp_max': 285.09, u'sea_level': 1034.97, u'humidity': 69, u'pressure': 1027.41, u'temp_min': 285.09}, u'wind': {u'speed': 3.31, u'deg': 314.501}}, {u'clouds': {u'all': 0}, u'rain': {}, u'sys': {u'pod': u'n'}, u'dt_txt': u'2016-07-14 03:00:00', u'weather': [{u'main': u'Clear', u'id': 800, u'icon': u'01n', u'description': u'clear sky'}], u'dt': 1468465200, u'main': {u'temp_kf': 0, u'temp': 282.827, u'grnd_level': 1028.13, u'temp_max': 282.827, u'sea_level': 1035.72, u'humidity': 80, u'pressure': 1028.13, u'temp_min': 282.827}, u'wind': {u'speed': 2.8, u'deg': 299.005}}, {u'clouds': {u'all': 0}, u'rain': {}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2016-07-14 06:00:00', u'weather': [{u'main': u'Clear', u'id': 800, u'icon': u'01d', u'description': u'clear sky'}], u'dt': 1468476000, u'main': {u'temp_kf': 0, u'temp': 283.864, u'grnd_level': 1028.77, u'temp_max': 283.864, u'sea_level': 1036.48, u'humidity': 78, u'pressure': 1028.77, u'temp_min': 283.864}, u'wind': {u'speed': 2.91, u'deg': 287.001}}, {u'clouds': {u'all': 0}, u'rain': {}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2016-07-14 09:00:00', u'weather': [{u'main': u'Clear', u'id': 800, u'icon': u'01d', u'description': u'clear sky'}], u'dt': 1468486800, u'main': {u'temp_kf': 0, u'temp': 289.656, u'grnd_level': 1029.22, u'temp_max': 289.656, u'sea_level': 1036.8, u'humidity': 70, u'pressure': 1029.22, u'temp_min': 289.656}, u'wind': {u'speed': 2.9, u'deg': 293.501}}, {u'clouds': {u'all': 68}, u'rain': {}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2016-07-14 12:00:00', u'weather': [{u'main': u'Clouds', u'id': 803, u'icon': u'04d', u'description': u'broken clouds'}], u'dt': 1468497600, u'main': {u'temp_kf': 0, u'temp': 291.467, u'grnd_level': 1029.2, u'temp_max': 291.467, u'sea_level': 1036.73, u'humidity': 63, u'pressure': 1029.2, u'temp_min': 291.467}, u'wind': {u'speed': 3.87, u'deg': 276.002}}, {u'clouds': {u'all': 76}, u'rain': {}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2016-07-14 15:00:00', u'weather': [{u'main': u'Clouds', u'id': 803, u'icon': u'04d', u'description': u'broken clouds'}], u'dt': 1468508400, u'main': {u'temp_kf': 0, u'temp': 292.174, u'grnd_level': 1028.99, u'temp_max': 292.174, u'sea_level': 1036.48, u'humidity': 55, u'pressure': 1028.99, u'temp_min': 292.174}, u'wind': {u'speed': 4.41, u'deg': 276.003}}, {u'clouds': {u'all': 92}, u'rain': {u'3h': 0.005}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2016-07-14 18:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10d', u'description': u'light rain'}], u'dt': 1468519200, u'main': {u'temp_kf': 0, u'temp': 291.688, u'grnd_level': 1028.76, u'temp_max': 291.688, u'sea_level': 1036.32, u'humidity': 52, u'pressure': 1028.76, u'temp_min': 291.688}, u'wind': {u'speed': 4.21, u'deg': 276.004}}, {u'clouds': {u'all': 56}, u'rain': {}, u'sys': {u'pod': u'n'}, u'dt_txt': u'2016-07-14 21:00:00', u'weather': [{u'main': u'Clouds', u'id': 803, u'icon': u'04n', u'description': u'broken clouds'}], u'dt': 1468530000, u'main': {u'temp_kf': 0, u'temp': 289.126, u'grnd_level': 1028.96, u'temp_max': 289.126, u'sea_level': 1036.45, u'humidity': 57, u'pressure': 1028.96, u'temp_min': 289.126}, u'wind': {u'speed': 2.88, u'deg': 267.502}}, {u'clouds': {u'all': 56}, u'rain': {}, u'sys': {u'pod': u'n'}, u'dt_txt': u'2016-07-15 00:00:00', u'weather': [{u'main': u'Clouds', u'id': 803, u'icon': u'04n', u'description': u'broken clouds'}], u'dt': 1468540800, u'main': {u'temp_kf': 0, u'temp': 287.32, u'grnd_level': 1028.76, u'temp_max': 287.32, u'sea_level': 1036.33, u'humidity': 61, u'pressure': 1028.76, u'temp_min': 287.32}, u'wind': {u'speed': 3.2, u'deg': 257.5}}, {u'clouds': {u'all': 68}, u'rain': {}, u'sys': {u'pod': u'n'}, u'dt_txt': u'2016-07-15 03:00:00', u'weather': [{u'main': u'Clouds', u'id': 803, u'icon': u'04n', u'description': u'broken clouds'}], u'dt': 1468551600, u'main': {u'temp_kf': 0, u'temp': 286.273, u'grnd_level': 1028.04, u'temp_max': 286.273, u'sea_level': 1035.62, u'humidity': 66, u'pressure': 1028.04, u'temp_min': 286.273}, u'wind': {u'speed': 2.41, u'deg': 248.007}}, {u'clouds': {u'all': 76}, u'rain': {u'3h': 0.02}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2016-07-15 06:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10d', u'description': u'light rain'}], u'dt': 1468562400, u'main': {u'temp_kf': 0, u'temp': 286.299, u'grnd_level': 1027.08, u'temp_max': 286.299, u'sea_level': 1034.7, u'humidity': 79, u'pressure': 1027.08, u'temp_min': 286.299}, u'wind': {u'speed': 3.26, u'deg': 218.001}}, {u'clouds': {u'all': 92}, u'rain': {u'3h': 0.21}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2016-07-15 09:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10d', u'description': u'light rain'}], u'dt': 1468573200, u'main': {u'temp_kf': 0, u'temp': 287.982, u'grnd_level': 1026.22, u'temp_max': 287.982, u'sea_level': 1033.7, u'humidity': 79, u'pressure': 1026.22, u'temp_min': 287.982}, u'wind': {u'speed': 5.58, u'deg': 215.001}}, {u'clouds': {u'all': 92}, u'rain': {u'3h': 0.67}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2016-07-15 12:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10d', u'description': u'light rain'}], u'dt': 1468584000, u'main': {u'temp_kf': 0, u'temp': 288.755, u'grnd_level': 1025.05, u'temp_max': 288.755, u'sea_level': 1032.53, u'humidity': 82, u'pressure': 1025.05, u'temp_min': 288.755}, u'wind': {u'speed': 6.38, u'deg': 218.01}}, {u'clouds': {u'all': 92}, u'rain': {u'3h': 0.9}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2016-07-15 15:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10d', u'description': u'light rain'}], u'dt': 1468594800, u'main': {u'temp_kf': 0, u'temp': 290.723, u'grnd_level': 1023.48, u'temp_max': 290.723, u'sea_level': 1030.96, u'humidity': 82, u'pressure': 1023.48, u'temp_min': 290.723}, u'wind': {u'speed': 5.85, u'deg': 222.003}}, {u'clouds': {u'all': 92}, u'rain': {u'3h': 0.13}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2016-07-15 18:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10d', u'description': u'light rain'}], u'dt': 1468605600, u'main': {u'temp_kf': 0, u'temp': 292.663, u'grnd_level': 1021.83, u'temp_max': 292.663, u'sea_level': 1029.3, u'humidity': 78, u'pressure': 1021.83, u'temp_min': 292.663}, u'wind': {u'speed': 6.07, u'deg': 228.001}}, {u'clouds': {u'all': 64}, u'rain': {u'3h': 0.13}, u'sys': {u'pod': u'n'}, u'dt_txt': u'2016-07-15 21:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10n', u'description': u'light rain'}], u'dt': 1468616400, u'main': {u'temp_kf': 0, u'temp': 291.603, u'grnd_level': 1021.62, u'temp_max': 291.603, u'sea_level': 1029, u'humidity': 81, u'pressure': 1021.62, u'temp_min': 291.603}, u'wind': {u'speed': 6.11, u'deg': 229.502}}, {u'clouds': {u'all': 76}, u'rain': {u'3h': 0.09}, u'sys': {u'pod': u'n'}, u'dt_txt': u'2016-07-16 00:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10n', u'description': u'light rain'}], u'dt': 1468627200, u'main': {u'temp_kf': 0, u'temp': 290.827, u'grnd_level': 1020.88, u'temp_max': 290.827, u'sea_level': 1028.36, u'humidity': 85, u'pressure': 1020.88, u'temp_min': 290.827}, u'wind': {u'speed': 5.9, u'deg': 229}}, {u'clouds': {u'all': 92}, u'rain': {u'3h': 0.28}, u'sys': {u'pod': u'n'}, u'dt_txt': u'2016-07-16 03:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10n', u'description': u'light rain'}], u'dt': 1468638000, u'main': {u'temp_kf': 0, u'temp': 290.188, u'grnd_level': 1019.67, u'temp_max': 290.188, u'sea_level': 1027.15, u'humidity': 87, u'pressure': 1019.67, u'temp_min': 290.188}, u'wind': {u'speed': 5.72, u'deg': 225}}, {u'clouds': {u'all': 92}, u'rain': {u'3h': 0.85}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2016-07-16 06:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10d', u'description': u'light rain'}], u'dt': 1468648800, u'main': {u'temp_kf': 0, u'temp': 289.028, u'grnd_level': 1019.44, u'temp_max': 289.028, u'sea_level': 1026.88, u'humidity': 94, u'pressure': 1019.44, u'temp_min': 289.028}, u'wind': {u'speed': 5.17, u'deg': 228}}, {u'clouds': {u'all': 92}, u'rain': {u'3h': 0.81}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2016-07-16 09:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10d', u'description': u'light rain'}], u'dt': 1468659600, u'main': {u'temp_kf': 0, u'temp': 289.627, u'grnd_level': 1019.5, u'temp_max': 289.627, u'sea_level': 1026.97, u'humidity': 95, u'pressure': 1019.5, u'temp_min': 289.627}, u'wind': {u'speed': 4.21, u'deg': 234.501}}, {u'clouds': {u'all': 92}, u'rain': {u'3h': 2.32}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2016-07-16 12:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10d', u'description': u'light rain'}], u'dt': 1468670400, u'main': {u'temp_kf': 0, u'temp': 289.154, u'grnd_level': 1019.65, u'temp_max': 289.154, u'sea_level': 1027.09, u'humidity': 98, u'pressure': 1019.65, u'temp_min': 289.154}, u'wind': {u'speed': 4.12, u'deg': 242.004}}, {u'clouds': {u'all': 8}, u'rain': {u'3h': 0.5}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2016-07-16 15:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10d', u'description': u'light rain'}], u'dt': 1468681200, u'main': {u'temp_kf': 0, u'temp': 289.442, u'grnd_level': 1019.21, u'temp_max': 289.442, u'sea_level': 1026.6, u'humidity': 90, u'pressure': 1019.21, u'temp_min': 289.442}, u'wind': {u'speed': 4.91, u'deg': 227}}, {u'clouds': {u'all': 48}, u'rain': {u'3h': 0.1}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2016-07-16 18:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10d', u'description': u'light rain'}], u'dt': 1468692000, u'main': {u'temp_kf': 0, u'temp': 289.982, u'grnd_level': 1018.95, u'temp_max': 289.982, u'sea_level': 1026.43, u'humidity': 87, u'pressure': 1018.95, u'temp_min': 289.982}, u'wind': {u'speed': 4.66, u'deg': 246.503}}, {u'clouds': {u'all': 8}, u'rain': {u'3h': 0.01}, u'sys': {u'pod': u'n'}, u'dt_txt': u'2016-07-16 21:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10n', u'description': u'light rain'}], u'dt': 1468702800, u'main': {u'temp_kf': 0, u'temp': 288.037, u'grnd_level': 1020.04, u'temp_max': 288.037, u'sea_level': 1027.53, u'humidity': 85, u'pressure': 1020.04, u'temp_min': 288.037}, u'wind': {u'speed': 4.11, u'deg': 259.501}}], u'cod': u'200', u'cnt': 34}

#test_data = {u'city': {u'name': u'London', u'country': u'GB', u'coord': {u'lat': 51.50853, u'lon': -0.12574}, u'sys': {u'population': 0}, u'id': 2643743, u'population': 0}, u'message': 0.3365, u'list': [{u'clouds': {u'all': 44}, u'rain': {u'3h': 0.005}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2016-07-12 18:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10d', u'description': u'light rain'}], u'dt': 1468346400, u'main': {u'temp_kf': -0.22, u'temp': 290.68, u'grnd_level': 1017.85, u'temp_max': 290.908, u'sea_level': 1025.36, u'humidity': 70, u'pressure': 1017.85, u'temp_min': 290.68}, u'wind': {u'speed': 2.41, u'deg': 324.004}}, {u'clouds': {u'all': 88}, u'rain': {u'3h': 0.035}, u'sys': {u'pod': u'n'}, u'dt_txt': u'2016-07-12 21:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10n', u'description': u'light rain'}], u'dt': 1468357200, u'main': {u'temp_kf': -0.15, u'temp': 288, u'grnd_level': 1019.03, u'temp_max': 288.145, u'sea_level': 1026.39, u'humidity': 77, u'pressure': 1019.03, u'temp_min': 288}, u'wind': {u'speed': 2.77, u'deg': 305.502}}, {u'clouds': {u'all': 88}, u'rain': {u'3h': 0.39}, u'sys': {u'pod': u'n'}, u'dt_txt': u'2016-07-13 00:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10n', u'description': u'light rain'}], u'dt': 1468368000, u'main': {u'temp_kf': -0.07, u'temp': 286.89, u'grnd_level': 1019.63, u'temp_max': 286.965, u'sea_level': 1027.13, u'humidity': 81, u'pressure': 1019.63, u'temp_min': 286.89}, u'wind': {u'speed': 3.37, u'deg': 332.003}}, {u'clouds': {u'all': 68}, u'rain': {u'3h': 0.1}, u'sys': {u'pod': u'n'}, u'dt_txt': u'2016-07-13 03:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10n', u'description': u'light rain'}], u'dt': 1468378800, u'main': {u'temp_kf': 0, u'temp': 284.346, u'grnd_level': 1020.26, u'temp_max': 284.346, u'sea_level': 1027.8, u'humidity': 79, u'pressure': 1020.26, u'temp_min': 284.346}, u'wind': {u'speed': 3.48, u'deg': 327.501}}, {u'clouds': {u'all': 56}, u'rain': {}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2016-07-13 06:00:00', u'weather': [{u'main': u'Clouds', u'id': 803, u'icon': u'04d', u'description': u'broken clouds'}], u'dt': 1468389600, u'main': {u'temp_kf': 0, u'temp': 284.451, u'grnd_level': 1021.31, u'temp_max': 284.451, u'sea_level': 1028.84, u'humidity': 80, u'pressure': 1021.31, u'temp_min': 284.451}, u'wind': {u'speed': 3.57, u'deg': 318.501}}, {u'clouds': {u'all': 44}, u'rain': {}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2016-07-13 09:00:00', u'weather': [{u'main': u'Clouds', u'id': 802, u'icon': u'03d', u'description': u'scattered clouds'}], u'dt': 1468400400, u'main': {u'temp_kf': 0, u'temp': 288.397, u'grnd_level': 1022.03, u'temp_max': 288.397, u'sea_level': 1029.56, u'humidity': 77, u'pressure': 1022.03, u'temp_min': 288.397}, u'wind': {u'speed': 3.66, u'deg': 323.003}}, {u'clouds': {u'all': 20}, u'rain': {}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2016-07-13 12:00:00', u'weather': [{u'main': u'Clouds', u'id': 801, u'icon': u'02d', u'description': u'few clouds'}], u'dt': 1468411200, u'main': {u'temp_kf': 0, u'temp': 290.63, u'grnd_level': 1022.83, u'temp_max': 290.63, u'sea_level': 1030.28, u'humidity': 69, u'pressure': 1022.83, u'temp_min': 290.63}, u'wind': {u'speed': 4.21, u'deg': 311.506}}, {u'clouds': {u'all': 88}, u'rain': {}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2016-07-13 15:00:00', u'weather': [{u'main': u'Clouds', u'id': 804, u'icon': u'04d', u'description': u'overcast clouds'}], u'dt': 1468422000, u'main': {u'temp_kf': 0, u'temp': 290.652, u'grnd_level': 1023.52, u'temp_max': 290.652, u'sea_level': 1030.96, u'humidity': 59, u'pressure': 1023.52, u'temp_min': 290.652}, u'wind': {u'speed': 4.93, u'deg': 308.504}}, {u'clouds': {u'all': 68}, u'rain': {}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2016-07-13 18:00:00', u'weather': [{u'main': u'Clouds', u'id': 803, u'icon': u'04d', u'description': u'broken clouds'}], u'dt': 1468432800, u'main': {u'temp_kf': 0, u'temp': 290.176, u'grnd_level': 1024.65, u'temp_max': 290.176, u'sea_level': 1032.14, u'humidity': 56, u'pressure': 1024.65, u'temp_min': 290.176}, u'wind': {u'speed': 4.57, u'deg': 310.504}}, {u'clouds': {u'all': 0}, u'rain': {}, u'sys': {u'pod': u'n'}, u'dt_txt': u'2016-07-13 21:00:00', u'weather': [{u'main': u'Clear', u'id': 800, u'icon': u'01n', u'description': u'clear sky'}], u'dt': 1468443600, u'main': {u'temp_kf': 0, u'temp': 287.804, u'grnd_level': 1026.28, u'temp_max': 287.804, u'sea_level': 1033.84, u'humidity': 60, u'pressure': 1026.28, u'temp_min': 287.804}, u'wind': {u'speed': 4, u'deg': 314.005}}, {u'clouds': {u'all': 0}, u'rain': {}, u'sys': {u'pod': u'n'}, u'dt_txt': u'2016-07-14 00:00:00', u'weather': [{u'main': u'Clear', u'id': 800, u'icon': u'01n', u'description': u'clear sky'}], u'dt': 1468454400, u'main': {u'temp_kf': 0, u'temp': 285.09, u'grnd_level': 1027.41, u'temp_max': 285.09, u'sea_level': 1034.97, u'humidity': 69, u'pressure': 1027.41, u'temp_min': 285.09}, u'wind': {u'speed': 3.31, u'deg': 314.501}}, {u'clouds': {u'all': 0}, u'rain': {}, u'sys': {u'pod': u'n'}, u'dt_txt': u'2016-07-14 03:00:00', u'weather': [{u'main': u'Clear', u'id': 800, u'icon': u'01n', u'description': u'clear sky'}], u'dt': 1468465200, u'main': {u'temp_kf': 0, u'temp': 282.827, u'grnd_level': 1028.13, u'temp_max': 282.827, u'sea_level': 1035.72, u'humidity': 80, u'pressure': 1028.13, u'temp_min': 282.827}, u'wind': {u'speed': 2.8, u'deg': 299.005}}, {u'clouds': {u'all': 0}, u'rain': {}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2016-07-14 06:00:00', u'weather': [{u'main': u'Clear', u'id': 800, u'icon': u'01d', u'description': u'clear sky'}], u'dt': 1468476000, u'main': {u'temp_kf': 0, u'temp': 283.864, u'grnd_level': 1028.77, u'temp_max': 283.864, u'sea_level': 1036.48, u'humidity': 78, u'pressure': 1028.77, u'temp_min': 283.864}, u'wind': {u'speed': 2.91, u'deg': 287.001}}, {u'clouds': {u'all': 0}, u'rain': {}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2016-07-14 09:00:00', u'weather': [{u'main': u'Clear', u'id': 800, u'icon': u'01d', u'description': u'clear sky'}], u'dt': 1468486800, u'main': {u'temp_kf': 0, u'temp': 289.656, u'grnd_level': 1029.22, u'temp_max': 289.656, u'sea_level': 1036.8, u'humidity': 70, u'pressure': 1029.22, u'temp_min': 289.656}, u'wind': {u'speed': 2.9, u'deg': 293.501}}, {u'clouds': {u'all': 68}, u'rain': {}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2016-07-14 12:00:00', u'weather': [{u'main': u'Clouds', u'id': 803, u'icon': u'04d', u'description': u'broken clouds'}], u'dt': 1468497600, u'main': {u'temp_kf': 0, u'temp': 291.467, u'grnd_level': 1029.2, u'temp_max': 291.467, u'sea_level': 1036.73, u'humidity': 63, u'pressure': 1029.2, u'temp_min': 291.467}, u'wind': {u'speed': 3.87, u'deg': 276.002}}, {u'clouds': {u'all': 76}, u'rain': {}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2016-07-14 15:00:00', u'weather': [{u'main': u'Clouds', u'id': 803, u'icon': u'04d', u'description': u'broken clouds'}], u'dt': 1468508400, u'main': {u'temp_kf': 0, u'temp': 292.174, u'grnd_level': 1028.99, u'temp_max': 292.174, u'sea_level': 1036.48, u'humidity': 55, u'pressure': 1028.99, u'temp_min': 292.174}, u'wind': {u'speed': 4.41, u'deg': 276.003}}, {u'clouds': {u'all': 92}, u'rain': {u'3h': 0.005}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2016-07-14 18:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10d', u'description': u'light rain'}], u'dt': 1468519200, u'main': {u'temp_kf': 0, u'temp': 291.688, u'grnd_level': 1028.76, u'temp_max': 291.688, u'sea_level': 1036.32, u'humidity': 52, u'pressure': 1028.76, u'temp_min': 291.688}, u'wind': {u'speed': 4.21, u'deg': 276.004}}, {u'clouds': {u'all': 56}, u'rain': {}, u'sys': {u'pod': u'n'}, u'dt_txt': u'2016-07-14 21:00:00', u'weather': [{u'main': u'Clouds', u'id': 803, u'icon': u'04n', u'description': u'broken clouds'}], u'dt': 1468530000, u'main': {u'temp_kf': 0, u'temp': 289.126, u'grnd_level': 1028.96, u'temp_max': 289.126, u'sea_level': 1036.45, u'humidity': 57, u'pressure': 1028.96, u'temp_min': 289.126}, u'wind': {u'speed': 2.88, u'deg': 267.502}}, {u'clouds': {u'all': 56}, u'rain': {}, u'sys': {u'pod': u'n'}, u'dt_txt': u'2016-07-15 00:00:00', u'weather': [{u'main': u'Clouds', u'id': 803, u'icon': u'04n', u'description': u'broken clouds'}], u'dt': 1468540800, u'main': {u'temp_kf': 0, u'temp': 287.32, u'grnd_level': 1028.76, u'temp_max': 287.32, u'sea_level': 1036.33, u'humidity': 61, u'pressure': 1028.76, u'temp_min': 287.32}, u'wind': {u'speed': 3.2, u'deg': 257.5}}, {u'clouds': {u'all': 68}, u'rain': {}, u'sys': {u'pod': u'n'}, u'dt_txt': u'2016-07-15 03:00:00', u'weather': [{u'main': u'Clouds', u'id': 803, u'icon': u'04n', u'description': u'broken clouds'}], u'dt': 1468551600, u'main': {u'temp_kf': 0, u'temp': 286.273, u'grnd_level': 1028.04, u'temp_max': 286.273, u'sea_level': 1035.62, u'humidity': 66, u'pressure': 1028.04, u'temp_min': 286.273}, u'wind': {u'speed': 2.41, u'deg': 248.007}}, {u'clouds': {u'all': 76}, u'rain': {u'3h': 0.02}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2016-07-15 06:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10d', u'description': u'light rain'}], u'dt': 1468562400, u'main': {u'temp_kf': 0, u'temp': 286.299, u'grnd_level': 1027.08, u'temp_max': 286.299, u'sea_level': 1034.7, u'humidity': 79, u'pressure': 1027.08, u'temp_min': 286.299}, u'wind': {u'speed': 3.26, u'deg': 218.001}}, {u'clouds': {u'all': 92}, u'rain': {u'3h': 0.21}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2016-07-15 09:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10d', u'description': u'light rain'}], u'dt': 1468573200, u'main': {u'temp_kf': 0, u'temp': 287.982, u'grnd_level': 1026.22, u'temp_max': 287.982, u'sea_level': 1033.7, u'humidity': 79, u'pressure': 1026.22, u'temp_min': 287.982}, u'wind': {u'speed': 5.58, u'deg': 215.001}}, {u'clouds': {u'all': 92}, u'rain': {u'3h': 0.67}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2016-07-15 12:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10d', u'description': u'light rain'}], u'dt': 1468584000, u'main': {u'temp_kf': 0, u'temp': 288.755, u'grnd_level': 1025.05, u'temp_max': 288.755, u'sea_level': 1032.53, u'humidity': 82, u'pressure': 1025.05, u'temp_min': 288.755}, u'wind': {u'speed': 6.38, u'deg': 218.01}}, {u'clouds': {u'all': 92}, u'rain': {u'3h': 0.9}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2016-07-15 15:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10d', u'description': u'light rain'}], u'dt': 1468594800, u'main': {u'temp_kf': 0, u'temp': 290.723, u'grnd_level': 1023.48, u'temp_max': 290.723, u'sea_level': 1030.96, u'humidity': 82, u'pressure': 1023.48, u'temp_min': 290.723}, u'wind': {u'speed': 5.85, u'deg': 222.003}}, {u'clouds': {u'all': 92}, u'rain': {u'3h': 0.13}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2016-07-15 18:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10d', u'description': u'light rain'}], u'dt': 1468605600, u'main': {u'temp_kf': 0, u'temp': 292.663, u'grnd_level': 1021.83, u'temp_max': 292.663, u'sea_level': 1029.3, u'humidity': 78, u'pressure': 1021.83, u'temp_min': 292.663}, u'wind': {u'speed': 6.07, u'deg': 228.001}}, {u'clouds': {u'all': 64}, u'rain': {u'3h': 0.13}, u'sys': {u'pod': u'n'}, u'dt_txt': u'2016-07-15 21:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10n', u'description': u'light rain'}], u'dt': 1468616400, u'main': {u'temp_kf': 0, u'temp': 291.603, u'grnd_level': 1021.62, u'temp_max': 291.603, u'sea_level': 1029, u'humidity': 81, u'pressure': 1021.62, u'temp_min': 291.603}, u'wind': {u'speed': 6.11, u'deg': 229.502}}, {u'clouds': {u'all': 76}, u'rain': {u'3h': 0.09}, u'sys': {u'pod': u'n'}, u'dt_txt': u'2016-07-16 00:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10n', u'description': u'light rain'}], u'dt': 1468627200, u'main': {u'temp_kf': 0, u'temp': 290.827, u'grnd_level': 1020.88, u'temp_max': 290.827, u'sea_level': 1028.36, u'humidity': 85, u'pressure': 1020.88, u'temp_min': 290.827}, u'wind': {u'speed': 5.9, u'deg': 229}}, {u'clouds': {u'all': 92}, u'rain': {u'3h': 0.28}, u'sys': {u'pod': u'n'}, u'dt_txt': u'2016-07-16 03:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10n', u'description': u'light rain'}], u'dt': 1468638000, u'main': {u'temp_kf': 0, u'temp': 290.188, u'grnd_level': 1019.67, u'temp_max': 290.188, u'sea_level': 1027.15, u'humidity': 87, u'pressure': 1019.67, u'temp_min': 290.188}, u'wind': {u'speed': 5.72, u'deg': 225}}, {u'clouds': {u'all': 92}, u'rain': {u'3h': 0.85}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2016-07-16 06:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10d', u'description': u'light rain'}], u'dt': 1468648800, u'main': {u'temp_kf': 0, u'temp': 289.028, u'grnd_level': 1019.44, u'temp_max': 289.028, u'sea_level': 1026.88, u'humidity': 94, u'pressure': 1019.44, u'temp_min': 289.028}, u'wind': {u'speed': 5.17, u'deg': 228}}, {u'clouds': {u'all': 92}, u'rain': {u'3h': 0.81}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2016-07-16 09:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10d', u'description': u'light rain'}], u'dt': 1468659600, u'main': {u'temp_kf': 0, u'temp': 289.627, u'grnd_level': 1019.5, u'temp_max': 289.627, u'sea_level': 1026.97, u'humidity': 95, u'pressure': 1019.5, u'temp_min': 289.627}, u'wind': {u'speed': 4.21, u'deg': 234.501}}, {u'clouds': {u'all': 92}, u'rain': {u'3h': 2.32}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2016-07-16 12:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10d', u'description': u'light rain'}], u'dt': 1468670400, u'main': {u'temp_kf': 0, u'temp': 289.154, u'grnd_level': 1019.65, u'temp_max': 289.154, u'sea_level': 1027.09, u'humidity': 98, u'pressure': 1019.65, u'temp_min': 289.154}, u'wind': {u'speed': 4.12, u'deg': 242.004}}, {u'clouds': {u'all': 8}, u'rain': {u'3h': 0.5}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2016-07-16 15:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10d', u'description': u'light rain'}], u'dt': 1468681200, u'main': {u'temp_kf': 0, u'temp': 289.442, u'grnd_level': 1019.21, u'temp_max': 289.442, u'sea_level': 1026.6, u'humidity': 90, u'pressure': 1019.21, u'temp_min': 289.442}, u'wind': {u'speed': 4.91, u'deg': 227}}, {u'clouds': {u'all': 48}, u'rain': {u'3h': 0.1}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2016-07-16 18:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10d', u'description': u'light rain'}], u'dt': 1468692000, u'main': {u'temp_kf': 0, u'temp': 289.982, u'grnd_level': 1018.95, u'temp_max': 289.982, u'sea_level': 1026.43, u'humidity': 87, u'pressure': 1018.95, u'temp_min': 289.982}, u'wind': {u'speed': 4.66, u'deg': 246.503}}, {u'clouds': {u'all': 8}, u'rain': {u'3h': 0.01}, u'sys': {u'pod': u'n'}, u'dt_txt': u'2016-07-16 21:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10n', u'description': u'light rain'}], u'dt': 1468702800, u'main': {u'temp_kf': 0, u'temp': 288.037, u'grnd_level': 1020.04, u'temp_max': 288.037, u'sea_level': 1027.53, u'humidity': 85, u'pressure': 1020.04, u'temp_min': 288.037}, u'wind': {u'speed': 4.11, u'deg': 259.501}}], u'cod': u'200', u'cnt': 34}


main()