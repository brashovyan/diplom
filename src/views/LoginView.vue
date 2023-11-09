<template>
    <div>
        <input v-model="email" type="email">
        <input v-model="password" type="password">
        <button @click="login()">Войти</button>
        <template v-for="(error, key) in errors" :key="key">
            {{ error }}
        </template>
        <template v-for="(error2, key) in errors2" :key="key">
            {{ error2 }}
        </template>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'LogIn',
    data() {
        return {
            email: '',
            password: '',
            token: '',
            errors: [],
            error2: "", 
        }
    },

    // это название страницы в закладках браузера
    mounted() {
        document.title = 'Авторизация'
    },

    methods: {
        async login() {
            // обнуляю дефолтный хэдер
            axios.defaults.headers.common["Authorization"] = "";

            // обнуляю localStorage
            localStorage.removeItem("token");
            localStorage.removeItem("userid");

            // удаляю токен и айди из store
            this.$store.commit('removeToken');

            // формирую данные, которые отправлю на сервак (json'чик)
            const formData = {
                email: this.email,
                password: this.password
            }

            // отправляю на сервак пост запрос
            await axios
                .post("auth/token/login/", formData)
                .then(response => {

                    // когда я получаю ответ, то извлекаю токен
                    this.token = response.data.auth_token;

                    // ставлю дефолтный хэдер
                    axios.defaults.headers.common["Authorization"] = "Token " + this.token

                    // вызываю функцию для получения айдишника и сохранения данных
                    this.get_id();
                    
                    
                })
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

        },

        async get_id(){
            // запрос на получение айди юзера
            await axios.get('auth/users/me/').then(response => {
                const userid = response.data.id;

                // ложу в localstorage токен и айдишник
                localStorage.setItem("userid", userid);
                localStorage.setItem("token", this.token);

                console.log(userid);
                // сохраняю всё в store
                this.$store.commit('setToken', this.token);
                this.$store.commit('setUserid', userid);

                // перенаправляю его на главную страницу
                this.$router.push('/');
            })
            .catch(error => {
                this.errors2 = [];
                if (error.response) {
                    this.errors2 = [];
                    for (const property in error.response.data) {
                        this.errors2.push(`${error.response.data[property]}`)
                    }
                } else {
                    this.errors2.push('Что-то пошло не так! Повторите попытку позже)')
                }
            })
        }
    }
}
</script>