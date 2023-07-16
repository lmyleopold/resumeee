<script setup>
import JobCard from './JobCard.vue'
import { defineComponent } from 'vue'
import axios from 'axios'
</script>

<script>
export default defineComponent({
    data() {
        return {
            jobs: [
                {name: "1", desc: "岗位描述"},
                {name: "2", desc: "岗位描述"},
            ],
            pagenum: 1
        }
    },
    // mounted() {
    //     axios.get(`/applicant/jobs?pagenum=${pagenum}&pagesize=10`)
    //         .then(response => response.json())
    //         .then(data => {
    //             console.log(data)
    //         })
    //         .catch(error => console.error(error))
    // },
    watch: {
        pagenum(newValue, oldValue) {
            console.log(`${oldValue} -> ${newValue}, ${this.pagenum}`);
            // axios
            //     .get(`/applicant/jobs?pagenum=${newValue}&pagesize=10`)
            //     .then((response) => response.json())
            //     .then((data) => {
            //     console.log(data);
            //     })
            //     .catch((error) => console.error(error));
        }
    }
})
</script>

<template>
    <el-row justify="center">
        <el-col class="grid-content">
            <div v-for="j in jobs" class="job-card">
                <JobCard :name="j.name" :desc="j.desc" :detail_url="1"/>
            </div>
        </el-col>
        <el-col class="grid-content" justify="center">
            <el-pagination background layout="prev, pager, next" :total="1000" v-model:current-page="pagenum" />
        </el-col>
    </el-row>
</template>

<style scoped>
    .job-card {
        margin-top: 10px;
        margin-bottom: 10px;
    }

    .grid-content {
        max-width: 768px;
    }
</style>