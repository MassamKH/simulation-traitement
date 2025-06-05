# simulateur/dist/simulateur.py
import random
import statistics
import string

class SimulateurTraitement:
    def __init__(self):
        self.traitements = {
            'A': self.traitement_A,
            'B': self.traitement_B,
            'C': self.traitement_C,
            'D': self.traitement_D,
            'E': self.traitement_E,
        }

    def administrer_traitement(self, t):
        if t not in self.traitements:
            print(f"❌ Traitement {t} non reconnu.")
            return False
        return self.traitements[t]()

    def traitement_A(self):
        print("\n🧪 Traitement A : Analyse de texte")
        texte = """Python est un langage de programmation très utilisé.
Il est populaire pour la data science, le web, et l'automatisation."""
        nb_lignes = len(texte.splitlines())
        nb_mots = len(texte.split())
        nb_caracteres = len(texte)
        print(f"Lignes : {nb_lignes} | Mots : {nb_mots} | Caractères : {nb_caracteres}")
        return random.random() < 0.7  # 70 % de réussite

    def traitement_B(self):
        print("\n🔍 Traitement B : Recherche dans une liste")
        liste = ["banane", "pomme", "orange", "kiwi"]
        recherche = "kiwi"
        if recherche in liste:
            print(f"{recherche} trouvé dans la liste.")
            return random.random() < 0.5  # 70 % de réussite
        else:
            print(f"{recherche} introuvable.")
            return False

    def traitement_C(self):
        print("\n📊 Traitement C : Statistiques sur une liste")
        valeurs = [12, 45, 33, 22, 59, 41]
        moyenne = statistics.mean(valeurs)
        minimum = min(valeurs)
        maximum = max(valeurs)
        print(f"Moyenne : {moyenne} | Min : {minimum} | Max : {maximum}")
        return random.random() < 0.8  # 70 % de réussite

    def traitement_D(self):
        print("\n🎲 Traitement D : Simulation de tirages de dés")
        resultats = [random.randint(1, 6) for _ in range(1000)]
        histogramme = {i: resultats.count(i) for i in range(1, 7)}
        for face, freq in histogramme.items():
            print(f"Face {face} : {freq} fois")
        return random.random() < 0.3  # 70 % de réussite

    def traitement_E(self):
        print("\n🧼 Traitement E : Nettoyage de texte")
        texte_brut = "Ceci est un TEST!!! Avec PLEIN de... MAJUSCULES?? Et de la ponctuation..."
        texte_nettoye = texte_brut.lower().translate(str.maketrans('', '', string.punctuation))
        print("Avant :")
        print(texte_brut)
        print("Après :")
        print(texte_nettoye)
        return random.random() < 0.2
