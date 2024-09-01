import xml.etree.ElementTree as ET
import random

# Constants :
TYPE_SPELL = "spell_a_string"
TYPE_QCM = "multiple_choice_1_correct"
TYPE_TRUE_FALSE = "true_false"

# Charger le fichier XML
MAIN_FILE = 'data/quiz_set_evoluted.xml'
tree = ET.parse(MAIN_FILE)

root = tree.getroot()


def input_int_range(msg, inf, sup):
    """Vérifie que la saisie est un entier entre inf et sup compris"""
    while True:
        try:
            rep = int(input(msg + (" (Saisir un entier ({}-{})) : ".format(inf, sup))))
            if isinstance(rep, int) and (rep >= inf) and (rep <= sup):
                return rep
        except:
            pass


class Question:
    """General type question"""
    def __init__(self, text, explanation = None, xml_element = None):
        self.text = text
        self.explanation = explanation
        self.xml_element = xml_element

    def poser(self):
        raise NotImplementedError("Cette méthode n'a pas été implémentée.")

    @classmethod
    def create(cls):
        rep = input('Ennoncé dans Class Question : ')
        return cls(rep)


class VraiFaux(Question):
    """True or False question"""
    def __init__(self, text, correct, explanation=None, xml_element=None):
        super().__init__(text, explanation= explanation, xml_element=xml_element)
        self.correct = correct

    def poser(self):
        print(self.text)
        rep = input("répondre par vrai ou faux").lower()
        # Attention la base est codée en anglais, la ligne suivante corrige pour le francais mais accèpte l'anglais.
        if rep == "vrai":
            rep = "true"
        elif rep == "faux":
            rep = "false"

        correct = self.correct == rep
        if not correct:
            print("Réponse incorrecte")
        else:
            print("Réponse correcte")

        try:
            print(self.explanation)
        except:
            pass

        return correct

    @classmethod
    def create(cls):
        """Créer le xml à partir de questions"""
        text = input("Ennoncé vrai_faux :")
        while True:
            response = input("Vrai ou faux ? ").lower()
            if response in ["vrai", "faux"]:
                break
        explanation = input("Explication : ")

        xml_str = f"""<question type="{TYPE_TRUE_FALSE}">
  <text correct="{response}">{text}</text>
  <explanation>{explanation}</explanation>
</question>"""
        return xml_str


class SpellString(Question):
    def __init__(self, xml_element):
        super().__init__(xml_element)

    def poser(self):
        texte = self.xml_element.find('text')
        print(texte.text)
        rep = input("réponse : ")
        answer = self.xml_element.find('answer').text
        if answer == rep:
            print("OK")
            return True
        else:
            print(f"Erreur :     {answer}")
            return False

    @classmethod
    def create(cls):
        """Créer le xml à partir de questions"""
        text = input("Ennoncé de type orthographe :")
        answer = input("Réponse attendue : ")
        xml_str = f"""<question type="{TYPE_SPELL}">
  <text>{text}</text>
  <answer>{answer}</answer>
</question>"""
        return xml_str


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

        rep = input_int_range("Votre choix : ", 1, len(option_lst))

        print(option_lst[int(rep) - 1].get('correct'))
        return option_lst[int(rep) - 1].get('correct') == "true"

    @classmethod
    def create(cls):
        # Créer un nouvel élément question
        new_question = ET.Element('question')
        new_question.set("type", TYPE_QCM)

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

        ET.indent(new_question, space="  ", level=0)
        return new_question


def charger_questions(xml_file) -> list:
    """Load questions of the xml_file. Return a list of object pointing to a question xml.element"""

    questions = []

    for questions_elem in root.findall("question"):
        text = questions_elem.find("text").text
        question_type = questions_elem.get("type")

        if question_type == 'multiple_choice_1_correct':
            # question_choix = questions_elem.find("options")
            # choix = [choix_elem for choix_elem in question_choix.findall("option")]
            # questions.append(QuestionChoixMultiple(questions_elem))
            pass
        if question_type == 'true_false':
            # correct = "Aucun"
            correct = questions_elem.find("text").get("correct", None)

            explanation = None
            expl = questions_elem.find("explanation")
            if expl is not None:
                explanation = expl.text

            questions.append(VraiFaux(text, correct, explanation, questions_elem))

        if question_type == "spell_a_string":
            pass
            # questions.append(SpellString(questions_elem))

    return questions


def quiz(source_of_questions, fraction=1.0):
    # Extraire toutes les questions, les mélanger en sélectionner une fraction
    random.shuffle(source_of_questions)

    total_questions = len(source_of_questions)
    num_questions = int(total_questions * fraction)

    print(f"Sélection de {num_questions} questions")
    selected_questions = source_of_questions[:num_questions]

    for question_i, question in enumerate(selected_questions, 1):
        print(f"\nQUESTION {question_i} / {num_questions}")
        if question.poser():
            print("Bonne réponse !")
        else:
            print("Mauvaise réponse !")
        print()


def test_for_question(id_tag=None):
    """Search for and test a question with a given value"""
    if id_tag is None:
        id_tag = int(input("id de la question à tester"))

    for question in questions:
        if question.xml_element:
            print("Je cherche ...")
            if question.xml_element.get('id') == str(id_tag):
                question.poser()
                break



def ajouter_quiz():
    # Créer un nouvel élément question
    new_question = ET.Element('question')
    new_question.set("type", TYPE_QCM)

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


def create_question(quest):
    """Ask the type of question to create, then create it"""
    while True:
        print("1. Question de type QCM")
        print("2. Question de type vrai ou faux")
        print("3. Question de type orthographe exacte")
        print("10.    Sortir")
        choice = input("Choisissez une option: ").strip()

        if choice == '1':
            new_question = QuestionChoixMultiple.create()
            pass
        elif choice == '2':
            lmx_str = VraiFaux.create()
            print(lmx_str)
            new_question = ET.fromstring(lmx_str)

        elif choice == "3":
            lmx_str = SpellString.create()
            print(lmx_str)
            new_question = ET.fromstring(lmx_str)

        elif choice == '10':
            print("Au revoir !")
            break
        else:
            print("Option invalide, veuillez réessayer.")

        if new_question:
            root.append(new_question)
            # Sauvegarder le fichier XML
            tree.write(MAIN_FILE, encoding='utf-8')
            print("Nouveau quiz ajouté et enregistré avec succès !")


def main_menu(questions):
    while True:
        print("1. Lancer le quiz")
        print("2. Ajouter une nouvelle question")
        print("4. Tester une question particulière (pour mise au point)")
        print("5. Créer une question")
        print("10. Quitter")
        choice = input("Choisissez une option: ").strip()

        if choice == '1':
            quiz(questions, fraction=1.0)
        elif choice == '2':
            ajouter_quiz()
        elif choice == '4':
            test_for_question()
        elif choice == '5':
            create_question(questions)
        elif choice == '10':
            print("Au revoir !")
            break

        else:
            print("Option invalide, veuillez réessayer.")


# Lancer le menu principal
questions = charger_questions(MAIN_FILE)

main_menu(questions)
