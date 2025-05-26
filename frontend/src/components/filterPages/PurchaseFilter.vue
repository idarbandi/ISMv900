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
        <label class="block text-sm font-medium text-gray-700">تاریخ شروع</label>
        <input 
          type="date" 
          v-model="filters.startDate"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
      </div>
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">تاریخ پایان</label>
        <input 
          type="date" 
          v-model="filters.endDate"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
      </div>

      <!-- Status and Type -->
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">وضعیت</label>
        <select 
          v-model="filters.shipmentStatus"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
          <option value="">همه</option>
          <option value="Registered">ثبت شده</option>
          <option value="LoadingUnloading">در حال بارگیری/تخلیه</option>
          <option value="LoadedUnloaded">بارگیری/تخلیه شده</option>
          <option value="Office">دفتر</option>
          <option value="Delivered">تحویل داده شده</option>
          <option value="Cancelled">لغو شده</option>
        </select>
      </div>

      <!-- Location -->
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">موقعیت</label>
        <input 
          type="text" 
          v-model="filters.shipmentLocation"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
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
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
      </div>
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

      <!-- Weights -->
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">وزن اول</label>
          <input 
            type="number" 
          v-model="filters.weight1"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          >
      </div>
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">وزن دوم</label>
          <input 
            type="number" 
          v-model="filters.weight2"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          >
      </div>
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">وزن خالص</label>
          <input 
          type="text" 
          v-model="filters.netWeight"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
      </div>

      <!-- Prices -->
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">قیمت هر کیلو</label>
          <input 
            type="number" 
          v-model="filters.pricePerKg"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          >
      </div>
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">قیمت کل</label>
          <input 
            type="number" 
          v-model="filters.totalPrice"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          >
      </div>
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">هزینه اضافی</label>
          <input 
            type="number" 
          v-model="filters.extraCost"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          >
        </div>

      <!-- Status -->
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">وضعیت فاکتور</label>
        <select 
          v-model="filters.invoiceStatus"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
          <option value="">همه</option>
          <option value="NA">بدون فاکتور</option>
          <option value="Sent">ارسال شده</option>
          <option value="Received">دریافت شده</option>
        </select>
      </div>
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">وضعیت پرداخت</label>
        <select 
          v-model="filters.paymentStatus"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
          <option value="">همه</option>
          <option value="Terms">نسیه</option>
          <option value="Paid">پرداخت شده</option>
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
import { validateForm, cleanFormData, handleEmptyResponse } from './filterValidate'

export default {
  name: 'PurchaseFilter',
  data() {
    return {
      filters: {
        startDate: '',
        endDate: '',
        shipmentStatus: '',
        shipmentType: '',
        shipmentLocation: '',
        licenseNumber: '',
        customerName: '',
        supplierName: '',
        materialType: '',
        materialName: '',
        weight1: '',
        weight2: '',
        netWeight: '',
        pricePerKg: '',
        totalPrice: '',
        extraCost: '',
        invoiceStatus: '',
        paymentStatus: ''
      },
      loading: false,
      error: null,
      fieldErrors: {},
      purchases: [],
      filteredPurchases: []
    }
  },
  async created() {
    // Load initial data when component is created
    await this.loadPurchases()
  },
  methods: {
    async loadPurchases() {
      this.loading = true
      try {
        const { data } = await apolloClient.query({
          query: gql`
            query FilterPurchaseData($filterInput: FilterInput) {
              filteredData(filterInput: $filterInput) {
                ... on ShipmentType {
                  id
                  date
                  status
                  location
                  supplierName
                  materialType
                  materialName
                  pricePerKg
                  totalPrice
                  vat
                  extraCost
                  paymentStatus
                  documentInfo
                  comments
                  username
                  logs
                }
              }
            }
          `,
          variables: {
            filterInput: {
              shipmentType: "Incoming",
              shipmentStatus: null,
              shipmentLocation: null,
              licenseNumber: null,
              customerName: null,
              supplierName: null,
              materialType: null,
              materialName: null,
              invoiceStatus: null,
              paymentStatus: null,
              startDate: null,
              endDate: null
            }
          }
        })
        console.log('Raw response:', data) // Debug log
        
        // Handle empty or invalid responses
        if (!data?.filteredData) {
          console.log('No data received')
          this.purchases = []
          this.filteredPurchases = []
          this.$emit('filter-applied', [])
          return
        }

        // Filter out empty objects and ensure we have valid purchase data
        const validPurchases = data.filteredData.filter(item => 
          item && 
          typeof item === 'object' && 
          Object.keys(item).length > 0 &&
          item.id &&
          item.__typename === 'ShipmentType' &&
          item.shipmentType === 'Incoming'
        )

        console.log('Valid purchases:', validPurchases) // Debug log
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
        shipmentStatus: '',
        shipmentType: '',
        shipmentLocation: '',
        licenseNumber: '',
        customerName: '',
        supplierName: '',
        materialType: '',
        materialName: '',
        weight1: '',
        weight2: '',
        netWeight: '',
        pricePerKg: '',
        totalPrice: '',
        extraCost: '',
        invoiceStatus: '',
        paymentStatus: ''
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
        const { isValid, errors } = validateForm(this.filters, 'shipment')
        
        if (!isValid) {
          this.fieldErrors = errors
          this.error = 'لطفا خطاهای فرم را برطرف کنید'
          return
        }

        const cleanFilters = cleanFormData(this.filters)
        
        // Add shipmentType to filter for purchases
        const filterInput = {
          ...cleanFilters,
          shipmentType: "Incoming"
        }

        const { data } = await apolloClient.query({
          query: gql`
            query FilterPurchaseData($filterInput: FilterInput) {
              filteredData(filterInput: $filterInput) {
                ... on ShipmentType {
                  id
                  date
                  status
                  location
                  supplierName
                  materialType
                  materialName
                  pricePerKg
                  totalPrice
                  vat
                  extraCost
                  paymentStatus
                  documentInfo
                  comments
                  username
                  logs
                }
              }
            }
          `,
          variables: {
            filterInput
          }
        })

        if (!data?.filteredData) {
          console.log('No data received')
          this.filteredPurchases = []
          this.$emit('filter-applied', [])
          return
        }

        // Filter out empty objects and ensure we have valid purchase data
        const validPurchases = data.filteredData.filter(item => 
          item && 
          typeof item === 'object' && 
          Object.keys(item).length > 0 &&
          item.id &&
          item.__typename === 'ShipmentType' &&
          item.shipmentType === 'Incoming'
        )

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