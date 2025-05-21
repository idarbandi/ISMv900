<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-8 text-right">فیلتر داده‌ها</h1>
    
    <!-- Filter Form -->
    <div class="bg-white rounded-lg shadow-lg p-6 mb-8">
      <form @submit.prevent="applyFilters" class="space-y-4">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <!-- Truck License -->
          <div class="form-group">
            <label class="block text-right mb-2">شماره پلاک کامیون</label>
            <input 
              type="text" 
              v-model="filters.truckLicenseNumber"
              class="w-full rounded-lg border p-2 text-right"
              placeholder="شماره پلاک را وارد کنید"
            >
          </div>

          <!-- Driver Name -->
          <div class="form-group">
            <label class="block text-right mb-2">نام راننده</label>
            <input 
              type="text" 
              v-model="filters.driverName"
              class="w-full rounded-lg border p-2 text-right"
              placeholder="نام راننده را وارد کنید"
            >
          </div>

          <!-- Shipment Type -->
          <div class="form-group">
            <label class="block text-right mb-2">نوع ارسال</label>
            <select v-model="filters.shipmentType" class="w-full rounded-lg border p-2 text-right">
              <option value="">همه</option>
              <option value="regular">عادی</option>
              <option value="express">فوری</option>
            </select>
          </div>

          <!-- Customer National ID -->
          <div class="form-group">
            <label class="block text-right mb-2">کد ملی مشتری</label>
            <input 
              type="text" 
              v-model="filters.customerNationalId"
              class="w-full rounded-lg border p-2 text-right"
              placeholder="کد ملی را وارد کنید"
            >
          </div>
        </div>

        <div class="flex justify-end mt-6">
          <button 
            type="submit"
            class="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            اعمال فیلتر
          </button>
        </div>
      </form>
    </div>

    <!-- Results -->
    <div v-if="loading" class="text-center py-8">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
      <p class="mt-4 text-gray-600">در حال بارگذاری...</p>
    </div>

    <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
      <strong class="font-bold">خطا!</strong>
      <span class="block sm:inline">{{ error }}</span>
    </div>

    <div v-else-if="results.length > 0" class="bg-white rounded-lg shadow-lg overflow-hidden">
      <table class="min-w-full">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">نوع</th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">اطلاعات</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="item in results" :key="item.id">
            <td class="px-6 py-4 whitespace-nowrap text-right">{{ getItemType(item) }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-right">{{ getItemInfo(item) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-else class="text-center py-8 text-gray-500">
      هیچ نتیجه‌ای یافت نشد
    </div>
  </div>
</template>

<script>
import { ref, reactive, watch } from 'vue'
import { useQuery } from '@vue/apollo-composable'
import gql from 'graphql-tag'

const FILTER_QUERY = gql`
  query FilterData($filterInput: FilterInput) {
    filteredData(filterInput: $filterInput) {
      ... on TruckType {
        id
        licenseNumber
        driverName
      }
      ... on SalesType {
        id
        totalPrice
      }
      ... on CustomerType {
        id
        customerName
        nationalId
      }
      ... on ProductType {
        id
        profileName
      }
      ... on ShipmentType {
        id
        shipmentType
      }
    }
  }
`

export default {
  name: 'FilterPage',
  setup() {
    const filters = reactive({
      truckLicenseNumber: '',
      driverName: '',
      shipmentType: '',
      customerNationalId: '',
    })

    const { result, loading, error, refetch } = useQuery(FILTER_QUERY, {
      filterInput: filters,
      fetchPolicy: 'network-only'  // Don't use cache
    })

    const results = ref([])

    // Watch for changes in the result
    watch(result, (newResult) => {
      if (newResult && newResult.filteredData) {
        results.value = newResult.filteredData
      }
    })

    const applyFilters = async () => {
      try {
        await refetch()
      } catch (err) {
        console.error('Error applying filters:', err)
      }
    }

    const getItemType = (item) => {
      if (item.licenseNumber) return 'کامیون'
      if (item.customerName && item.nationalId) return 'مشتری'
      if (item.shipmentType) return 'ارسال'
      if (item.totalPrice) return 'فاکتور فروش'
      if (item.profileName) return 'محصول'
      return 'نامشخص'
    }

    const getItemInfo = (item) => {
      if (item.licenseNumber) return `پلاک: ${item.licenseNumber} (راننده: ${item.driverName || 'نامشخص'})`
      if (item.customerName && item.nationalId) return `مشتری: ${item.customerName} (کد ملی: ${item.nationalId})`
      if (item.shipmentType) return `نوع ارسال: ${item.shipmentType}`
      if (item.totalPrice) return `مبلغ کل: ${item.totalPrice} تومان`
      if (item.profileName) return `محصول: ${item.profileName}`
      return 'اطلاعات نامشخص'
    }

    return {
      filters,
      results,
      loading,
      error,
      applyFilters,
      getItemType,
      getItemInfo,
    }
  }
}
</script>

<style scoped>
.form-group {
  @apply text-right;
}

input, select {
  @apply focus:ring-2 focus:ring-blue-500 focus:border-blue-500;
}
</style> 