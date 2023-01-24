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
      button.innerHTML = nextDate;
    })
    .catch((error) => {
      alert("Error:", error);
    });
};

const load_spinner = () => {
  setTimeout(() => {
    document.querySelector(".loading-section").style.display = "flex";
    document.getElementById("date-form").style.display = "none";
    document.querySelector(".error").style.display = "none";
  }, "500");
};
