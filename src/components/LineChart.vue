<template>
  <div class="line-chart-container">

    <!-- ApexCharts 主图表 -->
    <apexchart 
      v-if="chartSeries.length > 0"
      ref="chart"
      type="line" 
      height="400"
      :options="chartOptions"
      :series="chartSeries"
      @click="handleChartClick"
    />
    <p v-else>No data available for the selected filters.</p>
  </div>
</template>


<script setup>
import { computed, ref, watch } from 'vue';
import { useDataStore } from '@/store/dataStore';
import { DateTime } from 'luxon';


const store = useDataStore();
const chart = ref(null); // 图表实例引用


// 生成颜色序列
// const colors = [
//   '#409EFF', '#67C23A', '#E6A23C', '#F56C6C', 
//   '#909399', '#FF82AB', '#7B68EE'
// ];

// const regionOptions = computed(() => 
//   [...new Set(store.rawData.map(item => item.RegionName))]
// );

// 生成图表数据系列
const chartSeries = computed(() => {
  const series = [];
  const selectedRegions = store.selectedRegions.length > 0 ? 
    store.selectedRegions : 
    []; // 使用 regionOptions 作为默认值

  // 确保 filteredData 存在且不为空
  if (!store.filteredData || store.filteredData.length === 0) {
    console.log('filteredData is null')
    return series; // 如果 filteredData 为空，返回空数组
  }

  // 1. 实际价格线（仅展示选中的区域）
  selectedRegions.forEach(region => {
    const regionData = store.filteredData.filter(d => d.RegionName === region); // 使用 filter 而不是 find
    if (regionData && regionData.length > 0) { // 检查 regionData 是否存在
      series.push({
        name: `${region} (Actual)`,
        data: regionData.map(d => ({
          x: new Date(d.Date).getTime(),
          y: d.Price
        })),
        color: '#2196F3', // 蓝色实线
        type: 'line'
      });
    }
  });

  // 2. 预测线与置信区间（仅当开启预测且选中区域时）
  if (store.showForecast && selectedRegions.length > 0) {
    selectedRegions.forEach(region => {
      const forecastForRegion = store.forecastData
        .filter(f => f.RegionName === region)
        .map(f => ({
          x: new Date(f.Date).getTime(),
          y: f.Price,
          upper: f.Upper,
          lower: f.Lower
        }));

      // 预测线（橙色虚线）
      if (forecastForRegion.length > 0) { // 检查预测数据是否存在
        series.push({
          name: `${region} (Forecast)`,
          data: forecastForRegion.map(d => ({ x: d.x, y: d.y })),
          color: '#FF9800',
          type: 'line',
          dashStyle: 'Dash'
        });

        // 置信区间（半透明区域）
        series.push({
          name: `${region} (Confidence)`,
          data: forecastForRegion.map(d => ({ x: d.x, y: [d.lower, d.upper] })),
          type: 'area',
          color: '#f9c25a',
          fill: {
            type: 'gradient',
            gradient: {
              shadeIntensity: 0.2,
              opacityFrom: 0.2,
              opacityTo: 0.1
            }
          }
        });
      }
    });
  }

  return series;
});

const hasData = computed(() => chartSeries.value.length > 0);
console.log('hasData:', hasData)

// 图表配置选项
const chartOptions = computed(() => ({
  chart: {
    id: 'price-trend',
    toolbar: {
      show: true,
      tools: {
        zoom: true,
        zoomin: true,
        zoomout: true,
        pan: true,
        download: '<strong>Download</strong>',
        reset: true
      },
      export: {
        csv: { filename: 'price-data' },
        svg: { filename: 'price-chart' },
        png: { filename: 'price-chart' }
      }
    }
  },
  xaxis: {
    type: 'datetime',
    labels: {
      format: 'MMM yyyy', // 显示为 "Jan 2020"
      datetimeUTC: false
    },
    title: { text: 'Date' }
  },
  yaxis: {
    title: { text: 'Price (USD)' },
    labels: {
      formatter: (value) => `$${value.toLocaleString()}` // 格式化货币
    }
  },
  stroke: {
    width: 2,
    curve: 'smooth'
  },
  markers: {
    size: 4
  },
  tooltip: {
    x: {
      formatter: (value) => DateTime.fromMillis(value).toFormat('MMM yyyy')
    },
    y: {
      formatter: (value) => `$${value.toLocaleString()}`
    }
  },
  legend: {
    position: 'top',
    itemMargin: {
      horizontal: 10
    }
  }
}));

// 处理图表点击事件（更新选中月份）
const handleChartClick = (event, chartContext, config) => {
  if (config.seriesIndex !== undefined) {
    const timestamp = chartSeries.value[config.seriesIndex]?.data[config.dataPointIndex]?.x;
    if (timestamp) {
      store.setSelectedMonth(timestamp);
    }
  }
};

// 监听 refreshCharts 变化，强制刷新图表
watch(() => store.refreshCharts, () => {
  if (chart.value) {
    chart.value.updateSeries(chartSeries.value, true); // 强制重绘
  }
});

// 监听预测开关变化强制刷新图表
// watch(() => store.showForecast, () => {
//   if (chart.value) {
//     chart.value.updateSeries(chartSeries.value, true); // 强制重绘
//   }
// });
</script>

<style scoped>
.line-chart-container {
  background: white;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px #eaed3e1a;
  margin-bottom: 1rem;
}

.formula {
  margin-bottom: 1rem;
  color: #666;
  /* color: '#FF9800'; */
  font-style: italic;
  font-size: 0.9em;
}
</style>