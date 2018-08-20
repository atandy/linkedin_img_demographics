import pandas as pd
import ast

# use the data from the csv that we made in face_demographics.py
main_df = pd.DataFrame.from_csv('main_data.csv')

# remove all NA clarifai data cause it's not helpful
main_df = main_df[~main_df.clarifai_data.isna()]

main_df['masculine_score'] = None
main_df['feminine_score'] = None
main_df['top_appearance'] = None
main_df['second_appearance'] = None


#reads str as dict 
for idx, row in main_df.iterrows():
    pdict = ast.literal_eval(row['clarifai_data'])
    
    try:
        face_data = pdict['outputs'][0]['data']['regions'][0]['data']['face']
    except:
        face_data = None
    if not face_data:
        continue
    
    # get masculine and feminine scores
    try:
        concepts = face_data['gender_appearance']['concepts']
        for c in concepts:
            if c['name'] == 'masculine':
                masculine_score = c['value']
            elif c['name'] == 'feminine':
                feminine_score = c['value']
    except Exception as e:
        masculine_score = None
        feminine_score = None

    # get first and second mc values
    
    mc_concepts = face_data['multicultural_appearance']['concepts']
    mc_count = 0
    for mcc in mc_concepts:
        mc_count +=1
        if mc_count == 1:
            top_mc = mcc['name']
            top_mc_val = mcc['value']
        else:
            second_mc = mcc['name']
            second_mc_val = mcc['value']

        if mc_count == 2:
            break

    main_df.at[idx, 'masculine_score'] = masculine_score
    main_df.at[idx, 'feminine_score'] = feminine_score

    main_df.at[idx, 'top_appearance'] = top_mc
    main_df.at[idx, 'second_appearance'] = second_mc

# create a dataframe that contains all data in a csv with the fem and masc scores
main_df.to_csv('all_data_with_scores.csv')

# example slice showing female asians based on the photos
asian_women_df = main_df[
    (main_df.feminine_score >= 0.75) & \
    (main_df.top_appearance=='asian')]