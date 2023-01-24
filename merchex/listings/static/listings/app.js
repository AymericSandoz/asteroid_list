// Fonction permettant de récupérer la date de la prochain passage près de la terre d'un astéroïdes.
// Renvoie "Non définie" si aucune date n'est prévu.
const get_next_approach_date = (id) => {
  const asteroidId = id;
  const apiKey = "lkU4tlO9nq6DMmRHmd8yWXz6h5kJL2cwQ6QZa6BC";
  const apiUrl = `https://api.nasa.gov/neo/rest/v1/neo/${asteroidId}?api_key=${apiKey}`;

  fetch(apiUrl)
    .then((response) => response.json())
    .then((data) => {
      var button = document.getElementById(`asteroid-${id}`);
      let today = new Date();
      var test = document.getElementById("test");
      dates = [];

      for (let approach of data["close_approach_data"]) {
        date = new Date(approach["close_approach_date"]);

        if (today < date) {
          dates.push(approach["close_approach_date"]);
        }
      }
      nextDate = dates[0];
      if (nextDate != undefined) {
        button.innerHTML = nextDate;
        console.log(nextDate);
      } else {
        console.log("undefined :", nextDate);
        button.innerHTML = "Non définie";
      }
    })
    .catch((error) => {
      alert("Error:", error);
    });
};

// Fonction permettant d'afficher le spinner et de masquer certains élements lors de l'envoie du formulaire.
const load_spinner = () => {
  setTimeout(() => {
    document.querySelector(".loading-section").style.display = "flex";
    document.getElementById("date-form").style.display = "none";
    document.querySelector(".error").style.display = "none";
  }, "500");
};
