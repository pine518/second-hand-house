async function loadAnalysisCharts() {
  try {
    const avgPrice = await fetchJson("/api/analysis/avg-price-by-district");
    createBarChart("avgPriceChart", "区域均价", avgPrice.labels, avgPrice.values);
  } catch (error) {
    showChartError("avgPriceChart", "区域均价加载失败");
  }

  try {
    const count = await fetchJson("/api/analysis/count-by-district");
    createPieChart("countChart", count.items);
  } catch (error) {
    showChartError("countChart", "区域房源数量加载失败");
  }

  try {
    const priceRange = await fetchJson("/api/analysis/price-range");
    createLineChart("priceRangeChart", priceRange.labels, priceRange.values);
  } catch (error) {
    showChartError("priceRangeChart", "总价区间加载失败");
  }

  try {
    const scatter = await fetchJson("/api/analysis/area-price-scatter");
    createScatterChart("scatterChart", scatter.items);
  } catch (error) {
    showChartError("scatterChart", "面积总价关系加载失败");
  }
}

document.addEventListener("DOMContentLoaded", loadAnalysisCharts);
