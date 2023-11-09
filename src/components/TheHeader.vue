<template>
    <header>
        <p><router-link to="/">Home</router-link></p>
        <p><router-link to="/about">About</router-link></p>

        <!-- Если челик авторизован -->
        <template v-if="$store.state.isAuthenticated">
            <button @click="logout()">Logout</button>
            {{ $store.state.userid }}

        </template>

        <!-- Если челик неавторизован -->
        <template v-else>
            <p><router-link to="/login">Login</router-link></p>
            <p><router-link to="/register">Register</router-link></p>
        </template>

        <template v-for="(error, key) in errors" :key="key">
            {{ error }}
        </template>
    </header>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      errors: [],
    };
  },

  methods: {
    async logout() {
        // отправляю на сервак пост запрос, что хочу разлогиниться
        await axios
                .post("auth/token/logout/")

                // здесь обрабатываем ошибки
                .catch(error => {
                    this.errors = [];
                    if (error.response) {  
                        for (const property in error.response.data) {
                            this.errors.push(`${error.response.data[property]}`)
                        }
                    } else {
                        this.errors.push('Что-то пошло не так! Повторите попытку позже)')
                    }
                })

        // обнуляю дефолтный хэдер
        axios.defaults.headers.common["Authorization"] = "";

        // обнуляю localStorage
        localStorage.removeItem("token");
        localStorage.removeItem("userid");

        // удаляю токен и айди из store
        this.$store.commit('removeToken');

        // перенаправляю на главную
        this.$router.push('/');
    },
  },
};
</script>

<style scoped>
    header{
        background-color: aqua;
        width: 100%;
        height: 100%;
        margin-top: -8px;
        display: flex;
    }

    p{
        margin: 5px;
    }
</style>