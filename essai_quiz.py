import xml.etree.ElementTree as ET



# Charger le fichier XML
MAIN_FILE = 'data/quiz_set.xml'
tree = ET.parse(MAIN_FILE)

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


def ajouter_quiz():
    # Créer un nouvel élément question
    new_question = ET.Element('question')

    # Demander à l'utilisateur d'entrer le texte de la question
    question_text = input("Entrez le texte de la question: ")
    question_text_element = ET.SubElement(new_question, 'text')
    question_text_element.text = question_text

    # Ajouter les options de réponse
    options_element = ET.SubElement(new_question, 'options')
    for i in range(4):
        option_text = input(f"Entrez le texte de la réponse {i + 1}: ")
        option_element = ET.SubElement(options_element, 'option')
        option_element.text = option_text

        # Demander si cette réponse est la bonne
        is_correct = input(f"Est-ce que la réponse {i + 1} est correcte ? (oui/non): ").strip().lower()
        if is_correct == 'oui':
            option_element.set('correct', 'true')
        else:
            option_element.set('correct', 'false')

    # Ajouter la nouvelle question à la racine
    root.append(new_question)

    # Sauvegarder le fichier XML
    tree.write(MAIN_FILE, encoding='utf-8', xml_declaration=True)
    print("Nouveau quiz ajouté et enregistré avec succès !")


def main_menu():
    while True:
        print("1. Lancer le quiz")
        print("2. Ajouter une nouvelle question")
        print("3. Quitter")
        choice = input("Choisissez une option: ").strip()

        if choice == '1':
            quiz()
        elif choice == '2':
            ajouter_quiz()
        elif choice == '3':
            print("Au revoir !")
            break
        else:
            print("Option invalide, veuillez réessayer.")


# Lancer le menu principal
main_menu()
