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
defineProps(['name', 'desc', 'detail_url'])
</script>

<template>
  <el-card class="box-card" shadow="hover">
    <template #header>
      <div class="card-header">
        <span id="job-title">{{ name }}</span>
        <el-button class="button" text v-if="detail_url">详细信息</el-button>
      </div>
    </template>
    <div>
      <div class="text item">{{ desc }}</div>
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
</style>

<style scoped>
</style>
