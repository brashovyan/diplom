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
                <input type="text" placeholder="Название блюда (обязательно)" v-model="dish_title" class="text__input" required>
            </div>

            <div class="row__textarea">
                <p class="label__input">Краткое описание:</p>
                <textarea placeholder="Краткое описание (обязательно)" v-model="dish_description" class="textarea__input" required></textarea>
                
            </div>
            <p class="label__input">Подсказка:</p>
            <div class="row">
                <p style="margin-left: 10px;">Указывайте кол-во ингредиентов для одной порции. Расчёт КБЖУ так же идёт на одну порцию. Точнее всего будет, если указывать в граммах. Вы можете самостоятельно указать КБЖУ блюда.</p>
            </div>
            <div class="row">
            <p style="margin-left: 10px;">Начните вводить название ингредиента, и выберите его в выпадающем списке. Если ничего не нашлось, то вы всё равно можете добавить этот ингредиент, но он не будет учитываться при подсчёте КБЖУ.</p>
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
                                <template v-for="(ingredient, key) in ingredient_list" :key="key">
                                    <p class="ingredient__result" @click="addIngredientCandidate(ingredient.title, ingredient.id, ingredient.calories, ingredient.proteins, ingredient.fats, ingredient.carbohydrates)">{{ ingredient.title }}</p>
                                </template>
                            </template>
                        </div>
                        
                        <div class="ingredient__add">
                            <input type="number" placeholder="Кол-во" v-model="ingredient_count" min=0 class="ingredient__count">
                            <select v-model="ingredient_unit" class="ingredient__unit">
                                <option value="gr" selected>Гр</option>
                                <option value="sht">Шт</option>
                                <option value="st_losh">Ст. ложка</option>
                                <option value="ch_losh">Ч. ложка</option>
                                <option value="ml">Мл</option>
                            </select>
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
                    <textarea placeholder="Напишите рецепт (обязательно)" v-model="dish_recipe" class="textarea__recipe" required></textarea>
                </div>
            </div>
            
            <!-- Создать -->
            <template v-if="dish_title != '' && dish_description != '' && dish_recipe != ''">
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
            calories: 0, // калории
            proteins: 0, // белки
            fats: 0, // жиры
            carbohydrates: 0, // углеводы
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
            ingredient_count: "0", // кол-во ингредиента
            ingredient_unit: "gr", // единица измерения ингредиента
            ingredient_response: {"result": []}, // результат поиска игредиента
            ingredient_find: false, // выбран ли ингредиент из списка
            ingredient_response_count: 0, // кол-во результатов поиска
            ingredient_candidate: "", // блюдо, которое юзер выбрал из выпадающего списка
            ingredient_candidates: [], // список добавленных кандидатов
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

        if(this.$store.state.isAuthenticated==false){
            // перенаправляю его на главную страницу
            this.$router.push('/');
        }

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
        async addIngredientCandidate(ingredient, id, calories, proteins, fats, carbohydrates){
            this.ingredient_title = ingredient; 
            this.ingredient_find = true;
            this.ingredient_candidate = {"id": id, "title": ingredient, "calories": calories, "proteins": proteins, "fats": fats, "carbohydrates": carbohydrates};
        },

        // добавление ингредиента в блюдо
        async addIngredientDish(){
            // если мы выбрали ингредиент из списка
            if(this.ingredient_candidate != ""){

                // нельзя добавлять несколько одинаковых ингредиентов
                var flag = true;
                for(let ingredient of this.ingredients_dish){
                    if(ingredient["id"]==this.ingredient_candidate["id"]){
                        flag = false;
                    }
                }

                if(flag==true){
                    // пытаемся считать кбжу
                    var ing_unit = "";
                    if(this.ingredient_unit=="gr"){
                        ing_unit = "гр";
                        this.calories = (Number(this.calories) + ((Number(this.ingredient_count) / 100) * Number(this.ingredient_candidate["calories"]))).toFixed(2);
                        this.proteins = (Number(this.proteins) + ((Number(this.ingredient_count) / 100) * Number(this.ingredient_candidate["proteins"]))).toFixed(2);
                        this.fats = (Number(this.fats) + ((Number(this.ingredient_count) / 100) * Number(this.ingredient_candidate["fats"]))).toFixed(2);
                        this.carbohydrates = (Number(this.carbohydrates) + ((Number(this.ingredient_count) / 100) * Number(this.ingredient_candidate["carbohydrates"]))).toFixed(2);
                    }
                    else if(this.ingredient_unit=="sht"){
                        ing_unit = "шт";
                        this.calories = (Number(this.calories) + ((Number(this.ingredient_count) * 0.9) * Number(this.ingredient_candidate["calories"]))).toFixed(2);
                        this.proteins = (Number(this.proteins) + ((Number(this.ingredient_count) * 0.9) * Number(this.ingredient_candidate["proteins"]))).toFixed(2);
                        this.fats = (Number(this.fats) + ((Number(this.ingredient_count) * 0.9) * Number(this.ingredient_candidate["fats"]))).toFixed(2);
                        this.carbohydrates = (Number(this.carbohydrates) + ((Number(this.ingredient_count) * 0.9) * Number(this.ingredient_candidate["carbohydrates"]))).toFixed(2);
                    }
                    else if(this.ingredient_unit=="st_losh"){
                        ing_unit = "ст. ложка";
                        this.calories = (Number(this.calories) + ((Number(this.ingredient_count) * 0.25) * Number(this.ingredient_candidate["calories"]))).toFixed(2);
                        this.proteins = (Number(this.proteins) + ((Number(this.ingredient_count) * 0.25) * Number(this.ingredient_candidate["proteins"]))).toFixed(2);
                        this.fats = (Number(this.fats) + ((Number(this.ingredient_count) * 0.25) * Number(this.ingredient_candidate["fats"]))).toFixed(2);
                        this.carbohydrates = (Number(this.carbohydrates) + ((Number(this.ingredient_count) * 0.25) * Number(this.ingredient_candidate["carbohydrates"]))).toFixed(2);
                    }
                    else if(this.ingredient_unit=="ch_losh"){
                        ing_unit = "ч. ложка";
                        this.calories = (Number(this.calories) + ((Number(this.ingredient_count) * 0.08) * Number(this.ingredient_candidate["calories"]))).toFixed(2);
                        this.proteins = (Number(this.proteins) + ((Number(this.ingredient_count) * 0.08) * Number(this.ingredient_candidate["proteins"]))).toFixed(2);
                        this.fats = (Number(this.fats) + ((Number(this.ingredient_count) * 0.08) * Number(this.ingredient_candidate["fats"]))).toFixed(2);
                        this.carbohydrates = (Number(this.carbohydrates) + ((Number(this.ingredient_count) * 0.08) * Number(this.ingredient_candidate["carbohydrates"]))).toFixed(2);
                    }
                    else if(this.ingredient_unit=="ml"){
                        ing_unit = "мл";
                        this.calories = (Number(this.calories) + ((Number(this.ingredient_count) / 100) * Number(this.ingredient_candidate["calories"]))).toFixed(2);
                        this.proteins = (Number(this.proteins) + ((Number(this.ingredient_count) / 100) * Number(this.ingredient_candidate["proteins"]))).toFixed(2);
                        this.fats = (Number(this.fats) + ((Number(this.ingredient_count) / 100) * Number(this.ingredient_candidate["fats"]))).toFixed(2);
                        this.carbohydrates = (Number(this.carbohydrates) + ((Number(this.ingredient_count) / 100) * Number(this.ingredient_candidate["carbohydrates"]))).toFixed(2);
                    }
                    this.ingredient_candidates.push(this.ingredient_candidate);

               
                    let ing = {"id": this.ingredient_candidate["id"], "title": this.ingredient_candidate["title"], "count": `${this.ingredient_count} ${ing_unit}`}
                    this.ingredients_dish.push(ing);
                }
                else{
                    alert("Этот ингредиент уже добавлен!");
                }
            }
            // если в списке не было нашего ингредиента
            else{
                // нельзя добавлять несколько одинаковых ингредиентов
                var flag2 = true;
                for(let ingredient of this.ingredients_dish){
                    if(ingredient["title"].toLowerCase() == this.ingredient_title.toLowerCase()){
                        flag2 = false;
                    }
                }

                if(flag2==true){
                    var ing_unit2 = "";
                    if(this.ingredient_unit=="gr")
                        ing_unit2 = "гр";
                    else if(this.ingredient_unit=="sht")
                        ing_unit2 = "шт";
                    else if(this.ingredient_unit=="st_losh")
                        ing_unit2 = "ст. ложка";
                    else if(this.ingredient_unit=="ch_losh")
                        ing_unit2 = "ч. ложка";
                    else if(this.ingredient_unit=="ml")
                        ing_unit2 = "мл";
                    let ing2 = {"id": "no", "title": this.ingredient_title, "count": `${this.ingredient_count} ${ing_unit2}`}
                    this.ingredients_dish.push(ing2);
                }
                else{
                    alert("Этот ингредиент уже добавлен!");
                }
            }

            this.ingredient_title = "";
            this.ingredient_count = "0";
            this.ingredient_find = false;
            this.ingredient_candidate = "";
            this.ingredient_response = {"result": []};
            this.ingredient_response_count = 0;
        },

        // удаление ингредиента из блюда
        async deleteIngredintFromDish(ingredient){
            const index = this.ingredients_dish.indexOf(ingredient);
            if (index > -1){
                var id = this.ingredients_dish[index]["id"];
                var count_list = this.ingredients_dish[index]["count"].split(" ");
                var count = 0;
                if(count_list[0] == ""){
                    count = 0;
                }
                else{
                    count = count_list[0];
                }
                this.ingredients_dish.splice(index, 1);
                // отнимаю кбжу 
                var cand = "";
                for(var candidate of this.ingredient_candidates){
                    if(id == candidate["id"]){
                        cand = candidate;
                        if(count_list[1]=="гр"){
                            this.calories = (Number(this.calories) - ((Number(count) / 100) * Number(candidate["calories"]))).toFixed(2);
                            this.proteins = (Number(this.proteins) - ((Number(count) / 100) * Number(candidate["proteins"]))).toFixed(2);
                            this.fats = (Number(this.fats) - ((Number(count) / 100) * Number(candidate["fats"]))).toFixed(2);
                            this.carbohydrates = (Number(this.carbohydrates) - ((Number(count) / 100) * Number(candidate["carbohydrates"]))).toFixed(2);
                        }
                        else if(count_list[1]=="шт"){
                            this.calories = (Number(this.calories) - ((Number(count) * 0.9) * Number(candidate["calories"]))).toFixed(2);
                            this.proteins = (Number(this.proteins) - ((Number(count) * 0.9) * Number(candidate["proteins"]))).toFixed(2);
                            this.fats = (Number(this.fats) - ((Number(count) * 0.9) * Number(candidate["fats"]))).toFixed(2);
                            this.carbohydrates = (Number(this.carbohydrates) - ((Number(count) * 0.9) * Number(candidate["carbohydrates"]))).toFixed(2);
                        }
                        else if(count_list[1]=="ст."){
                            this.calories = (Number(this.calories) - ((Number(count) * 0.25) * Number(candidate["calories"]))).toFixed(2);
                            this.proteins = (Number(this.proteins) - ((Number(count) * 0.25) * Number(candidate["proteins"]))).toFixed(2);
                            this.fats = (Number(this.fats) - ((Number(count) * 0.25) * Number(candidate["fats"]))).toFixed(2);
                            this.carbohydrates = (Number(this.carbohydrates) - ((Number(count) * 0.25) * Number(candidate["carbohydrates"]))).toFixed(2);
                        }
                        else if(count_list[1]=="ч."){
                            this.calories = (Number(this.calories) - ((Number(count) * 0.08) * Number(candidate["calories"]))).toFixed(2);
                            this.proteins = (Number(this.proteins) - ((Number(count) * 0.08) * Number(candidate["proteins"]))).toFixed(2);
                            this.fats = (Number(this.fats) - ((Number(count) * 0.08) * Number(candidate["fats"]))).toFixed(2);
                            this.carbohydrates = (Number(this.carbohydrates) - ((Number(count) * 0.08) * Number(candidate["carbohydrates"]))).toFixed(2);
                        }
                        else if(count_list[1]=="мл"){
                            this.calories = (Number(this.calories) - ((Number(count) / 100) * Number(candidate["calories"]))).toFixed(2);
                            this.proteins = (Number(this.proteins) - ((Number(count) / 100) * Number(candidate["proteins"]))).toFixed(2);
                            this.fats = (Number(this.fats) - ((Number(count) / 100) * Number(candidate["fats"]))).toFixed(2);
                            this.carbohydrates = (Number(this.carbohydrates) - ((Number(count) / 100) * Number(candidate["carbohydrates"]))).toFixed(2);
                        }
                    }
                }
                const index2 = this.ingredient_candidates.indexOf(cand);
                if(index2 > -1){
                    this.ingredient_candidates.splice(index, 1);
                }

                if(this.ingredient_candidates.length < 1){
                    this.calories = 0;
                    this.proteins = 0;
                    this.fats = 0;
                    this.carbohydrates = 0;
                }
            }
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

        // создание блюда
        async createDish(){
            var formData = new FormData();
            formData.append("title", this.dish_title);
            formData.append("description", this.dish_description);
            
            // если белки/жиры и т.д. не указаны, то я их не добавляю (по дефолту на бэке 0)
            if(this.proteins == ""){
                this.warning = true;
            }
            else{
                formData.append("proteins", this.proteins);
                
            }

            if(this.fats == ""){
                this.warning = true;
            }
            else{
                formData.append("fats", this.fats)
            }

            if(this.carbohydrates == ""){
                this.warning = true;
            }
            else{
                formData.append("carbohydrates", this.carbohydrates)
            }

            if(this.calories == ""){
                this.warning = true;
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
            }
            else{
                formData.append("time", this.time)
            }

            if(this.dish_cookware.length > 0){
                for(let i=0; i < this.dish_cookware.length; i++)
                    formData.append("cookware", this.dish_cookware[i]);
            }
            else{
                this.warning = true;
            }
            
            // тут сложная отправка списка словарей
            if(this.ingredients_dish.length > 0){
                for(let i=0; i < this.ingredients_dish.length; i++)
                    formData.append("ingredients", JSON.stringify({"id": this.ingredients_dish[i]["id"], "title": this.ingredients_dish[i]["title"], "count": this.ingredients_dish[i]["count"]}));
          
            }
            else{
                this.warning = true; 
            }
            

            // фотки
            var mainPhoto = document.querySelector('#main__photo').files[0];
            if(mainPhoto){
                formData.append("mainphoto", mainPhoto);
            }

            var otherPhoto = document.querySelector('#other__photo').files;
            for(var i=0; i < otherPhoto.length; i++){
                formData.append(`photo${i+1}`, otherPhoto[i]);
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

                        // перенаправляю его на главную страницу
                        this.$router.push('/');
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

                    // перенаправляю его на главную страницу
                    this.$router.push('/');
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
        box-shadow: 3px 3px 3px rgb(0, 0, 0, 0.4);
    }

    .textarea__input{
        width: 300px; 
        height: 200px; 
        resize: none; 
        margin: 10px;
        font-size: 20px;
        border-radius: 5px;
        border: 2px solid rgb(0, 0, 0);
        box-shadow: 3px 3px 3px rgb(0, 0, 0, 0.4);
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
        margin-right: 0px;
        margin-top: 10px;
        font-size: 20px;
        border-radius: 5px;
        width: 280px;
        box-shadow: 3px 3px 3px rgb(0, 0, 0, 0.4);
    }

    .ingredient__count{
        margin-left: 10px;
        margin-right: 10px;
        margin-top: 33.5px;
        font-size: 20px;
        border-radius: 5px;
        width: 60px;
        box-shadow: 3px 3px 3px rgb(0, 0, 0, 0.4);
    }

    .ingredient__unit{
        border-radius: 5px;
        border: 2px solid rgb(0, 0, 0);
        font-size: 16px;
        width: 80px;
        margin-top: 35.5px;
        margin-right: 10px;
        margin-left: 10px;
        box-shadow: 3px 3px 3px rgb(0, 0, 0, 0.4);
    }

    .ingredients__column{
        display: flex;
        flex-direction: column;
    }

    .ingredient__result{
        margin-left: 11px;
        margin-right: 10px;
        width: 280px;
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
        box-shadow: 3px 3px 3px rgb(0, 0, 0, 0.4);
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
        box-shadow: 3px 3px 3px rgb(0, 0, 0, 0.4);
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
        box-shadow: 3px 3px 3px rgb(0, 0, 0, 0.4);
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
        box-shadow: 3px 3px 3px rgb(0, 0, 0, 0.4);
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