#!/usr/bin/env python
import sqlite3
import sys
from pygooglechart import PieChart2D
from pygooglechart import Chart
from pygooglechart import SimpleLineChart
from pygooglechart import Axis

#
#	Basic Python script for generating Graphs of your Honeypot using the pygooglechart wrapper
#       Support for Dionaea and Glastopf Honeypot
#
#	Author:	Johannes Schroeter - www.devwerks.net
#

#Change here the Size of your pieCharts
pieChartHeight = 350
pieChartWidth = 450 

#Change here the Color of your pie charts
pieColours = ['ff0000', '0000ff']    

#Change here the path to your Dionaea Database
dbfiledionaea = '/var/dionaea/logsql.sqlite'

#Change here the path to your Glastopf Database
dbfileglastopf = '/opt/myhoneypot/db/glastopf.db'
    
def generateGraphs():
	version()
        
        conn = sqlite3.connect(dbfiledionaea)
	c = conn.cursor()
        
        #Connections per Day - 7 Days
        querySQL = "SELECT strftime('%Y', connection_timestamp,'unixepoch') as 'year', strftime('%m', connection_timestamp,'unixepoch') as 'month', strftime('%d', connection_timestamp,'unixepoch') as 'day', count(strftime('%m', connection_timestamp,'unixepoch')) as 'num' FROM connections GROUP BY strftime('%Y', connection_timestamp,'unixepoch'), strftime('%m', connection_timestamp,'unixepoch'), strftime('%d', connection_timestamp,'unixepoch') ORDER BY strftime('%Y', connection_timestamp,'unixepoch') DESC, strftime('%m', connection_timestamp,'unixepoch') DESC, strftime('%d', connection_timestamp,'unixepoch') DESC LIMIT 7"
        print querySQL
        c.execute(querySQL)
        
        chart = SimpleLineChart(pieChartWidth, pieChartHeight, y_range=[0, 5000])
        
        list = []
        seclist = []
        
	for row in c:
		print(row)
                list.append(row[3])
                date = '%s-%s-%s' % (str(row[0]),str(row[1]),str(row[2]))
                seclist.append(date)
                
        list.reverse()
        seclist.reverse()
                
        chart.add_data(list)
        chart.set_axis_labels(Axis.BOTTOM,seclist)
        
        chart.set_colours(['0000FF'])
        chart.fill_linear_stripes(Chart.CHART, 0, 'CCCCCC', 0.2, 'FFFFFF', 0.2)
        chart.set_grid(0, 20, 5, 5)
        
        left_axis = range(0, 5001, 1000)
        left_axis[0] = ''
        chart.set_axis_labels(Axis.LEFT, left_axis)
         
        chart.download('connections_per_day.png')

        #Most attacked ports
        querySQL = 'SELECT COUNT(local_port) AS hitcount,local_port AS port FROM connections WHERE connection_type = "accept" GROUP BY local_port HAVING COUNT(local_port) > 10'
        print querySQL
        c.execute(querySQL)
        
        chart = PieChart2D(pieChartWidth, pieChartHeight, colours=pieColours)
        
        list = []
        seclist = []
        
	for row in c:
		print(row)
                list.append(row[0])
                seclist.append(str(row[1]))
                
        chart.add_data(list)
        chart.set_legend(seclist)

        chart.download('attacked_ports.png')

        #Top10 Malware
        querySQL = 'SELECT COUNT(download_md5_hash), download_md5_hash FROM downloads GROUP BY download_md5_hash ORDER BY COUNT(download_md5_hash) DESC LIMIT 10'
        print querySQL
        c.execute(querySQL)
			
        chart = PieChart2D(pieChartWidth, pieChartHeight, colours=pieColours)
        
        list = []
        seclist = []
        
	for row in c:
		print(row)
                list.append(row[0])
                seclist.append(str(row[1]))
                
        chart.add_data(list)
        chart.set_legend(seclist)

        chart.download('popular_malware.png')
        
        #
        #
        # Glastopf Queries starting here!
        #
        #
  
        conn = sqlite3.connect(dbfileglastopf)
        c = conn.cursor()
        
        #Top15 intext requests
        querySQL = 'SELECT count, content FROM intext ORDER BY count DESC LIMIT 15'
        print querySQL
        c.execute(querySQL)
        
        chart = PieChart2D(pieChartWidth, pieChartHeight, colours=pieColours)
        
        list = []
        seclist = []
        
        for row in c:
		print(row)
                list.append(row[0])
                seclist.append(str(row[1]))
                
        chart.add_data(list)
        chart.set_legend(seclist)

        chart.download('popular_intext.png')
        
        #Top15 intitle requests
        querySQL = 'SELECT count, content FROM intitle ORDER BY count DESC LIMIT 15'
        print querySQL
        c.execute(querySQL)
        
        chart = PieChart2D(pieChartWidth, pieChartHeight, colours=pieColours)
        
        list = []
        seclist = []
        
        for row in c:
		print(row)
                list.append(row[0])
                seclist.append(str(row[1]))
                
        chart.add_data(list)
        chart.set_legend(seclist)

        chart.download('popular_intitle.png')
        
        #Top10 inurl requests
        querySQL = 'SELECT count, content FROM inurl ORDER BY count DESC LIMIT 10'
        print querySQL
        c.execute(querySQL)
        
        chart = PieChart2D(pieChartWidth, pieChartHeight, colours=pieColours)
        
        list = []
        seclist = []
        
        for row in c:
		print(row)
                list.append(row[0])
                seclist.append(str(row[1]))
                
        chart.add_data(list)
        chart.set_legend(seclist)

        chart.download('popular_inurl.png')

def version():
	sys.stdout.write("\nHoneypot Statistics 0.1\n")
	sys.stdout.write("Author: Johannes Schroeter - www.devwerks.net\n\n")

def main():
        generateGraphs()

        sys.exit()

if __name__ == "__main__":
        main()

