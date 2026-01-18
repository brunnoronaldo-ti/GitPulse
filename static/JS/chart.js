const dataValues = {
  labels: ["HTML", "CSS", "Python", "JavaScript", "Portugol"], 
  datasets: [{
    label: "Bytes por linguagem",
    data: [25223, 14428, 31378, 4632, 8950],
    borderWidth: 1
  }]
};

const ctx = document.getElementById("languageChart");
let chart = new Chart(ctx, {
  type: "bar",
  data: dataValues
});

document.getElementById("chartType").addEventListener("change", (e) => {
  chart.destroy();
  chart = new Chart(ctx, {
    type: e.target.value,
    data: dataValues
  });
});
