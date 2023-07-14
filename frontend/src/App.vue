<script setup>
import Login from './components/Login.vue'
import JobCard from './components/JobCard.vue'
import { ref } from 'vue'
const jobs = ref([
  { name: "Job1", desc:"测试描述测试描述测试描述测试描述" },
  { name: "Job2", desc:"测试描述测试描述测试描述测试描述" },
  { name: "Job3", desc:"测试描述测试描述测试描述测试描述" },
])
</script>

<template>
  <!-- <Login/> -->
  <JobCard name="Name your job here" desc="测试"/>
  <JobCard v-for="j in jobs" :name="j.name" :desc="j.desc"></JobCard>
</template>

<style scoped>
</style>
