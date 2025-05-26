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

      <!-- Status and Payment -->
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">وضعیت</label>
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
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">وضعیت فاکتور</label>
        <select 
          v-model="filters.invoiceStatus"
          :class="[
            'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
            fieldErrors.invoiceStatus ? 'border-red-500' : ''
          ]"
        >
          <option value="">همه</option>
          <option value="Received">دریافت شده</option>
          <option value="NA">بدون فاکتور</option>
        </select>
        <p v-if="fieldErrors.invoiceStatus" class="mt-1 text-sm text-red-600">{{ fieldErrors.invoiceStatus }}</p>
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

      <!-- Quantity and Weight -->
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">Quantity Range</label>
        <div class="flex items-center space-x-4">
          <input 
            type="number" 
            v-model="filters.minQuantity"
            class="mt-1 block w-24 rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            placeholder="Min"
          >
          <span>to</span>
          <input 
            type="number" 
            v-model="filters.maxQuantity"
            class="mt-1 block w-24 rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            placeholder="Max"
          >
        </div>
      </div>
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">Weight Range (kg)</label>
        <div class="flex items-center space-x-4">
          <input 
            type="number" 
            v-model="filters.minWeight"
            class="mt-1 block w-24 rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            placeholder="Min"
          >
          <span>to</span>
          <input 
            type="number" 
            v-model="filters.maxWeight"
            class="mt-1 block w-24 rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            placeholder="Max"
          >
        </div>
      </div>

      <!-- Price Range -->
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
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">قیمت کل</label>
        <input 
          type="number" 
          v-model="filters.totalPrice"
          :class="[
            'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
            fieldErrors.totalPrice ? 'border-red-500' : ''
          ]"
        >
        <p v-if="fieldErrors.totalPrice" class="mt-1 text-sm text-red-600">{{ fieldErrors.totalPrice }}</p>
      </div>
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">هزینه اضافی</label>
        <input 
          type="number" 
          v-model="filters.extraCost"
          :class="[
            'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
            fieldErrors.extraCost ? 'border-red-500' : ''
          ]"
        >
        <p v-if="fieldErrors.extraCost" class="mt-1 text-sm text-red-600">{{ fieldErrors.extraCost }}</p>
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

export default {
  name: 'PurchaseFilter',
  data() {
    return {
      filters: {
        startDate: '',
        endDate: '',
        status: '',
        invoiceStatus: '',
        supplierName: '',
        materialType: '',
        materialName: '',
        minQuantity: '',
        maxQuantity: '',
        minWeight: '',
        maxWeight: '',
        pricePerKg: '',
        totalPrice: '',
        extraCost: ''
      },
      loading: false,
      error: null,
      fieldErrors: {}
    }
  },
  methods: {
    resetFilters() {
      this.filters = {
        startDate: '',
        endDate: '',
        status: '',
        invoiceStatus: '',
        supplierName: '',
        materialType: '',
        materialName: '',
        minQuantity: '',
        maxQuantity: '',
        minWeight: '',
        maxWeight: '',
        pricePerKg: '',
        totalPrice: '',
        extraCost: ''
      }
      this.fieldErrors = {}
      this.error = null
      this.$emit('filter-reset')
    },
    async applyFilters() {
      this.loading = true
      this.error = null
      this.fieldErrors = {}
      
      try {
        // Convert numeric strings to numbers before validation
        const numericFields = ['minQuantity', 'maxQuantity', 'minWeight', 'maxWeight', 'pricePerKg', 'totalPrice', 'extraCost']
        const processedFilters = { ...this.filters }
        
        numericFields.forEach(field => {
          if (processedFilters[field] !== '') {
            processedFilters[field] = Number(processedFilters[field])
          }
        })

        // Validate form
        const { isValid, errors } = validateForm(processedFilters, 'purchase')
        
        if (!isValid) {
          this.fieldErrors = errors
          this.error = 'لطفا خطاهای فرم را برطرف کنید'
          return
        }

        // Clean and emit filter data
        const cleanFilters = cleanFormData(processedFilters)
        this.$emit('filter-applied', cleanFilters)
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