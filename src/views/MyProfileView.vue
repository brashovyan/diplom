<template>
  <div>
    <h1>Id {{ profile }}</h1>
  </div>
</template>

<script>
export default{
  data() {
      return {
          profile: this.$route.params.id,
      }
  },

  mounted() {
      
  },
}
</script>