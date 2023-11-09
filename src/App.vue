<template style="margin: 0;">
  <Header></Header>

  <div>
   <router-view />
  </div>

   <Footer></Footer>
</template>

<script>
  // app.vue - это, грубо говоря, шаблон, который применяется к каждому последующему компоненту/представлению vue
  import Header from './components/TheHeader.vue'
  import Footer from './components/TheFooter.vue'
  import axios from 'axios'
  export default {
    // устанавливаю шапку и подвал
    components: {
      Header,
      Footer,
    },

    // устанавливаю токен и хэдер
    beforeCreate() {

      this.$store.commit('initialize')

      const token = this.$store.state.token

      if (token) {
          axios.defaults.headers.common['Authorization'] = "Token " + token
      } else {
          axios.defaults.headers.common['Authorization'] = ""
      }
    },
  }
</script>

<style>
    #app {
      font-family: 'Avenir', Helvetica, Arial, sans-serif;
      margin-top: -8px;
      margin-left: -8px;
      margin-right: -8px;
      margin-bottom: -8px;
      padding: 0;
    }

</style>