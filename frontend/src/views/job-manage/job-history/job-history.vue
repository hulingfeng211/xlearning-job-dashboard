<template>
<div>

    <Row v-for="item in history_list" :key="item._id">
        <Col>
        <Card>
            <p slot="title">
                <Icon type="ios-film-outline"></Icon>
                {{item['name']}}
            </p>
            <a href="#" slot="extra" @click.prevent="changeLimit">
                <Icon type="play"></Icon>

                开始运行
            </a>
            <a href="#" slot="extra" @click.prevent="changeLimit">
                <Icon type="ios-loop-strong"></Icon>
                查看运行
            </a>
            <div>
                <Row>
                    <Col span="18">
                    <Form>
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

                        <b>内存:{{item['worker_memory']}}</b>
                        <b>CPU核数:{{item['worker_cores']}}</b>
                        <b>进程数:{{item['worker_num']}}</b>
                    </Form>
                    </Col>

                    <Col span="6">
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
        </Col>
    </Row>
</div>
</template>

<script>
import axios from "axios";

export default {
  name: "page1",
  data() {
    return {
      history_list: []
    };
  },
  mounted: function() {
    let self = this;
    axios
      .get("/api/jobs")
      .then(function(res) {
        console.log(res);
        if (res.data.code == 0) {
          self.history_list = res.data.data;
        } else {
          self.$Notice.open({
            title: "服务异常",
            desc: "请联系管理员"
          });
        }
      })
      .catch(function(err) {
        console.log(err);
      });
  }
};
</script>
