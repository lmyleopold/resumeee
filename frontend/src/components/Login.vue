<script>
import { defineComponent } from 'vue'
import { ElConfigProvider } from 'element-plus'

export default defineComponent({
    data() {
        return {
            input: ''
        }
    }
})
</script>

<template>
    <el-main justify="center">
        <el-row justify="center">
        <el-card class="box-card" shadow="hover">
        <div class="logo-container">
            <el-col>
                <img class="logo-container" src="logo.png"/>
            </el-col>
        </div>
        <el-tabs type="card" v-model="activeName" @tab-click="handleClick">
            <el-tab-pane label="求职者">
            <el-row justify="center">
                <el-col class="grid-content"><el-input v-model="input" placeholder="手机号、账号或邮箱"></el-input></el-col>
            </el-row>
            <el-row justify="center">
                <el-col><el-input v-model="input" placeholder="密码"></el-input></el-col>
            </el-row>
            <el-row justify="end">
                <el-button type="primary">登录</el-button>
            </el-row>
            </el-tab-pane>
            <el-tab-pane label="HR">
            <el-row justify="center">
                <el-col class="grid-content"><el-input v-model="input" placeholder="手机号、账号或邮箱"></el-input></el-col>
            </el-row>
            <el-row justify="center">
                <el-col><el-input v-model="input" placeholder="密码"></el-input></el-col>
            </el-row>
            <el-row justify="end">
                <el-button type="primary">登录</el-button>
            </el-row>
            </el-tab-pane>
        </el-tabs>
        </el-card>
        </el-row>
        <el-row justify="center">
        <el-card class="box-card" shadow="hover">
            <el-row>
                <el-col><el-link>注册</el-link></el-col>
            </el-row>
            <el-row>
                <el-col><el-link>找回密码</el-link></el-col>
            </el-row>

        </el-card>
        </el-row>
    </el-main>
</template>

<style scoped>
.grid-content {
    width: 378px;
}

.logo-container {
    height: 80px;
    margin-bottom: 20px;
}

.el-card {
    width: 378px;
}

.el-row {
    margin-bottom: 10px;
}

.el-row:last-child {
    margin-bottom: 0px;
}

.el-col {
    text-align: center;
}

.el-divider {
    margin: 5px;
}

</style>
