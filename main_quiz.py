import xml.etree.ElementTree as ET
import random
# test

# Charger le fichier XML
MAIN_FILE = 'data/quiz_set_evoluted.xml'
tree = ET.parse(MAIN_FILE)

root = tree.getroot()

class Question:
    def __init__(self, xml_element):
        self.xml_element = xml_element

    def poser(self):
        raise NotImplementedError("Cette méthode n'a pas été implémentée.")

class VraiFaux(Question):
    def __init__(self, xml_element):
        super().__init__(xml_element)


    def poser(self):
        texte = self.xml_element.find('text')
        print(texte.text)
        rep = input("répondre par vrai ou faux").lower()
        return texte.get("correct") == rep


class SpellString(Question):
    def __init__(self, xml_element):
        super().__init__(xml_element)

    def poser(self):
        texte = self.xml_element.find('text')
        print(texte.text)
        rep = input("réponse : ")
        answer = self.xml_element.find('answer').text
        if answer == rep:
            print ("OK")
            return True
        else:
            print(f"Erreur :     {answer}")
            return False


class QuestionChoixMultiple(Question):
    """Epreuve dans laquelle on doit saisir exactement une chaîne de caractères"""
    def __init__(self, elm):
        super().__init__(elm)
        # self.choix = choix
        # self.correct = correct

    def poser(self):
        texte = self.xml_element.find('text')

        # Extraire les options de réponse, les présenter dans un ordre aléatoire.
        options = self.xml_element.find("options")
        option_lst = options.findall('option').copy()
        random.shuffle(option_lst)

        print(texte.text)
        for i, choix in enumerate(option_lst, 1):
            print(f"{i}. {choix.text}")
        rep = input("Votre choix : ")
        print(option_lst)
        print(option_lst[int(rep) - 1].get('correct'))
        return option_lst[int(rep) -1].get('correct') == "true"


def charger_questions(xml_file) -> list:
    """Load questions of the xml_file. Return a list of object pointing to a question xml.element"""
    tree = ET.parse(xml_file)
    root = tree.getroot()
    questions = []

    for questions_elem in root.findall("question"):
        # text = questions_elem.find("text").text
        question_type = questions_elem.get("type")

        if question_type == 'multiple_choice_1_correct':
            # question_choix = questions_elem.find("options")
            # choix = [choix_elem for choix_elem in question_choix.findall("option")]
            questions.append(QuestionChoixMultiple(questions_elem))

        if question_type == 'true_false':
            # correct = "Aucun"
            questions.append(VraiFaux(questions_elem))

        if question_type == "spell_a_string":
            questions.append(SpellString(questions_elem))

    return questions

def quiz(questions, fraction = 1.0):

    # Extraire toutes les questions, les mélanger en sélectionner une fraction
    random.shuffle(questions)

    total_questions = len(questions)
    num_questions = int(total_questions * fraction)
    selected_questions = questions[:num_questions]

    for question in selected_questions:
        if question.poser():
            print("Bonne réponse !")
        else:
            print("Mauvaise réponse !")
        print()

def test_for_question(questions, id=None):
    """Search for and test a question with a given value"""
    if id is None:
        id = int(input("id de la question à tester"))

    for question in questions:
        if question.xml_element.get('id') == str(id):
            question.poser()
            break


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
    tree.write(MAIN_FILE, encoding='utf-8')
    print("Nouveau quiz ajouté et enregistré avec succès !")


def main_menu(questions):

    while True:
        print("1. Lancer le quiz")
        print("2. Ajouter une nouvelle question")
        print("4. Tester une question particulière (pour mise au point)")
        print("3. Quitter")
        choice = input("Choisissez une option: ").strip()

        if choice == '1':
            quiz(questions, fraction = 1.0)
        elif choice == '2':
            ajouter_quiz()
        elif choice == '3':
            print("Au revoir !")
            break
        elif choice == '4':
            test_for_question(questions)
        else:
            print("Option invalide, veuillez réessayer.")


# Lancer le menu principal
questions = charger_questions(MAIN_FILE)

main_menu(questions)
