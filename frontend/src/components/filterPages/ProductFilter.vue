<template>
  <div class="bg-white rounded-lg shadow-md p-6">
    <h2 class="text-2xl font-semibold mb-6">فیلتر محصولات</h2>
    
    <!-- Error Message -->
    <div v-if="error" class="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
      {{ error }}
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="mb-4 p-4 bg-blue-100 border border-blue-400 text-blue-700 rounded">
      Loading...
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <!-- Date Range -->
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">تاریخ شروع <span class="text-red-500">*</span></label>
        <input 
          type="date" 
          v-model="filters.startDate"
          required
          :class="[
            'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
            fieldErrors.startDate ? 'border-red-500' : ''
          ]"
        >
        <p v-if="fieldErrors.startDate" class="mt-1 text-sm text-red-600">{{ fieldErrors.startDate }}</p>
      </div>
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">تاریخ پایان <span class="text-red-500">*</span></label>
        <input 
          type="date" 
          v-model="filters.endDate"
          required
          :class="[
            'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
            fieldErrors.endDate ? 'border-red-500' : ''
          ]"
        >
        <p v-if="fieldErrors.endDate" class="mt-1 text-sm text-red-600">{{ fieldErrors.endDate }}</p>
      </div>

      <!-- Basic Information -->
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">شماره رول</label>
        <input 
          type="text" 
          v-model="filters.productReelNumber"
          :class="[
            'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
            fieldErrors.productReelNumber ? 'border-red-500' : ''
          ]"
        >
        <p v-if="fieldErrors.productReelNumber" class="mt-1 text-sm text-red-600">{{ fieldErrors.productReelNumber }}</p>
      </div>
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">نام پروفایل</label>
        <input 
          type="text" 
          v-model="filters.productProfileName"
          :class="[
            'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
            fieldErrors.productProfileName ? 'border-red-500' : ''
          ]"
        >
        <p v-if="fieldErrors.productProfileName" class="mt-1 text-sm text-red-600">{{ fieldErrors.productProfileName }}</p>
      </div>

      <!-- Measurements -->
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">عرض</label>
        <div class="mt-1 relative width-dropdown">
          <div 
            @click="toggleWidthDropdown"
            class="relative w-full cursor-pointer rounded-md border border-gray-300 bg-white py-2 pl-3 pr-10 text-left shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
          >
            <span class="block truncate">
              {{ selectedWidths.length ? selectedWidths.join(', ') : 'انتخاب کنید' }}
            </span>
            <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
              <svg class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 3a1 1 0 01.707.293l3 3a1 1 0 01-1.414 1.414L10 5.414 7.707 7.707a1 1 0 01-1.414-1.414l3-3A1 1 0 0110 3zm-3.707 9.293a1 1 0 011.414 0L10 14.586l2.293-2.293a1 1 0 011.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            </span>
          </div>
          <div v-if="isWidthDropdownOpen" class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
            <div class="px-2 py-1">
              <div v-for="option in widthOptions" :key="option.value" class="flex items-center">
                <input
                  type="checkbox"
                  :id="'width-' + option.value"
                  :value="option.value"
                  v-model="filters.productWidth"
                  class="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  @click.stop
                >
                <label :for="'width-' + option.value" class="mr-2 block cursor-pointer py-2 text-sm text-gray-900">
                  {{ option.label }}
                </label>
              </div>
            </div>
          </div>
        </div>
        <p v-if="fieldErrors.productWidth" class="mt-1 text-sm text-red-600">{{ fieldErrors.productWidth }}</p>
      </div>
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">طول</label>
        <input 
          type="number" 
          v-model="filters.productLength"
          :class="[
            'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
            fieldErrors.productLength ? 'border-red-500' : ''
          ]"
        >
        <p v-if="fieldErrors.productLength" class="mt-1 text-sm text-red-600">{{ fieldErrors.productLength }}</p>
      </div>
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">گرماژ</label>
        <input 
          type="number" 
          v-model="filters.productGsm"
          :class="[
            'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
            fieldErrors.productGsm ? 'border-red-500' : ''
          ]"
        >
        <p v-if="fieldErrors.productGsm" class="mt-1 text-sm text-red-600">{{ fieldErrors.productGsm }}</p>
      </div>

      <!-- Status and Location -->
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">وضعیت</label>
        <select 
          v-model="filters.productStatus"
          :class="[
            'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
            fieldErrors.productStatus ? 'border-red-500' : ''
          ]"
        >
          <option value="">همه</option>
          <option value="IN_STOCK">موجود</option>
          <option value="SOLD">فروخته شده</option>
          <option value="MOVED">انتقال یافته</option>
          <option value="DELIVERED">تحویل داده شده</option>
        </select>
        <p v-if="fieldErrors.productStatus" class="mt-1 text-sm text-red-600">{{ fieldErrors.productStatus }}</p>
      </div>
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">موقعیت</label>
        <div class="mt-1 relative location-dropdown">
          <div 
            @click="toggleLocationDropdown"
            class="relative w-full cursor-pointer rounded-md border border-gray-300 bg-white py-2 pl-3 pr-10 text-left shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
          >
            <span class="block truncate">
              {{ selectedLocations.length ? selectedLocations.join(', ') : 'انتخاب کنید' }}
            </span>
            <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
              <svg class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 3a1 1 0 01.707.293l3 3a1 1 0 01-1.414 1.414L10 5.414 7.707 7.707a1 1 0 01-1.414-1.414l3-3A1 1 0 0110 3zm-3.707 9.293a1 1 0 011.414 0L10 14.586l2.293-2.293a1 1 0 011.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            </span>
          </div>
          <div v-if="isLocationDropdownOpen" class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
            <div class="px-2 py-1">
              <div v-for="option in locationOptions" :key="option.value" class="flex items-center">
                <input
                  type="checkbox"
                  :id="'location-' + option.value"
                  :value="option.value"
                  v-model="filters.productLocation"
                  class="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  @click.stop
                >
                <label :for="'location-' + option.value" class="mr-2 block cursor-pointer py-2 text-sm text-gray-900">
                  {{ option.label }}
                </label>
              </div>
            </div>
          </div>
        </div>
        <p v-if="fieldErrors.productLocation" class="mt-1 text-sm text-red-600">{{ fieldErrors.productLocation }}</p>
      </div>

      <!-- Breaks -->
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">پارگی</label>
        <input 
          type="number" 
          v-model="filters.productBreaks"
          :class="[
            'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
            fieldErrors.productBreaks ? 'border-red-500' : ''
          ]"
          placeholder="میزان پارگی"
        >
        <p v-if="fieldErrors.productBreaks" class="mt-1 text-sm text-red-600">{{ fieldErrors.productBreaks }}</p>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="mt-6 flex justify-end space-x-4">
      <button 
        @click="resetFilters"
        class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        :disabled="loading"
      >
        پاک کردن
      </button>
      <button 
        @click="applyFilters"
        class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        :disabled="loading"
      >
        {{ loading ? 'در حال بارگذاری...' : 'اعمال فیلتر' }}
      </button>
    </div>
  </div>
</template>

<script>
import { validateForm, cleanFormData } from './filterValidate'
import { gql } from '@apollo/client/core'
import { apolloClient } from '@/apollo'

export default {
  name: 'ProductFilter',
  data() {
    return {
      filters: {
        startDate: '',
        endDate: '',
        productReelNumber: '',
        productWidth: [],
        productLength: '',
        productGsm: '',
        productStatus: '',
        productLocation: [],
        productProfileName: '',
        productBreaks: '',
      },
      loading: false,
      error: null,
      fieldErrors: {},
      products: [],
      filteredProducts: [],
      widthOptions: [
        { value: '210', label: '2/10' },
        { value: '220', label: '2/20' },
        { value: '230', label: '2/30' },
        { value: '240', label: '2/40' },
        { value: '250', label: '2/50' }
      ],
      isWidthDropdownOpen: false,
      locationOptions: [
        { value: 'Anbar_Salon_Tolid', label: 'انبار سالن تولید' },
        { value: 'Anbar_Sangin', label: 'انبار سنگین' },
        { value: 'Anbar_Koochak', label: 'انبار کوچک' },
        { value: 'Anbar_Khamir_Ghadim', label: 'انبار خمیر قدیم' },
        { value: 'Anbar_Khamir_Kordan', label: 'انبار خمیر کردن' },
        { value: 'Anbar_Muhvateh_Kardan', label: 'انبار محوطه کردن' },
        { value: 'Anbar_Akhal', label: 'انبار اخل' }
      ],
      isLocationDropdownOpen: false
    }
  },
  async created() {
    await this.loadProducts()
  },
  computed: {
    selectedWidths() {
      return this.filters.productWidth.map(width => {
        const option = this.widthOptions.find(opt => opt.value === width)
        return option ? option.label : width
      })
    },
    selectedLocations() {
      return this.filters.productLocation.map(location => {
        const option = this.locationOptions.find(opt => opt.value === location)
        return option ? option.label : location
      })
    }
  },
  methods: {
    translateStatus(status) {
      const statusMap = {
        'IN_STOCK': 'موجود',
        'SOLD': 'فروخته شده',
        'MOVED': 'انتقال یافته',
        'DELIVERED': 'تحویل داده شده'
      }
      return statusMap[status] || status
    },
    async loadProducts() {
      this.loading = true
      try {
        const { data } = await apolloClient.query({
          query: gql`
            query GetAllProducts($filterInput: FilterInput) {
              filteredData(filterInput: $filterInput) {
                ... on ProductType {
                  id
                  reelNumber
                  width
                  gsm
                  length
                  grade
                  status
                  location
                  profileName
                  breaks
                  receiveDate
                  lastDate
                  comments
                  qrCode
                }
              }
            }
          `,
          variables: {
            filterInput: {
              productLocation: this.filters.productLocation
            }
          }
        })
        this.products = data.filteredData.map(product => ({
          ...product,
          status: this.translateStatus(product.status)
        }))
        this.filteredProducts = this.products
        this.$emit('filter-applied', this.products)
      } catch (err) {
        this.error = 'خطا در بارگذاری محصولات'
        console.error('Error loading products:', err)
      } finally {
        this.loading = false
      }
    },
    resetFilters() {
      this.filters = {
        startDate: '',
        endDate: '',
        productReelNumber: '',
        productWidth: [],
        productLength: '',
        productGsm: '',
        productStatus: '',
        productLocation: [],
        productProfileName: '',
        productBreaks: '',
      }
      this.fieldErrors = {}
      this.error = null
      this.filteredProducts = this.products
      this.$emit('filter-reset', this.products)
    },
    async applyFilters() {
      this.loading = true
      this.error = null
      this.fieldErrors = {}
      
      try {
        // Validate dates first
        if (!this.filters.startDate) {
          this.fieldErrors.startDate = 'تاریخ شروع الزامی است'
          this.error = 'لطفا تاریخ شروع را وارد کنید'
          return
        }
        if (!this.filters.endDate) {
          this.fieldErrors.endDate = 'تاریخ پایان الزامی است'
          this.error = 'لطفا تاریخ پایان را وارد کنید'
          return
        }

        const startDate = new Date(this.filters.startDate)
        const endDate = new Date(this.filters.endDate)

        if (startDate > endDate) {
          this.fieldErrors.endDate = 'تاریخ پایان باید بعد از تاریخ شروع باشد'
          this.error = 'تاریخ پایان باید بعد از تاریخ شروع باشد'
          return
        }

        // Custom validation for width array
        if (this.filters.productWidth && this.filters.productWidth.length > 0) {
          const invalidWidths = this.filters.productWidth.filter(width => !['210', '220', '230', '240', '250'].includes(width))
          if (invalidWidths.length > 0) {
            this.fieldErrors.productWidth = 'عرض انتخاب شده نامعتبر است'
            this.error = 'لطفا خطاهای فرم را برطرف کنید'
            return
          }
        }

        const { isValid, errors } = validateForm(this.filters, 'product')
        
        if (!isValid) {
          this.fieldErrors = errors
          this.error = 'لطفا خطاهای فرم را برطرف کنید'
          return
        }

        const cleanFilters = cleanFormData(this.filters)
        
        this.filteredProducts = this.products.filter(product => {
          if (Object.keys(cleanFilters).length === 0) return true

          if (cleanFilters.productReelNumber && !product.reelNumber.includes(cleanFilters.productReelNumber)) return false
          if (cleanFilters.productWidth && cleanFilters.productWidth.length > 0) {
            const productWidth = String(product.width)
            if (!cleanFilters.productWidth.includes(productWidth)) return false
          }
          if (cleanFilters.productLength && product.length !== Number(cleanFilters.productLength)) return false
          if (cleanFilters.productGsm && product.gsm !== Number(cleanFilters.productGsm)) return false
          if (cleanFilters.productStatus && product.status !== cleanFilters.productStatus) return false
          if (cleanFilters.productLocation && cleanFilters.productLocation.length > 0) {
            if (!product.location || !cleanFilters.productLocation.includes(product.location)) return false
          }
          if (cleanFilters.productProfileName && !product.profileName.includes(cleanFilters.productProfileName)) return false
          if (cleanFilters.productBreaks && product.breaks !== Number(cleanFilters.productBreaks)) return false

          if (cleanFilters.startDate || cleanFilters.endDate) {
            const productDate = new Date(product.receiveDate)
            if (cleanFilters.startDate) {
              if (productDate < startDate) return false
            }
            if (cleanFilters.endDate) {
              if (productDate > endDate) return false
            }
          }

          return true
        })

        this.$emit('filter-applied', this.filteredProducts)
      } catch (err) {
        this.error = err.message
        console.error('Filter error:', err)
      } finally {
        this.loading = false
      }
    },
    toggleWidthDropdown() {
      this.isWidthDropdownOpen = !this.isWidthDropdownOpen
    },
    handleClickOutside(event) {
      const dropdown = this.$el.querySelector('.width-dropdown')
      if (dropdown && !dropdown.contains(event.target)) {
        this.isWidthDropdownOpen = false
      }
    },
    toggleLocationDropdown() {
      this.isLocationDropdownOpen = !this.isLocationDropdownOpen
    },
    handleLocationClickOutside(event) {
      const dropdown = this.$el.querySelector('.location-dropdown')
      if (dropdown && !dropdown.contains(event.target)) {
        this.isLocationDropdownOpen = false
      }
    }
  },
  mounted() {
    document.addEventListener('click', this.handleClickOutside)
    document.addEventListener('click', this.handleLocationClickOutside)
  },
  beforeDestroy() {
    document.removeEventListener('click', this.handleClickOutside)
    document.removeEventListener('click', this.handleLocationClickOutside)
  }
}
</script>
