<template>
  <div class="bg-white rounded-lg shadow-md p-6">
    <h2 class="text-2xl font-semibold mb-6">فیلتر خرید</h2>
    
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

      <!-- Vehicle and Supplier -->
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">شماره پلاک</label>
        <input 
          type="text" 
          v-model="filters.licenseNumber"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
      </div>
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">نام تامین کننده</label>
        <input 
          type="text" 
          v-model="filters.supplierName"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
      </div>

      <!-- Material Information -->
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">نوع مواد</label>
        <input 
          type="text" 
          v-model="filters.materialType"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
      </div>
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">نام مواد</label>
        <input 
          type="text" 
          v-model="filters.materialName"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
      </div>

      <!-- Price -->
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">قیمت هر کیلو</label>
        <input 
          type="number" 
          v-model="filters.pricePerKg"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
      </div>

      <!-- Status -->
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">وضعیت پرداخت</label>
        <select 
          v-model="filters.status"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
          <option value="">همه</option>
          <option value="Paid">پرداخت شده</option>
          <option value="Terms">نسیه</option>
          <option value="Cancelled">لغو شده</option>
        </select>
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
        {{ loading ? 'Loading...' : 'اعمال فیلتر' }}
      </button>
    </div>
  </div>
</template>

<script>
import { gql } from '@apollo/client/core'
import { apolloClient } from '@/apollo'
import { validateForm, cleanFormData } from './filterValidate'

export default {
  name: 'PurchaseFilter',
  data() {
    return {
      filters: {
        startDate: '',
        endDate: '',
        status: '',
        licenseNumber: '',
        supplierName: '',
        materialType: '',
        materialName: '',
        pricePerKg: ''
      },
      loading: false,
      error: null,
      fieldErrors: {},
      purchases: [],
      filteredPurchases: []
    }
  },
  async created() {
    await this.loadPurchases()
  },
  methods: {
    translateValue(value, type) {
      const translations = {
        status: {
          'PAID': 'پرداخت شده',
          'TERMS': 'نسیه',
          'CANCELLED': 'لغو شده'
        }
      }

      const translationMap = translations[type] || {}
      return translationMap[value] || value
    },
    async loadPurchases() {
      this.loading = true
      try {
        const { data } = await apolloClient.query({
          query: gql`
            query FilteredPurchases($filterInput: PurchaseFilterInput) {
              filteredPurchases(filterInput: $filterInput) {
                id
                date
                status
                supplierName
                materialType
                materialName
                pricePerKg
                totalPrice
                vat
                extraCost
                documentInfo
                comments
                username
                logs
                licenseNumber
                weight1
                weight2
                receiveDate
                unit
                quantity
                quality
                penalty
                invoiceStatus
                paymentDate
                paymentDetails
              }
            }
          `,
          variables: {
            filterInput: {
              status: this.filters.status || null,
              startDate: null,
              endDate: null,
              supplierName: "",
              materialType: "",
              materialName: "",
              pricePerKg: null
            }
          }
        })
        
        if (!data?.filteredPurchases) {
          console.log('No data received')
          this.purchases = []
          this.filteredPurchases = []
          this.$emit('filter-applied', [])
          return
        }

        const validPurchases = data.filteredPurchases
          .filter(item => 
            item && 
            typeof item === 'object' && 
            Object.keys(item).length > 0 &&
            item.id
          )
          .map(purchase => ({
            ...purchase,
            status: this.translateValue(purchase.status, 'status')
          }))

        this.purchases = validPurchases
        this.filteredPurchases = validPurchases
        this.$emit('filter-applied', validPurchases)
      } catch (err) {
        this.error = 'خطا در بارگذاری خریدها'
        console.error('Error loading purchases:', err)
        this.purchases = []
        this.filteredPurchases = []
        this.$emit('filter-applied', [])
      } finally {
        this.loading = false
      }
    },
    resetFilters() {
      this.filters = {
        startDate: '',
        endDate: '',
        status: '',
        licenseNumber: '',
        supplierName: '',
        materialType: '',
        materialName: '',
        pricePerKg: ''
      }
      this.fieldErrors = {}
      this.error = null
      this.filteredPurchases = this.purchases
      this.$emit('filter-reset', this.purchases)
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

        const { isValid, errors } = validateForm(this.filters, 'purchase')
        
        if (!isValid) {
          this.fieldErrors = errors
          this.error = 'لطفا خطاهای فرم را برطرف کنید'
          return
        }

        const cleanFilters = cleanFormData(this.filters)

        const { data } = await apolloClient.query({
          query: gql`
            query FilteredPurchases($filterInput: PurchaseFilterInput) {
              filteredPurchases(filterInput: $filterInput) {
                id
                date
                status
                supplierName
                materialType
                materialName
                pricePerKg
                vat
                documentInfo
                comments
                username
                logs
                licenseNumber
                weight1
                weight2
                receiveDate
                unit
                quantity
                quality
                penalty
                invoiceStatus
                paymentDate
                paymentDetails
              }
            }
          `,
          variables: {
            filterInput: {
              status: cleanFilters.status || null,
              startDate: cleanFilters.startDate || null,
              endDate: cleanFilters.endDate || null,
              supplierName: cleanFilters.supplierName || "",
              materialType: cleanFilters.materialType || "",
              materialName: cleanFilters.materialName || "",
              pricePerKg: cleanFilters.pricePerKg ? Number(cleanFilters.pricePerKg) : null
            }
          }
        })

        if (!data?.filteredPurchases) {
          console.log('No data received')
          this.filteredPurchases = []
          this.$emit('filter-applied', [])
          return
        }

        const validPurchases = data.filteredPurchases
          .filter(item => 
            item && 
            typeof item === 'object' && 
            Object.keys(item).length > 0 &&
            item.id
          )
          .filter(purchase => {
            // Apply date filter
            const purchaseDate = new Date(purchase.date)
            const isInDateRange = purchaseDate >= startDate && purchaseDate <= endDate

            // Apply other filters if they exist
            const matchesLicense = !cleanFilters.licenseNumber || purchase.licenseNumber?.includes(cleanFilters.licenseNumber)
            const matchesSupplier = !cleanFilters.supplierName || purchase.supplierName?.includes(cleanFilters.supplierName)
            const matchesMaterialType = !cleanFilters.materialType || purchase.materialType?.includes(cleanFilters.materialType)
            const matchesMaterialName = !cleanFilters.materialName || purchase.materialName?.includes(cleanFilters.materialName)
            const matchesPrice = !cleanFilters.pricePerKg || purchase.pricePerKg === Number(cleanFilters.pricePerKg)

            return isInDateRange && matchesLicense && matchesSupplier && matchesMaterialType && matchesMaterialName && matchesPrice
          })
          .map(purchase => ({
            ...purchase,
            status: this.translateValue(purchase.status, 'status')
          }))

        this.filteredPurchases = validPurchases
        this.$emit('filter-applied', validPurchases)
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