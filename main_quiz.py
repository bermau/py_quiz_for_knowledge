import xml.etree.ElementTree as ET
import random
# test

# Charger le fichier XML
MAIN_FILE = 'data/quiz_set_evoluted.xml'
tree = ET.parse(MAIN_FILE)

root = tree.getroot()

class Question:
    def __init__(self, text):
        self.text = text

    def poser(self):
        raise NotImplementedError("Cette méthode n'a pas été implémentée.")

class VraiFaux(Question):
    def __init__(self, text):
        super().__init__(text)


    def poser(self):
        print(self.text)
        rep = input("répondre par vrai ou faux").lower()
        return rep


class QuestionChoixMultiple(Question):
    """Epreuve dans laquelle on doit saisir exactement une chaîne de caractères"""
    def __init__(self, text, choix, ):
        super().__init__(text)
        self.choix = choix
        # self.correct = correct

    def poser(self):
        print(self.text)
        for i, choix in enumerate(self.choix, 1):
            print(f"{i}. choix")
        rep = input("Votre choix : ")
        return self.choix[int(rep) -1] == self.correct


def poser_question_OLD(question_element):
    # Extraire le texte de la question
    question_text = question_element.find('text').text
    print(question_text)

    # Extraire les options de réponse, les présenter dans un ordre aléatoire.
    options = question_element.find('options')
    reponses_possibles = options.findall('option')
    random.shuffle(reponses_possibles)

    for idx, item in enumerate(reponses_possibles, 1):
        print(f"{idx}. {item.text}")

    # Demander une réponse à l'utilisateur
    user_answer_int = int(input("Votre réponse (entrez le numéro): "))
    if user_answer_int >= len(reponses_possibles) or user_answer_int < 0:
        return False
    # Vérifier la réponse
    correctness = reponses_possibles[user_answer_int - 1].get('correct', None)

    if correctness == "true":
        return True
    else:
        return False

def charger_questions(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    questions = []

    for questions_elem in root.findall("question"):
        text = questions_elem.find("text").text
        question_type = questions_elem.get("type")

        if question_type == 'multiple_choice_1_correct':
            question_choix = questions_elem.find("options")
            choix = [choix_elem for choix_elem in question_choix.findall("option")]
            questions.append(QuestionChoixMultiple(text, choix))

        if question_type == 'true_false':
            correct = "Aucun"
            questions.append(VraiFaux(text))

    return questions

def quiz(fraction = 1.0):

    # Extraire toutes les questions
    questions = root.findall('question')
    # les mélanger
    random.shuffle(questions)

    total_questions = len(questions)
    num_questions = int(total_questions * fraction)
    selected_questions = questions[:num_questions]

    for question in selected_questions:
        # Mélanger les questions

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

    # Indentation
    ET.indent(tree, space="  ", level=0)

    # Sauvegarder le fichier XML
    tree.write(MAIN_FILE, encoding='utf-8'
               # , xml_declaration=True
               )
    print("Nouveau quiz ajouté et enregistré avec succès !")


def main_menu(questions):

    while True:
        print("1. Lancer le quiz")
        print("2. Ajouter une nouvelle question")
        print("3. Quitter")
        choice = input("Choisissez une option: ").strip()

        if choice == '1':
            quiz(questions)
        elif choice == '2':
            ajouter_quiz()
        elif choice == '3':
            print("Au revoir !")
            break
        else:
            print("Option invalide, veuillez réessayer.")


# Lancer le menu principal
questions = charger_questions(MAIN_FILE)

main_menu(questions)
