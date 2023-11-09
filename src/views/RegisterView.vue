<template>
    <div>
        <input type="email" v-model="email" placeholder="email">
        <input type="password" v-model="password1" placeholder="password">
        <input type="password" v-model="password2" placeholder="repeat password">
        <button @click="register()">Зарегистрироваться</button>
        {{ errors }}
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'SignUp',
    data() {
        return {
            email: '',
            password1: '',
            password2: '',
            errors: [],
            data: "",
        }
    },
    methods: {
        async register() {
            // сперва я проверяю на фронте, что юзер всё заполнил
            this.errors = []

            if (this.email === '') {
                this.errors.push('The username is missing')
            }

            if (this.password1 === '') {
                this.errors.push('The password is too short')
            }

            if (this.password1 !== this.password2) {
                this.errors.push('The passwords doesn\'t match')
            }

            // если юзер всё заполнил, то пытаемся регаться
            if (!this.errors.length) {
                const formData = {
                    email: this.email,
                    password: this.password1
                }

                await axios
                    .post("auth/users/", formData)
                    .then(response => {

                        // если юзер успешно зареган, то мы оказываемся тут и логиним его
                                this.data = response.data;
                            // обнуляю дефолтный хэдер
                                 axios.defaults.headers.common["Authorization"] = ""

                                // обнуляю localStorage
                                localStorage.removeItem("token")

                                // формирую данные, которые отправлю на сервак (json'чик)
                                const formData = {
                                    email: this.email,
                                    password: this.password1
                                }

                                // отправляю на сервак пост запрос
                                axios
                                    .post("auth/token/login/", formData)
                                    .then(response => {

                                        // когда я получаю ответ, то извлекаю токен
                                        const token = response.data.auth_token

                                        // сохраняю его в localStorage (т.е. вызываю store/index.js/SetToken)
                                        this.$store.commit('setToken', token)
                                        
                                        // ставлю дефолтный хэдер
                                        axios.defaults.headers.common["Authorization"] = "Token " + token

                                        // сохраняю его в классический localStorage
                                        localStorage.setItem("token", token)

                                        // перенаправляю его на главную страницу
                                        this.$router.push('/')

                                    })
                                    // здесь обрабатываем ошибки (ну мало ли)
                                    .catch(error => {
                                        if (error.response) {
                                            for (const property in error.response.data) {
                                                this.errors.push(`${property}: ${error.response.data[property]}`)
                                            }
                                        } else {
                                            this.errors.push('Something went wrong. Please try again')
                                            
                                            console.log(JSON.stringify(error))
                                        }
                                    })


                    })
                    .catch(error => {
                        if (error.response) {
                            for (const property in error.response.data) {
                                this.errors.push(`${property}: ${error.response.data[property]}`)
                            }

                            console.log(JSON.stringify(error.response.data))
                        } else if (error.message) {
                            this.errors.push('Something went wrong. Please try again')
                            
                            console.log(JSON.stringify(error))
                        }
                    })
            }
        }
    }
}
</script>