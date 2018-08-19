import pandas as pd
import ast

main_df = pd.DataFrame.from_csv('main_data.csv')
main_df = main_df[~main_df.clarifai_data.isna()]

#reads str as dict 
ast.literal_eval((main_df.iloc[0].clarifai_data))

