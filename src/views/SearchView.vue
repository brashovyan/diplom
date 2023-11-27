<template>
    <div>
      <h1>Поиск</h1>
      {{ searchStr }}
    </div>
  </template>

<script>
export default{
    data() {
        return {
            searchStr: '',
        }
    },

    mounted() {
        this.searchStr = this.$route.query.search_str;
    },
}
</script>