<template>
    <div class="cart_item">
        <div class="cart_column column_1">
            <el-checkbox class="my_el_checkbox" v-model="course.selected"></el-checkbox>
        </div>
        <div class="cart_column column_2">
            <img :src="course.course_img" alt="">
            <span><router-link to="/course/detail/1">{{course.name}}</router-link></span>
        </div>
        <div class="cart_column column_3">
            <el-select v-model="course.expire_id" size="mini" placeholder="请选择购买有效期"
                       class="my_el_select">
                <el-option label="1个月有效" :value="30" key="30"></el-option>
                <el-option label="2个月有效" :value="60" key="60"></el-option>
                <el-option label="3个月有效" :value="90" key="90"></el-option>
                <el-option label="永久有效" :value="10000" key="10000"></el-option>
            </el-select>
        </div>
        <div class="cart_column column_4">¥{{course.price}}</div>
        <div class="cart_column column_4" @click="del_cart">删除</div>
    </div>
</template>

<script>
export default {
    name: "CartItem",
    props: ['course'],
    watch: {
        // 监听selected是否发生了变化
        "course.selected": function () {
            this.change_selected();
        },
    },
    methods: {

        // 在修改选中状态之前判断用户是否已经登录
        check_user_login() {
            let token = sessionStorage.token || localStorage.token;
            if (!token) {
                let self = this;
                this.$confirm("对不起，请登录后再添加购物车", {
                    callback() {
                        self.$router.push("/login");
                    }
                })
                return false
            }
            return token
        },

        // 发起请求，修改redis中购物车的勾选状态
        change_selected() {
            let token = this.check_user_login();
            this.$axios({
                url: this.$settings.HOST + "cart/change/",
                method: 'patch',
                headers: {
                    // 必须请求头中携带token "jwt token值"
                    "Authorization": "jwt " + token,
                },
                data: {
                    selected: this.course.selected,
                    course_id: this.course.id
                }
            }).then(res=>{
                this.$message.success("选中状态修改成功")
                console.log(this.course.selected,this.course.id)

            }).catch(error=>{

            })


        },

        //删除商品
        del_cart(){
            let token = this.check_user_login();
            this.$axios({
                url:this.$settings.HOST+"cart/change/",
                method:"delete",
                headers:{
                    "Authorization": "jwt " + token,
                },
                data:{
                    course_id:this.course.id
                }
            }).then(res=>{
                    this.$message.success(res.data.msg)
                    this.$router.go(0)
            }).catch(error=>{

            })

        }
    }
}
</script>

<style scoped>
.cart_item::after {
    content: "";
    display: block;
    clear: both;
}

.cart_column {
    float: left;
    height: 250px;
}

.cart_item .column_1 {
    width: 88px;
    position: relative;
}

.my_el_checkbox {
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    top: 0;
    margin: auto;
    width: 16px;
    height: 16px;
}

.cart_item .column_2 {
    padding: 67px 10px;
    width: 520px;
    height: 116px;
}

.cart_item .column_2 img {
    width: 175px;
    height: 115px;
    margin-right: 35px;
    vertical-align: middle;
}

.cart_item .column_3 {
    width: 197px;
    position: relative;
    padding-left: 10px;
}

.my_el_select {
    width: 117px;
    height: 28px;
    position: absolute;
    top: 0;
    bottom: 0;
    margin: auto;
}

.cart_item .column_4 {
    padding: 67px 10px;
    height: 116px;
    width: 142px;
    line-height: 116px;
}

</style>
