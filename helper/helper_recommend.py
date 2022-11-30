import pandas as pd
import numpy as np
import time
from sklearn.metrics.pairwise import cosine_similarity


def load():
    df = pd.read_csv('datasets/city_ranking.csv')
    data = df.set_index('city'). iloc[:,1:-1]
    scores = df.set_index('city'). iloc[:,1:-1].round().astype(int)
    location = []
    for index, city, country in df[["city", "country"]].sort_values("country").itertuples():
        new = f'{city}, {country}'
        location.append(new)
    return df, data,scores, location


def find_similarity(column, user, number,scores, city):
    if city == 'Others':
        new_df = scores[column]
    else:
        locate = city.split(',')
        new_df = scores[scores.index !=  locate[0]][column]
    value = []
    for index,city in enumerate(new_df.index):
        city_old = new_df.loc[city].values.reshape(-1,number)
        user = user.reshape(-1, number)
        score = cosine_similarity(city_old, user)
        value.append(score)
    similarity = pd.Series(value, index=new_df.index)
    city_similar = similarity.sort_values(ascending=False).astype(float).idxmax()
    # message = f'Based on your aggregate preferences and ratings, {city_similar} is the top recommended city to move/travel to.'
    return city_similar

def final_answer(df,word, data):
    # subtitle = 'City Ranking in terms of Business, essentials, Openness and recreation scores(over 10.0)'
    country = df.loc[df['city'] == word, 'country'].iloc[0]
    if word in df['city'].head().values:
        response = "It is actually one of the top 5 cities that has piqued millennials' interests."
    elif word in df['city'].head(10).values:
        response = "It is actually one of the top 10 cities that has piqued millennials' interests."
    elif word in df['city'].tail(5).values:
        response = "It is actually one of the least 5 cities that has piqued millennials' interests."
    else:
        response = ""

    ranking = list(zip(list(data.loc[word].index),data.loc[word]))
    breakdown = pd.DataFrame(ranking, columns = ['Category','Score'])
    breakdown['Score'] = breakdown['Score'].round(1)
    breakdown = breakdown.iloc[[2,4,5,7,14],].reset_index().iloc[:,1:3]
    return country, response, breakdown

def get_locations():
    _, _, _, locations = load()
    return locations

def get_recommendation(city, levels):
    df, data, scores, locations = load()
    preferences = ["Tourism Score", "Food Ranking", "Transport Score", "Internet Speed Score", "Nightlife Score"]
    number = 5
    user = np.array(levels)
    column = preferences
    recommended_city = find_similarity(column, user, number, scores, city)
    country, response, breakdown = final_answer(df, recommended_city, data)
    breakdown.at[3,"Category"]= "Internet Speed"   
    table_html = breakdown.to_html()
    return recommended_city, country, response, table_html, locations
