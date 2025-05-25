<template>
  <div class="bg-white rounded-lg shadow-md p-6">
    <h2 class="text-2xl font-semibold mb-6">فیلتر ارسال</h2>
    
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
        <label class="block text-sm font-medium text-gray-700">نوع ارسال</label>
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
      shipments: []
    }
  },
  methods: {
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
      this.$emit('filter-reset')
    },
    async applyFilters() {
      this.loading = true
      this.error = null
      
      try {
        const filterInput = {
          startDate: this.filters.startDate || null,
          endDate: this.filters.endDate || null,
          shipmentStatus: this.filters.shipmentStatus || null,
          shipmentType: this.filters.shipmentType || null,
          shipmentLocation: this.filters.shipmentLocation || null,
          licenseNumber: this.filters.licenseNumber || null,
          customerName: this.filters.customerName || null,
          supplierName: this.filters.supplierName || null,
          materialType: this.filters.materialType || null,
          materialName: this.filters.materialName || null,
          weight1: this.filters.weight1 ? parseInt(this.filters.weight1) : null,
          weight2: this.filters.weight2 ? parseInt(this.filters.weight2) : null,
          netWeight: this.filters.netWeight || null,
          pricePerKg: this.filters.pricePerKg ? parseInt(this.filters.pricePerKg) : null,
          totalPrice: this.filters.totalPrice ? parseInt(this.filters.totalPrice) : null,
          extraCost: this.filters.extraCost ? parseInt(this.filters.extraCost) : null,
          invoiceStatus: this.filters.invoiceStatus || null,
          paymentStatus: this.filters.paymentStatus || null
        }

        this.$emit('filter-applied', filterInput)
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