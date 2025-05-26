<template>
  <div class="bg-white rounded-lg shadow-md p-6">
    <h2 class="text-2xl font-semibold mb-6">فیلتر بارنامه</h2>
    
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
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">نوع بارنامه</label>
        <select 
          v-model="filters.shipmentType"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
          <option value="">همه</option>
          <option value="Incoming">ورودی</option>
          <option value="Outgoing">خروجی</option>
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

export default {
  name: 'ShipmentFilter',
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
      shipments: [],
      filteredShipments: []
    }
  },
  async created() {
    await this.loadShipments()
  },
  methods: {
    async loadShipments() {
      this.loading = true
      try {
        const { data } = await apolloClient.query({
          query: gql`
            query GetAllShipments {
              filteredData(filterInput: { 
                shipmentStatus: null,
                shipmentType: null,
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
              }) {
                ... on ShipmentType {
                  id
                  date
                  status
                  location
                  receiveDate
                  entryTime
                  weight1Time
                  weight2Time
                  exitTime
                  shipmentType
                  licenseNumber
                  customerName
                  supplierName
                  weight1
                  unloadLocation
                  unit
                  quantity
                  quality
                  penalty
                  weight2
                  netWeight
                  listOfReels
                  profileName
                  width
                  salesId
                  pricePerKg
                  totalPrice
                  extraCost
                  materialType
                  materialName
                  vat
                  invoiceStatus
                  paymentStatus
                  documentInfo
                  comments
                  cancellationReason
                  username
                  logs
                }
              }
            }
          `
        })
        console.log('Shipments loaded:', data.filteredData)
        this.shipments = data.filteredData
        this.filteredShipments = data.filteredData
        this.$emit('filter-applied', this.shipments)
      } catch (err) {
        this.error = 'خطا در بارگذاری بارنامه‌ها'
        console.error('Error loading shipments:', err)
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
      this.filteredShipments = this.shipments
      this.$emit('filter-reset', this.shipments)
    },
    async applyFilters() {
      this.loading = true
      this.error = null
      
      try {
        this.filteredShipments = this.shipments.filter(shipment => {
          if (Object.keys(this.filters).every(key => !this.filters[key])) return true

          if (this.filters.shipmentStatus && shipment.status !== this.filters.shipmentStatus) return false
          if (this.filters.shipmentType && shipment.shipmentType !== this.filters.shipmentType) return false
          if (this.filters.shipmentLocation && !shipment.location.includes(this.filters.shipmentLocation)) return false
          if (this.filters.licenseNumber && !shipment.licenseNumber.includes(this.filters.licenseNumber)) return false
          if (this.filters.customerName && !shipment.customerName.includes(this.filters.customerName)) return false
          if (this.filters.supplierName && !shipment.supplierName.includes(this.filters.supplierName)) return false
          if (this.filters.materialType && !shipment.materialType.includes(this.filters.materialType)) return false
          if (this.filters.materialName && !shipment.materialName.includes(this.filters.materialName)) return false
          if (this.filters.invoiceStatus && shipment.invoiceStatus !== this.filters.invoiceStatus) return false
          if (this.filters.paymentStatus && shipment.paymentStatus !== this.filters.paymentStatus) return false

          if (this.filters.weight1 && shipment.weight1 !== Number(this.filters.weight1)) return false
          if (this.filters.weight2 && shipment.weight2 !== Number(this.filters.weight2)) return false
          if (this.filters.netWeight && shipment.netWeight !== Number(this.filters.netWeight)) return false
          if (this.filters.pricePerKg && shipment.pricePerKg !== Number(this.filters.pricePerKg)) return false
          if (this.filters.totalPrice && shipment.totalPrice !== Number(this.filters.totalPrice)) return false
          if (this.filters.extraCost && shipment.extraCost !== Number(this.filters.extraCost)) return false

          if (this.filters.startDate) {
            const startDate = new Date(this.filters.startDate)
            const shipmentDate = new Date(shipment.date)
            if (shipmentDate < startDate) return false
          }
          if (this.filters.endDate) {
            const endDate = new Date(this.filters.endDate)
            const shipmentDate = new Date(shipment.date)
            if (shipmentDate > endDate) return false
          }

          return true
        })

        this.$emit('filter-applied', this.filteredShipments)
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