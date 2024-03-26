<template>
    <template v-if="$store.state.isAuthenticated">
        <template v-if="menu == '' || menu == []">
            <div class="main__without__menu">
                <p class="main__p">На эту неделю у тебя ещё нет меню😞</p>
                <div class="diet">
                    <p class="diet__p">Диета:</p>

                    <div class="form_radio_btn">
                        <input id="radio-1" type="radio" name="diet" value="usualdiet" v-model="diet" checked>
                        <label for="radio-1">Обычная</label>
                    </div>

                    <div class="form_radio_btn">
                        <input id="radio-2" type="radio" name="diet" value="weightloss" v-model="diet">
                        <label for="radio-2">Для похудения</label>
                    </div>

                    <div class="form_radio_btn">
                        <input id="radio-3" type="radio" name="diet" value="weightgain" v-model="diet">
                        <label for="radio-3">Для набора веса</label>
                    </div>
                </div>

                <div class="cookware">
                    <p class="cookware__p">Посуда в наличии:</p>
                    <div class="cookware__list">
                        <template v-for="(cookware, key) in cookware_response" :key="key">
                            <input type="checkbox" :id="`cookware${cookware.id}`" @click="chooseCookware(cookware.id, `#cookware${cookware.id}`)">
                            <label :for="`cookware${cookware.id}`" class="cookware__label">{{ cookware.title }}</label>
                        </template>
                    </div>
                </div>
                <div class="div__btn">
                    <button @click="createMenu()" class="create__btn">Создать меню</button>
                </div>

                 <!-- Ошибки, если не удалось получить список посуды с бэка -->
                <div class="errors__cookware">
                    <template v-for="(error, key) in errors_cookware" :key="key">
                        <p>{{ error }}</p>
                    </template>
                </div>

                <!-- Ошибки, если не удалось создать меню -->
                <div class="errors__menu__create">
                    <template v-for="(error, key) in errors_menu_create" :key="key">
                        <p>{{ error }}</p>
                    </template>
                </div>
                
                <div class="empty">

                </div>
            </div>
        </template>
        <template v-else>
            <div class="main__with__menu">
                <template v-for="(m, k) in menu" :key="k">
                    <p class="main__p">Твоё меню с {{ m.datestart }} по {{ m.dateend }}</p>
                    <p class="calories__info">{{ m.info }}</p>

                    <div class="day__main">
                        <div class="day">
                            <p class="day__week">Понедельник</p>
                            <div class="dish__day__main">
                                <div class="dish__label__main">
                                    <div class="dish__day">
                                        <div class="dish__day__inside">
                                            <router-link :to="{name: 'dish', params: {id: m.br_mon.id}}" class="link">
                                                <div class="photo__info">
                                                    <template v-if="m.br_mon.mainphoto == null || m.br_mon.mainphoto == ''">
                                                    <img src="@/assets/default_dish.png" class="img"/>
                                                    </template>
                                                    <template v-else>
                                                        <img v-bind:src=m.br_mon.mainphoto class="img">
                                                    </template>
                                                    <div class="photo__info__table">
                                                        <p class="dish__info">⚡: {{ m.br_mon.calories }} ккал</p>
                                                        <p class="dish__info">🕓: {{ m.br_mon.time }}</p>
                                                        <template v-if="m.br_mon.creator.first_name != '' && m.br_mon.creator.last_name != ''">
                                                            <p class="dish__info">👨‍🍳: {{  m.br_mon.creator.last_name }} {{ m.br_mon.creator.first_name }}</p>
                                                        </template>
                                                        <template v-else>
                                                            <p class="dish__info">👨‍🍳: {{ m.br_mon.creator.email }}</p>
                                                        </template>
                                                    </div>
                                                </div>
                                                <p class="dish__title">{{ m.br_mon.title }}</p>
                                                <p class="dish__description">{{ m.br_mon.description }}</p>
                                            </router-link>                                                
                                            <div class="dish__buttons__main">
                                                <button class="replace">Заменить</button>
                                                <div class="dish__buttons">
                                                    <template v-if="m.br_mon.like == true">
                                                        <img src="@/assets/like.png" class="like" @click="dishLike('br_mon', m.br_mon.id)"/>
                                                    </template>
                                                    <template v-else>
                                                        <img src="@/assets/not_like.png" class="like" @click="dishLike('br_mon', m.br_mon.id)"/>
                                                    </template>
                                                    <p>Дизлайк</p>
                                                </div>
                                            </div>
                                            
                                        </div>
                                    </div>
                                    <p class="dish__label">Завтрак</p>
                                </div>

                                <div class="dish__label__main">
                                    <div class="dish__day">

                                    </div>
                                    <p class="dish__label">Обед</p>
                                </div>

                                <div class="dish__label__main">
                                    <div class="dish__day">
                                        
                                    </div>
                                    <p class="dish__label">Ужин</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                </template>
            </div>


            <!-- Ошибки, если не удалось получить меню -->
            <div class="errors__menu">
                <template v-for="(error, key) in errors_menu" :key="key">
                    <p>{{ error }}</p>
                </template>
            </div>
        </template>
    </template>
    <template v-else>
        <p>Ты не авторизован!</p>
    </template>

    
</template>

<script>
import axios from 'axios'

export default{
  data() {
      return {
          diet: "usualdiet", // выбранная диета
          menu: "", // сеню на эту неделю
          cookware_response: [], // список посуды с сервака
          errors_cookware: [], // ошибки с получением посуды
          menu_cookware: [], // посуда для меню
          errors_menu_create: [], // ошибки при создании меню
          errors_menu: [], // ошибки при получении меню
          errors_like: [],
      }
  },

  // это название страницы в закладках браузера
  async mounted() {
    document.title = 'Artemida Food';

    // включаю анимацию загрузки
    let load = document.querySelector('.loading'); 
    load.style.display = 'block';

    // получаю список всей посуды
    await axios.get('dish/cookware/').then(response => {
            let load = document.querySelector('.loading'); load.style.display = 'none';
            this.cookware_response = response.data;
        })
        .catch(error => {
            this.errors_cookware = [];
            let load = document.querySelector('.loading'); load.style.display = 'none';
            if (error.response) {
                for (const property in error.response.data) {
                    this.errors_cookware.push(`${error.response.data[property]}`)
                }
            } else {
                this.errors_cookware.push('Что-то пошло не так! Повторите попытку позже)')
            }
        })

    // Получаю меню на эту неделю
    this.getMenu();
  },

  methods: {
        async getMenu(){
            // включаю анимацию загрузки
            let load = document.querySelector('.loading'); 
            load.style.display = 'block';

            await axios.get('get_menu/').then(response => {
            let load = document.querySelector('.loading'); load.style.display = 'none';
            this.menu = response.data;
            this.checkMenu();
            })
            .catch(error => {
                this.errors_menu = [];
                let load = document.querySelector('.loading'); load.style.display = 'none';
                if (error.response) {
                    for (const property in error.response.data) {
                        this.errors_menu.push(`${error.response.data[property]}`)
                    }
                } else {
                    this.errors_menu.push('Что-то пошло не так! Повторите попытку позже)')
                }
            })
        },

        async checkMenu(){
            // проверяю лайки/дизлайки
            if(this.menu.length > 0){
                var days = ['br_mon', 'lu_mon', 'dn_mon', 'br_tue', 'lu_tue', 'dn_tue', 'br_wed', 'lu_wed', 'dn_wed', 'br_thu', 'lu_thu', 'dn_thu', 'br_fri', 'lu_fri', 'dn_fri', 'br_sat', 'lu_sat', 'dn_sat', 'br_sun', 'lu_sun', 'dn_sun']
                for(let day of days){
                    if(this.menu[0][day]['likes'].indexOf(Number(this.$store.state.userid)) > -1){
                        this.menu[0][day]['like'] = true;
                    }
                    else{
                        this.menu[0][day]['like'] = false;
                    }

                    if(this.menu[0][day]['dislikes'].indexOf(Number(this.$store.state.userid)) > -1){
                    this.menu[0][day]['dislike'] = true;
                    }
                    else{
                        this.menu[0][day]['dislike'] = false;
                    }
                }

                // костыльно меняю формат даты
                let datestart_str = this.menu[0]['datestart'].split('-')
                this.menu[0]['datestart'] = `${datestart_str[2]}.${datestart_str[1]}`;

                let dateend_str = this.menu[0]['dateend'].split('-')
                this.menu[0]['dateend'] = `${dateend_str[2]}.${dateend_str[1]}`;
            }
        },

        // добавление посуды
        async chooseCookware(id, input_id){
            var input = document.querySelector(input_id);
            if(input.checked){
                this.menu_cookware.push(id);
            }
            else{
                const index = this.menu_cookware.indexOf(id);
                if (id > -1)  
                    this.menu_cookware.splice(index, 1); 
            }
        },

        async createMenu(){
            // включаю анимацию загрузки
            let load = document.querySelector('.loading'); 
            load.style.display = 'block';

            var formData = new FormData();
            formData.append("diet", this.diet);
            // formData.append("cookware", this.menu_cookware);
            for(let i=0; i < this.menu_cookware.length; i++)
                formData.append("cookware", this.menu_cookware[i]);

            // создаю меню
            await axios.post('create_menu/', formData).then(response => {
                        let load = document.querySelector('.loading'); load.style.display = 'none';
                        this.menu = response.data;
                        this.checkMenu();
                    })
                    .catch(error => {
                        this.errors_menu_create = [];
                        let load = document.querySelector('.loading'); load.style.display = 'none';
                        if (error.response) {
                            for (const property in error.response.data) {
                                this.errors_menu_create.push(`${error.response.data[property]}`)
                            }
                        } else {
                            this.errors_menu_create.push('Что-то пошло не так! Повторите попытку позже)')
                        }
                    })
        },

        // поставить (убрать) лайк
        async dishLike(day, id){
            // если ставим лайк
            if(this.menu[0][day]['like'] == false){
                // включаю анимацию загрузки
                let load = document.querySelector('.loading'); 
                load.style.display = 'block';

                await axios.post(`dish/like/${id}/`).then(response => {
                    let load = document.querySelector('.loading'); load.style.display = 'none';
                    console.log(response.data);
                    this.getMenu();
                    this.checkMenu();
                    })
                    .catch(error => {
                        this.errors_like = [];
                        let load = document.querySelector('.loading'); load.style.display = 'none';
                        if (error.response) {
                            for (const property in error.response.data) {
                                this.errors_like.push(`${error.response.data[property]}`)
                            }
                        } else {
                            this.errors_like.push('Что-то пошло не так! Повторите попытку позже)')
                        }
                    })
               
            }
            // убираем лайк
            else{
                // включаю анимацию загрузки
                let load = document.querySelector('.loading'); 
                load.style.display = 'block';

                await axios.delete(`dish/clear_like/${id}/`).then(response => {
                    let load = document.querySelector('.loading'); load.style.display = 'none';
                    console.log(response.data);
                    this.getMenu();
                    this.checkMenu();
                    })
                    .catch(error => {
                        this.errors_like = [];
                        let load = document.querySelector('.loading'); load.style.display = 'none';
                        if (error.response) {
                            for (const property in error.response.data) {
                                this.errors_like.push(`${error.response.data[property]}`)
                            }
                        } else {
                            this.errors_like.push('Что-то пошло не так! Повторите попытку позже)')
                        }
                    })
            }
        },
    },
}
</script>

<style scoped>
    .main__p{
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 40px;
        margin-top: 10px;
        font-weight: 600;
        text-align: center;
    }

    .diet, .cookware{
        display: flex; 
        flex-direction: row;
        align-items: center;
        margin-left: 30px;
        margin-top: 20px;
    }

    .diet__p, .cookware__p{
        font-size: 30px;
        font-weight: 500;
        margin-right: 10px;
    }

    /* Красивый radiobutton */
    .form_radio_btn {
        display: inline-block;
        margin-right: 10px;
        
    }
    .form_radio_btn input[type=radio] {
        display: none;
    }
    .form_radio_btn label {
        display: inline-block;
        cursor: pointer;
        padding: 0px 15px;
        line-height: 34px;
        border: 1px solid #999;
        border-radius: 6px;
        user-select: none;
    }
    
    /* Checked */
    .form_radio_btn input[type=radio]:checked + label {
        background: linear-gradient(rgb(255, 149, 167), #6078ff);
        color: white;
    }
    
    /* Hover */
    .form_radio_btn label:hover {
        background-color: #dfdfdf;
    }
    
    /* Disabled */
    .form_radio_btn input[type=radio]:disabled + label {
        background: #efefef;
        color: #666;
    }

     /* Красивый чекбокс */

    input[type="checkbox"]:checked, 
    input[type="checkbox"]:not(:checked)
    {
        position: absolute;
        left: -9999px;
    }

    input[type="checkbox"]:checked + label, 
    input[type="checkbox"]:not(:checked) + label
    {
        display: inline-block;
        position: relative;
        padding-left: 28px;
        line-height: 20px;
        cursor: pointer;
    }

    input[type="checkbox"]:checked + label:before, 
    input[type="checkbox"]:not(:checked) + label:before
    {
        content: "";
        position: absolute;
        left: 0px;
        top: 0px;
        width: 18px;
        height: 18px;
        border: 1px solid #dddddd;
        background-color: #ffffff;
    }

    input[type="checkbox"]:checked + label:before, 
    input[type="checkbox"]:not(:checked) + label:before {
        border-radius: 2px;
    }

    input[type="checkbox"]:checked + label:after, 
    input[type="checkbox"]:not(:checked) + label:after
    {
        content: "";
        position: absolute;
        -webkit-transition: all 0.2s ease;
        -moz-transition: all 0.2s ease;
        -o-transition: all 0.2s ease;
        transition: all 0.2s ease;
    }

    input[type="checkbox"]:checked + label:after, 
    input[type="checkbox"]:not(:checked) + label:after {
        left: 3px;
        top: 4px;
        width: 10px;
        height: 5px;
        border-radius: 1px;
        border-left: 4px solid #e145a3;
        border-bottom: 4px solid #e145a3;
        -webkit-transform: rotate(-45deg);
        -moz-transform: rotate(-45deg);
        -o-transform: rotate(-45deg);
        -ms-transform: rotate(-45deg);
        transform: rotate(-45deg);
    }

    input[type="checkbox"]:not(:checked) + label:after
    {
        opacity: 0;
    }

    input[type="checkbox"]:checked + label:after
    {
        opacity: 1;
    }

    .cookware__label{
        margin-right: 10px;
        font-size: 18px;
        margin-top: 5px;
        margin-bottom: 5px;
    }

    .cookware__list{
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
    }

    .div__btn{
        display: flex;
        align-items: center;
        justify-content: center;
        margin-top: 30px;
        margin-bottom: 30px;
    }

    .create__btn{
        width: 160px;
        height: 50px;
        background: linear-gradient(#3150ff, rgb(255, 107, 132));
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        border: 1px solid black;
        box-shadow: 3px 3px 3px rgb(0, 0, 0, 0.3);
        font-size: 22px;
    }

    .create__btn:hover{
        background: linear-gradient(#7086ff, rgb(255, 150, 167));
        cursor: pointer;
    }

    .errors__menu, .errors__menu__create, .errors__cookware{
        color: red;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .empty{
        margin-top: 21%;
    }

    .calories__info{
        font-size: 18px;
        font-weight: 500;
        margin-left: 30px;
        margin-top: 20px;
    }

    .day__main{
        display: flex;
        align-items: center;
        justify-content: center;
        margin-top: 20px;
        margin-bottom: 20px;
    }

    .day{
        width: 90%;
        height: 100%;
        background-color: #F9E8FF;
        border-radius: 20px;
    }

    .day__week{
        margin-top: 20px;
        margin-left: 30px;
        font-size: 28px;
        font-weight: 600;
    }

    .dish__day__main{
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
    }

    .dish__day{
        margin-top: 10px;
        margin-left: 20px;
        width: 400px;
        height: 460px;
        background-color: #CED6FF;
        border-radius: 20px;
        margin-right: 20px;
    }

    .dish__label__main{
        display: flex;
        align-items: center;
        flex-direction: column;
        justify-content: space-between;
        flex-wrap: wrap;
    }

    .dish__label{
        margin-top: 10px;
        margin-bottom: 10px;
        font-size: 22px;
        font-weight: 500;
    }

    .img{
        width: 175px;
        height: 150px;
        object-fit: cover;
        border-radius: 10px;
    }

    .dish__day__inside{
        margin: 10px;
    }

    .photo__info{
        display: flex;
        align-items: center;
        justify-content: flex-start;
        flex-direction: row;
    }

    .photo__info__table{
        display: flex;
        flex-direction: column;
    }

    .dish__info{
        margin-bottom: 10px;
        font-size: 17px;
        margin-left: 10px;
        margin-top: 10px;
        text-overflow: ellipsis;
        white-space: nowrap;
        overflow: hidden;
        width: 195px;
    }

    .dish__title{
        text-align: center;
        margin-top: 10px;
        width: 100%;
        font-size: 18px;
        font-weight: 550;
        text-overflow: ellipsis;
        white-space: nowrap;
        overflow: hidden;
    }

    .dish__description{
        overflow: hidden;
        margin-top: 5px;
        height: 200px;
        white-space: pre-wrap;
    }

    .dish__buttons__main{
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-top: 20px;
    }

    .dish__buttons{
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-direction: row;
        width: 100px;
    }

    .replace{
        color: black;
        background-color: white;
        border-radius: 10px;
        width: 100px;
        height: 25px;
        font-size: 16px;
        border: 0px solid rgb(0, 0, 0);
        box-shadow: 3px 3px 3px rgb(0, 0, 0, 0.4);
    }

    .replace:hover{
        cursor: pointer;
        background-color: rgb(200, 200, 200);
    }

    .link{
        color: black;
        text-decoration: none;
    }

    .link:hover{
        color: rgb(127, 127, 127);
    }

    .like{
        width: 25px;
        height: 25px;
    }

    .like:hover{
        cursor: pointer;
    }
</style>