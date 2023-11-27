<template>
    <div class="login__form__main">
        <div class="login__form">
            <div class="login__form2">
                <p class="auth">Авторизация</p>
                <div class="div__input">
                    <p class="p__placeholder">Эл. почта:</p>
                    <input v-model="email" type="email" class="email" placeholder="Эл. почта" required>
                </div>
                <div class="div__input">
                    <p class="p__placeholder">Пароль:</p>
                    <input v-model="password" type="password" placeholder="Пароль" class="email" required>
                </div>
                <p class="forgetpas"><router-link to="/forgetpassword" class="forgetpas__router">Забыли пароль?</router-link></p>
                
                <button @click="login()" class="login__btn">Войти</button>
                <div class="login__errors">
                    <template v-for="(error, key) in errors_login" :key="key">
                        <p>{{ error }}</p>
                    </template>
                    <template v-for="(error, key) in errors_id" :key="key">
                        <p>{{ error }}</p>
                    </template>
                </div>
            </div>
        </div>
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
            errors_login: [],
            error_id: "", 
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
            localStorage.removeItem("userphoto");

            // удаляю токен и айди из store
            this.$store.commit('removeToken');

            // формирую данные, которые отправлю на сервак (json'чик)
            const formData = {
                email: this.email,
                password: this.password
            }

            
            // отправляю на сервак пост запрос
            if(this.email != "" && this.password != ""){
                // включаем анимацию загрузки
                let load = document.querySelector('.loading'); 
                load.style.display = 'block';

                await axios
                .post("auth/token/login/", formData)
                .then(response => {

                    let load = document.querySelector('.loading'); load.style.display = 'none';

                    // когда я получаю ответ, то извлекаю токен
                    this.token = response.data.auth_token;

                    // ставлю дефолтный хэдер
                    axios.defaults.headers.common["Authorization"] = "Token " + this.token

                    // вызываю функцию для получения айдишника и сохранения данных
                    this.get_id();
                    
                    
                })
                // здесь обрабатываем ошибки
                .catch(error => {
                    this.errors_login = [];
                    let load = document.querySelector('.loading'); load.style.display = 'none';
                    if (error.response) {  
                        for (const property in error.response.data) {
                            this.errors_login.push(`${error.response.data[property]}`)
                        }
                    } else {
                        this.errors_login.push('Что-то пошло не так! Повторите попытку позже)')
                    }
                })
            }
            else{
                this.errors_login = [];
                this.errors_login.push('Пожалуйста, заполните все поля!');
            }
        },

        async get_id(){
            // запрос на получение айди юзера
            // включаем анимацию загрузки
            let load = document.querySelector('.loading'); 
                load.style.display = 'block';

            await axios.get('auth/users/me/').then(response => {
                const userid = response.data.id;
                const userphoto = response.data.image;
                let load = document.querySelector('.loading'); load.style.display = 'none';
                // ложу в localstorage токен и айдишник
                localStorage.setItem("userid", userid);
                localStorage.setItem("token", this.token);
                localStorage.setItem("userphoto", userphoto);

                // сохраняю всё в store
                this.$store.commit('setToken', this.token);
                this.$store.commit('setUserid', userid);
                this.$store.commit('setUserphoto', userphoto);

                // перенаправляю его на главную страницу
                this.$router.push('/');
            })
            .catch(error => {
                this.errors_id = [];
                let load = document.querySelector('.loading'); load.style.display = 'none';
                if (error.response) {
                    for (const property in error.response.data) {
                        this.errors_id.push(`${error.response.data[property]}`)
                    }
                } else {
                    this.errors_id.push('Что-то пошло не так! Повторите попытку позже)')
                }
            })
        }
    }
}
</script>

<style scoped>
 .login__form__main{
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    min-height: 84.8vh;
 }

 .login__form{
    display: flex;
    align-items: center;
    flex-direction: column;
    background-color: rgb(213, 147, 197);
    height: 450px;
    width: 600px;
    margin-left: 10px;
    margin-right: 10px;
    border-radius: 10px;
    box-shadow: 5px 5px 5px rgb(0, 0, 0, 0.4);
    margin-top: 10px;
    margin-bottom: 10px;
 }

 .auth{
    color: white;
    font-size: 36px;
    padding-bottom: 20px;
    padding-top: 20px;
 }

 .email{
    font-size: 20px;
    width: 450px;
    border-radius: 5px;
    box-shadow: 3px 3px 3px rgb(0, 0, 0, 0.4);

 }

 .p__placeholder{
    color: white;
    padding-bottom: 5px;
 }

 .div__input{
    padding-bottom: 40px;
 }

 .login__btn{
    width: 80px;
    height: 35px;
    background: linear-gradient(rgb(255, 107, 132), #3150ff);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    border: 1px solid black;
    box-shadow: 3px 3px 3px rgb(0, 0, 0, 0.3);
    font-size: 18px;
}

.login__btn:hover{
    background: linear-gradient(rgb(255, 150, 167), #7086ff);
    cursor: pointer;
}

.login__errors{
    padding-top: 20px;
    color: red;
}

.forgetpas{
    margin-bottom: 40px;
}

.forgetpas__router{
    color: white;
}

.forgetpas__router:hover{
    color: rgb(208, 208, 208);
}

.login__form2{
    width: 455px;
}

@media (max-width: 1000px){
    .login__form{
        width: 90%;
    }

    .login__form__main{
        min-height: 80vh;
    }

    .login__form2{
       width: 90%;
    }

    .email{
        width: 95%;
    }
}

</style>