<script>
import { initFlowbite } from 'flowbite'
import Card from '../Card'
import Alert from "@/components/Alert.vue";
import Lic_numer from "@/components/lic_numer.vue";
import Input from "@/components/custom/Input.vue";
import Dropdown from "@/components/custom/Dropdown.vue";

export default {
  name: "Filter",
  components: {
    Dropdown,
    Input,
    Lic_numer,
    Card,
    Alert
  },
  mounted() {
    initFlowbite();
  },
  data() {
    return {
      // License plate components
      first: { val: '', error: false },
      letter: { 
        val: '', 
        error: false, 
        alphabets: ['الف', 'ب', 'پ', 'ت', 'ث', 'ج', 'چ', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'ژ', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ک', 'گ', 'ل', 'م', 'ن', 'و', 'ه', 'ی']
      },
      second: { val: '', error: false },
      year: { val: '', error: false },
      
      // Search filters
      filters: {
        driver_name: { type: 'input', name: 'نام راننده', title: 'راننده', value: '' },
        customer_name: { type: 'input', name: 'نام مشتری', title: 'مشتری', value: '' },
        customer_national_id: { type: 'input', name: 'کد ملی', title: 'کد ملی', value: '', label: 'number' },
        start_date: { type: 'input', name: 'تاریخ شروع', title: 'تاریخ شروع', value: '', label: 'date' },
        end_date: { type: 'input', name: 'تاریخ پایان', title: 'تاریخ پایان', value: '', label: 'date' },
      },

      // Results
      searchResults: [],
      error: false,
      errors: [],
      loading: false,
    }
  },
  methods: {
    clicked(k, name) {
      if (k == 'letter') {
        this.letter.val = name
      }
    },
    async search() {
      this.loading = true
      this.error = false
      this.errors = []
      this.searchResults = []

      // Validate license plate if any part is filled
      if (this.first.val || this.letter.val || this.second.val || this.year.val) {
        if (!this.first.val || !this.letter.val || !this.second.val || !this.year.val) {
          this.error = true
          this.errors.push({ message: 'لطفا تمام قسمت‌های پلاک را وارد کنید' })
          this.loading = false
          return
        }
      }

      try {
        const filterInput = {
          truckLicenseNumber: this.first.val + this.letter.val + this.second.val + "ایران" + this.year.val,
          driverName: this.filters.driver_name.value,
          customerName: this.filters.customer_name.value,
          customerNationalId: this.filters.customer_national_id.value,
          startDate: this.filters.start_date.value,
          endDate: this.filters.end_date.value,
        }

        const response = await this.axios.post('/filter/api/', {
          query: `
            query FilterData($filterInput: FilterInput) {
              filteredData(filterInput: $filterInput) {
                ... on TruckType {
                  id
                  license_number
                  driver_name
                  driver_doc
                  phone
                  username
                }
                ... on CustomerType {
                  id
                  customer_name
                  national_id
                }
                ... on SalesType {
                  id
                  total_price
                }
              }
            }
          `,
          variables: { filterInput }
        })

        this.searchResults = response.data.data.filteredData
      } catch (error) {
        this.error = true
        this.errors.push({ message: 'خطا در دریافت اطلاعات' })
        console.error('Search error:', error)
      }

      this.loading = false
    },
    viewDetails(item) {
      // Navigate to details page based on item type
      if (item.__typename === 'TruckType') {
        this.$router.push({ name: 'truckDetails', params: { id: item.id } })
      } else if (item.__typename === 'CustomerType') {
        this.$router.push({ name: 'customerDetails', params: { id: item.id } })
      } else if (item.__typename === 'SalesType') {
        this.$router.push({ name: 'saleDetails', params: { id: item.id } })
      }
    }
  },
  watch: {
    "first.val"(c, p) {
      if (Number.isInteger(parseInt(c))) {
        this.first.val = parseInt(c)
        if (this.first.error) {
          this.first.error = false
        }
      } else {
        this.first.val = parseInt(p)
        this.first.error = true
      }
    },
    "second.val"(c, p) {
      if (Number.isInteger(parseInt(c))) {
        this.second.val = parseInt(c)
        if (this.second.error) {
          this.second.error = false
        }
      } else {
        this.second.val = parseInt(p)
        this.second.error = true
      }
    },
    "year.val"(c, p) {
      if (Number.isInteger(parseInt(c))) {
        this.year.val = parseInt(c)
        if (this.year.error) {
          this.year.error = false
        }
      } else {
        this.year.val = parseInt(c)
        this.year.error = true
      }
    }
  }
}
</script>

<template>
  <Card title="جستجو">
    <!-- License plate search -->
    <div class="flex flex-row justify-center">
      <div class="rounded-lg bg-white shadow-lg max-w-sm">
        <div class="flex rounded-lg border-4 border-black shadow">
          <label class="flex flex-none flex-col items-center px-2 justify-center sm:justify-start sm:px-4 border-e-4 border-black font-bold">
            ایران
            <p class="place-self-center sm:text-4xl">{{ year.val }}</p>
          </label>
          <label class="flex-grow flex flex-row px-2 gap-2 sm:gap-4 justify-center items-center sm:p-4 font-mono text-4xl sm:text-5xl font-bold">
            <h>{{ second.val }}</h>
            <h>{{ letter.val }}</h>
            <h>{{ first.val }}</h>
          </label>
          <label class="flex flex-none flex-col items-end justify-between px-1 py-1 bg-blue-700 border-s-4 border-black font-bold sm:text-sm text-white">
            <img src="@/assets/Flag_of_Iran.svg.png" class="h-5">
            <span class="flex flex-col items-end">
              <h>IR</h>
              <h>IRAN</h>
            </span>
          </label>
        </div>
      </div>
    </div>

    <!-- License plate form -->
    <div class="flex flex-col items-center mt-5 gap-4">
      <div class="flex space-x-2 rtl:space-x-reverse">
        <div>
          <label for="code-1" class="sr-only">First code</label>
          <input v-model="year.val" placeholder="سال" type="text" maxlength="2" id="code-1" :class="[year.error ? 'appearance-none bg-red-50 border border-red-500 text-red-900 placeholder-red-700 text-sm rounded-lg focus:ring-red-500 dark:bg-gray-700 focus:border-red-500 dark:text-red-500 dark:placeholder-red-500 dark:border-red-500' : 'text-gray-900 bg-white border border-gray-300 rounded-lg focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500']" class="block w-12 h-9 py-3 text-sm font-extrabold text-center" />
        </div>
        <div>
          <label for="code-3" class="sr-only">Third code</label>
          <input v-model="second.val" placeholder="شماره" type="text" maxlength="3" id="code-3" :class="[second.error ? 'bg-red-50 border border-red-500 text-red-900 placeholder-red-700 text-sm rounded-lg focus:ring-red-500 dark:bg-gray-700 focus:border-red-500 dark:text-red-500 dark:placeholder-red-500 dark:border-red-500' : 'text-gray-900 bg-white border border-gray-300 rounded-lg focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500']" class="block w-14 h-9 py-3 text-sm font-extrabold text-center" />
        </div>
        <button id="letterButton" data-dropdown-toggle="letterdropdown" :class="[letter.error ? 'bg-red-50 border border-red-500 text-red-900 placeholder-red-700 text-sm rounded-lg focus:ring-red-500 dark:bg-gray-700 focus:border-red-500 dark:text-red-500 dark:placeholder-red-500 dark:border-red-500' : 'text-gray-900 bg-white border border-gray-300 rounded-lg focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500']" class="block w-9 h-9 text-sm font-extrabold rounded-lg" type="button">
          {{ letter.val || 'حرف' }}
        </button>
        <!-- Dropdown menu -->
        <div id="letterdropdown" class="z-50 hidden bg-white divide-y divide-gray-100 rounded-lg shadow w-14 dark:bg-gray-700">
          <ul class="overflow-y-auto h-auto max-h-48 py-2 text-sm text-gray-700 dark:text-gray-200" aria-labelledby="letterButtonButton">
            <li v-for="l in letter.alphabets">
              <a @click="clicked('letter', l)" type="button" class="block text-center px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">
                {{ l }}
              </a>
            </li>
          </ul>
        </div>
        <div>
          <label for="code-4" class="sr-only">Fourth code</label>
          <input v-model="first.val" placeholder="شماره" type="text" maxlength="2" id="code-4" :class="[first.error ? 'bg-red-50 border border-red-500 text-red-900 placeholder-red-700 text-sm rounded-lg focus:ring-red-500 dark:bg-gray-700 focus:border-red-500 dark:text-red-500 dark:placeholder-red-500 dark:border-red-500' : 'text-gray-900 bg-white border border-gray-300 rounded-lg focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500']" class="block w-12 h-9 py-3 text-sm font-extrabold text-center" />
        </div>
      </div>

      <!-- Additional filters -->
      <div class="w-full max-w-md space-y-4">
        <template v-for="(val, form_name) in filters">
          <Input
            :key="form_name"
            :formName="form_name"
            :label="val.name"
            :type="val.label"
            @update="val.value = $event"
          />
        </template>
      </div>

      <!-- Error alert -->
      <div v-if="error" class="w-full max-w-md">
        <Alert type="error" :messages="errors" />
      </div>

      <!-- Search button -->
      <button 
        @click="search" 
        :disabled="loading"
        class="w-44 block text-white bg-green-500 hover:bg-green-600 focus:ring-4 focus:outline-none focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
        type="button"
      >
        {{ loading ? 'در حال جستجو...' : 'جستجو' }}
      </button>

      <!-- Results -->
      <div v-if="searchResults.length > 0" class="w-full max-w-4xl mt-8">
        <h3 class="text-lg font-semibold mb-4">نتایج جستجو</h3>
        <div class="grid gap-4">
          <div v-for="item in searchResults" :key="item.id" class="bg-white p-4 rounded-lg shadow">
            <div class="flex justify-between items-center">
              <div>
                <template v-if="item.__typename === 'TruckType'">
                  <p class="font-semibold">کامیون</p>
                  <p>پلاک: {{ item.license_number }}</p>
                  <p>راننده: {{ item.driver_name }}</p>
                </template>
                <template v-else-if="item.__typename === 'CustomerType'">
                  <p class="font-semibold">مشتری</p>
                  <p>نام: {{ item.customer_name }}</p>
                  <p>کد ملی: {{ item.national_id }}</p>
                </template>
                <template v-else-if="item.__typename === 'SalesType'">
                  <p class="font-semibold">فروش</p>
                  <p>مبلغ کل: {{ item.total_price }}</p>
                </template>
              </div>
              <button
                @click="viewDetails(item)"
                class="text-white bg-blue-500 hover:bg-blue-600 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2 text-center"
              >
                مشاهده جزئیات
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Card>
</template> 