"use strict";

const API_URL = "http://127.0.0.1:8000";

const recherche = document.querySelector("#recherche");
const filtreCategorie = document.querySelector("#filtre-categorie");
const tri = document.querySelector("#tri");
const disponiblesSeulement = document.querySelector("#disponibles-seulement");
const nombreLivres = document.querySelector("#nombre-livres");
const listeLivres = document.querySelector("#liste-livres");
const aucunResultat = document.querySelector("#aucun-resultat");

const formulaire = document.querySelector("#formulaire-livre");
const champTitre = document.querySelector("#titre");
const champAuteur = document.querySelector("#auteur");
const champAnnee = document.querySelector("#annee");
const champCategorie = document.querySelector("#categorie");
const champDisponible = document.querySelector("#disponible");
const messageFormulaire = document.querySelector("#message-formulaire");

const erreurTitre = document.querySelector("#erreur-titre");
const erreurAuteur = document.querySelector("#erreur-auteur");
const erreurAnnee = document.querySelector("#erreur-annee");
const erreurCategorie = document.querySelector("#erreur-categorie");

let livres = [];

function normaliser(texte) {
  return String(texte)
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .trim();
}

function remplirCategories() {
  categories.forEach((categorie) => {
    const optionFiltre = document.createElement("option");
    optionFiltre.value = categorie;
    optionFiltre.textContent = categorie;
    filtreCategorie.appendChild(optionFiltre);

    const optionFormulaire = document.createElement("option");
    optionFormulaire.value = categorie;
    optionFormulaire.textContent = categorie;
    champCategorie.appendChild(optionFormulaire);
  });
}

function obtenirMessageErreur(donnees) {
  if (Array.isArray(donnees.detail)) {
    return donnees.detail
      .map((erreur) => {
        const champ = erreur.loc ? erreur.loc.slice(1).join(".") : "Donnée";
        return `${champ} : ${erreur.msg}`;
      })
      .join(" ");
  }

  if (typeof donnees.detail === "string") {
    return donnees.detail;
  }

  return "Une erreur est survenue lors de la communication avec l'API.";
}

async function chargerLivres() {
  nombreLivres.textContent = "Chargement des livres...";
  listeLivres.replaceChildren();
  aucunResultat.hidden = true;

  try {
    const reponse = await fetch(`${API_URL}/livres/?skip=0&limit=100`);

    if (!reponse.ok) {
      throw new Error(`Erreur HTTP ${reponse.status}`);
    }

    livres = await reponse.json();
    afficherLivres();
  } catch (erreur) {
    console.error("Erreur lors du chargement des livres :", erreur);
    nombreLivres.textContent =
      "Impossible de charger les livres. Vérifiez que l'API est démarrée.";
    aucunResultat.hidden = true;
  }
}

function obtenirLivresFiltres() {
  const rechercheTexte = normaliser(recherche.value);
  const categorieChoisie = filtreCategorie.value;

  let resultat = livres.filter((livre) => {
    const correspondRecherche =
      normaliser(livre.titre).includes(rechercheTexte) ||
      normaliser(livre.auteur).includes(rechercheTexte);

    const correspondCategorie =
      categorieChoisie === "" || livre.categorie === categorieChoisie;

    const correspondDisponibilite =
      !disponiblesSeulement.checked || livre.disponible === true;

    return (
      correspondRecherche &&
      correspondCategorie &&
      correspondDisponibilite
    );
  });

  switch (tri.value) {
    case "titre-asc":
      resultat.sort((a, b) => a.titre.localeCompare(b.titre, "fr"));
      break;
    case "titre-desc":
      resultat.sort((a, b) => b.titre.localeCompare(a.titre, "fr"));
      break;
    case "annee-asc":
      resultat.sort((a, b) => a.annee - b.annee);
      break;
    case "annee-desc":
      resultat.sort((a, b) => b.annee - a.annee);
      break;
  }

  return resultat;
}

function afficherLivres() {
  const livresAffiches = obtenirLivresFiltres();

  listeLivres.replaceChildren();

  livresAffiches.forEach((livre) => {
    const carte = document.createElement("article");
    carte.className = "book-card";

    const titre = document.createElement("h3");
    titre.textContent = livre.titre;

    const auteur = document.createElement("p");
    auteur.textContent = `Auteur : ${livre.auteur}`;

    const annee = document.createElement("p");
    annee.textContent = `Année : ${livre.annee}`;

    const categorie = document.createElement("p");
    categorie.textContent = `Catégorie : ${livre.categorie}`;

    const statut = document.createElement("p");
    statut.className = "book-status";

    if (livre.disponible) {
      statut.textContent = "Disponible";
    } else {
      statut.textContent = "Non disponible";
      statut.classList.add("unavailable");
    }

    const boutonSupprimer = document.createElement("button");
    boutonSupprimer.type = "button";
    boutonSupprimer.textContent = "Supprimer";
    boutonSupprimer.setAttribute(
      "aria-label",
      `Supprimer le livre ${livre.titre}`
    );

    boutonSupprimer.addEventListener("click", () => {
      supprimerLivre(livre.id, livre.titre, boutonSupprimer);
    });

    carte.append(titre, auteur, annee, categorie, statut, boutonSupprimer);
    listeLivres.appendChild(carte);
  });

  nombreLivres.textContent =
    `${livresAffiches.length} livre${livresAffiches.length > 1 ? "s" : ""}`;

  aucunResultat.hidden = livresAffiches.length > 0;
}

function afficherErreur(champ, elementErreur, message) {
  elementErreur.textContent = message;
  champ.setAttribute("aria-invalid", message ? "true" : "false");
}

function effacerErreurs() {
  afficherErreur(champTitre, erreurTitre, "");
  afficherErreur(champAuteur, erreurAuteur, "");
  afficherErreur(champAnnee, erreurAnnee, "");
  afficherErreur(champCategorie, erreurCategorie, "");
}

function validerFormulaire() {
  effacerErreurs();

  let valide = true;
  const titre = champTitre.value.trim();
  const auteur = champAuteur.value.trim();
  const annee = Number(champAnnee.value);
  const categorie = champCategorie.value;
  const anneeActuelle = new Date().getFullYear();

  if (titre.length < 2 || titre.length > 200) {
    afficherErreur(
      champTitre,
      erreurTitre,
      "Le titre doit contenir entre 2 et 200 caractères."
    );
    valide = false;
  }

  if (auteur.length < 2 || auteur.length > 200) {
    afficherErreur(
      champAuteur,
      erreurAuteur,
      "L'auteur doit contenir entre 2 et 200 caractères."
    );
    valide = false;
  }

  if (
    champAnnee.value.trim() === "" ||
    !Number.isInteger(annee) ||
    annee < 1450 ||
    annee > anneeActuelle
  ) {
    afficherErreur(
      champAnnee,
      erreurAnnee,
      `L'année doit être comprise entre 1450 et ${anneeActuelle}.`
    );
    valide = false;
  }

  if (!categories.includes(categorie)) {
    afficherErreur(
      champCategorie,
      erreurCategorie,
      "Veuillez choisir une catégorie."
    );
    valide = false;
  }

  return valide;
}

async function ajouterLivre(evenement) {
  evenement.preventDefault();
  messageFormulaire.textContent = "";

  if (!validerFormulaire()) {
    messageFormulaire.textContent =
      "Veuillez corriger les erreurs du formulaire.";
    return;
  }

  const nouveauLivre = {
    titre: champTitre.value.trim(),
    auteur: champAuteur.value.trim(),
    annee: Number(champAnnee.value),
    categorie: champCategorie.value,
    disponible: champDisponible.value === "true"
  };

  const boutonAjouter = formulaire.querySelector('button[type="submit"]');
  boutonAjouter.disabled = true;
  messageFormulaire.textContent = "Enregistrement du livre...";

  try {
    const reponse = await fetch(`${API_URL}/livres/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(nouveauLivre)
    });

    const donnees = await reponse.json();

    if (!reponse.ok) {
      throw new Error(obtenirMessageErreur(donnees));
    }

    formulaire.reset();
    effacerErreurs();
    messageFormulaire.textContent =
      `Le livre « ${donnees.titre} » a été ajouté avec succès.`;

    await chargerLivres();
  } catch (erreur) {
    console.error("Erreur lors de l'ajout du livre :", erreur);
    messageFormulaire.textContent =
      `Impossible d'ajouter le livre : ${erreur.message}`;
  } finally {
    boutonAjouter.disabled = false;
  }
}

async function supprimerLivre(id, titre, bouton) {
  const confirmation = window.confirm(
    `Voulez-vous vraiment supprimer « ${titre} » ?`
  );

  if (!confirmation) {
    return;
  }

  bouton.disabled = true;

  try {
    const reponse = await fetch(`${API_URL}/livres/${id}`, {
      method: "DELETE"
    });

    if (!reponse.ok) {
      let message = `Erreur HTTP ${reponse.status}`;

      try {
        const donnees = await reponse.json();
        message = obtenirMessageErreur(donnees);
      } catch {
        // La réponse ne contient pas de message JSON.
      }

      throw new Error(message);
    }

    messageFormulaire.textContent =
      `Le livre « ${titre} » a été supprimé avec succès.`;

    await chargerLivres();
  } catch (erreur) {
    console.error("Erreur lors de la suppression du livre :", erreur);
    messageFormulaire.textContent =
      `Impossible de supprimer le livre : ${erreur.message}`;
    bouton.disabled = false;
  }
}

recherche.addEventListener("input", afficherLivres);
filtreCategorie.addEventListener("change", afficherLivres);
tri.addEventListener("change", afficherLivres);
disponiblesSeulement.addEventListener("change", afficherLivres);
formulaire.addEventListener("submit", ajouterLivre);

formulaire.addEventListener("reset", () => {
  messageFormulaire.textContent = "";
  window.setTimeout(effacerErreurs, 0);
});

remplirCategories();
chargerLivres();
