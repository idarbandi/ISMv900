<script>
import {initFlowbite} from "flowbite";
import modal from "@/components/Modal.vue";
import Alert from "@/components/Alert.vue";
import Card from "@/components/Card.vue";
import ModalButton from "@/components/custom/ModalButton.vue";
import Input from "@/components/custom/Input.vue";
import Dropdown from "@/components/custom/Dropdown.vue";

export default {
  name: "sales",
  components: {Dropdown, Input, ModalButton, Card, Alert, modal},
  data(){
    return {
      forms: {
        lic_number: {type: 'dropdown', name: 'شماره پلاک',title: 'شماره پلاک', data: '', value: ''},
        customer_name: {type:'input', name: 'اسم مشتری',title: 'اسم مشتری', value: '', disabled:true},
        list_of_reels: {type:'list', name: 'لیست رول ها',title: 'لیست رول ها', value: '', disabled:true},
        weight1: {type:'input', name: 'وزن 1',title: 'وزن 1', value: '', disabled:true, lable:'number'},
        weight2: {type:'input', name: 'وزن 2',title: 'وزن 2', value: '', disabled:true, lable:'number'},
        net_weight: {type:'input', name: 'وزن خالص', title: 'وزن خالص', value: '', disabled:true, lable:'number'},
        loading_location: {type:'input', name: 'محل بار شده',title: 'محل بار شده', value: '', disabled:true},
        consuption_profile_name: {type:'input', name: 'اسم پوفایل مصرفی',title: 'اسم پوفایل مصرفی', value: '', disabled:true},
        price_pre_kg: {type:'input', name: 'قیمت هر کیلوگرم', title: 'قیمت هر کیلوگرم', value: '', numbertype:true, lable:'number'},
        vat: {type: 'dropdown', name: 'مالیات بر ارزش افزوده',title: 'مالیات بر ارزش افزوده', data: ['0%', '1%', '2%', '3%', '4%', '5%', '6%', '7%', '8%', '9%', '10%'], value: '0'},
        total_price: {type:'input', name: 'قمیت کل',title: 'قمیت کل', value: '', disabled:true, lable:'number'},
        extra_cost: {type:'input', name: 'هزینه اضافی',title: 'هزینه اضافی', value: '', numbertype:true, lable:'number'},
        invoice_status: {type: 'dropdown', name: 'وضعیت فاکتور',title: 'وضعیت فاکتور', data: ['Sent', 'NA'], value: ''},
        invoice_number: {type:'input', name: 'شماره فاکتور', title: 'شماره فاکتور', value: '', lable:'number'},
        payment_status:{type:'dropdown', name: 'وضعیت پرداخت',title: 'وضعیت پرداخت', data: ['Terms', 'Paid'], value: ''},
        document_info: {type:'input', name: 'اظلاعات سند',title: 'اظلاعات سند', value: ''},
        commnet: {type:'input', name: 'توضیحات',title: 'توضیحات', value: '', lable:'comment'},
        username: {type:'input', name: 'نام کاربر',title: 'نام کاربر', value: ''},
      },
      // New product form fields
      productForm: {
        name: {type:'input', name: 'نام محصول', title: 'نام محصول', value: '', lable:'text'},
        gsm: {type:'input', name: 'گرماژ', title: 'گرماژ', value: '', lable:'text'},
        width: {type:'input', name: 'عرض کاغذ', title: 'عرض کاغذ', value: '', lable:'text'},
        buyer: {type:'input', name: 'نام خریدار', title: 'نام خریدار', value: '', lable:'text'},
        quantity: {type:'input', name: 'تعداد', title: 'تعداد', value: '', lable:'number'},
        weight: {type:'input', name: 'وزن', title: 'وزن', value: '', lable:'number'},
      },
      // Array to store added products
      products: [],
      showProductForm: false,
      success: false,
      error: false,
      errors: [],
    }
  },
  computed:{
    formattedValue() {
      return this.formatNumber(this.inputValue);
    },
    total_price(){
      let vat = this.forms.vat.value;
      vat = parseInt(vat.replace('%', ''))
      let price = parseInt(this.forms.net_weight.value.replace(/,/g, '')) * parseInt(this.forms.price_pre_kg.value.replace(/,/g, ''))
      if (vat == 0 ){
        return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
      } else {
         return (price+(price * (vat/100))).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
      }
    },
    // Calculate total weight of all products
    totalProductWeight() {
      if (this.products.length === 0) return 0;
      return this.products.reduce((sum, product) => sum + parseFloat(product.weight.replace(/,/g, '')), 0);
    }
  },
  mounted() {
    initFlowbite();
    const params = {
      "status": 'Office',
      "location": 'Office',
      'shipment_type': 'Outgoing',
    }
    this.axios.post('/myapp/api/getShipmentLicenseNumbers', {}, {params: params}).then((response) => {
      console.log('lics:',response.data)
      this.forms.lic_number.data = response.data['license_numbers']
    })
  },
  watch: {
    success(c, p) {
      if (c == true) {
        setTimeout(() => {
          this.success = false
          location.reload();
        }, 5000)
      }
    },
  },
  methods:{
    formatNumber(value) {
      return value.replace(/\D/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    },
    formatInput() {
      this.forms.extra_cost.value = this.formatNumber(this.forms.extra_cost.value);
      this.forms.price_pre_kg.value = this.formatNumber(this.forms.price_pre_kg.value);
    },
    formatProductInput() {
      this.productForm.quantity.value = this.formatNumber(this.productForm.quantity.value);
      this.productForm.weight.value = this.formatNumber(this.productForm.weight.value);
    },
    clicked(k, name){
      console.log(k, name)
      if (k == 'lic_number'){
        this.forms.lic_number.name = name
        this.forms.lic_number.value = name
        const params = {
          "license_number": this.forms.lic_number.value,
        }
        this.axios.post('/myapp/api/getShipmentDetails2ByLicenseNumber', {},{params:params}).then((response) => {
          console.log(response.data)
          this.forms.customer_name.value = response.data['customer_name']
          this.forms.list_of_reels.value = response.data['list_of_reels']
          this.forms.weight1.value = response.data['weight1'].toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
          this.forms.weight2.value = response.data['weight2'].toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
          this.forms.net_weight.value = response.data['net_weight'].toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
          this.forms.loading_location.value = response.data['unloaded_location']
          this.forms.consuption_profile_name.value = response.data['consuption_profile_name']
        })
      }
      if (k == 'vat'){
        this.forms.vat.name = name
        this.forms.vat.value = name
        console.log(this.total_price)
        this.forms.total_price.value = this.total_price
        
      }
      if (k == 'invoice_status'){
        this.forms.invoice_status.name = name
        this.forms.invoice_status.value = name
      }
      if (k == 'payment_status'){
        this.forms.payment_status.name = name
        this.forms.payment_status.value = name
      }
    },
    // Toggle product form visibility
    toggleProductForm() {
      this.showProductForm = !this.showProductForm;
      // Reset form fields when opening
      if (this.showProductForm) {
        for (const key in this.productForm) {
          this.productForm[key].value = '';
          this.productForm[key].error = false;
        }
      }
    },
    // Add a new product to the list
    addProduct() {
      // Validate product form
      let hasError = false;
      this.errors = [];
      
      for (const key in this.productForm) {
        if (this.productForm[key].value === '') {
          this.productForm[key].error = true;
          this.errors.push({message: `${this.productForm[key].name} مورد نیاز است`});
          hasError = true;
        } else {
          this.productForm[key].error = false;
        }
      }
      
      if (hasError) {
        this.error = true;
        return;
      }
      
      // Add the product
      this.products.push({
        name: this.productForm.name.value,
        gsm: this.productForm.gsm.value,
        width: this.productForm.width.value,
        buyer: this.productForm.buyer.value,
        quantity: this.productForm.quantity.value,
        weight: this.productForm.weight.value
      });
      
      // Close form and reset
      this.toggleProductForm();
      this.error = false;
    },
    // Remove a product from the list
    removeProduct(index) {
      this.products.splice(index, 1);
    },
    async createsSales() {
      let vat = this.forms.vat.value;
      const params = {
        'lic_number': this.forms.lic_number.value,
        'customer_name': this.forms.customer_name.value,
        'list_of_reels': this.forms.list_of_reels.value,
        'weight1': parseInt(this.forms.weight1.value.replace(/,/g, '')),
        'weight2': parseInt(this.forms.weight2.value.replace(/,/g, '')),
        'net_weight': parseInt(this.forms.net_weight.value.replace(/,/g, '')),
        'loading_location': this.forms.loading_location.value,
        'consuption_profile_name': this.forms.consuption_profile_name.value,
        'price_pre_kg': this.forms.price_pre_kg.value.replace(/,/g, ''),
        'vat': parseInt(vat.replace('%', '')) ,
        'total_price': parseInt(this.forms.total_price.value.replace(/,/g, '')),
        'extra_cost': parseInt(this.forms.extra_cost.value.replace(/,/g, '')),
        'invoice_status': this.forms.invoice_status.value,
        'invoice_number': parseInt(this.forms.invoice_number.value.replace(/,/g, '')),
        'payment_status': this.forms.payment_status.value,
        'document_info': this.forms.document_info.value,
        'commnet': this.forms.commnet.value,
        'username': this.forms.username.value,
        'products': this.products  // Include the products array
      };
      console.log(params)
      this.errors = []
      for (const key in this.forms) {
        if (this.forms[key].value == ''){
          if (key!='comment'){
            this.forms[key].error = true
          this.errors.push({'message': `${this.forms[key].name} مورد نیاز است`})
          }
        }else {
           this.forms[key].error = false
        }
      }
      
      // Validate products
      if (this.products.length === 0) {
        this.errors.push({'message': 'حداقل یک محصول باید اضافه شود'});
      }
      
      if (this.errors.length == 0){
        this.error = false
        const response = await this.axios.post('/myapp/createSalesOrder/', {}, {params: params})
        console.log(response.data); // Access response data
        if (response.data['status'] == 'success'){
          this.success = true
        }else {
          this.error = true
          this.errors = response.data['errors']
        }
      } else {
        this.error = true
      }
    },
  }
}
</script>

<template>
  <Card title="ایجاد سفارش فروش">
    <form class="flex flex-col items-center mt-5 gap-4">
      <div v-if="error" class="flex p-4 mb-4 text-sm text-red-800 rounded-lg bg-red-50 dark:bg-gray-800 dark:text-red-400" role="alert">
            <svg class="flex-shrink-0 inline w-4 h-4 me-3 mt-[2px]" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
              <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5ZM9.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3ZM12 15H8a1 1 0 0 1 0-2h1v-3H8a1 1 0 0 1 0-2h2a1 1 0 0 1 1 1v4h1a1 1 0 0 1 0 2Z"/>
            </svg>
            <span class="sr-only">Danger</span>
            <div>
              <span class="font-medium">خطا! لطفا اطلاعات را برسی کنید:</span>
                <ul class="mt-1.5 list-disc list-inside">
                  <li v-for="error in errors">{{ error.message }}</li>
              </ul>
            </div>
          </div>
      <div v-if="success" class="flex p-4 mb-4 text-sm text-green-800 rounded-lg bg-green-50 dark:bg-gray-800 dark:text-green-400" role="alert">
        <svg class="flex-shrink-0 inline w-4 h-4 me-3 mt-[2px]" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
          <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5ZM9.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3ZM12 15H8a1 1 0 0 1 0-2h1v-3H8a1 1 0 0 1 0-2h2a1 1 0 0 1 1 1v4h1a1 1 0 0 1 0 2Z"/>
        </svg>
        <div>
          <span class="font-medium">
            مشتری جدید با نام {{ forms.customer_name.value }} با موفقیت به سیستم اضافه شد.
            <template v-for="(val, key) in forms">
                <p v-if="key=='reel_numbers'">شماره رول:</p>
                <ul v-if="key=='reel_numbers'">
                  <li v-for="item in val.value" :key="item">{{ item }}</li>
                </ul>
                <p v-else>{{val.title}}: {{val.value}}</p>
            </template>
          </span>
        </div>
      </div>
      
      <!-- Products Section -->
      <div class="w-full p-4 mb-4 border border-gray-200 rounded-lg bg-white dark:bg-gray-800 dark:border-gray-700">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">محصولات</h3>
          <button @click="toggleProductForm" type="button" class="text-white bg-green-500 hover:bg-green-600 focus:ring-4 focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
            {{ showProductForm ? 'بستن فرم' : 'افزودن محصول' }}
          </button>
        </div>
        
        <!-- Product Form -->
        <div v-if="showProductForm" class="mb-4 p-4 border border-gray-200 rounded-lg">
          <h4 class="text-md font-semibold mb-3 text-gray-900 dark:text-white">افزودن محصول جدید</h4>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <template v-for="(val, form_name) in productForm">
              <Input
                :formName="'product_'+form_name"
                :label="val.name"
                :type="val.lable"
                :disabled="val.disabled"
                @update="val.value = $event"
                :value="val.value"
                @input="formatProductInput"
              />
            </template>
          </div>
          <div class="flex justify-end mt-4">
            <button @click="addProduct" type="button" class="text-white bg-green-500 hover:bg-green-600 focus:ring-4 focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
              افزودن
            </button>
          </div>
        </div>
        
        <!-- Products Table -->
        <div v-if="products.length > 0" class="relative overflow-x-auto shadow-md sm:rounded-lg">
          <table class="w-full text-sm text-right text-gray-500 dark:text-gray-400">
            <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
              <tr>
                <th scope="col" class="px-6 py-3">ردیف</th>
                <th scope="col" class="px-6 py-3">نام کالا</th>
                <th scope="col" class="px-6 py-3">گرماژ</th>
                <th scope="col" class="px-6 py-3">عرض کاغذ</th>
                <th scope="col" class="px-6 py-3">نام خریدار</th>
                <th scope="col" class="px-6 py-3">تعداد</th>
                <th scope="col" class="px-6 py-3">وزن کالا</th>
                <th scope="col" class="px-6 py-3">عملیات</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(product, index) in products" :key="index" class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                <td class="px-6 py-4">{{ index + 1 }}</td>
                <td class="px-6 py-4">{{ product.name }}</td>
                <td class="px-6 py-4">{{ product.gsm }}</td>
                <td class="px-6 py-4">{{ product.width }}</td>
                <td class="px-6 py-4">{{ product.buyer }}</td>
                <td class="px-6 py-4">{{ product.quantity }}</td>
                <td class="px-6 py-4">{{ product.weight }}</td>
                <td class="px-6 py-4">
                  <button @click="removeProduct(index)" type="button" class="text-red-500 hover:text-red-700">
                    حذف
                  </button>
                </td>
              </tr>
              <tr class="font-semibold bg-gray-50 dark:bg-gray-700">
                <td colspan="6" class="px-6 py-4 text-left">جمع کل وزن:</td>
                <td class="px-6 py-4">{{ formatNumber(totalProductWeight.toString()) }}</td>
                <td class="px-6 py-4"></td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <div v-else class="p-4 text-center text-gray-500 dark:text-gray-400">
          محصولی اضافه نشده است. لطفا با کلیک بر روی دکمه "افزودن محصول" یک محصول جدید اضافه کنید.
        </div>
      </div>
      
      <template v-for="(val, form_name) in forms">
        <template v-if="val.type=='list'">
          <h3 class="font-semibold text-gray-900 dark:text-white">لیست شماره رول:</h3>
          <ul class="w-48 overflow-y-auto max-h-48 text-sm font-medium text-gray-900 bg-white border border-gray-200 rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white">
            <li v-for="reel in val.value.split(',')" :key="reel" class="w-full p-2  border-b border-gray-200 rounded-t-lg dark:border-gray-600">
                {{ reel }}
            </li>
          </ul>
        </template>
        <template v-if="val.type=='input'">
            <Input
              :formName="form_name"
              :label="val.name"
              :type="val.lable"
              :disabled="val.disabled"
              @update="val.value = $event"
              :value="val.value"
            />
        </template>
        <template v-if="val.type=='dropdown'">
          <Dropdown :formName="form_name">
            <template v-slot:btnName>
              {{val.name}}
            </template>
            <template v-slot:list>
              <li v-for="(data, index) in val.data" :key="index">
                <a @click="clicked(form_name, data)" type="button" class="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">
                  {{ data }}
                </a>
              </li>
            </template>
          </Dropdown>
        </template>
      </template>
      <modal type="confirm">
        <template v-slot:button>اضافه کردن</template>
        <template v-slot:text>
          <div class="flex flex-col gap-2 font-bold">
            <template v-for="(val, key) in forms">
                <p v-if="key=='reel_numbers'">شماره رول:</p>
                <ul v-if="key=='reel_numbers'">
                  <li v-for="item in val.value" :key="item">{{ item }}</li>
                </ul>
                <p v-else>{{val.title}}: {{val.value}}</p>
            </template>
            
            <!-- Show products in confirmation -->
            <p class="mt-4">محصولات:</p>
            <ul>
              <li v-for="(product, index) in products" :key="index">
                {{ product.name }} - {{ product.gsm }} - {{ product.weight }}
              </li>
            </ul>
          </div>
        </template>
        <template v-slot:btns>
          <div>
            <ModalButton @close="createsSales"/>
          </div>
        </template>
      </modal>
    </form>
  </Card>
</template>