<template>
    <template v-if="$store.state.isAuthenticated">
        <div class="main">
            <div>
                <p class="main__title">Создание рецепта 🍔</p>
            </div>

            <div class="line"></div>

            <!-- Название, описание -->
            <div class="row">
                <p class="label__input">Название рецепта:</p>
                <input type="text" placeholder="Название рецепта" v-model="dish_title" class="text__input">
            </div>

            <div class="row__textarea">
                <p class="label__input">Краткое описание:</p>
                <textarea placeholder="Краткое описание" v-model="dish_description" class="textarea__input"></textarea>
            </div>
            
            <!-- Ингредиенты -->
            <div class="pink">
                <div class="row__pink__ingredients">
                    <div class="ingredients__title">
                        <p class="label__input">Ингредиенты 🧅:</p>
                        <div class="ingredients__title__empty"></div>
                    </div>
                    
                    <div class="ingredients">
                        <div class="ingredients__column">
                            <p class="ingredients__label">Введите название ингредиента:</p>
                            <input type="text" placeholder="Название игредиента" v-model="ingredient_title" class="ingredient__input">
                            <template v-for="(ingredient_list, key_list) in ingredient_response" :key="key_list">
                                <template v-for="(ingredient_json, key_json) in ingredient_list" :key="key_json">
                                    <template v-for="(ingredient, key) in ingredient_json" :key="key">
                                        <p class="ingredient__result" @click="addIngredientCandidate(ingredient, key)">{{ ingredient }}</p>
                                    </template>
                                </template>
                            </template>
                        </div>
                        
                        <div class="ingredient__add">
                            <input type="text" placeholder="Кол-во" v-model="ingredient_count" maxlength="10" class="ingredient__count">
                            <template v-if="ingredient_find == true">
                                <button id="add__ing__btn" @click="addIngredientDish()">Добавить</button>
                            </template>
                            <template v-else-if="ingredient_title.length > 1 && ingredient_response_count == 0">
                                <button id="add__ing__btn" @click="addIngredientDish()">Добавить</button>
                            </template>
                            <template v-else>
                                <button id="add__ing__btn__dis" disabled>Добавить</button>
                            </template>
                        </div>
                    </div>

                    <div class="ingredients__added">
                        <div>
                            <p class="ingredients__added__label">Добавленные ингредиенты:</p>
                        
                                <template v-for="(ingredient, key) in ingredients_dish" :key="key">
                                    <div class="ingredients__list__row">
                                        <p class="ingredients__added__list">{{ ingredient["title"] }} - {{ ingredient["count"] }}</p>
                                        <p @click="deleteIngredintFromDish(ingredient)" class="remove__ingredient">X</p>
                                    </div>
                                </template>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Энергетическая ценность -->
            <div class="row">
                <div class="div__calories">
                    <p class="label__input" style="margin-right: 21.3px;">Калории:</p>
                    <input type="number" placeholder="Калории" v-model="calories" min=0 class="number__input">
                </div>

                <div class="div__calories">
                    <p class="label__input">Белки:</p>
                    <input type="number" placeholder="Белки, гр" v-model="proteins" min=0 class="number__input">
                </div>
            </div>

            <div class="row">
                <div class="div__calories">
                    <p class="label__input">Углеводы:</p>
                    <input type="number" placeholder="Углеводы, гр" v-model="carbohydrates" min=0 class="number__input">
                </div>
                

                <div class="div__calories">
                    <p class="label__input">Жиры:</p>
                    <input type="number" placeholder="Жиры, гр" v-model="fats" min=0 class="number__input">
                </div>
            </div>

            <!-- Типы диет -->
            <div class="pink">
                <div class="column">
                    <div class="row">
                        <p class="label__input">Время готовки 🕓:</p>
                        <input type="text" placeholder="Время (произвольно)" v-model="time" maxlength="30" class="text__input">
                    </div>

                    <p class="label__input">Подходит для:</p>
                    <div class="checkboxes">
                        <input type="checkbox" v-model="breakfast" id="checkbox1">
                        <label for="checkbox1" class="checkbox__label">Завтрака</label>

                        <input type="checkbox" v-model="usualdiet" id="checkbox2">
                        <label for="checkbox2" class="checkbox__label">Обычного рациона</label>
                    </div>
                    <div class="checkboxes">
                        <input type="checkbox" v-model="lunch" id="checkbox3">
                        <label for="checkbox3" class="checkbox__label">Обеда</label>

                        <input type="checkbox" v-model="weightloss" id="checkbox4">
                        <label for="checkbox4" class="checkbox__label" style="margin-right: 75.2px;">Похудения</label>
                    </div>
                    <div class="checkboxes">
                        <input type="checkbox" v-model="dinner" id="checkbox5">
                        <label for="checkbox5" class="checkbox__label">Ужина</label>

                        <input type="checkbox" v-model="weightgain" id="checkbox6">
                        <label for="checkbox6" class="checkbox__label" style="margin-right: 57.2px;">Набора веса</label>
                    </div>
                </div>
            </div>

            <!-- фоточки -->
            <div class="row">
                <p class="label__input">Фотографии 📷:</p>
            </div>

            <!-- главное фото -->
            <div class="row">
                <p class="label__input" style="font-size: 20px;">Выберите главное фото:</p>
              
                    <label for="main__photo" class="photo__input">Выбрать</label>
                    <input type="file" accept="image/*,image/jpeg" id="main__photo" @change="photoPreviewMain()">
            </div>
            <template v-if="photo_preview_main.length > 0">
                <template v-for="(photo, index) in photo_preview_main" :key="index">
                    <img :src="photo" class="img"/>
                    <p @click="deleteMainPhoto()" class="remove__main__photo">X</p>
                </template>
            </template>
            
            <!-- Остальные фото -->
            <div class="row" style="margin-bottom: -20px;">
                <p class="label__input" style="font-size: 20px; ">Выберите ещё до 9 фотографий:</p>
            </div>
            <div class="row">
                <p class="label__input" style="font-size: 14px;">Подсказка: на компьютере нажимайте Ctrl + ЛКМ, чтобы выбрать несколько фото</p>
            </div>
            <div class="row" style="margin-left: 20px; margin-top: -5px;">
                <label for="other__photo" class="photo__input">Выбрать</label>
                <input type="file" accept="image/*,image/jpeg" id="other__photo" multiple @change="checkLength()">
            </div>

            <div class="photos">
                <template v-if="photo_preview_other.length > 0">
                    <template v-for="(photo, index) in photo_preview_other" :key="index">
                        <img :src="photo" class="one__photo"/>
                    </template>
                </template>
            </div>
            <template v-if="photo_preview_other.length > 0">
                <p @click="deleteOtherPhoto()" class="remove__main__photo">X</p>
            </template>

            <!-- Выбор посуды -->
            <div class="pink">
                
                <div class="row">
                    
                    <div class="column">
                        <p class="label__input">Посуда для готовки 🍽️:</p>
                        <template v-for="(cookware, key) in cookware_response" :key="key">
                            <input type="checkbox" :id="`cookware${cookware.id}`" @click="chooseCookware(cookware.id, `#cookware${cookware.id}`)">
                            <label :for="`cookware${cookware.id}`" class="checkbox__label" style="margin-left: 10px; margin-bottom: 10px;">{{ cookware.title }}</label>
                        </template>
                    </div>
                </div>
            </div>

            <div class="row">
                <div class="column">
                    <p class="label__input">Рецепт 📜:</p>
                    <textarea placeholder="Напишите рецепт" v-model="dish_recipe" class="textarea__recipe"></textarea>
                </div>
            </div>
            
            <!-- Создать -->
            <template v-if="dish__title != '' && dish__description != '' && dish_recipe != ''">
                <button class="create__dish" @click="createDish()">Создать</button>
            </template>
            <template v-else>
                <button class="create__dish__disabled">Создать</button>
            </template>

            <!-- Ошибки, если не удалось получить список посуды с бэка -->
            <div class="errors__cookware">
                <template v-for="(error, key) in errors_cookware" :key="key">
                    <p>{{ error }}</p>
                </template>
            </div>

            <!-- Ошибки, если не удалось получить список посуды с бэка -->
            <div class="errors__cookware">
                <template v-for="(error, key) in errors_dish" :key="key">
                    <p>{{ error }}</p>
                </template>
            </div>
        </div>
    </template>
    <template v-else>
        <h1>Ты не зареган</h1>
    </template>
</template>


<script>
import axios from 'axios'

export default{
    data() {
        return {
            dish_title: "", // название блюда
            dish_description: "", // краткое описани
            calories: "", // калории
            proteins: "", // белки
            fats: "", // жиры
            carbohydrates: "", // углеводы
            time: "", // время готовки
            breakfast: false, // для завтрака
            lunch: false, // для обеда
            dinner: false, // для ужина
            usualdiet: false, // для обычной диеты
            weightloss: false, // для похудения
            weightgain: false, // для  набора веса
            photo_preview_main: [], // превьюшка для главной фотки
            photo_preview_other: [], // превьюшки для остальных фоток
            cookware_response: [], // список посуды с сервака
            errors_cookware: [], // ошибки с получением посуды
            errors_dish: [], // ошибки при создании блюда
            dish_cookware: [], // выбранная посуда для блюда
            dish_recipe: "", // сам рецепт
            warning: false, // предупреждение при создании

            ingredient_title: "", // название ингредиента, которое вводит пользователь
            ingredient_count: "", // кол-во ингредиента
            ingredient_response: {"result": []}, // результат поиска игредиента
            ingredient_find: false, // выбран ли ингредиент из списка
            ingredient_response_count: 0, // кол-во результатов поиска
            ingredient_candidate: "", // блюдо, которое юзер выбрал из выпадающего списка
            ingredients_dish: [], // добавленные ингредиенты в блюдо
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

    // это название страницы в закладках браузера
    async mounted() {
        document.title = 'Создание рецепта';

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
                this.ingredients_dish.push(ing);
            }
            // если в списке не было нашего ингредиента
            else{
                let ing2 = {"id": "no", "title": this.ingredient_title, "count": this.ingredient_count}
                this.ingredients_dish.push(ing2);
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
            const index = this.ingredients_dish.indexOf(ingredient);
            if (index > -1)  
                this.ingredients_dish.splice(index, 1); 
        },

        // превьюшка главной фотки
        async photoPreviewMain() {
            this.photo_preview_main = [];
            var imagefiles = document.querySelector('#main__photo').files;
            for(var i=0; i < imagefiles.length; i++){
                this.photo_preview_main.push(URL.createObjectURL(imagefiles[i]))
            }
        },

        // Удаление главной фотографии
        async deleteMainPhoto(){
            var imagefiles = document.querySelector('#main__photo');
            imagefiles.value = "";
            this.photo_preview_main = [];
        },

        // Удаление остальных фотографий
        async deleteOtherPhoto(){
            var imagefiles = document.querySelector('#other__photo');
            imagefiles.value = "";
            this.photo_preview_other = [];
        },

        // при каждом добавлении фоток
        async checkLength() {
            // проверяю кол-во фоток (если больше 9, то я всё очищаю)
            var imagefiles = document.querySelector('#other__photo');
            if (imagefiles.files.length > 9) {
                alert("Можно прикрепить не больше 9 фото");
                imagefiles.value = "";
                this.photo_preview_other = [];
            }
            else{
                this.photoPreviewOther();
            }
        },

        // превьюшки остальных фоток
        async photoPreviewOther(){
            this.photo_preview_other = [];
            var imagefiles = document.querySelector('#other__photo').files;
            for(var i=0; i < imagefiles.length; i++){
                this.photo_preview_other.push(URL.createObjectURL(imagefiles[i]))
            }
        },

        // добавление посуды
        async chooseCookware(id, input_id){
            var input = document.querySelector(input_id);
            if(input.checked){
                this.dish_cookware.push(id);
            }
            else{
                const index = this.dish_cookware.indexOf(id);
                if (id > -1)  
                    this.dish_cookware.splice(index, 1); 
            }
        },

        async createDish(){
            var formData = new FormData();
            formData.append("title", this.dish_title);
            formData.append("description", this.dish_description);
            
            // если белки/жиры и т.д. не указаны, то я их не добавляю (по дефолту на бэке 0)
            if(this.proteins == ""){
                this.warning = true;
                console.log("белки");
            }
            else{
                formData.append("proteins", this.proteins);
                
            }

            if(this.fats == ""){
                this.warning = true;
                console.log("жиры");
            }
            else{
                formData.append("fats", this.fats)
            }

            if(this.carbohydrates == ""){
                this.warning = true;
                console.log("углеводы");
            }
            else{
                formData.append("carbohydrates", this.carbohydrates)
            }

            if(this.calories == ""){
                this.warning = true;
                console.log("калории");
            }
            else{
                formData.append("calories", this.calories)
            }
            
            formData.append("breakfast", this.breakfast);
            formData.append("lunch", this.lunch);
            formData.append("dinner", this.dinner);
            formData.append("usualdiet", this.usualdiet);
            formData.append("weightloss", this.weightloss);
            formData.append("weightgain", this.weightgain);
            formData.append("recipe", this.dish_recipe);
            if(this.time == ""){
                this.warning = true;
                console.log("время");
            }
            else{
                formData.append("time", this.time)
            }
            formData.append("cookware", this.dish_cookware);
            formData.append("ingredients", this.ingredients_dish);

            // фотки
            var mainPhoto = document.querySelector('#main__photo').files[0];
            if(mainPhoto){
                formData.append("mainphoto", mainPhoto);
            }

            var otherPhoto = document.querySelector('#other__photo').files;
            for(var i=0; i < otherPhoto.length; i++){
                formData.append(`photo${i+1}`, otherPhoto[i]);
            }

            if(this.ingredients_dish.length < 1){
                this.warning = true;
                console.log("ингредиенты");
            }

            // предупреждение
            if(this.warning){
                if(confirm('Вы заполнили не все поля. Хотите продолжить?')) {
                    // включаю анимацию загрузки
                    let load = document.querySelector('.loading'); 
                    load.style.display = 'block';

                    // создаю блюдо
                    await axios.post('dish/create/', formData).then(response => {
                        let load = document.querySelector('.loading'); load.style.display = 'none';
                        console.log(response.data);
                    })
                    .catch(error => {
                        this.errors_dish = [];
                        let load = document.querySelector('.loading'); load.style.display = 'none';
                        if (error.response) {
                            for (const property in error.response.data) {
                                this.errors_dish.push(`${error.response.data[property]}`)
                            }
                        } else {
                            this.errors_dish.push('Что-то пошло не так! Повторите попытку позже)')
                        }
                    })
                } 
            }
            else{
                // включаю анимацию загрузки
                let load = document.querySelector('.loading'); 
                load.style.display = 'block';

                // создаю блюдо
                await axios.post('dish/create/', formData).then(response => {
                    let load = document.querySelector('.loading'); load.style.display = 'none';
                    console.log(response.data);
                })
                .catch(error => {
                    this.errors_dish = [];
                    let load = document.querySelector('.loading'); load.style.display = 'none';
                    if (error.response) {
                        for (const property in error.response.data) {
                            this.errors_dish.push(`${error.response.data[property]}`)
                        }
                    } else {
                        this.errors_dish.push('Что-то пошло не так! Повторите попытку позже)')
                    }
                })
            }
        },
    },      
}
</script>

<style scoped>
    .main{
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    .main__title{
        font-size: 40px;
        margin-bottom: 10px;
        font-weight: 600;
    }

    .line{
        width: 300px;
        border-bottom: 2px solid rgb(0, 0, 0);
        margin-bottom: 10px;
    }

    .label__input{
        font-size: 24px;
        margin: 10px;
    }

    .text__input{
        margin: 10px;
        font-size: 20px;
        border-radius: 5px;
        width: 300px;
        border: 2px solid rgb(0, 0, 0);
    }

    .textarea__input{
        width: 300px; 
        height: 200px; 
        resize: none; 
        margin: 10px;
        font-size: 20px;
        border-radius: 5px;
        border: 2px solid rgb(0, 0, 0);
    }

    .row{
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-direction: row;
        width: 570px;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    .pink{
        width: 100%;
        background-color: #F9E8FF;
        display: flex;
        align-items: center;
        justify-content: center;
        padding-top: 10px;
        padding-bottom: 10px;
    }

    .row__pink__ingredients{
        display: flex;
        align-items: center;
        justify-content: space-between;
        
        flex-direction: column;
        width: 570px;
    }

    .row__textarea{
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        flex-direction: row;
        width: 570px;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    .ingredients{
        display: flex;
        flex-direction: row;
    }

    .ingredients__title{
        display: flex;
        flex-direction: row;
        margin-left: -10px;
    }

    .ingredients__label{
        margin-left: 10px;
        font-size: 20px;
    }

    .ingredients__title__empty{
        width: 347px;
        height: 10px;
    }

    .ingredient__input{
        margin-left: 10px;
        margin-right: 10px;
        margin-top: 10px;
        font-size: 20px;
        border-radius: 5px;
        width: 300px;
    }

    .ingredient__count{
        margin-left: 10px;
        margin-right: 10px;
        margin-top: 33px;
        font-size: 20px;
        border-radius: 5px;
        width: 100px;
    }

    .ingredients__column{
        display: flex;
        flex-direction: column;
    }

    .ingredient__result{
        margin-left: 11px;
        margin-right: 10px;
        width: 300px;
        background-color: white;
    }
    
    .ingredient__result:hover{
        cursor: pointer;
        background-color: antiquewhite;
    }

    .ingredients__added{
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        justify-content: center;
        width: 493px;
    }

    .ingredients__added__label{
        font-size: 20px;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    #add__ing__btn{
        margin-top: 33px;
        height: 25px;
        width: 70px;
        background-color: rgb(200, 0, 255);
        color: white;
        border-radius: 5px;
    }

    #add__ing__btn__dis
    {
        margin-top: 33px;
        height: 25px;
        width: 70px;
        background-color: rgb(246, 211, 255);
        color: white;
        border-radius: 5px;
    }

    #add__ing__btn:hover
    {
        cursor: pointer;
        background-color: rgb(221, 97, 255);
    }

    .ingredient__add{
        display: flex;
        align-items: flex-start;
        justify-content: flex-start;
    }

    .ingredients__added__list{
        margin-bottom: 10px;
    }

    .ingredients__list__row{
        display: flex;
        flex-direction: row;
    }

    .remove__ingredient{
        margin-left: 10px;
        font-size: 18px;
        color: red;
    }

    .remove__ingredient:hover{
        cursor: pointer;
        color: rgb(255, 146, 146);
    }

    .number__input{
        margin: 10px;
        font-size: 20px;
        border-radius: 5px;
        width: 120px;
    }

    .div__calories{
        display: flex; 
        flex-direction: row;
    }

    .column{
        display: flex;
        flex-direction: column;
    }

    .checkboxes{
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
        margin-left: 10px;
        margin-bottom: 10px;
    }

    .checkbox__label{
        font-size: 20px;
    }

    /* Красивый чекбокс */

    input[type="checkbox"]:checked, 
    input[type="checkbox"]:not(:checked), 
    input[type="radio"]:checked, 
    input[type="radio"]:not(:checked) 
    {
        position: absolute;
        left: -9999px;
    }

    input[type="checkbox"]:checked + label, 
    input[type="checkbox"]:not(:checked) + label, 
    input[type="radio"]:checked + label, 
    input[type="radio"]:not(:checked) + label {
        display: inline-block;
        position: relative;
        padding-left: 28px;
        line-height: 20px;
        cursor: pointer;
    }

    input[type="checkbox"]:checked + label:before, 
    input[type="checkbox"]:not(:checked) + label:before,
    input[type="radio"]:checked + label:before, 
    input[type="radio"]:not(:checked) + label:before {
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

    input[type="radio"]:checked + label:before, 
    input[type="radio"]:not(:checked) + label:before {
        border-radius: 100%;
    }

    input[type="checkbox"]:checked + label:after, 
    input[type="checkbox"]:not(:checked) + label:after, 
    input[type="radio"]:checked + label:after, 
    input[type="radio"]:not(:checked) + label:after {
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

    input[type="radio"]:checked + label:after, 
    input[type="radio"]:not(:checked) + label:after {
        left: 5px;
        top: 5px;
        width: 10px;
        height: 10px;
        border-radius: 100%;
        background-color: #e145a3;
    }

    input[type="checkbox"]:not(:checked) + label:after, 
    input[type="radio"]:not(:checked) + label:after {
        opacity: 0;
    }

    input[type="checkbox"]:checked + label:after, 
    input[type="radio"]:checked + label:after {
        opacity: 1;
    }

    .img{
        width: 300px;
        height: 250px;
        object-fit: cover;
        border-radius: 10px;
        margin-bottom: 10px;
    }

    input[type="file"] {
        display: none;
    }

    .photo__input{  
        height: 20px;
        width: 75px;
        background-color: rgb(200, 0, 255);
        color: white;
        border-radius: 5px;
        text-align: center;
        border: 2px solid rgb(0, 0, 0);
    }

    .photo__input:hover{
        cursor: pointer;
        background-color: rgb(221, 97, 255);
    }

    .remove__main__photo{
        font-size: 22px;
        color: red;
    }

    .remove__main__photo:hover{
        cursor: pointer;
        color: rgb(255, 146, 146);
    }

    .photos{
        display: flex;
        flex-wrap: wrap;
        flex-direction: row;
        align-items: center;
        justify-content: flex-start;
        width: 440px;
    }

    .one__photo{
        width: 100px;
        height: 100px;
        border-radius: 5px;
        margin: 5px;
        object-fit: cover;
    }

    .errors__cookware{
        color: red;
    }

    .textarea__recipe{
        width: 546px; 
        height: 200px; 
        margin: 10px;
        font-size: 20px;
        border-radius: 5px;
        border: 2px solid rgb(0, 0, 0);
        resize: vertical;
    }

    .create__dish{
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

    .create__dish:hover{
        background: linear-gradient(#7086ff, rgb(255, 150, 167));
        cursor: pointer;
    }

    .create__dish__disabled{
        width: 80px;
        height: 35px;
        background: linear-gradient(rgb(188, 198, 255), rgb(255, 217, 223));
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        border: 1px solid black;
        box-shadow: 3px 3px 3px rgb(0, 0, 0, 0.3);
    }

</style>