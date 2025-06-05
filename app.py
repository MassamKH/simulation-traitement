# fichier : simulateur_web/app.py (ajout de /rapport et export zip)

from flask import Flask, render_template, request, send_file
import matplotlib.pyplot as plt
import pandas as pd
import os
import zipfile
from strategies import (
    strategie_uniforme,
    strategie_greedy,
    strategie_epsilon,
    strategie_hoeffding
)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", show_rapport_button=True)

@app.route("/simulate", methods=["POST"])
def simulate():
    strategie = request.form["strategie"]
    n = int(request.form["n"])

    if strategie == "uniforme":
        df = strategie_uniforme(n)
        nom = "Uniforme"
        csv_file = "resultats_uniforme.csv"
    elif strategie == "greedy":
        df = strategie_greedy(n)
        nom = "Greedy"
        csv_file = "resultats_greedy.csv"
    elif strategie == "epsilon":
        df = strategie_epsilon(n)
        nom = "ε-Greedy"
        csv_file = "resultats_epsilon_greedy.csv"
    elif strategie == "hoeffding":
        df = strategie_hoeffding(n)
        nom = "Hoeffding (UCB)"
        csv_file = "resultats_hoeffding.csv"
    else:
        return "Stratégie inconnue", 400

    taux_cumule = df["Succes"].cumsum() / (df.index + 1)
    plot_path = f"static/plots/{strategie}_plot.png"
    image_export = f"static/images/{strategie}_image.png"

    plt.figure(figsize=(6, 4))
    plt.plot(taux_cumule, label=nom, color="teal")
    plt.title(f"Taux de succès cumulatif - {nom}")
    plt.xlabel("Patient")
    plt.ylabel("Taux")
    plt.ylim(0, 1)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(plot_path)
    os.makedirs("static/images", exist_ok=True)
    plt.savefig(image_export)
    plt.close()

    return render_template("result.html", strategie=nom, image_path=plot_path, csv_file=f"static/{csv_file}")

@app.route("/graphes")
def graphes():
    strategies = {
        "Uniforme": "static/resultats_uniforme.csv",
        "Greedy": "static/resultats_greedy.csv",
        "ε-Greedy": "static/resultats_epsilon_greedy.csv",
        "Hoeffding (UCB)": "static/resultats_hoeffding.csv"
    }
    fig, axs = plt.subplots(2, 2, figsize=(10, 8))
    axs = axs.flatten()
    for i, (nom, fichier) in enumerate(strategies.items()):
        if os.path.exists(fichier):
            df = pd.read_csv(fichier)
            taux = df["Succes"].cumsum() / (df.index + 1)
            axs[i].plot(taux, label=nom)
            axs[i].set_title(nom)
            axs[i].set_ylim(0, 1)
            axs[i].grid(True)
        axs[i].set_xlabel("Patient")
        axs[i].set_ylabel("Taux")
    plt.tight_layout()
    graphe_path = "static/plots/tous_graphes.png"
    plt.savefig(graphe_path)
    plt.close()
    return render_template("graphes.html", image_path=graphe_path)

@app.route("/comparaison")
def comparaison():
    fichiers = {
        "Uniforme": "static/resultats_uniforme.csv",
        "Greedy": "static/resultats_greedy.csv",
        "ε-Greedy": "static/resultats_epsilon_greedy.csv",
        "Hoeffding (UCB)": "static/resultats_hoeffding.csv"
    }
    plt.figure(figsize=(10, 6))
    for nom, chemin in fichiers.items():
        if os.path.exists(chemin):
            df = pd.read_csv(chemin)
            taux = df["Succes"].cumsum() / (df.index + 1)
            plt.plot(taux, label=nom)
    plt.title("Comparaison des taux de succès cumulés")
    plt.xlabel("Patient")
    plt.ylabel("Taux cumulatif")
    plt.ylim(0, 1)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    graphe_path = "static/plots/comparaison.png"
    plt.savefig(graphe_path)
    plt.close()
    return render_template("comparaison.html", image_path=graphe_path)

@app.route("/rapport")
def rapport():
    images = {
        "Uniforme": "static/images/uniforme_image.png",
        "Greedy": "static/images/greedy_image.png",
        "ε-Greedy": "static/images/epsilon_greedy.png",
        "Hoeffding (UCB)": "static/images/hoeffding_image.png"
    }
    return render_template("rapport.html", images=images)

@app.route("/download-all")
def download_all():
    zip_path = "static/export/resultats_graphes.zip"
    os.makedirs("static/export", exist_ok=True)
    with zipfile.ZipFile(zip_path, 'w') as zf:
        for folder in ["static/images", "static/plots"]:
            for root, _, files in os.walk(folder):
                for f in files:
                    full_path = os.path.join(root, f)
                    zf.write(full_path, arcname=os.path.relpath(full_path, start="static"))
    return send_file(zip_path, as_attachment=True)

@app.route("/fichiers")
def fichiers():
    dossier = "static"
    fichiers_csv = [f for f in os.listdir(dossier) if f.endswith(".csv")]
    return render_template("fichiers.html", fichiers=fichiers_csv)

@app.route("/voir-fichier")
def voir_fichier():
    nom_fichier = request.args.get("nom")
    chemin = os.path.join("static", nom_fichier)
    if not os.path.exists(chemin):
        return "Fichier non trouvé", 404

    df = pd.read_csv(chemin)

    # Calculer les stats par traitement
    tableau = df.groupby("Traitement")["Succes"].agg(
        total="count",
        succes="sum"
    ).reset_index()

    tableau["taux"] = (tableau["succes"] / tableau["total"] * 100).round(1)

    return render_template("voir_fichier.html", nom=nom_fichier, stats=tableau.to_dict(orient="records"))




if __name__ == "__main__":
    os.makedirs("static/plots", exist_ok=True)
    os.makedirs("static/images", exist_ok=True)
    app.run(debug=True)
