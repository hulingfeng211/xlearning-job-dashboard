<template>
    <div>
        <h1>Create NEW JOB</h1>
        <Button @click="button_click_handle(true)" type="primary">通知</Button>
    </div>
</template>

<script>
export default {
    name: 'page2',
    mounted:function(){
        
    },
    methods:{
        button_click_handle:function(nodesc) {
                this.$Notice.open({
                    title: 'Notification title',
                    desc: nodesc ? '' : 'Here is the notification description. Here is the notification description. '
                });
            }
    }
};
</script>