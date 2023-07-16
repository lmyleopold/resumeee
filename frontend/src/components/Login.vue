<script setup>
import { defineComponent, ref } from 'vue'
import axios from 'axios';
</script>

<script>
const activeName = ref('applicant');
export default defineComponent({
    data() {
        return {
            username: '',
            password: '',
            
        }
    },
    methods: {
        handleSubmit() {
            if (activeName.value === 'applicant') {
                var api_url = 'applicant/signin';
            } else if (activeName.value === 'mgr') {
                var api_url = 'api/mgr/signin';
            } 
            const params = new URLSearchParams();
            params.append('username', this.username);
            params.append('password', this.password);
            axios.post(api_url, params)
                .then(response => {
                    console.log(response.data)
                    if (response.data.ret) {
                        const loginErrorContainer = document.getElementById('login-error-container');
                        console.log(loginErrorContainer)
                        loginErrorContainer.innerText = response.data.msg;
                    } else {
                        if (activeName.value === 'applicant') {
                            this.$router.push('/applicant')
                        } else if (activeName.value === 'mgr') {
                            this.$router.push('/mgr')
                        } 
                    }
                })
                .catch(error => {
                    console.log(error)
                })
        },
        handleClick(tab, event) {
            console.log(tab, event)
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
                        <img class="logo-container" src="/logo.png" />
                    </el-col>
                </div>
                <el-tabs type="card" v-model="activeName" @tab-click="handleClick">
                    <el-tab-pane label="求职者" name="applicant">
                        <el-row justify="center">
                            <el-col class=""><el-input v-model="username" placeholder="手机号、账号或邮箱"></el-input></el-col>
                        </el-row>
                        <el-row justify="center">
                            <el-col><el-input v-model="password" placeholder="密码" type="password"></el-input></el-col>
                        </el-row>
                        <el-row justify="end">
                            <el-col class="text-end"><el-link>忘记密码？</el-link></el-col>
                        </el-row>
                        <el-row justify="center">
                            <el-button type="primary" :onclick="handleSubmit" round>登录</el-button>
                            <el-button round>注册</el-button>
                        </el-row>
                    </el-tab-pane>
                    <el-tab-pane label="HR" name="mgr">
                        <el-row justify="center">
                            <el-col><el-input v-model="username" placeholder="手机号、账号或邮箱"></el-input></el-col>
                        </el-row>
                        <el-row justify="center">
                            <el-col><el-input v-model="password" placeholder="密码" type="password"></el-input></el-col>
                        </el-row>
                        <el-row justify="end">
                            <el-col class="text-end"><el-link>忘记密码？</el-link></el-col>
                        </el-row>
                        <el-row justify="center">
                            <el-button type="primary" :onclick="handleSubmit" round>登录</el-button>
                            <el-button round>注册</el-button>
                        </el-row>
                    </el-tab-pane>
                </el-tabs>
                
                <el-col style="text-align: center; margin-top: 10px;">
                    <el-text id="login-error-container" type="danger"></el-text>
                </el-col>
            </el-card>
        </el-row>
    </el-main>
</template>

<style scoped>
.logo-container {
    height: 80px;
    margin-bottom: 20px;
    text-align: center;
}

.el-card {
    width: 378px;
}

.el-row {
    margin-bottom: 10px;
    padding-left: 10px;
    padding-right: 10px;
}

.el-row:last-child {
    margin-bottom: 0px;
}

.text-center {
    text-align: center;
}

.text-end {
    text-align: end;
}


.el-divider {
    margin: 5px;
}
</style>
