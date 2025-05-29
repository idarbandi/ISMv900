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
        <label class="block text-sm font-medium text-gray-700">تاریخ شروع</label>
        <input 
          type="date" 
          v-model="filters.startDate"
          :class="[
            'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
            fieldErrors.startDate ? 'border-red-500' : ''
          ]"
        >
        <p v-if="fieldErrors.startDate" class="mt-1 text-sm text-red-600">{{ fieldErrors.startDate }}</p>
      </div>
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">تاریخ پایان</label>
        <input 
          type="date" 
          v-model="filters.endDate"
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
        <select 
          v-model="filters.productWidth"
          :class="[
            'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
            fieldErrors.productWidth ? 'border-red-500' : ''
          ]"
        >
          <option value="">انتخاب کنید</option>
          <option value="210">2/10</option>
          <option value="220">2/20</option>
          <option value="230">2/30</option>
          <option value="240">2/40</option>
          <option value="250">2/50</option>
        </select>
        <p v-if="fieldErrors.productWidth" class="mt-1 text-sm text-red-600">{{ fieldErrors.productWidth }}</p>
      </div>
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">GSM</label>
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
        <input 
          type="text" 
          v-model="filters.productLocation"
          :class="[
            'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
            fieldErrors.productLocation ? 'border-red-500' : ''
          ]"
        >
        <p v-if="fieldErrors.productLocation" class="mt-1 text-sm text-red-600">{{ fieldErrors.productLocation }}</p>
      </div>

      <!-- Grade and Breaks -->
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">گرید</label>
        <input 
          type="text" 
          v-model="filters.productGrade"
          :class="[
            'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
            fieldErrors.productGrade ? 'border-red-500' : ''
          ]"
        >
        <p v-if="fieldErrors.productGrade" class="mt-1 text-sm text-red-600">{{ fieldErrors.productGrade }}</p>
      </div>
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">شکستگی</label>
        <input 
          type="number" 
          v-model="filters.productBreaks"
          :class="[
            'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
            fieldErrors.productBreaks ? 'border-red-500' : ''
          ]"
          placeholder="تعداد شکستگی"
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
        productWidth: '',
        productGsm: '',
        productGrade: '',
        productStatus: '',
        productLocation: '',
        productProfileName: '',
        productBreaks: '',
      },
      loading: false,
      error: null,
      fieldErrors: {},
      products: [],
      filteredProducts: []
    }
  },
  async created() {
    await this.loadProducts()
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
            query GetAllProducts {
              products {
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
          `
        })
        this.products = data.products.map(product => ({
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
        productWidth: '',
        productGsm: '',
        productGrade: '',
        productStatus: '',
        productLocation: '',
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
          if (cleanFilters.productWidth && product.width !== Number(cleanFilters.productWidth)) return false
          if (cleanFilters.productGsm && product.gsm !== Number(cleanFilters.productGsm)) return false
          if (cleanFilters.productGrade && product.grade !== cleanFilters.productGrade) return false
          if (cleanFilters.productStatus && product.status !== cleanFilters.productStatus) return false
          if (cleanFilters.productLocation && !product.location.includes(cleanFilters.productLocation)) return false
          if (cleanFilters.productProfileName && !product.profileName.includes(cleanFilters.productProfileName)) return false
          if (cleanFilters.productBreaks && product.breaks !== Number(cleanFilters.productBreaks)) return false

          if (cleanFilters.startDate) {
            const startDate = new Date(cleanFilters.startDate)
            const productDate = new Date(product.receiveDate)
            if (productDate < startDate) return false
          }
          if (cleanFilters.endDate) {
            const endDate = new Date(cleanFilters.endDate)
            const productDate = new Date(product.receiveDate)
            if (productDate > endDate) return false
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
    }
  }
}
</script>
