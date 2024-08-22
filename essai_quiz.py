
import xml.etree.ElementTree as ET

# Charger le fichier XML
tree = ET.parse('data/quiz_set.xml')
root = tree.getroot()

def poser_question(question_element):
    # Extraire le texte de la question
    question_text = question_element.find('text').text
    print(question_text)

    # Extraire les options de réponse
    options = question_element.find('options')
    for idx, option in enumerate(options.findall('option'), 1):
        print(f"{idx}. {option.text}")

    # Demander une réponse à l'utilisateur
    user_answer = int(input("Votre réponse (entrez le numéro): "))

    # Vérifier la réponse
    correct_option_index = None
    for idx, option in enumerate(options.findall('option'), 1):
        if option.get('correct') == 'true':
            correct_option_index = idx
            break

    # Retourner si la réponse est correcte ou non
    return user_answer == correct_option_index

def quiz():
    for question in root.findall('question'):
        if poser_question(question):
            print("Bonne réponse !")
        else:
            print("Mauvaise réponse !")
        print()

# Lancer le quiz
quiz()
