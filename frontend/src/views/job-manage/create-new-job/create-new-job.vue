<style lang="less">
@import "./new-job.less";
</style>
<template>
<div class="form-con">
    <Form ref="jobForm" :model="form" :rules="rules" :label-width="80">
        <Card :bordered="false">
            <p slot="title">常规设置

            </p>
            <div>
                <Row>
                    <Col span="12">
                    <FormItem prop="name" label="任务名:">
                        <Input v-model="form.name" placeholder="请输入任务名">

                        </Input>
                    </FormItem>
                    <FormItem prop="type" label="任务类型:">
                        <Input disabled v-model="form.type">

                        </Input>
                    </FormItem>
                    <FormItem prop="input" label="输入路径:">
                        <Input v-model="form.input" placeholder="格式为 HDFS路径#本地文件夹名称 eg: /tmp/data/tensorflow#data">

                        </Input>
                    </FormItem>
                    <FormItem prop="output" label="输出路径:">
                        <Input v-model="form.output" placeholder="格式为 HDFS路径#本地文件夹名称 eg:/tmp/tensorflow_model#model">

                        </Input>
                    </FormItem>
                    <FormItem prop="files" label="本地文件:">
                        <Input v-model="form.files" placeholder="指定作业执行所需本地文件 eg:demo.py,dataDeal.py">

                        </Input>
                    </FormItem>
                    <FormItem prop="command" label="命令:">
                        <Input v-model="form.command" placeholder="作业执行命令 eg:python demo.py --data_path=./data --save_path=./model --log_dir=./eventLog --training_epochs=10">

                        </Input>
                    </FormItem>
                    </Col>
                    <Col span="12">
                    <Upload multiple accept=".py" type="drag" :on-error="handle_upload_error" :action="model_upload_url">
                        <div style="padding: 20px 0">
                            <Icon type="ios-cloud-upload" size="52" style="color: #3399ff"></Icon>
                            <p>上传模型文件</p>
                        </div>
                    </Upload>
                    <Upload type="drag" :action="data_upload_url">
                        <div style="padding: 20px 0">
                            <Icon type="ios-cloud-upload" size="52" style="color: #3399ff"></Icon>
                            <p>上传数据文件</p>
                        </div>
                    </Upload>
                    </Col>
                </Row>
            </div>
        </Card>



        <Card :bordered="false">
            <p slot="title">Worker设置</p>
            <div>
                <FormItem prop="worker_memory" label="worker内存:">
                    <Input v-model="form.worker_memory" placeholder="指定worker申请内存，默认单位为MB eg:10G">

                    </Input>
                </FormItem>
                <FormItem prop="worker_cores" label="worker CPU:">

                    <InputNumber :max="10" :min="1" v-model="form.worker_cores"></InputNumber>
                    <span>指定worker申请的CPU核数</span>
                </FormItem>
                <FormItem prop="worker_num" label="worker数量:">

                    <InputNumber :max="10" :min="1" v-model="form.worker_num"></InputNumber>
                    <span>指定worker申请数目</span>
                </FormItem>

            </div>
        </Card>


        <Card :bordered="false">
            <p slot="title">PS设置</p>
            <div>
                <FormItem prop="ps_memory" label="worker内存:">
                    <Input v-model="form.ps_memory" placeholder="指定ps申请的内存大小，默认单位为MB eg:10G">

                    </Input>
                </FormItem>
                <FormItem prop="ps_cores" label="ps CPU:">

                    <InputNumber :max="10" :min="1" v-model="form.ps_cores"></InputNumber>
                    <span>指定ps申请的CPU核数</span>
                </FormItem>
                <FormItem prop="ps_num" label="ps 数量:">

                    <InputNumber :max="10" :min="1" v-model="form.ps_num"></InputNumber>
                    <span>指定ps申请数目</span>
                </FormItem>
            </div>
        </Card>

        <Card :bordered="false">
            <p slot="title">AM 设置</p>
            <div>
                <FormItem prop="am_memory" label="AM 内存:">
                    <Input v-model="form.am_memory" placeholder="指定am申请的内存大小，默认单位为MB eg:10G">

                    </Input>
                </FormItem>
                <FormItem prop="am_cores" label="AM CPU:">

                    <InputNumber :max="10" :min="1" v-model="form.am_cores"></InputNumber>
                    <span>指定am申请的CPU核数</span>
                </FormItem>
                <FormItem prop="am_num" label="am 数量:">

                    <InputNumber :max="10" :min="1" v-model="form.am_num"></InputNumber>
                    <span>指定am申请数目</span>
                </FormItem>
            </div>
            <div>
                <Button type="primary" icon="checkmark-round">提交</Button>
            </div>
        </Card>

    </Form>
</div>
</template>

<script>
export default {
    name: "page2",
    data() {
        return {
            form: {
                name: "tensorflow_demo  ",
                type: "tensorflow",
                input:"/tmp/data/tensorflow#data",
                output:"/tmp/tensorflow_model#model",
                files:"demo.py,dataDeal.py",
                command:"python3 demo.py --data_path=./data --save_path=./model  --log_dir=./eventLog --training_epochs=10",
                worker_memory:"2G",
                worker_cores:2,
                worker_num:1,
                ps_memory:"2G",
                ps_cores:2,
                ps_num:1,
                am_memory:"2G",
                am_cores:2,
                am_num:1
            },
            model_file_type:'.py',
            uuid:"",
            rules: {
                name: [{
                    required: true,
                    message: "任务名不能为空！",
                    trigger: "blur"
                }]
            }
        };
    },
    mounted: function() {
        this.uuid=this.util.guid()
    },
    methods: {
        handle_upload_error:function(error, file, fileList){
            console.log(error)
            this.$Notice.warning({
                        title: '上传文件错误.'
                    });
        }
    },
    computed:{
        model_upload_url:function(){
           return  '/api/upload/model?type=model&uuid='+this.uuid
        },
        data_upload_url:function(){
           return  '/api/upload/model?type=data&uuid='+this.uuid
        },
         
    }
};
</script>