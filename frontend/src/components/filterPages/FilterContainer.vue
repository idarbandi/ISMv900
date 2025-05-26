<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Filter Type Selector -->
    <div class="mb-6">
      <div class="flex space-x-4">
        <button
          v-for="type in filterTypes"
          :key="type.value"
          @click="currentFilterType = type.value"
          :class="[
            'px-4 py-2 rounded-md font-medium',
            currentFilterType === type.value
              ? 'bg-blue-600 text-white'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          ]"
        >
          {{ type.label }}
        </button>
      </div>
    </div>

    <!-- Product Filter Container -->
    <div v-if="currentFilterType === 'product'" class="mb-6">
      <ProductFilter
        @filter-applied="handleProductFilterApplied"
        @filter-reset="handleFilterReset"
      />
      
      <!-- Product Results Section -->
      <div v-if="loading" class="text-center py-8">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
        <p class="mt-4 text-gray-600">در حال بارگذاری...</p>
      </div>

      <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
        <strong class="font-bold">خطا!</strong>
        <span class="block sm:inline">{{ error }}</span>
      </div>

      <div v-else-if="productData.length > 0" class="bg-white rounded-lg shadow-md p-6">
        <h3 class="text-xl font-semibold mb-4">نتایج محصولات ({{ productData.length }})</h3>
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th v-for="header in productTableHeaders" :key="header" class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {{ header }}
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="item in productData" :key="item.id">
                <td v-for="field in getProductTableFields(item)" :key="field" class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ field }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div v-else-if="hasSearched" class="bg-white rounded-lg shadow-md p-6 text-center text-gray-500">
        هیچ نتیجه‌ای یافت نشد
      </div>
    </div>

    <!-- Shipment Filter Container -->
    <div v-if="currentFilterType === 'shipment'" class="mb-6">
      <ShipmentFilter
        @filter-applied="handleShipmentFilterApplied"
        @filter-reset="handleFilterReset"
      />
      
      <!-- Shipment Results Section -->
      <div v-if="loading" class="text-center py-8">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
        <p class="mt-4 text-gray-600">در حال بارگذاری...</p>
      </div>

      <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
        <strong class="font-bold">خطا!</strong>
        <span class="block sm:inline">{{ error }}</span>
      </div>

      <div v-else-if="shipmentData.length > 0" class="bg-white rounded-lg shadow-md p-6">
        <h3 class="text-xl font-semibold mb-4">نتایج ارسال‌ها ({{ shipmentData.length }})</h3>
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th v-for="header in shipmentTableHeaders" :key="header" class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {{ header }}
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="item in shipmentData" :key="item.id">
                <td v-for="field in getShipmentTableFields(item)" :key="field" class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ field }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div v-else-if="hasSearched" class="bg-white rounded-lg shadow-md p-6 text-center text-gray-500">
        هیچ نتیجه‌ای یافت نشد
      </div>
    </div>

    <!-- Purchase Filter Container -->
    <div v-if="currentFilterType === 'purchase'" class="mb-6">
      <PurchaseFilter
        @filter-applied="handlePurchaseFilterApplied"
        @filter-reset="handleFilterReset"
      />
      
      <!-- Purchase Results Section -->
      <div v-if="loading" class="text-center py-8">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
        <p class="mt-4 text-gray-600">در حال بارگذاری...</p>
      </div>

      <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
        <strong class="font-bold">خطا!</strong>
        <span class="block sm:inline">{{ error }}</span>
      </div>

      <div v-else-if="purchaseData.length > 0" class="bg-white rounded-lg shadow-md p-6">
        <h3 class="text-xl font-semibold mb-4">نتایج خریدها ({{ purchaseData.length }})</h3>
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th v-for="header in purchaseTableHeaders" :key="header" class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {{ header }}
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="item in purchaseData" :key="item.id">
                <td v-for="field in getPurchaseTableFields(item)" :key="field" class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ field }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div v-else-if="hasSearched" class="bg-white rounded-lg shadow-md p-6 text-center text-gray-500">
        هیچ نتیجه‌ای یافت نشد
      </div>
    </div>
  </div>
</template>

<script>
import ProductFilter from './ProductFilter.vue'
import ShipmentFilter from './ShipmentFilter.vue'
import PurchaseFilter from './PurchaseFilter.vue'
import { gql } from '@apollo/client/core'
import { apolloClient } from '@/apollo'

const PRODUCT_FILTER_QUERY = gql`
  query FilterProductData($filterInput: FilterInput) {
    filteredData(filterInput: $filterInput) {
      ... on ProductType {
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
  }
`

const SHIPMENT_FILTER_QUERY = gql`
  query FilterShipmentData($filterInput: FilterInput) {
    filteredData(filterInput: $filterInput) {
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

const PURCHASE_FILTER_QUERY = gql`
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
`

export default {
  name: 'FilterContainer',
  components: {
    ProductFilter,
    ShipmentFilter,
    PurchaseFilter
  },
  data() {
    return {
      currentFilterType: 'product',
      filterTypes: [
        { label: 'محصولات', value: 'product' },
        { label: 'ارسال‌ها', value: 'shipment' },
        { label: 'خریدها', value: 'purchase' }
      ],
      productData: [],
      shipmentData: [],
      purchaseData: [],
      hasSearched: false,
      loading: false,
      error: null
    }
  },
  computed: {
    productTableHeaders() {
      return ['نام پروفایل', 'شماره رول', 'عرض', 'GSM', 'طول', 'وضعیت', 'موقعیت', 'گرید', 'شکستگی']
    },
    shipmentTableHeaders() {
      return [
        'تاریخ',
        'وضعیت',
        'موقعیت',
        'تاریخ دریافت',
        'زمان ورود',
        'زمان وزن اول',
        'زمان وزن دوم',
        'زمان خروج',
        'نوع ارسال',
        'شماره پلاک',
        'نام مشتری',
        'نام تامین کننده',
        'وزن اول',
        'موقعیت تخلیه',
        'واحد',
        'تعداد',
        'کیفیت',
        'جریمه',
        'وزن دوم',
        'وزن خالص',
        'لیست رول‌ها',
        'نام پروفایل',
        'عرض',
        'کد فروش',
        'قیمت هر کیلو',
        'قیمت کل',
        'هزینه اضافی',
        'نوع مواد',
        'نام مواد',
        'مالیات بر ارزش افزوده',
        'وضعیت فاکتور',
        'وضعیت پرداخت',
        'اطلاعات سند',
        'توضیحات',
        'دلیل لغو',
        'نام کاربری',
        'گزارش‌ها'
      ]
    },
    purchaseTableHeaders() {
      return [
        'تاریخ',
        'وضعیت',
        'موقعیت',
        'نام تامین کننده',
        'نوع مواد',
        'نام مواد',
        'قیمت هر کیلو',
        'قیمت کل',
        'مالیات بر ارزش افزوده',
        'هزینه اضافی',
        'وضعیت پرداخت',
        'اطلاعات سند',
        'توضیحات',
        'نام کاربری',
        'گزارش‌ها'
      ]
    }
  },
  methods: {
    getProductTableFields(item) {
      return [
        item.profileName,
        item.reelNumber,
        item.width,
        item.gsm,
        item.length,
        item.status,
        item.location,
        item.grade,
        item.breaks
      ]
    },
    getShipmentTableFields(item) {
      return [
        item.date,
        item.status,
        item.location,
        item.receiveDate,
        item.entryTime,
        item.weight1Time,
        item.weight2Time,
        item.exitTime,
        item.shipmentType,
        item.licenseNumber,
        item.customerName,
        item.supplierName,
        item.weight1,
        item.unloadLocation,
        item.unit,
        item.quantity,
        item.quality,
        item.penalty,
        item.weight2,
        item.netWeight,
        item.listOfReels,
        item.profileName,
        item.width,
        item.salesId,
        item.pricePerKg,
        item.totalPrice,
        item.extraCost,
        item.materialType,
        item.materialName,
        item.vat,
        item.invoiceStatus,
        item.paymentStatus,
        item.documentInfo,
        item.comments,
        item.cancellationReason,
        item.username,
        item.logs
      ]
    },
    getPurchaseTableFields(item) {
      return [
        item.date,
        item.status,
        item.location,
        item.supplierName,
        item.materialType,
        item.materialName,
        item.pricePerKg,
        item.totalPrice,
        item.vat,
        item.extraCost,
        item.paymentStatus,
        item.documentInfo,
        item.comments,
        item.username,
        item.logs
      ]
    },
    async handleProductFilterApplied(filters) {
      this.loading = true
      this.error = null
      this.hasSearched = true

      try {
        this.productData = filters.filter(item => 
          item && 
          typeof item === 'object' && 
          Object.keys(item).length > 0 &&
          item.id
        )
      } catch (err) {
        this.error = 'خطا در دریافت اطلاعات'
        console.error('Filter error:', err)
        this.productData = []
      }

      this.loading = false
    },
    async handleShipmentFilterApplied(filters) {
      this.loading = true
      this.error = null
      this.hasSearched = true

      try {
        const response = await apolloClient.query({
          query: SHIPMENT_FILTER_QUERY,
          variables: {
            filterInput: filters
          },
          fetchPolicy: 'network-only'
        })

        if (response?.data?.filteredData && 
            Array.isArray(response.data.filteredData) && 
            response.data.filteredData.length > 0) {
          this.shipmentData = response.data.filteredData.filter(item => 
            item && 
            typeof item === 'object' && 
            Object.keys(item).length > 0 &&
            item.id &&
            item.__typename === 'ShipmentType'
          )
        } else {
          this.shipmentData = []
        }
      } catch (err) {
        this.error = 'خطا در دریافت اطلاعات'
        console.error('Filter error:', err)
        this.shipmentData = []
      }

      this.loading = false
    },
    async handlePurchaseFilterApplied(filters) {
      this.loading = true
      this.error = null
      this.hasSearched = true

      try {
        const response = await apolloClient.query({
          query: PURCHASE_FILTER_QUERY,
          variables: {
            filterInput: filters
          },
          fetchPolicy: 'network-only'
        })

        if (response?.data?.filteredData && 
            Array.isArray(response.data.filteredData) && 
            response.data.filteredData.length > 0) {
          this.purchaseData = response.data.filteredData.filter(item => 
            item && 
            typeof item === 'object' && 
            Object.keys(item).length > 0 &&
            item.id &&
            item.__typename === 'ShipmentType'
          )
        } else {
          this.purchaseData = []
        }
      } catch (err) {
        this.error = 'خطا در دریافت اطلاعات'
        console.error('Filter error:', err)
        this.purchaseData = []
      }

      this.loading = false
    },
    handleFilterReset() {
      this.productData = []
      this.shipmentData = []
      this.purchaseData = []
      this.hasSearched = false
      this.error = null
    }
  }
}
</script> 