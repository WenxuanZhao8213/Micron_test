import { defineStore } from 'pinia';
import data from '@/assets/data.json';
import forecastData from '@/assets/forecast.json';

export const useDataStore = defineStore('data', {
  state: () => ({
    rawData: data,
    forecastData: forecastData,
    selectedStates: [],
    selectedRegions: [],
    dateRange: [new Date('2000-01-01'), new Date('2023-12-31')], // 初始化为空数组表示未选择时间
    showForecast: false,
    refreshCharts: 0, // 用数字类型强制刷新
    showRegionAlert: false,
    showForecastAlert: false
  }),
  getters: {
    // 修复 filteredData 计算属性
    filteredData: (state) => {
      if (!state.rawData || state.rawData.length === 0) return []; // 如果 rawData 为空，返回空数组
      return state.rawData.filter(item => {
        const matchesRegion = state.selectedRegions.length === 0 || 
          state.selectedRegions.includes(item.RegionName);
          if (state.dateRange && state.dateRange.length === 2) {
            const itemDate = new Date(item.Date);
            const startDate = new Date(state.dateRange[0]);
            const endDate = new Date(state.dateRange[1]);
    
            // 检查日期是否在范围内
            const inDateRange = itemDate >= startDate && itemDate <= endDate;
            return matchesRegion && inDateRange;
          }
    
          // 如果没有选择时间范围，只匹配区域
          return matchesRegion;
        });
    },
    summaryStats(state) {
      const data = state.selectedRegions.length > 0 ? 
        this.filteredData : 
        state.rawData;
      
      if (data.length === 0) return null;
      const prices = data.map(item => item.Price);
      const sorted = [...prices].sort((a, b) => a - b);
      return {
        mean: prices.reduce((a, b) => a + b, 0) / prices.length,
        median: sorted[Math.floor(sorted.length / 2)],
        stdDev: Math.sqrt(prices.reduce((sq, n) => sq + Math.pow(n - (prices.reduce((a, b) => a + b, 0) / prices.length, 2), 0) / prices.length))
      };
    }
  },
  actions: {
    generateCharts() {
      this.showRegionAlert = this.selectedRegions.length === 0;
    },
    toggleForecast() {
      if (this.selectedRegions.length === 0) {
        this.showForecastAlert = true;
        this.showForecast = false;
      } else {
        this.showForecast = !this.showForecast;
        this.showForecastAlert = false;
      }
    },

    setSelectedMonth(timestamp) {
      this.selectedMonth = new Date(timestamp).toISOString(); // 将时间戳转换为 ISO 格式
    }
    
  }
});