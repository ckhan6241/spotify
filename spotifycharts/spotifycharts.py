import urllib.request
import datetime
URLHEAD = "https://spotifycharts.com/regional/"

region_dict = {
	"Global":"global",
	"United Kingdom":"gb",
	"United States":"us",
	"Andorra":"ad",
	"Argentina":"ar",
	"Austria":"at",
	"Australia":"au",
	"Belgium":"be",
	"Bulgaria":"bg",
	"Bolivia":"bo",
	"Brazil":"br",
	"Canada":"ca",
	"Switzerland":"ch",
	"Chile":"cl",
	"Colombia":"co",
	"Costa Rica":"cr",
	"Cyprus":"cy",
	"Czech Republic":"cz",
	"Germany":"de",
	"Denmark":"dk",
	"Dominican Republic":"do",
	"Ecuador":"ec",
	"Estonia":"ee",
	"Spain":"es",
	"Finland":"fi",
	"France":"fr",
	"Greece":"gr",
	"Guatemala":"gt",
	"Hong Kong":"hk",
	"Honduras":"hn",
	"Hungary":"hu",
	"Indonesia":"id",
	"Ireland":"ie",
	"Iceland":"is",
	"Italy":"it",
	"Japan":"jp",
	"Lithuania":"lt",
	"Luxembourg":"lu",
	"Latvia":"lv",
	"Monaco":"mc",
	"Malta":"mt",
	"Mexico":"mx",
	"Malaysia":"my",
	"Nicaragua":"ni",
	"Netherlands":"nl",
	"Norway":"no",
	"New Zealand":"nz",
	"Panama":"pa",
	"Peru":"pe",
	"Philippines":"ph",
	"Poland":"pl",
	"Portugal":"pt",
	"Paraguay":"py",
	"Sweden":"se",
	"Singapore":"sg",
	"Slovakia":"sk",
	"El Salvador":"sv",
	"Thailand":"th",
	"Turkey":"tr",
	"Taiwan":"tw",
	"Uruguay":"uy"
}


region_names = region_dict.keys()
region_codes = [region_dict[name] for name in region_names]
frequency_list = ["daily", "weekly"]

# This list is used when frequency is set to daily, from 2017-01-01 to 2018-03-01
base = datetime.datetime(2017, 1, 1)
daily_list = [date.strftime('%Y-%m-%d') for date in [base + datetime.timedelta(days=x) for x in range(425)]]

# This list is used when frequency is set to weekly, from 2016-12-23--2016-12-30 to 2018-03-02--2018-03-09
base = datetime.datetime(2016, 12, 23)
weekly_list = [date[0].strftime('%Y-%m-%d') + "--" + date[1].strftime('%Y-%m-%d') for date in [(base + datetime.timedelta(days=x*7), base + datetime.timedelta(days=(x+1)*7)) for x in range(63)]]

def region_help():
	'''
	print out regions supported and there region code
	use region code in the API
	'''
	help_text = ""
	for key in region_dict.keys():
		help_text += key + ": " + region_dict[key] + "\n"
	return help_text.strip()

def frequency_help():
	'''
	print out frequency supported
	'''
	return ", ".join(frequency_list)

def day_help():
	'''
	print out week ranges supported, from 2017-01-01 to 2018-03-01
	'''
	help_text = ""
	for day in daily_list:
		help_text += day + "\n"
	return help_text.strip()

def week_help():
	'''
	print out date supported, from 2016-12-23--2016-12-30 to 2018-03-02--2018-03-09 
	'''
	help_text = ""
	for week in weekly_list:
		help_text += week + "\n"
	return help_text.strip()

def search_region_code(region):
	try:
		region = region[0].upper() + region[1:].lower()
		return region_dict[region]
	except:
		return region

def num_day():
	return len(daily_list)

def num_week():
	return len(weekly_list)

def num_region():
	return len(region_dict)

def download(region='global', frequency='daily', num_record=10, start_date='2017-01-01'):
	'''
	This function will takes in a few attributes and based on these attributes to download csv data file from
	spotifycharts.com

	@region: region code, default is global, see region_help() for full list of regions supported, both region codes and names are supported
	@frequency: daily or weekly, default is daily, see frequency_help() for full list of frequencies supported
	@num_record: number of days/weeks to download, default is 10
	@start_date: download data from this date, date range for weekly frequency, see day_help() and week_help() for full list of dates and weeks supported

	@return: null
	'''

	# check region
	if region not in region_codes:
		region = search_region_code(region)
	assert region in region_codes, "%s is not a valid region name/code"%region
	
	# check frequncy
	assert frequency in frequency_list, "%s is not a valid frequency"%frequency

	# check start_date and limit num_record 
	if frequency == "daily":
		assert start_date in daily_list, "%s is not a valid start date"%start_date
		start_index = daily_list.index(start_date)
		num_record = min(num_record, num_day() - start_index)
	else:
		assert start_date in weekly_list, "%s is not a valid start date"%start_date
		start_index = weekly_list.index(start_date)
		num_record = min(num_record, num_week() - start_index)

	# download
	for i in range(num_record):
		if frequency == "daily":
			URL = URLHEAD + region + '/' + frequency + '/' + daily_list[start_index + i] + "/download" 
			urllib.request.urlretrieve(URL, "%s_%s_%s.csv"%(region, frequency, daily_list[start_index + i]))
		else:
			URL = URLHEAD + region + '/' + frequency + '/' + weekly_list[start_index + i] + "/download" 
			urllib.request.urlretrieve(URL, "%s_%s_%s.csv"%(region, frequency, weekly_list[start_index + i]))
			
	return(URL)

# print(region_help())
# print(frequency_help())
# print(search_region_code("fuc"))
# print(search_region_code("global"))
# print(search_region_code("poland"))
# print(week_help())
# print(day_help())
# print(num_day(), num_region(), num_week())
# print(weekly_list[0], weekly_list[-1])
# print(daily_list[0],daily_list[-1])
# print ("Iceland" in region_names)
# print (region_codes)
# download(region="global")
download(num_record=999999, frequency='weekly', start_date='2016-12-23--2016-12-30')
download(num_record=999999, frequency='daily')

