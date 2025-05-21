import streamlit as st
import random
import statistics

def load_euromillions_data():
    # Données de fréquence simulées basées sur les résultats EuroMillions 2025
    main_number_frequencies = {
        17: 15.50, 20: 15.50, 23: 14.00, 48: 14.00, 44: 13.50, 15: 13.00, 39: 12.00,
        27: 12.00, 31: 12.00, 50: 12.00, 21: 11.50, 10: 11.50, 29: 11.00, 30: 11.00,
        43: 11.00, 3: 10.50, 11: 10.50, 12: 10.50, 49: 10.50, 28: 10.50, 7: 10.00,
        41: 10.00, 4: 10.00, 25: 10.00, 14: 10.00, 36: 10.00, 38: 10.00, 9: 9.50,
        22: 9.50, 6: 9.50, 26: 9.00, 19: 9.00, 45: 9.00, 8: 9.00, 24: 9.00, 5: 9.00,
        1: 8.50, 2: 8.50, 37: 8.00, 46: 8.00, 42: 8.00, 34: 8.00, 13: 8.00, 16: 7.50,
        35: 7.50, 47: 7.50, 33: 7.00, 40: 7.00, 18: 6.00, 32: 6.00
    }
    lucky_star_frequencies = {
        3: 20.00, 9: 20.00, 2: 19.50, 4: 18.50, 8: 18.00, 12: 17.00, 11: 16.50,
        5: 16.50, 10: 14.00, 6: 13.50, 1: 13.50, 7: 13.00
    }
    
    main_freq = {num: round(perc * 2) for num, perc in main_number_frequencies.items()}
    star_freq = {num: round(perc * 2) for num, perc in lucky_star_frequencies.items()}
    
    return main_freq, star_freq

def get_frequency_categories(main_freq, star_freq):
    main_sorted = sorted(main_freq.items(), key=lambda x: x[1], reverse=True)
    star_sorted = sorted(star_freq.items(), key=lambda x: x[1], reverse=True)
    
    most_frequent_main = [num for num, _ in main_sorted[:5]]
    most_frequent_stars = [num for num, _ in star_sorted[:2]]
    least_frequent_main = [num for num, _ in main_sorted[-5:]]
    least_frequent_stars = [num for num, _ in star_sorted[-2:]]
    
    main_freq_values = list(main_freq.values())
    star_freq_values = list(star_freq.values())
    main_median = statistics.median(main_freq_values)
    star_median = statistics.median(star_freq_values)
    
    median_main = [num for num, freq in main_freq.items() 
                  if abs(freq - main_median) <= 1][:5]
    median_stars = [num for num, freq in star_freq.items() 
                   if abs(freq - star_median) <= 1][:2]
    
    return {
        'most_main': most_frequent_main,
        'least_main': least_frequent_main,
        'median_main': median_main,
        'most_stars': most_frequent_stars,
        'least_stars': least_frequent_stars,
        'median_stars': median_stars
    }

def generate_random_euromillions():
    main_numbers = sorted(random.sample(range(1, 51), 5))
    lucky_stars = sorted(random.sample(range(1, 13), 2))
    return main_numbers, lucky_stars

def generate_frequency_based_euromillions(categories):
    main_pool = (random.sample(categories['most_main'], 2) +
                 random.sample(categories['least_main'], 2) +
                 random.sample(categories['median_main'], 1))
    stars_pool = (random.sample(categories['most_stars'], 1) +
                  random.sample(categories['least_stars'], 1))
    
    main_numbers = sorted(random.sample(main_pool, 5) if len(set(main_pool)) >= 5 else main_pool)
    lucky_stars = sorted(stars_pool)
    
    return main_numbers, lucky_stars

# Interface Streamlit en français
st.title("Générateur de numéros EuroMillions")

# Afficher l'analyse de fréquence
st.header("Analyse de fréquence")
main_freq, star_freq = load_euromillions_data()
categories = get_frequency_categories(main_freq, star_freq)
st.write("**Numéros principaux les plus fréquents** : " + ", ".join(map(str, categories['most_main'])))
st.write("**Numéros principaux les moins fréquents** : " + ", ".join(map(str, categories['least_main'])))
st.write("**Numéros principaux à fréquence médiane** : " + ", ".join(map(str, categories['median_main'])))
st.write("**Étoiles les plus fréquentes** : " + ", ".join(map(str, categories['most_stars'])))
st.write("**Étoiles les moins fréquentes** : " + ", ".join(map(str, categories['least_stars'])))
st.write("**Étoiles à fréquence médiane** : " + ", ".join(map(str, categories['median_stars'])))

# Boutons pour générer les tickets
st.header("Générez vos tickets EuroMillions")
if st.button("Générer un ticket aléatoire"):
    random_main, random_stars = generate_random_euromillions()
    st.write("**Ticket aléatoire**")
    st.write(f"Numéros principaux : {', '.join(map(str, random_main))}")
    st.write(f"Étoiles : {', '.join(map(str, random_stars))}")

if st.button("Générer un ticket basé sur la fréquence"):
    freq_main, freq_stars = generate_frequency_based_euromillions(categories)
    st.write("**Ticket basé sur la fréquence**")
    st.write(f"Numéros principaux : {', '.join(map(str, freq_main))}")
    st.write(f"Étoiles : {', '.join(map(str, freq_stars))}")

st.write("*Remarque* : Cet outil génère des numéros EuroMillions à des fins de divertissement. Les tirages de loterie sont aléatoires, et les fréquences passées ne garantissent pas de gains futurs.")
