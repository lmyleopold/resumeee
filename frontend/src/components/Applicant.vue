<template>
    <div>
        <el-header class="header">
            <div class="header-container">
                <div>
                    <el-image src="/logo.png" style="height: 50px" />
                </div>
                <div>
                    <Submit />
                </div>
            </div>
        </el-header>
        <JobList />
    </div>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
    data() {
        return {}
    }
})
</script>


<style>
.header {
    display: flex;
    justify-content: center;
    align-items: center;
}

.header-container {
    width: 768px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
</style>