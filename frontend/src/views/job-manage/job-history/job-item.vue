<template>
<Card>
    <p slot="title">
        <Icon type="navicon-round"></Icon>
        {{item['name']}}
    </p>
    <a v-show="show" href="#" slot="extra"  @click.prevent="show=false">
        <Icon type="ios-arrow-down"></Icon>
        折叠
    </a>
    <a v-show="!show" href="#" slot="extra"   @click.prevent="show=true">
        <Icon type="ios-arrow-right"></Icon>
        展开
    </a>
    <a href="#" slot="extra" style="color:#f90" @click.prevent="changeLimit">
        <Icon type="play"></Icon>
        开始运行
    </a>
    <a href="#" slot="extra" @click.prevent="changeLimit">
        <Icon type="ios-download"></Icon>
        下载训练结果
    </a>
    <a href="#" slot="extra" @click.prevent="handle_view_run_status">
        <Icon type="ios-loop-strong"></Icon>
        查看运行
    </a>
    <a href="#" slot="extra" style="color:red;" @click.prevent="changeLimit">
        <Icon type="trash-a"></Icon>
        删除
    </a>
    <div v-show="show">
        <Row>
            <Col span="20">
            <Form :label-width="80">
                <Row>
                    <Col span="12">
                    <FormItem prop="name" label="任务名:">
                        <Input v-model="item.name" placeholder="请输入任务名">

                        </Input>
                    </FormItem>

                    <FormItem prop="input" label="输入路径:">
                        <Input v-model="item.input" placeholder="格式为 HDFS路径#本地文件夹名称 eg: /tmp/data/tensorflow#data">

                        </Input>
                    </FormItem>
                    </Col>
                    <Col span="12">
                    <FormItem prop="output" label="输出路径:">
                        <Input v-model="item.output" placeholder="格式为 HDFS路径#本地文件夹名称 eg:/tmp/tensorflow_model#model">

                        </Input>
                    </FormItem>
                    <FormItem prop="files" label="本地文件:">
                        <Input v-model="item.files" placeholder="指定作业执行所需本地文件 eg:demo.py,dataDeal.py">

                        </Input>
                    </FormItem>

                    </Col>
                </Row>
                <Row>
                    <Col>
                    <FormItem prop="command" label="命令:">
                        <Input v-model="item.command" placeholder="作业执行命令 eg:python demo.py --data_path=./data --save_path=./model --log_dir=./eventLog --training_epochs=10">

                        </Input>
                    </FormItem>
                    </Col>
                </Row>
                <Row>
                    <Col span="8">
                    <h4 class="group">Worker配置</h4>
                    <FormItem prop="worker_memory" label="worker内存:">
                        <Input v-model="item.worker_memory">

                        </Input>
                    </FormItem>
                    <FormItem prop="worker_cores" label="CPU核数:">
                        <Input v-model="item.worker_cores">

                        </Input>
                    </FormItem>
                    <FormItem prop="worker_num" label="worker数量:">
                        <Input v-model="item.worker_num">

                        </Input>
                    </FormItem>
                    </Col>
                    <Col span="8">
                    <h4 class="group">PS配置</h4>
                    <FormItem prop="ps_memory" label="PS内存:">
                        <Input v-model="item.ps_memory">

                        </Input>
                    </FormItem>
                    <FormItem prop="ps_cores" label="CPU核数:">
                        <Input v-model="item.ps_cores">

                        </Input>
                    </FormItem>
                    <FormItem prop="ps_num" label="PS数量:">
                        <Input v-model="item.ps_num">

                        </Input>
                    </FormItem>
                    </Col>
                    <Col span="8">
                    <h4 class="group">AM配置</h4>
                    <FormItem prop="am_memory" label="AM内存:">
                        <Input v-model="item.am_memory">

                        </Input>
                    </FormItem>
                    <FormItem prop="am_cores" label="CPU核数:">
                        <Input v-model="item.am_cores">

                        </Input>
                    </FormItem>
                    <FormItem prop="am_num" label="am数量:">
                        <Input v-model="item.am_num">

                        </Input>
                    </FormItem>
                    </Col>
                </Row>

            </Form>
            </Col>

            <Col span="4">
            <Upload multiple accept=".py" type="drag" :on-error="handle_upload_error" :action="model_upload_url">
                <div style="padding: 20px 0">
                    <Icon type="ios-cloud-upload" size="30" style="color: #3399ff"></Icon>
                    <p>上传模型文件</p>
                </div>
            </Upload>
            <Upload type="drag" :action="data_upload_url">
                <div style="padding: 20px 0">
                    <Icon type="ios-cloud-upload" size="30" style="color: #3399ff"></Icon>
                    <p>上传数据文件</p>
                </div>
            </Upload>
            </Col>
        </Row>
    </div>

</Card>
</template>

<style scoped>

a {
    margin-right: 10px;
}

</style>


<script>
export default {
    props: ["item"],
    name: "job-item",
    data() {
        return {
            show: false

        }
    }
}
</script>

