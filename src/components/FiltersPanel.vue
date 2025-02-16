<template>
  <div class="filters-panel">

    <!-- 区域多选下拉菜单 -->
    <div class="filter-item">
      <label>Regions:</label>
      <el-select
        v-model="store.selectedRegions"
        multiple
        filterable
        placeholder="Select Regions(required)"
        :required="true"
        style="width: 100%"
      >
        <el-option
          v-for="item in regionOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>
    </div>

    <!-- 时间范围选择器 -->
    <div class="filter-item">
      <label>Date Range:</label>
      <el-date-picker
        v-model="store.dateRange"
        type="daterange"
        range-separator="-"
        start-placeholder="Start Date"
        end-placeholder="End Date"
        value-format="YYYY-MM-DD"
        :default-value="[new Date('2000-01-01'), new Date('2023-12-31')]"
        :picker-options="pickerOptions"
        style="width: 100%"
      />
    </div>

     
    <div class="filter-item forecast-switch">
      <el-switch
        v-model="store.showForecast"
        active-text="Show Forecast"
        :disabled="store.selectedRegions.length === 0"
        @change="handleForecastToggle"
      />
    </div>

    <!-- 提示信息 -->
    <!-- <div v-if="store.showForecastAlert" class="alert-message">
      Please select at least one region to enable forecast.
    </div> -->
    <el-alert
      v-if="showAlert"
      :title="alertMessage"
      type="error"
      :closable="false"
      show-icon
      style="margin-top: 1rem"
    />

    <!-- 搜索按钮与预测开关 -->
    <div class="filter-actions">
      <el-button
        type="primary"
        @click="generateCharts"
        style="width: 100%"
      >
        Generate Charts
      </el-button>
    </div>
  </div>
</template>


<script setup>
import { computed,ref } from 'vue';
import { useDataStore } from '@/store/dataStore';
// import { ElMessage } from 'element-plus';

const store = useDataStore();
const showAlert = ref(false);
const alertMessage = ref('');



// 时间选择器的限制配置
const pickerOptions = ref({
  disabledDate(time) {
    // 限制时间选择范围为 2000-01-01 到 2023-12-31
    const minDate = new Date('2000-01-01');
    const maxDate = new Date('2023-12-31');
    return time.getTime() < minDate.getTime() || time.getTime() > maxDate.getTime();
  }
});

// 区域选项
const regionOptions = computed(() => {
  return [...new Set(store.rawData.map(item => item.RegionName))].map(region => ({
    label: region,
    value: region
  }));
});

// 生成图表前验证
const validateSelection = () => {
  if (store.selectedRegions.length === 0) {
    showAlert.value = true;
    alertMessage.value = 'Please select at least one region.';
    return false;
  }
  showAlert.value = false;
  return true;
};

// 搜索按钮逻辑（可扩展异步操作）
// const generateCharts = () => {
//   store.refreshCharts = !store.refreshCharts; // 触发图表重新渲染
// };

// 生成图表
const generateCharts = () => {
  if (!validateSelection()) return;
  store.refreshCharts = !store.refreshCharts;
};

// 处理预测开关
const handleForecastToggle = (val) => {
  if (!validateSelection()) {
    store.showForecast = false;
    return;
  }
  store.showForecast = val;
};
</script>

<style scoped>
.filters-panel {
  padding: 1rem;
  background: #f5f5f5;
  border-radius: 8px;
  margin-bottom: 1rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.filter-item {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #333;
}

.filter-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-top: 1rem;
}

.generate-btn {
  padding: 0.5rem 1rem;
  background: #4CAF50;
  color: rgb(13, 13, 13);
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s;
}

.generate-btn:hover {
  background: #45a049;
}

.forecast-switch {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.alert-message {
  margin-top: 1rem;
  padding: 0.5rem;
  background: #fff3cd;
  border-radius: 4px;
  color: #856404;
}

</style>
