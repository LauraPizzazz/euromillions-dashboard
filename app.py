import streamlit as st
import random
import statistics
import pandas as pd

def load_euromillions_data():
    # Données de fréquence simulées basées sur les résultats EuroMillions (200 tirages, 2018)
    main_number_frequencies = {
        1: 8.50, 2: 8.50, 3: 10.50, 4: 10.00, 5: 9.00, 6: 9.50, 7: 10.00, 8: 9.00,
        9: 9.50, 10: 11.50, 11: 10.50, 12: 10.50, 13: 8.00, 14: 10.00, 15: 13.00,
        16: 7.50, 17: 15.50, 18: 6.00, 19: 9.00, 20: 15.50, 21: 11.50, 22: 9.50,
        23: 14.00, 24: 9.00, 25: 10.00, 26: 9.00, 27: 12.00, 28: 10.50, 29: 11.00,
        30: 11.00, 31: 12.00, 32: 6.00, 33: 7.00, 34: 8.00, 35: 7.50, 36: 10.00,
        37: 8.00, 38: 10.00, 39: 12.00, 40: 7.00, 41: 10.00, 42: 8.00, 43: 11.00,
        44: 13.50, 45: 9.00, 46: 8.00, 47: 7.50, 48: 14.00, 49: 10.50, 50: 12.00
    }
    lucky_star_frequencies = {
        1: 13.50, 2: 19.50, 3: 20.00, 4: 18.50, 5: 16.50, 6: 13.50, 7: 13.00,
        8: 18.00, 9: 20.00, 10: 14.00, 11: 16.50, 12: 17.00
    }
    
    # Convertir les pourcentages en estimations de tirages (sur 200 tirages)
    main_freq = {num: round(perc * 2) for num, perc in main_number_frequencies.items()}
    star_freq = {num: round(perc * 2) for num, perc in lucky_star_frequencies.items()}
    
    return main_freq, star_freq

def get_frequency_categories(main_freq, star_freq):
    # Trier les fréquences pour les numéros principaux et les étoiles
    main_sorted = sorted(main_freq.items(), key=lambda x: x[1], reverse=True)
    star_sorted = sorted(star_freq.items(), key=lambda x: x[1], reverse=True)
    
    # Calculer les terciles pour les numéros principaux
    main_freq_values = list(main_freq.values())
    main_third = len(main_freq_values) // 3
    main_freq_sorted = sorted(main_freq_values, reverse=True)
    main_high_threshold = main_freq_sorted[main_third - 1]
    main_low_threshold = main_freq_sorted[-main_third]
    
    # Calculer les terciles pour les étoiles
    star_freq_values = list(star_freq.values())
    star_third = len(star_freq_values) // 3
    star_freq_sorted = sorted(star_freq_values, reverse=True)
    star_high_threshold = star_freq_sorted[star_third - 1]
    star_low_threshold = star_freq_sorted[-star_third]
    
    # Catégoriser tous les numéros
    main_categories = {}
    star_categories = {}
    
    for num, freq in main_freq.items():
        if freq >= main_high_threshold:
            main_categories[num] = "Plus fréquent"
        elif freq <= main_low_threshold:
            main_categories[num] = "Moins fréquent"
        else:
            main_categories[num] = "Fréquence médiane"
    
    for num, freq in star_freq.items():
        if freq >= star_high_threshold:
            star_categories[num] = "Plus fréquent"
        elif freq <= star_low_threshold:
            star_categories[num] = "Moins fréquent"
        else:
            star_categories[num] = "Fréquence médiane"
    
    # Sélections pour le ticket basé sur la fréquence (comme avant)
    most_frequent_main = [num for num, _ in main_sorted[:5]]
    most_frequent_stars = [num for num, _ in star_sorted[:2]]
    least_frequent_main = [num for num, _ in main_sorted[-5:]]
    least_frequent_stars = [num for num, _ in star_sorted[-2:]]
    median_main = [num for num, freq in main_freq.items() 
                  if abs(freq - statistics.median(main_freq_values)) <= 1][:5]
    median_stars = [num for num, freq in star_freq.items() 
                   if abs(freq - statistics.median(star_freq_values)) <= 1][:2]
    
    return {
        'main_categories': main_categories,
        'star_categories': star_categories,
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

# Afficher l'analyse de fréquence complète
st.header("Analyse de fréquence")
main_freq, star_freq = load_euromillions_data()
categories = get_frequency_categories(main_freq, star_freq)

# Tableau pour les numéros principaux
st.subheader("Numéros principaux (1–50)")
main_data = [
    {"Numéro": num, "Tirages estimés": main_freq[num], "Catégorie": categories['main_categories'][num]}
    for num in range(1, 51)
]
main_df = pd.DataFrame(main_data)
st.dataframe(main_df, use_container_width=True)

# Tableau pour les étoiles
st.subheader("Étoiles (1–12)")
star_data = [
    {"Étoile": num, "Tirages estimés": star_freq[num], "Catégorie": categories['star_categories'][num]}
    for num in range(1, 13)
]
star_df = pd.DataFrame(star_data)
st.dataframe(star_df, use_container_width=True)

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
