<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-8 text-right">فیلتر داده‌ها</h1>
    
    <!-- Filter Form -->
    <div class="bg-white rounded-lg shadow-lg p-6 mb-8">
      <form @submit.prevent="applyFilters" class="space-y-4">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <!-- Truck License Input -->
          <div class="form-group col-span-full md:col-span-1 flex flex-col items-end">
            <label class="block text-right mb-2 w-full">شماره پلاک کامیون</label>
            <div class="flex flex-row justify-center">
              <div class="rounded-lg bg-white shadow-lg max-w-sm">
                <div class="flex rounded-lg border-4 border-black shadow">
                  <label class="flex flex-none flex-col items-center px-2 justify-center sm:justify-start sm:px-4 border-e-4 border-black font-bold">
                    ایران
                    <p class="place-self-center sm:text-4xl">{{ license.year.val }}</p>
                  </label>
                  <label class="flex-grow flex flex-row px-2 gap-2 sm:gap-4 justify-center items-center sm:p-4 font-mono text-4xl sm:text-5xl font-bold">
                    <h>{{ license.second.val }}</h>
                    <h>{{ license.letter.val }}</h>
                    <h>{{ license.first.val }}</h>
                  </label>
                  <label class="flex flex-none flex-col items-end justify-between px-1 py-1 bg-blue-700 border-s-4 border-black font-bold text-xs text-white">
                    <img src="@/assets/Flag_of_Iran.svg.png" class="h-5">
                    <span class="flex flex-col items-end">
                      <h>IR</h>
                      <h>IRAN</h>
                    </span>
                  </label>
                </div>
              </div>
            </div>
          </div>

          <!-- License form -->
          <div class="flex flex-col items-center mt-5 gap-4">
            <div class="flex space-x-2 rtl:space-x-reverse">
              <div>
                <label for="code-1" class="sr-only">First code</label>
                <input v-model="license.year.val" :placeholder="license.year.val" type="text" maxlength="2" data-focus-input-init data-focus-input-next="code-2" id="code-1" :class="[license.year.error ? 'appearance-none bg-red-50 border border-red-500 text-red-900 placeholder-red-700 text-sm rounded-lg focus:ring-red-500 dark:bg-gray-700 focus:border-red-500 dark:text-red-500 dark:placeholder-red-500 dark:border-red-500' : 'text-gray-900 bg-white border border-gray-300 rounded-lg focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500']" class="block w-12 h-9 py-3 text-sm font-extrabold text-center" required />
              </div>
              <div>
                <label for="code-3" class="sr-only">Third code</label>
                <input v-model="license.second.val" :placeholder="license.second.val" type="text" maxlength="3" data-focus-input-init data-focus-input-prev="code-2" data-focus-input-next="code-4" id="code-3" :class="[license.second.error ? 'bg-red-50 border border-red-500 text-red-900 placeholder-red-700 text-sm rounded-lg focus:ring-red-500 dark:bg-gray-700 focus:border-red-500 dark:text-red-500 dark:placeholder-red-500 dark:border-red-500' : 'text-gray-900 bg-white border border-gray-300 rounded-lg focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500']" class="block w-14 h-9 py-3 text-sm font-extrabold text-center" required />
              </div>
              <button id="letterButton" data-dropdown-toggle="letterdropdown" :class="[license.letter.error ? 'bg-red-50 border border-red-500 text-red-900 placeholder-red-700 text-sm rounded-lg focus:ring-red-500 dark:bg-gray-700 focus:border-red-500 dark:text-red-500 dark:placeholder-red-500 dark:border-red-500' : 'text-gray-900 bg-white border border-gray-300 rounded-lg focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500']" class="block w-9 h-9 text-sm font-extrabold rounded-lg" type="button">
                {{ license.letter.val }}
              </button>
              <!-- Dropdown menu -->
              <div id="letterdropdown" class="z-50 hidden bg-white divide-y divide-gray-100 rounded-lg shadow w-14 dark:bg-gray-700">
                <ul class="overflow-y-auto h-auto max-h-48 py-2 text-sm text-gray-700 dark:text-gray-200" aria-labelledby="letterButtonButton">
                  <li v-for="l in license.letter.alphabets">
                    <a @click="selectLetter(l)" type="button" class="block text-center px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">
                      {{ l }}
                    </a>
                  </li>
                </ul>
              </div>
              <div>
                <label for="code-4" class="sr-only">Fourth code</label>
                <input v-model="license.first.val" :placeholder="license.first.val" type="text" maxlength="2" data-focus-input-init data-focus-input-prev="code-3" data-focus-input-next="code-5" id="code-4" :class="[license.first.error ? 'bg-red-50 border border-red-500 text-red-900 placeholder-red-700 text-sm rounded-lg focus:ring-red-500 dark:bg-gray-700 focus:border-red-500 dark:text-red-500 dark:placeholder-red-500 dark:border-red-500' : 'text-gray-900 bg-white border border-gray-300 rounded-lg focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500']" class="block w-12 h-9 py-3 text-sm font-extrabold text-center" required />
              </div>
            </div>
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
import { ref, reactive, watch, onMounted } from 'vue'
import { useQuery } from '@vue/apollo-composable'
import gql from 'graphql-tag'
import { initFlowbite } from 'flowbite'

const FILTER_QUERY = gql`
  query FilterData($filterInput: FilterInput) {
    filteredData(filterInput: $filterInput) {
      ... on TruckType {
        id
        licenseNumber
        driverName
        status
        location
        phone
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

    // Reactive state for license plate input
    const license = reactive({
      first: {val: '', error: false},
      letter: {val: '', error: false, alphabets:['الف', 'ب', 'پ', 'ت', 'ث', 'ج', 'چ', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'ژ', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ک', 'گ', 'ل', 'م', 'ن', 'و', 'ه', 'ی']},
      second: {val: '', error: false},
      year: {val: '', error: false},
    })

    onMounted(() => {
      initFlowbite();
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
      } else {
        results.value = []
      }
    })

    const selectLetter = (l) => {
        license.letter.val = l;
    }

    const applyFilters = async () => {
      try {
        // Construct the full license number string, handling empty inputs
        const firstPart = license.first.val || '';
        const letterPart = license.letter.val || '';
        const secondPart = license.second.val || '';
        const yearPart = license.year.val || '';

        const fullLicenseNumber = `${firstPart}${letterPart}${secondPart}ایران${yearPart}`;

        // Only apply filter if license number parts are entered
        if (firstPart || letterPart || secondPart || yearPart) {
             filters.truckLicenseNumber = fullLicenseNumber;
        } else {
             filters.truckLicenseNumber = ''; // Clear filter if no parts entered
        }

        await refetch();
      } catch (err) {
        console.error('Error applying filters:', err);
      }
    }

    const getItemType = (item) => {
      if (item.__typename === 'TruckType') return 'کامیون'
      if (item.__typename === 'CustomerType') return 'مشتری'
      if (item.__typename === 'ShipmentType') return 'ارسال'
      if (item.__typename === 'SalesType') return 'فاکتور فروش'
      if (item.__typename === 'ProductType') return 'محصول'
      return 'نامشخص'
    }

    const getItemInfo = (item) => {
      if (item.__typename === 'TruckType') {
        return `پلاک: ${item.licenseNumber || 'نامشخص'}, راننده: ${item.driverName || 'نامشخص'}, وضعیت: ${item.status || 'نامشخص'}, مکان: ${item.location || 'نامشخص'}, تلفن: ${item.phone || 'نامشخص'}`
      }
      if (item.__typename === 'CustomerType') {
        return `مشتری: ${item.customerName || 'نامشخص'} (کد ملی: ${item.nationalId || 'نامشخص'})`
      }
      if (item.__typename === 'ShipmentType') {
        return `نوع ارسال: ${item.shipmentType || 'نامشخص'}`
      }
      if (item.__typename === 'SalesType') {
        return `مبلغ کل: ${item.totalPrice || 'نامشخص'} تومان`
      }
      if (item.__typename === 'ProductType') {
        return `محصول: ${item.profileName || 'نامشخص'}`
      }
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
      license,
      selectLetter,
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

/* Remove default input styles */
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

/* Ensure inputs are editable */
input:focus {
  @apply outline-none ring-0;
}

/* Dropdown styles */
#letterdropdown {
  @apply z-50 bg-white divide-y divide-gray-100 rounded-lg shadow w-14;
}

#letterdropdown ul {
  @apply overflow-y-auto h-auto max-h-48 py-2 text-sm text-gray-700;
}

#letterdropdown li a {
  @apply block text-center px-4 py-2 hover:bg-gray-100 cursor-pointer;
}
</style> 