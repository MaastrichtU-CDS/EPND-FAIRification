import pandas as pd

#Create Numeric/Unknown Metadata
def numericMetadata(df):
    dfMetadata = df.describe()
    return dfMetadata

#Create Categorical Metadata
def categoricalMetadata(df):
    dfMetadata = pd.DataFrame()
    dfMetadata['categoricalValue'] = df['cellValue'].unique()
    dfMetadata['cellValue'] = df['cellValue'].value_counts(normalize=True)
    return dfMetadata
