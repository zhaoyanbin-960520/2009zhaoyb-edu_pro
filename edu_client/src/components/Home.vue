<template>
   <div>
       <Header></Header>
       <Banner></Banner>
       <Footer></Footer>
   </div>

</template>

<script>
import Header from "./comon/Header";
import Footer from "./comon/Footer";
import Banner from "./Banner";

export default {
    name: "Home",
    components:{
        Header:Header,
        Footer:Footer,
        Banner:Banner,
    }
}
</script>

<style scoped>

</style>
