<template>
<div>

    <Row v-for="item in history_data.data" :key="item._id">
        <Col>
        <job-item v-bind:item="item"></job-item>
        </Col>
    </Row>
    <Row>
        <Col>
        <Page @on-change="handle_on_page_change" :total="history_data.total"></Page>
        </Col>
    </Row>
</div>
</template>

<script>
import axios from "axios";
import jobItem from "./job-item.vue";

export default {
    name: "page1",
    data() {
        return {
            history_data: {}
        };
    },
    components: {
        "job-item": jobItem
    },
    methods: {
        handle_view_run_status: function() {
            window.open('http://www.baidu.com', '', '', false)
        },
        handle_on_page_change: function(page_index) {
            this.load_job_list(page_index)
        },
        load_job_list: function(page_index) {
            let self = this;
            axios
                .get("/api/jobs?page_index=" + page_index)
                .then(function(res) {
                    console.log(res);
                    if (res.data.code == 0) {
                        self.history_data = res.data.data;
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
    },
    mounted: function() {
        this.load_job_list(1)
    }
};
</script>
