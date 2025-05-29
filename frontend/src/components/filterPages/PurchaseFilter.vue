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

      <!-- Vehicle and Customer -->
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">شماره پلاک</label>
        <input 
          type="text" 
          v-model="filters.licenseNumber"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
      </div>
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">نام مشتری</label>
        <input 
          type="text" 
          v-model="filters.customerName"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
      </div>

      <!-- Supplier and Material -->
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">نام تامین کننده</label>
        <input 
          type="text" 
          v-model="filters.supplierName"
          :class="[
            'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
            fieldErrors.supplierName ? 'border-red-500' : ''
          ]"
        >
        <p v-if="fieldErrors.supplierName" class="mt-1 text-sm text-red-600">{{ fieldErrors.supplierName }}</p>
      </div>
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">نوع مواد</label>
        <input 
          type="text" 
          v-model="filters.materialType"
          :class="[
            'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
            fieldErrors.materialType ? 'border-red-500' : ''
          ]"
        >
        <p v-if="fieldErrors.materialType" class="mt-1 text-sm text-red-600">{{ fieldErrors.materialType }}</p>
      </div>
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">نام مواد</label>
        <input 
          type="text" 
          v-model="filters.materialName"
          :class="[
            'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
            fieldErrors.materialName ? 'border-red-500' : ''
          ]"
        >
        <p v-if="fieldErrors.materialName" class="mt-1 text-sm text-red-600">{{ fieldErrors.materialName }}</p>
      </div>

      <!-- Price -->
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">قیمت هر کیلو</label>
        <input 
          type="number" 
          v-model="filters.pricePerKg"
          :class="[
            'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
            fieldErrors.pricePerKg ? 'border-red-500' : ''
          ]"
        >
        <p v-if="fieldErrors.pricePerKg" class="mt-1 text-sm text-red-600">{{ fieldErrors.pricePerKg }}</p>
      </div>

      <!-- Status -->
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">وضعیت پرداخت</label>
        <select 
          v-model="filters.status"
          :class="[
            'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
            fieldErrors.status ? 'border-red-500' : ''
          ]"
        >
          <option value="">همه</option>
          <option value="Paid">پرداخت شده</option>
          <option value="Terms">نسیه</option>
          <option value="Cancelled">لغو شده</option>
        </select>
        <p v-if="fieldErrors.status" class="mt-1 text-sm text-red-600">{{ fieldErrors.status }}</p>
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
import { validateForm, cleanFormData, handleEmptyResponse } from './filterValidate'
import { getTranslationOptions } from '@/config/translations'

export default {
  name: 'PurchaseFilter',
  data() {
    return {
      filters: {
        startDate: '',
        endDate: '',
        status: '',
        pricePerKg: '',
        supplierName: '',
        materialType: '',
        materialName: '',
        invoiceStatus: '',
        licenseNumber: '',
        invoiceNumber: '',
        documentInfo: '',
        comments: '',
        cancellationReason: ''
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
        invoiceStatus: {
          'NA': 'بدون فاکتور',
          'SENT': 'ارسال شده',
          'RECEIVED': 'دریافت شده'
        },
        paymentStatus: {
          'Terms': 'نسیه',
          'Paid': 'پرداخت شده',
          'Cancelled': 'لغو شده'
        }
      }

      const upperValue = value?.toUpperCase()
      const translationMap = translations[type] || {}
      const translatedValue = Object.entries(translationMap).find(([key]) => 
        key.toUpperCase() === upperValue
      )?.[1]

      return translatedValue || value
    },
    getStatusValue(persianStatus) {
      const statusMap = {
        'پرداخت شده': 'Paid',
        'نسیه': 'Terms',
        'لغو شده': 'Cancelled'
      }
      return statusMap[persianStatus] || persianStatus
    },
    async loadPurchases() {
      this.loading = true
      try {
        const { data } = await apolloClient.query({
          query: gql`
            query GetTermsPurchases {
              filteredPurchases(filterInput: { 
                status: "${this.filters.status || 'Paid'}"
              }) {
                id
                date
                status
                receiveDate
                paymentDate
                licenseNumber
                materialType
                materialName
                supplierName
                unit
                quantity
                quality
                penalty
                weight1
                weight2
                pricePerKg
                vat
                totalPrice
                extraCost
                invoiceStatus
                paymentDetails
                invoiceNumber
                documentInfo
                comments
                cancellationReason
                username
                logs
              }
            }
          `
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
            invoiceStatus: this.translateValue(purchase.invoiceStatus, 'invoiceStatus'),
            paymentStatus: this.translateValue(purchase.paymentStatus, 'paymentStatus')
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
        pricePerKg: '',
        supplierName: '',
        materialType: '',
        materialName: '',
        invoiceStatus: '',
        licenseNumber: '',
        invoiceNumber: '',
        documentInfo: '',
        comments: '',
        cancellationReason: ''
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
            query GetTermsPurchases {
              filteredPurchases(filterInput: { 
                status: "${cleanFilters.status || 'Paid'}"
              }) {
                id
                date
                status
                receiveDate
                paymentDate
                licenseNumber
                materialType
                materialName
                supplierName
                unit
                quantity
                quality
                penalty
                weight1
                weight2
                pricePerKg
                vat
                totalPrice
                extraCost
                invoiceStatus
                paymentDetails
                invoiceNumber
                documentInfo
                comments
                cancellationReason
                username
                logs
              }
            }
          `
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
            const purchaseDate = new Date(purchase.date)
            return purchaseDate >= startDate && purchaseDate <= endDate
          })
          .map(purchase => ({
            ...purchase,
            invoiceStatus: this.translateValue(purchase.invoiceStatus, 'invoiceStatus'),
            paymentStatus: this.translateValue(purchase.paymentStatus, 'paymentStatus')
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