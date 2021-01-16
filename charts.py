from os import path
import argparse	
from datetime import datetime
import pandas as pd 
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

if __name__ == "__main__":
# def show_chart():

	# add owner name as an argument
	parser = argparse.ArgumentParser(description='Specify owner name')
	parser.add_argument('-t', '--owner_name', type=str, action='store', 
		help='enter first name of the owner whose team you want to look at, e.g. Maziad, Ibrahim...', default='INFO')
	args = parser.parse_args()

	# initiate empty dataframe
	df = pd.DataFrame()
	
	# today's date
	today = datetime.today().strftime('%Y-%m-%d')

	# load historical data into one df
	data_folder = os.getcwd()
	for file in os.listdir(data_folder):
		if file.endswith(".csv"):
			raw = pd.read_csv(file)
			df = df.append(raw).sort_values(by = ['date', 'Rk'])

	# replace team name by first name of owner
	df['Team'] = df['Team'].str.extract(r'.*\((.*)\).*') # extract content of parenthesis
	df['Team'] = df.Team.str.split().str.get(0) # get first name
	df['Team'] = df.Team.str.capitalize()

	# tidy
	df.sort_values(['Team', 'date'], inplace = True)
	df.to_csv('standings.csv')
	print("Dataset saved successfully here:", os.getcwd())

	def create_plot(df, title):
		# format date
		df['date'] = df['date'].astype('datetime64[ns]')

		# group data set by team 
		grp = df.groupby('Team') 
		# for name, group in grp:
		# 	print(name)


		# define categories to loop over
		categories = ['FG%', 'FT%', '3PM', 'AST', 'REB', 'PTS', 'TO', 'STL', 'BLK']

		# ========= BEGIN PLOTTING ========= #

		plt.rcParams["font.family"] = "monospace"
		plt.rc('xtick', labelsize=8) 
		plt.rc('ytick', labelsize=8) 
		# set figure size
		plt.figure(figsize = (10,6), dpi = 150)


		# loop over categories to create subplots
		for i, category in enumerate(categories, 1):

			# i indicates the particular subplot instance
			plt.subplot(3, 3, i) 

			# grey lines
			for name, group in grp:   
				
				# set dates in MM/DD format
				ax = plt.gca()
				formatter = mdates.DateFormatter("%m/%d")
				ax.xaxis.set_major_formatter(formatter)

				# set x-axis so that it always shows 6 evenly-distributed ticks
				ax.xaxis.set_major_locator(plt.MaxNLocator(6))

				# plot
				plt.plot(group.date, group[category], marker='', color='grey', 
					linewidth=1, linestyle = '--', alpha=0.4, label = name)
			    # plt.text(name, horizontalalignment='left', size='small', color='grey')

			# main line 
			df = df.loc[df.Team == args.owner_name]
			plt.plot(df.date, df[category], marker= 'o', color='blue', linewidth= 2)
			
			# annotate
			# for x,y in zip(df.date,df[category]):
			#     label = "{:.1f}".format(y)
			#     plt.annotate(label, # this is the text
			#                  (x,y), # this is the point to label
			#                  textcoords="offset points", # how to position the text
			#                  xytext=(0,10), # distance from text to points (x,y)
			#                  ha='center') # horizontal alignment can be left, right or center

			# add title
			plt.title(category, loc = 'center', fontsize = 12, fontweight = 'bold')

		# increase space between subplots
		plt.suptitle(title + ": " + args.owner_name, fontsize = 24, x = .25, y = .95, fontweight = 'bold')
		plt.tight_layout(pad=2.0)
		# plt.title("Ya 3ayni Standings", loc = 'left', fontsize = 24, fontweight = 'bold')
		plt.savefig(title, dpi = 600)
	# team totals
	print("Saving first plot")
	create_plot(df, "Team Totals")

	# convert stats to per game
	categories = ['3PM', 'AST', 'REB', 'PTS', 'TO', 'STL', 'BLK']
	for cat in categories:
		df[cat] = df[cat] / df['GP']
	print("Saving second plot")
	create_plot(df, "Stats Per Game")
	print("Plots saved successfully here:", os.getcwd())


