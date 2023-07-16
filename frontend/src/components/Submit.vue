
<script setup lang="ts">
import { ref } from 'vue'
import { genFileId } from 'element-plus'
import type { UploadInstance, UploadProps, UploadRawFile } from 'element-plus'

const visible = ref(false)
const upload = ref<UploadInstance>()

const handleExceed: UploadProps['onExceed'] = (files) => {
    upload.value!.clearFiles()
    const file = files[0] as UploadRawFile
    file.uid = genFileId()
    upload.value!.handleStart(file)
}

const submitUpload = () => {
    upload.value!.submit()
}

const props = defineProps({
    prompt: String,
    url: String
})
</script>

<template>
    <el-popover :visible="visible" placement="top" :width="200">
        <div style="text-align: left; margin: 0">
            <el-text type="info" size="small">
                {{ props.prompt }}
            </el-text>
            <el-upload ref="upload"
                action="{{ url }}" :limit="1" :on-exceed="handleExceed"
                :auto-upload="false">
                <template #trigger>
                    <el-button text style="padding: 0;">
                        <el-text size="small">选择文件</el-text>
                    </el-button>
                </template>
            </el-upload>
            <div style="text-align: right; margin: 0">
                <el-button size="small" text @click="visible = false">取消</el-button>
                <el-button size="small" type="primary" @click="visible = false;submitUpload();">确认</el-button>
            </div>
        </div>
        <template #reference>
            <el-button @click="visible = true;" >上传</el-button>
        </template>
    </el-popover>
</template>