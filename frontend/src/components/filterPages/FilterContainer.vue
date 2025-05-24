<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Filter Type Selector -->
    <div class="mb-6">
      <div class="flex space-x-4">
        <button
          v-for="type in filterTypes"
          :key="type.value"
          @click="currentFilterType = type.value"
          :class="[
            'px-4 py-2 rounded-md font-medium',
            currentFilterType === type.value
              ? 'bg-blue-600 text-white'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          ]"
        >
          {{ type.label }}
        </button>
      </div>
    </div>

    <!-- Filter Components -->
    <div class="mb-6">
      <ProductFilter
        v-if="currentFilterType === 'product'"
        @filter-applied="handleFilterApplied"
        @filter-reset="handleFilterReset"
      />
      <ShipmentFilter
        v-if="currentFilterType === 'shipment'"
        @filter-applied="handleFilterApplied"
        @filter-reset="handleFilterReset"
      />
      <PurchaseFilter
        v-if="currentFilterType === 'purchase'"
        @filter-applied="handleFilterApplied"
        @filter-reset="handleFilterReset"
      />
    </div>

    <!-- Results Section -->
    <div v-if="loading" class="text-center py-8">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
      <p class="mt-4 text-gray-600">در حال بارگذاری...</p>
    </div>

    <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
      <strong class="font-bold">خطا!</strong>
      <span class="block sm:inline">{{ error }}</span>
    </div>

    <div v-else-if="filteredData.length > 0" class="bg-white rounded-lg shadow-md p-6">
      <h3 class="text-xl font-semibold mb-4">نتایج ({{ filteredData.length }})</h3>
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th v-for="header in tableHeaders" :key="header" class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                {{ header }}
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="item in filteredData" :key="item.id">
              <td v-for="field in getTableFields(item)" :key="field" class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ field }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div v-else-if="hasSearched" class="bg-white rounded-lg shadow-md p-6 text-center text-gray-500">
      هیچ نتیجه‌ای یافت نشد
    </div>
  </div>
</template>

<script>
import ProductFilter from './ProductFilter.vue'
import ShipmentFilter from './ShipmentFilter.vue'
import PurchaseFilter from './PurchaseFilter.vue'
import { gql } from '@apollo/client/core'
import { apolloClient } from '@/apollo'

const FILTER_QUERY = gql`
  query FilterData($filterInput: FilterInput) {
    filteredData(filterInput: $filterInput) {
      ... on ProductType {
        id
        profileName
        reelNumber
        width
        gsm
        length
        status
        location
        grade
        breaks
      }
    }
  }
`

export default {
  name: 'FilterContainer',
  components: {
    ProductFilter,
    ShipmentFilter,
    PurchaseFilter
  },
  data() {
    return {
      currentFilterType: 'product',
      filterTypes: [
        { label: 'محصولات', value: 'product' },
        { label: 'ارسال‌ها', value: 'shipment' },
        { label: 'خریدها', value: 'purchase' }
      ],
      filteredData: [],
      hasSearched: false,
      loading: false,
      error: null
    }
  },
  computed: {
    tableHeaders() {
      switch (this.currentFilterType) {
        case 'product':
          return ['نام پروفایل', 'شماره رول', 'عرض', 'GSM', 'طول', 'وضعیت', 'موقعیت', 'گرید', 'شکستگی']
        default:
          return []
      }
    }
  },
  methods: {
    getTableFields(item) {
      switch (this.currentFilterType) {
        case 'product':
          return [
            item.profileName,
            item.reelNumber,
            item.width,
            item.gsm,
            item.length,
            item.status,
            item.location,
            item.grade,
            item.breaks
          ]
        default:
          return []
      }
    },
    async handleFilterApplied(filters) {
      this.loading = true
      this.error = null
      this.hasSearched = true

      try {
        const response = await apolloClient.query({
          query: FILTER_QUERY,
          variables: {
            filterInput: filters
          },
          fetchPolicy: 'network-only'
        })

        if (response.data && response.data.filteredData) {
          this.filteredData = response.data.filteredData
        } else {
          this.filteredData = []
        }
      } catch (err) {
        this.error = 'خطا در دریافت اطلاعات'
        console.error('Filter error:', err)
      }

      this.loading = false
    },
    handleFilterReset() {
      this.filteredData = []
      this.hasSearched = false
      this.error = null
    }
  }
}
</script> 