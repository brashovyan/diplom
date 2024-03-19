<template>
    <template v-if="$store.state.isAuthenticated">
        <template v-if="menu == '' || menu == []">
            <div class="main__without__menu">
                <p class="main__p">На эту неделю у тебя ещё нет меню😞</p>
                <div class="diet">
                    <p class="diet__p">Диета:</p>

                    <div class="form_radio_btn">
                        <input id="radio-1" type="radio" name="diet" value="usual" v-model="diet" checked>
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
            {{ menu }}

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
          diet: "usual", // выбранная диета
          menu: "", // сеню на эту неделю
          cookware_response: [], // список посуды с сервака
          errors_cookware: [], // ошибки с получением посуды
          menu_cookware: [], // посуда для меню
          errors_menu_create: [], // ошибки при создании меню
          errors_menu: [], // ошибки при получении меню
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

    // включаю анимацию загрузки
    load = document.querySelector('.loading'); 
    load.style.display = 'block';
    
    // Получаю меню на эту неделю
    await axios.get('get_menu/').then(response => {
            let load = document.querySelector('.loading'); load.style.display = 'none';
            this.menu = response.data;
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

  methods: {
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
    

</style>