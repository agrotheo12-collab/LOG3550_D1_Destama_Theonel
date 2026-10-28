"use strict";

const STORAGE_KEY = "log3550_catalogue_livres";

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

let livres = chargerLivres();

function chargerLivres() {
  try {
    const donnees = localStorage.getItem(STORAGE_KEY);

    if (donnees !== null) {
      const livresSauvegardes = JSON.parse(donnees);

      if (Array.isArray(livresSauvegardes)) {
        return livresSauvegardes;
      }
    }
  } catch (erreur) {
    console.error("Impossible de charger les livres :", erreur);
  }

  return livresInitiaux.map((livre) => ({ ...livre }));
}

function sauvegarderLivres() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(livres));
  } catch (erreur) {
    console.error("Impossible de sauvegarder les livres :", erreur);
    messageFormulaire.textContent =
      "Impossible de sauvegarder les modifications dans le navigateur.";
  }
}

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
      supprimerLivre(livre.id);
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

  if (titre.length < 2) {
    afficherErreur(
      champTitre,
      erreurTitre,
      "Le titre doit contenir au moins 2 caractères."
    );
    valide = false;
  }

  if (auteur.length < 2) {
    afficherErreur(
      champAuteur,
      erreurAuteur,
      "L'auteur doit contenir au moins 2 caractères."
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

function ajouterLivre(evenement) {
  evenement.preventDefault();
  messageFormulaire.textContent = "";

  if (!validerFormulaire()) {
    messageFormulaire.textContent =
      "Veuillez corriger les erreurs du formulaire.";
    return;
  }

  const nouveauLivre = {
    id: Date.now(),
    titre: champTitre.value.trim(),
    auteur: champAuteur.value.trim(),
    annee: Number(champAnnee.value),
    categorie: champCategorie.value,
    disponible: champDisponible.value === "true"
  };

  livres.push(nouveauLivre);
  sauvegarderLivres();

  formulaire.reset();
  effacerErreurs();
  messageFormulaire.textContent = "Le livre a été ajouté.";
  afficherLivres();
}

function supprimerLivre(id) {
  const livre = livres.find((element) => element.id === id);

  if (!livre) {
    return;
  }

  const confirmation = window.confirm(
    `Voulez-vous vraiment supprimer « ${livre.titre} » ?`
  );

  if (!confirmation) {
    return;
  }

  livres = livres.filter((element) => element.id !== id);
  sauvegarderLivres();
  afficherLivres();
  messageFormulaire.textContent = "Le livre a été supprimé.";
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
afficherLivres();
