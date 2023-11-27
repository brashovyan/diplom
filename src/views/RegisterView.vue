<template>
    <div class="main">
        <div class="main__elements">
            <input type="email" v-model="email" placeholder="Почта">
            <input type="password" v-model="password1" placeholder="Пароль">
            <input type="password" v-model="password2" placeholder="Повторите пароль">
            <p>Заполните ифнормацию о себе (это нужно для составления меню, мы никому ничего не скажем)</p>
            <p>(Это нужно для составления меню, мы никому ничего не скажем)</p>
            <input type="number" v-model="height" placeholder="Рост, см">
            <input type="number" v-model="weight" placeholder="Вес, кг">
            <input type="date" v-model="date" placeholder="Дата рождения">
            <div>
                <input type="radio" v-model="sex" name="sex" placeholder="Мужской" value="M" id="male" checked>
                <label for="male">Мужской</label>
                <input type="radio" v-model="sex" name="sex" placeholder="Женский" value="F" id="female">
                <label for="female">Женский</label>
            </div>
            <input type="file" accept="image/*,image/jpeg" id="file" @change="photoPreview()">

            <template v-for="(photo, index) in photoPreviews" :key="index">
                <img :src="photo" width="100" height="100"/>
            </template>

            <button @click="register()">Зарегистрироваться</button>
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
        margin: 0px;
    }

    .main__elements{
        display: flex;
        flex-direction: column;
    }

    .errors{
        display: flex;
        flex-direction: column;
    }

</style>