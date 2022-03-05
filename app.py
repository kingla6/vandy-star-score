# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 13:48:27 2022

@author: kingl
"""

import streamlit as st
import pandas as pd
import requests
from PIL import Image # import Image from pillow to open images

# function to scale grades
def minmax_scaler(num, max_num):
    output = (num - 1)/(max_num-1)
    return output

# function to display score outputs
def score_output(on_field_weights, on_field_score, off_field_weights, off_field_score):
    star_score = on_field_score * (off_field_score/100)
    c1, c2, c3 = st.columns(3)
    if on_field_weights != 100 or off_field_weights != 100:
        error_details = f"Weights error: On-field weights={on_field_weights}. Off-field weights={off_field_weights}. Both must be equivalent to 100!"
        return st.error(error_details)
    else: 
        return (
                c1.title('On-Field Score:'),
                c1.title(f'{round(on_field_score,1)}'),
                c2.title('Off-Field Score:'),
                c2.title(f'{round(off_field_score,1)}'),
                c3.title('Star Score:'),
                c3.title(f'{round(star_score,1)}')
            )
    
# format app to fill screen width
st.set_page_config(layout="wide")
# set main title of application
st.markdown("<h1 style='text-align: center;'>Star Score Calculator</h1>", unsafe_allow_html=True)

# create sidebar with multiple options
sidebar = st.sidebar.selectbox("Navigation", ("Main", "Application"))

# load images that will be present in the app
vandy = Image.open(requests.get("https://github.com/kingla6/recruit-score-scraper/raw/main/images/vandy.png", stream=True).raw)

# code for main page
if sidebar == 'Main':
    
    # Page Content
    st.markdown("<h2 style='text-align: center;'>Main Page</h2>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Through the navigation sidebar, the main and application pages can be accessed.</h3>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>For documentation, code, and all other relevant files, see the <a href='https://github.com/kingla6/vandy-star-score'>project repo</a>.</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,1,1]) # this allows us to center the image by selecting col2 in next line
    col2.image(vandy, use_column_width=True)
    st.markdown("<h4 style='text-align: center;'>Developed by Logan King, Graduate Recruiting and Scouting Assistant - Vanderbilt Football</h4>", unsafe_allow_html=True)
    
# code for application page
if sidebar == 'Application':
    
    # Page Content
    st.markdown("<h2 style='text-align: center;'>Application Page</h2>", unsafe_allow_html=True)
    
    # selectbox for positions
    position = st.selectbox("Position:", 
                            ('QB', 'RB', 'WR', 'TE', 'OG/OC', 'OT', 
                             'DT', 'DE', 'STAR', 'ANCHOR', 'ILB', 'CB', 'SAF', 
                             'ATH', 'K/P', 'K', 'P', 'LS'))
    
    # load defailt weights for each position, set default weights for position selected
    position_weights_df = pd.read_csv('https://raw.githubusercontent.com/kingla6/vandy-star-score/main/default_weights.csv')
    default_weights = position_weights_df[position_weights_df.position==position]
    
    # on-field
    st.header('On-Field')
    c11, c12, = st.columns(2)
    
    ## grades
    c11.subheader('Grades')
    ### athleticism
    athleticism = c11.slider('Athleticism', 1, 5, 3)
    athleticism_scaled = minmax_scaler(athleticism, 5)
    c11.write(f'Scaled Athleticism Grade: {athleticism_scaled}')
    ### measurables
    measurables = c11.slider('Measurables', 1, 5, 3)
    measurables_scaled = minmax_scaler(measurables, 5)
    c11.write(f'Scaled Measurables Grade: {measurables_scaled}')
    ### multi_position
    multi_position = c11.slider('Multi-Position', 1, 3, 1)
    multi_position_scaled = minmax_scaler(multi_position, 3)
    c11.write(f'Scaled Multi-Position Grade: {multi_position_scaled}')
    ### multi_sport
    multi_sport = c11.slider('Multi-Sport', 1, 4, 1)
    multi_sport_scaled = minmax_scaler(multi_sport, 4)
    c11.write(f'Scaled Multi-Sport Grade: {multi_sport_scaled}')
    ### production
    production = c11.slider('Production', 1, 5, 3)
    production_scaled = minmax_scaler(production, 5)
    c11.write(f'Scaled Production Grade: {production_scaled}')
    
    ## weights
    c12.subheader('Weights')
    ### athleticism
    athleticism_weight = c12.slider('Athleticism Weight', 0, 100, int(default_weights['athleticism_grade']), 5)
    athleticism_score = athleticism_scaled * athleticism_weight
    c12.write(f'Athleticism Score: {athleticism_score}')
    ### measurables
    measurables_weight = c12.slider('Measurables Weight', 0, 100, int(default_weights['measurables_grade']), 5)
    measurables_score = measurables_scaled * measurables_weight
    c12.write(f'Measurables Score: {measurables_score}')
    ### multi_position
    multi_position_weight = c12.slider('Multi-Position Weight', 0, 100, int(default_weights['multi_position_grade']), 5)
    multi_position_score = multi_position_scaled * multi_position_weight
    c12.write(f'Multi-Position Score: {multi_position_score}')
    ### multi_sport
    multi_sport_weight = c12.slider('Multi-Sport Weight', 0, 100, int(default_weights['multi_sport_grade']), 5)
    multi_sport_score = multi_sport_scaled * multi_sport_weight
    c12.write(f'Multi-Sport Score: {multi_sport_score}')
    ### production
    production_weight = c12.slider('Production Weight', 0, 100, int(default_weights['production_grade']), 5)
    production_score = production_scaled * production_weight
    c12.write(f'Production Score: {production_score}')
    
    ## on-field final
    on_field_weights = athleticism_weight + measurables_weight + multi_position_weight + multi_sport_weight + production_weight
    on_field_score = athleticism_score + measurables_score + multi_position_score + multi_sport_score + production_score
    
    # off-field
    st.header('Off-Field')
    c21, c22 = st.columns(2)
    
    ## grades
    c21.subheader('Grades')
    ### distance
    distance = c21.slider('Distance', 1, 5, 3)
    distance_scaled = minmax_scaler(distance, 5)
    c21.write(f'Scaled Distance Grade: {distance_scaled}')
    ### academic
    academic = c21.slider('Academic', 1, 5, 3)
    academic_scaled = minmax_scaler(academic, 5)
    c21.write(f'Scaled Academic Grade: {academic_scaled}')
    ### support system
    support_system = c21.slider('Support System', 1, 3, 2)
    support_system_scaled = minmax_scaler(support_system, 3)
    c21.write(f'Scaled Support System Grade: {support_system_scaled}')
    
    ## weights
    c22.subheader('Weights')
    ### distance
    distance_weight = c22.slider('Distance Weight', 0, 100, int(default_weights['distance_grade']), 5)
    distance_score = distance_scaled * distance_weight
    c22.write(f'Distance Score: {distance_score}')
    ### academic
    academic_weight = c22.slider('Academic Weight', 0, 100, int(default_weights['academic_grade']), 5)
    academic_score = academic_scaled * academic_weight
    c22.write(f'Academic Score: {academic_score}')
    ### support system
    support_system_weight = c22.slider('Support System Weight', 0, 100, int(default_weights['support_system_grade']), 5)
    support_system_score = support_system_scaled * support_system_weight
    c22.write(f'Support System Score: {support_system_score}')
    
    ## off-field final
    off_field_weights = distance_weight + academic_weight + support_system_weight
    off_field_score = distance_score + academic_score + support_system_score
    
    if st.button('Get Scores'):
        score_output(on_field_weights, on_field_score, off_field_weights, off_field_score)
    
