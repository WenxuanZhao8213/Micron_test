<template>
  <div class="app-container">
    <!-- 筛选面板 -->
    <FiltersPanel />

    <!-- 主图表：价格趋势与预测 -->
    <div class="chart-container">
      <LineChart />
    </div>

    <!-- 统计摘要或月度柱状图 -->
    <div class="summary-container">
      <SummaryChart />
    </div>
  </div>
</template>

<script setup>
import FiltersPanel from './components/FiltersPanel.vue'
import LineChart from './components/LineChart.vue'
import SummaryChart from './components/SummaryChart.vue'
</script>

<style scoped>
.app-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 1rem;
  min-height: 100vh;
  display: grid;
  grid-template-rows: auto 1fr 1fr;
  gap: 1.5rem;
}

.chart-container,
.summary-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 1rem;
}

/* 响应式布局调整 */
@media (max-width: 768px) {
  .app-container {
    grid-template-rows: auto auto auto;
    gap: 1rem;
  }
}
</style>
