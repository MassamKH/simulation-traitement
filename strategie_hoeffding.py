# fichier : simulateur/strategie_hoeffding.py

from dist.simulateur import SimulateurTraitement
import matplotlib.pyplot as plt
import math
import csv

def enregistrer_resultats(nom_fichier, lignes):
    with open(nom_fichier, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Patient", "Traitement", "Succes", "Strategie"])
        writer.writerows(lignes)

def strategie_hoeffding(n=1000):
    simulateur = SimulateurTraitement()
    traitements = ['A', 'B', 'C', 'D', 'E']
    compte_admin = {t: 0 for t in traitements}
    compte_succes = {t: 0 for t in traitements}
    succes_total = 0
    lignes_csv = []

    # ⚙️ Initialisation : 1 essai de chaque traitement
    for i, t in enumerate(traitements):
        resultat = simulateur.administrer_traitement(t)
        compte_admin[t] += 1
        if resultat:
            compte_succes[t] += 1
            succes_total += 1
        lignes_csv.append([i + 1, t, int(resultat), "Hoeffding"])

    # 🔁 Simulation principale
    for i in range(len(traitements), n):
        ucb_scores = {}
        for t in traitements:
            moyenne = compte_succes[t] / compte_admin[t]
            marge = math.sqrt(math.log(i + 1) / (2 * compte_admin[t]))
            ucb_scores[t] = moyenne + marge

        meilleur = max(ucb_scores, key=ucb_scores.get)
        resultat = simulateur.administrer_traitement(meilleur)
        compte_admin[meilleur] += 1
        if resultat:
            compte_succes[meilleur] += 1
            succes_total += 1
        lignes_csv.append([i + 1, meilleur, int(resultat), "Hoeffding"])

    enregistrer_resultats("csv/resultats_hoeffding.csv", lignes_csv)


    # 📊 Résultats
    print("\n📈 Résultats stratégie Hoeffding (UCB) :")
    print(f"Patients totaux : {n}")
    print(f"Succès totaux : {succes_total}")
    print(f"Taux de succès global : {100 * succes_total / n:.2f}%\n")

    for t in traitements:
        print(f"Traitement {t} : utilisé {compte_admin[t]} fois, succès {compte_succes[t]}")

    # 📉 Graphique
    taux_par_traitement = [
        100 * compte_succes[t] / compte_admin[t]
        if compte_admin[t] > 0 else 0
        for t in traitements
    ]

    plt.bar(traitements, taux_par_traitement, color='lightcoral', edgecolor='black')
    plt.title("Taux de succès par traitement (Hoeffding/UCB)")
    plt.xlabel("Traitement")
    plt.ylabel("Taux de succès (%)")
    plt.ylim(0, 100)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.savefig("images/hoeffding.png")
    #plt.show()
    plt.close()

if __name__ == "__main__":
    strategie_hoeffding()