<template>
    <div>
        <h1>page1</h1>
        <h3>{{msg}}</h3>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'page1',
    data(){
        return {
            msg:"Hello,iView local"
        }
    },
    mounted:function(){
        let self=this
        axios.get('/api/hello').then(function(res){
            console.log(res)
            self.msg=res.data
        }).catch(function(err){
            console.log(err)
        })
    }


};

</script>
