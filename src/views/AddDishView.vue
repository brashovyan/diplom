<template>
    <div class="main">
        <div class="column">
            <p>Введите название ингредиента:</p>
            <input type="text" placeholder="Название игредиента" v-model="ingredient_title" style="width: 300px;">
            <template v-for="(ingredient_list, key_list) in ingredient_response" :key="key_list">
                <template v-for="(ingredient_json, key_json) in ingredient_list" :key="key_json">
                    <template v-for="(ingredient, key) in ingredient_json" :key="key">
                        <p class="ingredient__result" @click="addIngredientCandidate(ingredient, key)">{{ ingredient }}</p>
                    </template>
                </template>
            </template>
        </div>
            <input type="text" placeholder="Укажите количество" v-model="ingredient_count">
            <template v-if="ingredient_find == true">
                <button id="add__ing__btn" @click="addIngredientDish()">Добавить</button>
            </template>
            <template v-else-if="ingredient_title.length > 1 && ingredient_response_count == 0">
                <button id="add__ing__btn" @click="addIngredientDish()">Добавить</button>
            </template>
            <template v-else>
                <button id="add__ing__btn" disabled>Добавить</button>
            </template>
    </div>

    <template v-for="(ingredient, key) in ingrients_dish" :key="key">
        <p @click="deleteIngredintFromDish(ingredient)">{{ ingredient["title"] }} - {{ ingredient["count"] }}</p>
    </template>

  </template>


<script>
import axios from 'axios'

export default{
    data() {
        return {
            ingredient_title: "", // название ингредиента, которое вводит пользователь
            ingredient_count: "", // кол-во ингредиента
            ingredient_response: {"result": []}, // результат поиска игредиента
            ingredient_find: false,
            ingredient_response_count: 0, // кол-во результатов поиска (в html у меня не получилосб)
            ingredient_candidate: "", // блюдо, которое юзер выбрал из выпадающего списка
            ingrients_dish: [], // добавленные ингредиенты в блюдо
        }
    },

    watch: {
        async ingredient_title() {
            // если я еще не выбрал ингредиент из списка
            if(this.ingredient_find == false){
                // если я ввёл хотя-бы две буквы
                if(this.ingredient_title.length > 1){
                    var formData = new FormData();
                    formData.append("title", this.ingredient_title);
                    this.ingredient_response = "";

                    await axios
                        .post("dish/search_ingredient/", formData)
                        .then(response => {
                            this.ingredient_response = response.data;
                            this.ingredient_response_count = this.ingredient_response["result"].length;
                        }) 
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
                // если я ввёл меньше двух букв
                else{
                    this.ingredient_response = {"result": []};
                    this.ingredient_response_count = 0;
                }
            }
            // если мы снова начали что-то вводить, при этом уже выбрав ингредиент, всё обнуляем
            else{
                this.ingredient_response = {"result": []};
                this.ingredient_response_count = 0;
                this.ingredient_find = false;
            }
        }
    },

    mounted() {
        
    },

    methods: {
        // выбор ингредиента из списка
        async addIngredientCandidate(ingredient, key){
            this.ingredient_title = ingredient; 
            this.ingredient_find = true;
            this.ingredient_candidate = {"id": key, "title": ingredient};
        },

        // добавление ингредиента в блюдо
        async addIngredientDish(){
            // если мы выбрали ингредиент из списка
            if(this.ingredient_candidate != ""){
                let ing = {"id": this.ingredient_candidate["id"], "title": this.ingredient_candidate["title"], "count": this.ingredient_count}
                this.ingrients_dish.push(ing);
            }
            // если в списке не было нашего ингредиента
            else{
                let ing2 = {"id": "no", "title": this.ingredient_title, "count": this.ingredient_count}
                this.ingrients_dish.push(ing2);
            }

            this.ingredient_title = "";
            this.ingredient_count = "";
            this.ingredient_find = false;
            this.ingredient_candidate = "";
            this.ingredient_response = {"result": []};
            this.ingredient_response_count = 0;
        },

        // удаление ингредиента из блюда
        async deleteIngredintFromDish(ingredient){
            const index = this.ingrients_dish.indexOf(ingredient);
            if (index > -1)  
                this.ingrients_dish.splice(index, 1); 
        },
        
    },
}
</script>

<style scoped>
    .main{
        display: flex;
        align-items: center;
        justify-content: flex-start;
    }
    .column{
        display: flex;
        flex-direction: column;
    }
    
    .ingredient__result:hover{
        cursor: pointer;
        background-color: antiquewhite;
    }
</style>