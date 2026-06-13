function showChartError(elementId, message) {
  const element = document.getElementById(elementId);
  if (!element) return;
  element.innerHTML = `<div class="empty-state py-4">${message}</div>`;
}

async function fetchJson(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`请求失败: ${response.status}`);
  }
  return response.json();
}

function createBarChart(elementId, title, labels, values) {
  const chart = echarts.init(document.getElementById(elementId));
  chart.setOption({
    color: ["#58b982"],
    tooltip: { trigger: "axis" },
    grid: { left: 48, right: 20, bottom: 48, top: 30 },
    xAxis: { type: "category", data: labels, axisLabel: { rotate: 25 } },
    yAxis: { type: "value", name: "元/平" },
    series: [{ name: title, type: "bar", data: values, barMaxWidth: 36 }]
  });
  window.addEventListener("resize", () => chart.resize());
}

function createPieChart(elementId, items) {
  const chart = echarts.init(document.getElementById(elementId));
  chart.setOption({
    color: ["#257454", "#58b982", "#8fd6a8", "#b9e7c9", "#dff6e8", "#9bcfb0"],
    tooltip: { trigger: "item" },
    series: [{
      type: "pie",
      radius: ["42%", "70%"],
      data: items,
      label: { formatter: "{b}: {c}" }
    }]
  });
  window.addEventListener("resize", () => chart.resize());
}

function createLineChart(elementId, labels, values) {
  const chart = echarts.init(document.getElementById(elementId));
  chart.setOption({
    color: ["#257454"],
    tooltip: { trigger: "axis" },
    grid: { left: 48, right: 20, bottom: 42, top: 30 },
    xAxis: { type: "category", data: labels },
    yAxis: { type: "value", name: "套" },
    series: [{ type: "line", smooth: true, areaStyle: {}, data: values }]
  });
  window.addEventListener("resize", () => chart.resize());
}

function createScatterChart(elementId, items) {
  const chart = echarts.init(document.getElementById(elementId));
  chart.setOption({
    color: ["#58b982"],
    tooltip: {
      formatter: (params) => {
        const item = params.data.raw;
        return `${item.title}<br/>面积: ${item.area}㎡<br/>总价: ${item.total_price}万`;
      }
    },
    grid: { left: 54, right: 24, bottom: 46, top: 30 },
    xAxis: { type: "value", name: "面积㎡" },
    yAxis: { type: "value", name: "总价万" },
    series: [{
      type: "scatter",
      symbolSize: 10,
      data: items.map((item) => ({
        value: [item.area, item.total_price],
        raw: item
      }))
    }]
  });
  window.addEventListener("resize", () => chart.resize());
}
