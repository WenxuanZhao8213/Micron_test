<template>
  <div class="summary-chart-container">
    <h3>Statistical Summary</h3>
    <apexchart 
      v-if="formattedStats"
      type="bar"
      height="350"
      :options="barChartOptions"
      :series="barChartSeries"
    />
    <p v-else>No data available for the selected filters.</p>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useDataStore } from '@/store/dataStore';
// import { DateTime } from 'luxon';

const store = useDataStore();

// 格式化月份显示（如 "January 2023"）
// const formattedMonth = computed(() => {
//   if (!store.selectedMonth) return '';
//   return DateTime.fromISO(store.selectedMonth).toFormat('MMMM yyyy');
// });

// 统计摘要数据格式化（货币和数值格式）
// const formattedStats = computed(() => {
//     console.log('summaryStats:', store.summaryStats); // 调试信息
//   if (!store.summaryStats) return null;
//   return {
//     'Mean': `$${store.summaryStats.mean.toLocaleString(undefined, { maximumFractionDigits: 2 })}`,
//     'Median': `$${store.summaryStats.median.toLocaleString(undefined, { maximumFractionDigits: 2 })}`,
//     'Standard Deviation': `$${store.summaryStats.stdDev.toLocaleString(undefined, { maximumFractionDigits: 2 })}`,
//     'Minimum': `$${store.summaryStats.min.toLocaleString()}`,
//     'Maximum': `$${store.summaryStats.max.toLocaleString()}`,
//     '25th Percentile': `$${store.summaryStats.percentile25.toLocaleString()}`,
//     '75th Percentile': `$${store.summaryStats.percentile75.toLocaleString()}`
//   };
// });
const formattedStats = computed(() => {
  if (!store.summaryStats) return null;
  console.log('summaryStats:', store.summaryStats);
  return {
    'Mean': store.summaryStats.mean,
    'Median': store.summaryStats.median,
    'Standard Deviation': store.summaryStats.stdDev,
    // 'Minimum': store.summaryStats.min,
    // 'Maximum': store.summaryStats.max,
    // '25th Percentile': store.summaryStats.percentile25,
    // '75th Percentile': store.summaryStats.percentile75
  };
});


// const barChartSeries = computed(() => [{
//   name: 'Price (USD)',
//   data: Object.values(formattedStats.value || {})
// }]);

// // 柱状图配置选项
// // 柱状图配置
// const barChartOptions = computed(() => ({
//   chart: {
//     type: 'bar',
//     toolbar: { show: false }
//   },
//   plotOptions: {
//     bar: {
//       horizontal: false,
//       borderRadius: 4,
//       dataLabels: { position: 'top' }
//     }
//   },
//   xaxis: {
//     categories: Object.keys(formattedStats.value || {})
//   },
//   yaxis: {
//     title: { text: 'Price (USD)' },
//     labels: { formatter: (value) => `$${value.toLocaleString()}` }
//   },
//   dataLabels: {
//     enabled: true,
//     formatter: (val) => `$${val.toLocaleString()}`,
//     offsetY: -20
//   },
//   tooltip: {
//     y: { formatter: (val) => `$${val.toLocaleString()}` }
//   }
// }));
const barChartSeries = computed(() => {
  return store.selectedRegions.map(region => {
    const regionData = store.filteredData.filter(d => d.RegionName === region);
    const prices = regionData.map(d => d.Price);
    const sorted = [...prices].sort((a, b) => a - b);
    
    return {
      name: region,
      data: [
        prices.reduce((a, b) => a + b, 0) / prices.length, // Mean
        sorted[Math.floor(sorted.length / 2)], // Median
        Math.sqrt(prices.reduce((sq, n) => sq + Math.pow(n - (prices.reduce((a, b) => a + b, 0) / prices.length), 2), 0) / prices.length) // Std
      ]
    };
  });
});

const barChartOptions = computed(() => ({
  chart: { type: 'bar' },
  xaxis: {
    categories: ['Mean', 'Median', 'Standard Deviation']
  },
  plotOptions: {
    bar: {
      horizontal: false,
      columnWidth: '60%',
      endingShape: 'rounded'
    }
  },
  dataLabels: {
    enabled: false
  },
  legend: {
    position: 'top'
  },
  colors: ['#409EFF', '#67C23A', '#E6A23C'],
  yaxis: {
    title: { text: 'Price (USD)' },
    labels: {
      formatter: (val) => `$${val.toFixed(2)}`
    }
  }
}));
</script>

<style scoped>
.summary-chart-container {
  background: white;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-top: 1rem;
}

h3 {
  margin: 0 0 1rem 0;
  color: #333;
}

.stats-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 0.5rem;
}

.stats-table th,
.stats-table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.stats-table th {
  background-color: #f8f9fa;
  font-weight: 600;
}

.stats-table tr:hover {
  background-color: #f5f5f5;
}
</style>
