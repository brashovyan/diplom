<template>
    <div style="display: flex; flex-direction: row;">
        <p>Обычная:</p>
        <input type="radio" value="usual" name="diet" v-model="diet" checked>
        <p>Для похудения:</p>
        <input type="radio" value="weightloss" name="diet" v-model="diet">
        <p>Для набора веса:</p>
        <input type="radio" value="weightgain" name="diet" v-model="diet">
    </div>

    <template v-for="(cookware, key) in cookware_response" :key="key">
        <input type="checkbox" :id="`cookware${cookware.id}`" @click="chooseCookware(cookware.id, `#cookware${cookware.id}`)">
        <label :for="`cookware${cookware.id}`">{{ cookware.title }}</label>
    </template>

    <button @click="createMenu()">Создать меню</button>

  <!-- Ошибки, если не удалось получить список посуды с бэка -->
    <div class="errors__cookware">
        <template v-for="(error, key) in errors_cookware" :key="key">
            <p>{{ error }}</p>
        </template>
    </div>

    <!-- Ошибки, если не удалось создать меню -->
    <div class="errors__menu">
        <template v-for="(error, key) in errors_menu" :key="key">
            <p>{{ error }}</p>
        </template>
    </div>
</template>

<script>
import axios from 'axios'

export default{
  data() {
      return {
          diet: "usual", // выбранная диета
          cookware_response: [], // список посуды с сервака
          errors_cookware: [], // ошибки с получением посуды
          menu_cookware: [], // посуда для меню
          errors_menu: [], // ошибки при создании меню
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
            formData.append("cookware", this.menu_cookware);

            // создаю меню
            await axios.post('create_menu/', formData).then(response => {
                        let load = document.querySelector('.loading'); load.style.display = 'none';
                        console.log(response.data);
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
    },
}
</script>

<style scoped>
 

</style>