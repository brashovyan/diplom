<template>
    <div>
      <h1>Id {{ dish}}</h1>
    </div>
</template>

<script>
export default{
    data() {
        return {
            dish: this.$route.params.id,
        }
    },

    mounted() {
        
    },
}
</script>