<template>
    <footer>
        <p class="footer">Artemida Food © Все права защищены</p>
    </footer>
</template>

<style scoped>
    footer{
        background-color: #78258B;
        width: 100%;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .footer{
        color: white;
        font-size: 20px;
    }

     /* Мобильная верстка */
     @media (max-width: 1000px){
        .footer{
            font-size: 14px;
        }
    }
</style>