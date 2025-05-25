<template>
  <div class="bg-white rounded-lg shadow-md p-6">
    <h2 class="text-2xl font-semibold mb-6">Product Filter</h2>
    
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

      <!-- Basic Information -->
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">Reel Number</label>
        <input 
          type="text" 
          v-model="filters.productReelNumber"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
      </div>
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">Profile Name</label>
        <input 
          type="text" 
          v-model="filters.productProfileName"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
      </div>

      <!-- Measurements -->
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">Width (mm)</label>
        <input 
          type="number" 
          v-model="filters.productWidth"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
      </div>
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">GSM</label>
        <input 
          type="number" 
          v-model="filters.productGsm"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
      </div>
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">Length (m)</label>
        <input 
          type="number" 
          v-model="filters.productLength"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
      </div>

      <!-- Status and Location -->
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">Status</label>
        <select 
          v-model="filters.productStatus"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
          <option value="">All</option>
          <option value="In-stock">In Stock</option>
          <option value="Sold">Sold</option>
          <option value="Moved">Moved</option>
          <option value="Delivered">Delivered</option>
        </select>
      </div>
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">Location</label>
        <input 
          type="text" 
          v-model="filters.productLocation"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
      </div>

      <!-- Grade and Breaks -->
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">Grade</label>
        <input 
          type="text" 
          v-model="filters.productGrade"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
      </div>
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">Breaks Range</label>
        <div class="flex items-center space-x-4">
          <input 
            type="number" 
            v-model="filters.minBreaks"
            class="mt-1 block w-24 rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            placeholder="Min"
          >
          <span>to</span>
          <input 
            type="number" 
            v-model="filters.maxBreaks"
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
        :disabled="loading"
      >
        Reset
      </button>
      <button 
        @click="applyFilters"
        class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        :disabled="loading"
      >
        {{ loading ? 'Loading...' : 'Apply Filters' }}
      </button>
    </div>
  </div>
</template>

<script>
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
        productLength: '',
        productGrade: '',
        productStatus: '',
        productLocation: '',
        productProfileName: '',
        minBreaks: 0,
        maxBreaks: 10,
      },
      loading: false,
      error: null,
      products: []
    }
  },
  methods: {
    resetFilters() {
      this.filters = {
        startDate: '',
        endDate: '',
        productReelNumber: '',
        productWidth: '',
        productGsm: '',
        productLength: '',
        productGrade: '',
        productStatus: '',
        productLocation: '',
        productProfileName: '',
        minBreaks: 0,
        maxBreaks: 10,
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
          productReelNumber: this.filters.productReelNumber || null,
          productWidth: this.filters.productWidth ? parseInt(this.filters.productWidth) : null,
          productGsm: this.filters.productGsm ? parseInt(this.filters.productGsm) : null,
          productLength: this.filters.productLength ? parseInt(this.filters.productLength) : null,
          productGrade: this.filters.productGrade || null,
          productStatus: this.filters.productStatus || null,
          productLocation: this.filters.productLocation || null,
          productProfileName: this.filters.productProfileName || null,
          minBreaks: this.filters.minBreaks || null,
          maxBreaks: this.filters.maxBreaks || null
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