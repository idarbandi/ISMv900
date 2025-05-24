<template>
  <div class="bg-white rounded-lg shadow-md p-6">
    <h2 class="text-2xl font-semibold mb-6">Shipment Filter</h2>
    
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

      <!-- Status and Type -->
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">Status</label>
        <select 
          v-model="filters.status"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
          <option value="">All</option>
          <option value="Pending">Pending</option>
          <option value="In Transit">In Transit</option>
          <option value="Delivered">Delivered</option>
          <option value="Cancelled">Cancelled</option>
        </select>
      </div>
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">Shipment Type</label>
        <select 
          v-model="filters.shipmentType"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
          <option value="">All</option>
          <option value="Inbound">Inbound</option>
          <option value="Outbound">Outbound</option>
        </select>
      </div>

      <!-- Location -->
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">Origin</label>
        <input 
          type="text" 
          v-model="filters.origin"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
      </div>
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">Destination</label>
        <input 
          type="text" 
          v-model="filters.destination"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
      </div>

      <!-- Vehicle and Driver -->
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">Vehicle License Plate</label>
        <input 
          type="text" 
          v-model="filters.vehicleLicensePlate"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
      </div>
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">Driver Name</label>
        <input 
          type="text" 
          v-model="filters.driverName"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
      </div>

      <!-- Weight and Volume -->
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
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">Volume Range (m³)</label>
        <div class="flex items-center space-x-4">
          <input 
            type="number" 
            v-model="filters.minVolume"
            class="mt-1 block w-24 rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            placeholder="Min"
          >
          <span>to</span>
          <input 
            type="number" 
            v-model="filters.maxVolume"
            class="mt-1 block w-24 rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            placeholder="Max"
          >
        </div>
      </div>

      <!-- Cost -->
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">Cost Range</label>
        <div class="flex items-center space-x-4">
          <input 
            type="number" 
            v-model="filters.minCost"
            class="mt-1 block w-24 rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            placeholder="Min"
          >
          <span>to</span>
          <input 
            type="number" 
            v-model="filters.maxCost"
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
  name: 'ShipmentFilter',
  data() {
    return {
      filters: {
        startDate: '',
        endDate: '',
        status: '',
        shipmentType: '',
        origin: '',
        destination: '',
        vehicleLicensePlate: '',
        driverName: '',
        minWeight: '',
        maxWeight: '',
        minVolume: '',
        maxVolume: '',
        minCost: '',
        maxCost: '',
      }
    }
  },
  methods: {
    resetFilters() {
      this.filters = {
        startDate: '',
        endDate: '',
        status: '',
        shipmentType: '',
        origin: '',
        destination: '',
        vehicleLicensePlate: '',
        driverName: '',
        minWeight: '',
        maxWeight: '',
        minVolume: '',
        maxVolume: '',
        minCost: '',
        maxCost: '',
      }
      this.$emit('filter-reset')
    },
    applyFilters() {
      this.$emit('filter-applied', this.filters)
    }
  }
}
</script> 