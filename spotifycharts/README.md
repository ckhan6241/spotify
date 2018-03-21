# Spotifycharts.com downloader

## environment
-	python 3.5
- 	urllib.request

## usage

	download(region='global', num_record=200, frequency='daily', start_date='2017-01-01')
	download(region='global', num_record=200, frequency='weekly', start_date='2016-12-23--2016-12-30')
	
The above two will download global daily/weekly spotifycharts.com data from the start_date. 200 days records will be downloaded

	region_help()
	frequency_help()
	day_help()
	week_help()
	
The above will print out supported region, frequency, date range and week range for download function


	