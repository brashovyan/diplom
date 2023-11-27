<template>
    <div class="main">
        <div class="main__elements">
            <div class="main__elements2">
                <p class="reg">Регистрация</p>
                <div class="div__input">
                    <p class="p__placeholder">Эл. почта:</p>
                    <input v-model="email" type="email" class="email" placeholder="Эл. почта" required>
                </div>
                <div class="div__input">
                    <p class="p__placeholder">Пароль:</p>
                    <input v-model="password1" type="password" class="email" placeholder="Пароль" required>
                </div>
                <div class="div__input">
                    <p class="p__placeholder">Повторите пароль:</p>
                    <input v-model="password2" type="password" class="email" placeholder="Повторите пароль" required>
                </div>
                <p class="info">Заполните ниже ифнормацию о себе (это нужно для составления меню, мы никому ничего не скажем😉)</p>
                <div class="div__input">
                    <p class="p__placeholder">Рост, см:</p>
                    <input v-model="height" type="number" class="email" placeholder="Рост, см" required>
                </div>
                <div class="div__input">
                    <p class="p__placeholder">Вес, кг:</p>
                    <input v-model="weight" type="number" class="email" placeholder="Вес, кг" required>
                </div>
                <div class="div__input">
                    <p class="p__placeholder">Дата рождения:</p>
                    <input v-model="date" type="date" class="email" placeholder="Дата рождения" required>
                </div>
                <p class="p__placeholder">Пол:</p>
                <div class="div__radio">
                    <input type="radio" v-model="sex" name="sex" placeholder="Мужской" value="M" id="male" checked>
                    <label for="male">Мужской</label>
                    <input type="radio" v-model="sex" name="sex" placeholder="Женский" value="F" id="female">
                    <label for="female">Женский</label>
                </div>
                <p class="p__placeholder">Выберите фото профиля (необязательно):</p>
                <div class="div__photo">
                    <label for="file" class="photo__label">Выбрать...</label>
                    <input type="file" accept="image/*,image/jpeg" id="file" @change="photoPreview()" class="file">
                    <template v-if="photoPreviews.length > 0">
                        <template v-for="(photo, index) in photoPreviews" :key="index">
                            <img :src="photo" class="img"/>
                        </template>
                    </template>
                    <template v-else>
                        <img src="@/assets/default_user_img.jpg" class="img"/>
                    </template>
                    
                </div>
                <button @click="register()" class="register__btn">Зарегистрироваться</button>
                <div class="errors">
                    <template v-if="nonfields.length">
                    <p>Пожалуйста, заполните все поля!</p>
                    <template v-for="(nonfield, key) in nonfields" :key="key">
                        <p>{{ nonfield }}</p>
                    </template>
                    </template>
                    
                    <template v-for="(error, key) in errors_register" :key="key">
                        <p>{{ error }}</p>
                    </template>

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
    name: 'SignUp',
    data() {
        return {
            email: '',
            password1: '',
            password2: '',
            height: "",
            weight: "",
            date: "",
            sex: "M",
            photoPreviews: [],
            nonfields: [],
            token: "",
            errors_login: [],
            erros_id: [],
            errors_register: [],
        }
    },

    // это название страницы в закладках браузера
    mounted() {
        document.title = 'Регистрация'
    },

    methods: {
        async register() {
            // сперва я проверяю на фронте, что юзер всё заполнил
            this.nonfields = []

            if (this.email == '') {
                this.nonfields.push('Введите email')
            }
            if (this.password1 == '') {
                this.nonfields.push('Введите пароль')
            }
            if (this.password2 == '') {
                this.nonfields.push('Повторите пароль')
            }
            if (this.password1 != this.password2) {
                this.nonfields.push('Пароли не совпадают')
            }
            if (this.height == '') {
                this.nonfields.push('Введите рост')
            }
            if (this.weight == '') {
                this.nonfields.push('Введите вес')
            }
            if (this.date == '') {
                this.nonfields.push('Введите дату рождения')
            }

            // если юзер всё заполнил, то пытаемся регаться
            if (!this.nonfields.length) {
                var formData = new FormData();
                formData.append("email", this.email);
                formData.append("password", this.password1);
                formData.append("height", this.height);
                formData.append("weight", this.weight);
                formData.append("sex", this.sex);
                formData.append("date_of_birth", this.date);
                
                var imagefile = document.querySelector('#file').files[0];
                if(imagefile){
                    formData.append("image", imagefile);
                }

                // включаем анимацию загрузки
                let load = document.querySelector('.loading'); 
                load.style.display = 'block';

                await axios
                    .post("auth/users/", formData)
                    .then(response => {this.login(); console.log(response); let load = document.querySelector('.loading'); load.style.display = 'none';}) // если мы успешно зарегались, то идём в функцию логина
                    // ошибки при регистрации
                    .catch(error => {
                        this.errors_register = [];
                        let load = document.querySelector('.loading'); load.style.display = 'none';
                        if (error.response) {  
                            for (const property in error.response.data) {
                                this.errors_register.push(`${error.response.data[property]}`)
                            }
                        } else {
                            this.errors_register.push('Что-то пошло не так! Повторите попытку позже)')
                        }
                    })
            }
        },

        // превьюшки фоток
        photoPreview(){
            this.photoPreviews = [];
            var imagefiles = document.querySelector('#file').files;
            for(var i=0; i < imagefiles.length; i++){
                this.photoPreviews.push(URL.createObjectURL(imagefiles[i]))
            }
        },

        // логин
        async login(){
            // если юзер успешно зареган, то мы оказываемся тут и логиним его                     
            axios.defaults.headers.common["Authorization"] = ""
            localStorage.removeItem("token");
            localStorage.removeItem("userid");
            localStorage.removeItem("userphoto");
            this.$store.commit('removeToken');
            const formData2 = {
                email: this.email,
                password: this.password1
            }

            // включаем анимацию загрузки
            let load = document.querySelector('.loading'); 
            load.style.display = 'block';

            await axios
                .post("auth/token/login/", formData2)
                .then(response2 => {
                    this.token = response2.data.auth_token;
                    axios.defaults.headers.common["Authorization"] = "Token " + this.token;
                    let load = document.querySelector('.loading'); load.style.display = 'none';
                    this.get_id();          
                })
                // ошибки при логине
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
        },

        // для логина
        async get_id(){
            // включаем анимацию загрузки
            let load = document.querySelector('.loading'); 
            load.style.display = 'block';

            await axios.get('auth/users/me/').then(response => {
                const userid = response.data.id;
                const userphoto = response.data.image;
                localStorage.setItem("userid", userid);
                localStorage.setItem("token", this.token);
                localStorage.setItem("userphoto", userphoto);
                this.$store.commit('setToken', this.token);
                this.$store.commit('setUserid', userid);
                this.$store.commit('setUserphoto', userphoto);
                let load = document.querySelector('.loading'); load.style.display = 'none';
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
        },
    }
}
</script>

<style scoped>
    .main{
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        min-height: 84.8vh;
    }

    .main__elements{
        display: flex;
        align-items: center;
        flex-direction: column;
        background-color: rgb(213, 147, 197);
        height: 840px;
        width: 600px;
        margin-left: 10px;
        margin-right: 10px;
        border-radius: 10px;
        box-shadow: 5px 5px 5px rgb(0, 0, 0, 0.4);
        margin-top: 30px;
        margin-bottom: 30px;
    }

    .main__elements2{
        width: 455px;
    }

    .email{
        font-size: 20px;
        width: 450px;
        border-radius: 5px;
        box-shadow: 3px 3px 3px rgb(0, 0, 0, 0.4);
    }

    .div__input{
        padding-bottom: 10px;
    }

    .p__placeholder{
        color: white;
        padding-bottom: 5px;
    }

    .reg{
        color: white;
        font-size: 36px;
        padding-bottom: 20px;
        padding-top: 20px;
    }

    .info{
        text-align: center;
        padding-bottom: 10px;
    }

    #female{
        margin-left: 20px;
    }

    input[type=radio] {
        width: 20px;
        height: 20px;
    }

    .div__radio{
        display: flex;
        align-items: center;
        justify-content: flex-start;
        padding-bottom: 10px;
    }

    .div__photo{
        display: flex;
        align-items: center;
        justify-content: flex-start;
        margin-bottom: 20px;
    }

    #file{
        opacity: 0;
        position: absolute;
        z-index: -1;
    }

    .photo__label{
        background-color: rgb(255, 162, 177);
        border: 1px solid black;
        border-radius: 3px;
        width: 90px;
        height: 20px;
        margin-right: 30px;
    }

    .photo__label:hover{
        cursor: pointer;
        background-color: rgb(255, 194, 204);
    }

    .img{
        width: 50px;
        height: 50px;
        object-fit: cover;
        border-radius: 50px;
        padding-top: 3px;
    }

    .register__btn{
        width: 200px;
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

    .register__btn:hover{
        background: linear-gradient(rgb(255, 150, 167), #7086ff);
        cursor: pointer;
    }

    .errors{
        display: flex;
        flex-direction: column;
        color: red;
        padding-top: 10px;
        padding-bottom: 10px;
    }

    @media (max-width: 1000px){
        .main__elements{
            width: 90%;
            height: 900px;
        }

        .main__elements2{
            width: 90%;
        }

        .email{
            width: 95%;
        }
    }

</style>