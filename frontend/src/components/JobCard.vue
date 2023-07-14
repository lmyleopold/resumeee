<script>
import { defineComponent } from 'vue'

export default defineComponent({
  data() {
    return {
    }
  }
})
</script>

<script setup>
defineProps(['name', 'desc'])
</script>

<template>
  <el-card class="box-card" shadow="hover">
    <template #header>
      <div class="card-header">
        <span id="job-title">{{ name }}</span>
        <el-button class="button" text>详细信息</el-button>
      </div>
    </template>
    <div>
      <div v-for="o in 2" class="text item">{{ desc }}</div>
    </div>
  </el-card>
</template>

<style>
#job-title {
  font-size: 1.3em
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.text {
  font-size: 14px;
}

.item {
  margin-bottom: 18px;
}

.box-card {
  width: 480px;
}
</style>

<style scoped>
</style>
