<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-8 text-right">فیلتر داده‌ها</h1>
    <FilterContainer />
  </div>
</template>

<script>
import FilterContainer from './FilterContainer.vue'

export default {
  name: 'FilterPage',
  components: {
    FilterContainer
  }
}
</script> 