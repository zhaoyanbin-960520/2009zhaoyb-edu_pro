<template>
    <div class="footer">
        <ul >
            <li v-for="(footer,key) in footer_list" :key="key" v-if="footer.position==2"><a :href="footer.link">{{footer.title}}</a></li>
        </ul>
    </div>

</template>

<script>
export default {
    name: "Footer",
    data(){
        return {
            footer_list:[]
        }
    },
    methods:{
        get_all(){
            this.$axios({
                url:this.$settings.HOST+'home/nav/',
                method:'get'
            }).then(rst=>{
                // console.log(rst.data);
                this.footer_list=rst.data
            }).catch(error=>{
                console.log(error);
            })

        },
    },
    created() {
        this.get_all()
    }
}
</script>

<style scoped>
.footer {
    width: 100%;
    height: 128px;
    background: #25292e;
    color: #fff;
}

.footer ul {
    margin: 0 auto 16px;
    padding-top: 38px;
    width: 810px;
}

.footer ul li  {
    float: left;
    width: 112px;
    margin: 0 10px;
    text-align: center;
    font-size: 14px;
}

.footer ul li a {
    float: left;
    width: 112px;
    margin: 0 10px;
    text-align: center;
    font-size: 14px;
    color: white;
}



.footer ul::after {
    content: "";
    display: block;
    clear: both;
}

.footer p {
    text-align: center;
    font-size: 12px;
}

</style>
