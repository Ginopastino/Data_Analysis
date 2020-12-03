import datetime as dt
import pandas as pd
from dask import dataframe as ddf


#Utilities for Data Processing, DOMAIN SPECIFIC TO ISTAT FILES
redundant_columns = ['SEXISTAT1','TIME','Flag Codes','Flags']

renamed_columns = {'TIPO_DATO15':'Codice Indicatore',
				   'Tipo di indicatore demografico':'Indicatore Demografico',
				   'Seleziona periodo':'Periodo'}

#Dataset Acquisition - IMPLEMENT PARALLEL PROCESSING
data = ddf.read_csv('ISTAT - Popolazione - Bilancio Residenza - Comuni - ALL - Raw.csv', 
					sep = '|',
					dtype = {'Periodo':'object',
							 'ITTER107':'object',
							 'Flag Codes': 'object',
							 'Flags': 'object',
							 'Value':'float64'}, 
					low_memory = False)

data = data.compute(scheduler = 'threads')
print('Dataset caricato!')

# Renaming and Dropping Redundant Columns - DASK IMPLEMENTATION?
data.rename(renamed_columns, 
			axis = 1,
			inplace = True)

data.drop(redundant_columns,
		  axis = 1,
		  inplace = True)

print('Colonne rinominate e pulite...')

# Fixing Labels and Dropping Redundant Rows - DASK IMPLEMENTATION?
data['Indicatore Demografico'] = data['Indicatore Demografico'].str.strip()
data['Indicatore Demografico'] = data['Indicatore Demografico'].str.replace("  ", " ")
data['Indicatore Demografico'] = data['Indicatore Demografico'].str.title()
data = data[~data['Indicatore Demografico'].str.contains('Per Altri Motivi', regex = False)]
data = data[~data['Indicatore Demografico'].str.contains('Variazioni Territoriali', regex = False)]
data = data[~data['ITTER107'].str.contains('IT', regex = False)]
print('Righe eliminate...')

# Sorting Data for Output - DASK IMPLEMENTATION?
data.sort_values(['ITTER107', 'Indicatore Demografico','Periodo'], inplace=True)
print('Ordinato...')

# Exporting Monthly Aggregation to CSV for Analysis - DASK IMPLEMENTATION? 
data[data['Periodo'] \
    .str.contains('-', regex = False)] \
    .to_csv('ISTAT - Popolazione - Bilancio Residenza - Comuni - Mensile - Processed.csv', index = False)

# Exporting Yearly Aggregation to CSV for Analysis DASK IMPLEMENTATION?
data[~data['Periodo'] \
    .str.contains('-', regex = False)] \
    .to_csv('ISTAT - Popolazione - Bilancio Residenza - Comuni - Annuale - Processed.csv', index = False)

# Testing
print(data.head(50))
print(data.dtypes)
print('\nFinito!!!\n')