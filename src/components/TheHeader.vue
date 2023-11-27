<template>
    <header>
        <div class="header__left">

            <h1 class="title__h1"><router-link to="/" class="title">Artemida Food</router-link></h1>

            <router-link to="/recipes" class="menu">
                <div class="menu__button">
                    <p>Рецепты</p>
                </div>
            </router-link>
        </div>
        <div class="header__right">
            <form action="/search" method="get">
                <input type="search" name="search_str" class="search" placeholder="Поиск...">
            </form>
            
            <!-- Если челик авторизован -->
            <template v-if="$store.state.isAuthenticated">
                <template v-if="$store.state.userphoto && $store.state.userphoto != 'null'">
                    <!-- Фотка есть -->
                    <router-link to="/myprofile">
                        <img v-bind:src="$store.state.userphoto" class="img">
                    </router-link>
                </template>
                <template v-else>
                    <!-- Фотки нет -->
                    <router-link to="/myprofile">
                        <img src="@/assets/default_user_img.jpg" class="img"/>
                    </router-link>
                </template>
                <p @click="logout()" class="logout">Выйти</p>
            </template>

            <!-- Если челик неавторизован -->
            <template v-else>
                <p><router-link to="/login" class="login">Войти</router-link></p>
                <p><router-link to="/register" class="register">Регистрация</router-link></p>
            </template>
        </div>
        

        <!-- <template v-for="(error, key) in errors" :key="key">
            {{ error }}
        </template> -->
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

  mounted() {
        document.title = 'Artemida Food';
    },

  methods: {
    async logout() {
        // отправляю на сервак пост запрос, что хочу разлогиниться

        // включаем анимацию загрузки
        let load = document.querySelector('.loading'); 
        load.style.display = 'block';

        await axios
                .post("auth/token/logout/").then(ressponse => {let load = document.querySelector('.loading'); load.style.display = 'none'; console.log(ressponse); })

                // здесь обрабатываем ошибки
                .catch(error => {
                    this.errors = [];
                    let load = document.querySelector('.loading'); load.style.display = 'none';
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
        localStorage.removeItem("userphoto");

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
        background-color: #78258B;
        display: flex;
        align-items: center;
        padding-left: 20px;
        padding-right: 20px;
        justify-content: space-between;
        height: 60px;
        width: 100%;
        box-sizing: border-box;
    }

    .title{
        color: white;
        text-decoration: none;
        font-size: 44px;
    }

    .title:hover{
        color: rgb(255, 219, 219);
    }

    .menu{
        padding-left: 20px;
        padding-right: 20px;
        text-decoration: none;
    }

    .menu__button{
        width: 80px;
        height: 35px;
        background: linear-gradient(#3150ff, rgb(255, 107, 132));
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        border: 1px solid black;
        box-shadow: 3px 3px 3px rgb(0, 0, 0, 0.3);
    }

    .menu__button:hover{
        background: linear-gradient(#7086ff, rgb(255, 150, 167));
    }

    .header__left{
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .header__right{
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .img{
        width: 50px;
        height: 50px;
        object-fit: cover;
        border-radius: 50px;
        padding-top: 3px;
    }

    .logout{
        color: white;
        font-size: 22px;
        margin-left: 15px;
    }

    .logout:hover{
        cursor: pointer;
        color: rgb(255, 219, 219);
    }

    .search{
        margin-right: 15px;
        font-size: 20px;
        border-radius: 5px;
        box-shadow: 3px 3px 3px rgb(0, 0, 0, 0.3);
    }

    .login{
        color: white;
        font-size: 22px;
        text-decoration: none;
        margin-right: 15px;
    }

    .register{
        color: white;
        font-size: 22px;
        text-decoration: none;
    }

    .login:hover, .register:hover{
        color: rgb(255, 219, 219);
    }

    /* Мобильная верстка */
    @media (max-width: 1000px){
        header{
            display: flex;
            flex-direction: column;
            align-items: center;
            padding-left: 10px;
            padding-right: 10px;
            justify-content: center;
            height: 60px;
            width: 100%;
            box-sizing: border-box;
        }

        .header__left{
            display: flex;
            align-items: center;
            justify-content: center;
            height: 28px;
            margin-left: 15px;
        }

        .header__right{
            display: flex;
            align-items: center;
            justify-content: center;
            height: 25px;

        }

        .title__h1{
            padding-bottom: 8px;
        }

        .title{
            font-size: 20px;
        }

        .search{
            width: 110px;
            font-size: 12px;
            margin-right: 10px;
        }

        .login{
            font-size: 14px;
            margin-right: 10px;
        }

        .register{
            font-size: 14px;
        }

        .menu__button{
            width: 50px;
            height: 25px;
        }

        .menu{
            padding-left: 10px;
            padding-right: 10px;
            text-decoration: none;
            font-size: 10px;
        }
        
        .img{
            width: 25px;
            height: 25px;
        }

        .logout{
            font-size: 14px;
            margin-left: 10px;
        }
    }
</style>