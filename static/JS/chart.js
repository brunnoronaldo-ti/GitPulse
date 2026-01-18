const colors = languageLabels.map((_, index) => {
  const hue = (index * 360) / languageLabels.length;
  return `hsl(${hue}, 70%, 55%)`;
});

const dataValues = {
  labels: languageLabels,
  datasets: [{
    label: "Uso de linguagens (%)",
    data: languageData,
    backgroundColor: colors,
    borderColor: colors,
    borderWidth: 1
  }]
};

const ctx = document.getElementById("languageChart");
let chart = new Chart(ctx, {
  type: "bar",
  data: dataValues
});

const selector = document.getElementById("chartType");

if (selector) {
  selector.addEventListener("change", (e) => {
    chart.destroy();
    chart = new Chart(ctx, {
      type: e.target.value,
      data: dataValues
    });
  });
}
