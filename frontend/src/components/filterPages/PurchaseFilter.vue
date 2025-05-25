<template>
  <div class="bg-white rounded-lg shadow-md p-6">
    <h2 class="text-2xl font-semibold mb-6">Purchase Filter</h2>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <!-- Date Range -->
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">Start Date</label>
        <input 
          type="date" 
          v-model="filters.startDate"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
      </div>
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">End Date</label>
        <input 
          type="date" 
          v-model="filters.endDate"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
      </div>

      <!-- Status and Payment -->
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">Status</label>
        <select 
          v-model="filters.status"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
          <option value="">All</option>
          <option value="Paid">Paid</option>
          <option value="Terms">Terms</option>
          <option value="Cancelled">Cancelled</option>
        </select>
      </div>
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">Invoice Status</label>
        <select 
          v-model="filters.invoiceStatus"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
          <option value="">All</option>
          <option value="Received">Received</option>
          <option value="NA">Not Available</option>
        </select>
      </div>

      <!-- Supplier and Material -->
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">Supplier Name</label>
        <input 
          type="text" 
          v-model="filters.supplierName"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
      </div>
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">Material Type</label>
        <input 
          type="text" 
          v-model="filters.materialType"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
      </div>
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">Material Name</label>
        <input 
          type="text" 
          v-model="filters.materialName"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
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
        <label class="block text-sm font-medium text-gray-700">Price Range (per kg)</label>
        <div class="flex items-center space-x-4">
          <input 
            type="number" 
            v-model="filters.minPricePerKg"
            class="mt-1 block w-24 rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            placeholder="Min"
          >
          <span>to</span>
          <input 
            type="number" 
            v-model="filters.maxPricePerKg"
            class="mt-1 block w-24 rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            placeholder="Max"
          >
        </div>
      </div>
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">Total Price Range</label>
        <div class="flex items-center space-x-4">
          <input 
            type="number" 
            v-model="filters.minTotalPrice"
            class="mt-1 block w-24 rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            placeholder="Min"
          >
          <span>to</span>
          <input 
            type="number" 
            v-model="filters.maxTotalPrice"
            class="mt-1 block w-24 rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            placeholder="Max"
          >
        </div>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="mt-6 flex justify-end space-x-4">
      <button 
        @click="resetFilters"
        class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
      >
        Reset
      </button>
      <button 
        @click="applyFilters"
        class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
      >
        Apply Filters
      </button>
    </div>
  </div>
</template>

<script>
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
        minPricePerKg: '',
        maxPricePerKg: '',
        minTotalPrice: '',
        maxTotalPrice: '',
      }
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
        minPricePerKg: '',
        maxPricePerKg: '',
        minTotalPrice: '',
        maxTotalPrice: '',
      }
      this.$emit('filter-reset')
    },
    applyFilters() {
      this.$emit('filter-applied', this.filters)
    }
  }
}
</script> 