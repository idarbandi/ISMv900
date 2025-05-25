<template>
  <div class="havaleh-form">
    <h2>حواله خروج از انبار</h2>
    <div class="form-header">
      <div class="form-group">
        <label>تاریخ ارسال:</label>
        <input type="text" v-model="formData.date" readonly />
      </div>
      <div class="form-group">
        <label>زمان ارسال:</label>
        <input type="text" v-model="formData.time" readonly />
      </div>
      <div class="form-group">
        <label>شماره سریال:</label>
        <input type="text" v-model="formData.serial" />
      </div>
    </div>

    <!-- Items Table -->
    <div class="items-table">
      <table>
        <thead>
          <tr>
            <th>ردیف</th>
            <th>نام کالا و مشخصات کالا</th>
            <th>گرماژ</th>
            <th>عرض کاغذ</th>
            <th>نام خریدار</th>
            <th>تعداد / مقدار</th>
            <th>وزن کالا</th>
            <th>عملیات</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in formData.items" :key="index">
            <td>{{ index + 1 }}</td>
            <td>
              <div class="input-with-dropdown">
                <input type="text" v-model="item.name" @click="(e) => toggleProductDropdown(index, e)"
                  placeholder="نام کالا را وارد کنید" class="product-input" />
                <div v-show="showProductDropdown && selectedProductIndex === index" class="dropdown-list">
                  <div v-if="products.length === 0" class="dropdown-item error-message">
                    هیچ محصولی در دیتابیس یافت نشد
                  </div>
                  <div v-else v-for="product in products" :key="product.id"
                    @click="(e) => selectProduct(product, index, e)" class="dropdown-item">
                    {{ product.profile_name || product.grade }} - {{ product.gsm }} GSM - {{ product.width }}mm
                  </div>
                </div>
              </div>
            </td>
            <td>
              <input type="text" v-model="item.gsm" />
            </td>
            <td>
              <input type="text" v-model="item.width" />
            </td>
            <td>
              <div class="input-with-dropdown">
                <input type="text" v-model="item.buyer" @click="(e) => toggleProfileDropdown(index, e)"
                  placeholder="نام خریدار را وارد کنید" class="profile-input" />
                <div v-show="showProfileDropdown && selectedProfileIndex === index" class="dropdown-list">
                  <div v-if="profiles.length === 0" class="dropdown-item error-message">
                    هیچ مشتری در دیتابیس یافت نشد
                  </div>
                  <div v-else v-for="profile in profiles" :key="profile.id"
                    @click="(e) => selectProfile(profile, index, e)" class="dropdown-item">
                    {{ profile.customer_name }}
                  </div>
                </div>
              </div>
            </td>
            <td>
              <input type="number" v-model="item.quantity" />
            </td>
            <td>
              <input type="number" v-model="item.weight" />
            </td>
            <td>
              <button @click="removeItem(index)" class="remove-btn">حذف</button>
            </td>
          </tr>
        </tbody>
      </table>
      <button @click="addItem" class="add-btn">افزودن ردیف جدید</button>
    </div>

    <div class="form-footer">
      <div class="form-group">
        <label>پلاک:</label>
        <div class="plate-input">
          <input type="text" v-model="formData.plate.first" maxlength="2" placeholder="12" />
          <select v-model="formData.plate.letter" class="letter-select">
            <option value="">الف</option>
            <option v-for="letter in persianLetters" :key="letter" :value="letter">{{ letter }}</option>
          </select>
          <input type="text" v-model="formData.plate.second" maxlength="3" placeholder="365" />
          <input type="text" v-model="formData.plate.year" maxlength="2" placeholder="11" />
        </div>
        <Lic_numer :lic="formData.plate" :showPlaceholders="true" />
      </div>
      <div class="form-group">
        <label>نام:</label>
        <input type="text" v-model="formData.name" />
      </div>
      <div class="total-weight">
        <strong>جمع کل وزن:</strong> {{ calculateTotalWeight() }}
      </div>
      <button @click="generatePDF" class="generate-btn">تولید PDF</button>
    </div>

    <!-- PDF Template -->
    <div id="pdf-template" v-show="false">
      <div v-for="i in 3" :key="i" class="copy">
        <div class="header">
          <div class="logo-section">
            <img src="@/assets/images/homayoun-logo.png" alt="Homayoun Logo">
            <div>همایون</div>
            <div>HOMAYOUN</div>
          </div>
          <div class="company-info">
            <div class="company-name">شرکت صنایع تولیدی کاغذ و مقوای همایون</div>
            <div class="document-title">حواله خروج از انبار</div>
          </div>
          <div class="document-info">
            <div>تاریخ ارسال: {{ formData.date }}</div>
            <div>زمان ارسال: {{ formData.time }}</div>
            <div>شماره سریال: {{ formData.serial }}</div>
          </div>
        </div>
        <table>
          <thead>
            <tr>
              <th class="col-1">ردیف</th>
              <th class="col-2">نام کالا و مشخصات کالا</th>
              <th class="col-3">گرماژ</th>
              <th class="col-4">عرض کاغذ</th>
              <th class="col-5">نام خریدار</th>
              <th class="col-6">تعداد / مقدار</th>
              <th class="col-7">وزن کالا</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in formData.items" :key="index">
              <td>{{ index + 1 }}</td>
              <td>{{ item.name }}</td>
              <td>{{ item.gsm }}</td>
              <td>{{ item.width }}</td>
              <td>{{ item.buyer }}</td>
              <td>{{ item.quantity }}</td>
              <td>{{ item.weight }}</td>
            </tr>
            <tr class="total-row">
              <td colspan="6" style="text-align: center;">جمع</td>
              <td>{{ calculateTotalWeight() }}</td>
            </tr>
          </tbody>
        </table>
        <div class="notes">
          <div>ملاحضات پلاک: {{ formData.plate.first }} {{ formData.plate.letter }} {{ formData.plate.second }} {{
            formData.plate.year }} - نام: {{ formData.name }}</div>
        </div>
        <div class="footer">
          <div class="signature-line">حسابداری</div>
          <div class="signature-line">انبارداری</div>
          <div class="signature-line">مدیر فروش</div>
          <div class="signature-line">مدیریت کارخانه</div>
          <div class="signature-line">تحویل گیرنده</div>
        </div>
        <div class="confirmation-text">
          بار صحیح و سالم تحویل اینجانب .............................. گردید.
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import html2pdf from 'html2pdf.js';
import jalaali from 'jalaali-js';
import Lic_numer from "@/components/lic_numer.vue";
import { LicenseNumberParser } from "@/components/lic_num_split";
import axios from 'axios';

// تنظیم baseURL برای axios
axios.defaults.baseURL = 'http://localhost:8000';

export default {
  name: 'havaleh',
  components: {
    Lic_numer
  },
  data() {
    return {
      persianLetters: ['الف', 'ب', 'پ', 'ت', 'ث', 'ج', 'چ', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'ژ', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ک', 'گ', 'ل', 'م', 'ن', 'و', 'ه', 'ی'],
      products: [],
      profiles: [],
      showProductDropdown: false,
      showProfileDropdown: false,
      selectedProductIndex: -1,
      selectedProfileIndex: -1,
      formData: {
        date: this.getCurrentDate(),
        time: this.getCurrentTime(),
        serial: '',
        items: [],
        plate: {
          first: '',
          letter: '',
          second: '',
          year: ''
        },
        name: ''
      }
    }
  },
  created() {
    this.formData.date = this.getCurrentDate();
    this.formData.time = this.getCurrentTime();
    this.fetchProducts();
    this.fetchProfiles();
  },
  mounted() {
    document.addEventListener('click', this.handleClickOutside);
  },
  beforeDestroy() {
    document.removeEventListener('click', this.handleClickOutside);
  },
  methods: {
    getCurrentDate() {
      const today = new Date();
      const jDate = jalaali.toJalaali(today);
      return `${jDate.jy}/${String(jDate.jm).padStart(2, '0')}/${String(jDate.jd).padStart(2, '0')}`;
    },
    getCurrentTime() {
      const today = new Date();
      const iranOffset = 4.5 * 60; // Iran is UTC+3:30
      const localOffset = today.getTimezoneOffset();
      const totalOffset = (iranOffset + localOffset) * 60 * 1000;
      const iranTime = new Date(today.getTime() + totalOffset);
      return `${String(iranTime.getHours()).padStart(2, '0')}:${String(iranTime.getMinutes()).padStart(2, '0')}`;
    },
    addItem() {
      this.formData.items.push({
        name: '',
        gsm: '',
        width: '',
        buyer: '',
        quantity: '',
        weight: ''
      });
    },
    removeItem(index) {
      this.formData.items.splice(index, 1);
    },
    calculateTotalWeight() {
      return this.formData.items.reduce((total, item) => {
        return total + (parseFloat(item.weight) || 0);
      }, 0).toLocaleString();
    },
    parsePlateNumber(plateNumber) {
      const parsed = LicenseNumberParser(plateNumber);
      if (parsed) {
        this.formData.plate = parsed;
      }
    },
    async generatePDF() {
      const element = document.getElementById('pdf-template');
      element.style.display = 'block';

      const opt = {
        margin: [10, 10, 10, 10],
        filename: `havaleh_${this.formData.serial}.pdf`,
        image: { type: 'jpeg', quality: 1 },
        html2canvas: {
          scale: 2,
          useCORS: true,
          letterRendering: true
        },
        jsPDF: {
          unit: 'mm',
          format: 'a4',
          orientation: 'portrait'
        },
        pagebreak: { mode: 'avoid-all' }
      };

      try {
        await html2pdf().set(opt).from(element).save();
      } catch (error) {
        console.error('خطا در تولید PDF:', error);
        alert('خطا در تولید PDF: ' + error.message);
      } finally {
        element.style.display = 'none';
      }
    },
    async fetchProducts() {
      try {
        const response = await axios.get('/myapp/api/products/list');
        console.log('API Response:', response.data);
        if (response.data && response.data.products) {
          this.products = response.data.products;
          console.log('Products loaded:', this.products);
          if (this.products.length === 0) {
            console.error('No products found in database');
          }
        } else {
          console.error('Invalid response format:', response.data);
        }
      } catch (error) {
        console.error('Error fetching products:', error.response?.data || error.message);
        this.products = [];
      }
    },
    async fetchProfiles() {
      try {
        const response = await axios.get('/myapp/api/customers/list');
        console.log('API Response:', response.data);
        if (response.data && response.data.customers) {
          this.profiles = response.data.customers;
          console.log('Customers loaded:', this.profiles);
          if (this.profiles.length === 0) {
            console.error('No customers found in database');
          }
        } else {
          console.error('Invalid response format:', response.data);
        }
      } catch (error) {
        console.error('Error fetching customers:', error.response?.data || error.message);
        this.profiles = [];
      }
    },
    toggleProductDropdown(index) {
      if (this.selectedProductIndex === index) {
        this.showProductDropdown = !this.showProductDropdown;
      } else {
        this.selectedProductIndex = index;
        this.showProductDropdown = true;
      }
      this.showProfileDropdown = false;

      // اگر محصولی وجود نداشت، خطا نمایش داده شود
      if (this.products.length === 0) {
        console.error('هیچ محصولی در دیتابیس یافت نشد');
      }
    },
    toggleProfileDropdown(index) {
      if (this.selectedProfileIndex === index) {
        this.showProfileDropdown = !this.showProfileDropdown;
      } else {
        this.selectedProfileIndex = index;
        this.showProfileDropdown = true;
      }
      this.showProductDropdown = false;

      // اگر مشتری وجود نداشت، خطا نمایش داده شود
      if (this.profiles.length === 0) {
        console.error('هیچ مشتری در دیتابیس یافت نشد');
      }
    },
    selectProduct(product, index) {
      console.log('Selected product:', product);
      this.formData.items[index].name = product.profile_name || product.grade;
      this.formData.items[index].gsm = product.gsm;
      this.formData.items[index].width = product.width;
      this.showProductDropdown = false;
    },
    selectProfile(profile, index) {
      this.formData.items[index].buyer = profile.customer_name;
      this.showProfileDropdown = false;
    },
    handleClickOutside(event) {
      const productInputs = document.querySelectorAll('.product-input');
      const profileInputs = document.querySelectorAll('.profile-input');
      const dropdowns = document.querySelectorAll('.dropdown-list');

      let clickedInsideProduct = false;
      let clickedInsideProfile = false;
      let clickedInsideDropdown = false;

      productInputs.forEach(input => {
        if (input.contains(event.target)) {
          clickedInsideProduct = true;
        }
      });

      profileInputs.forEach(input => {
        if (input.contains(event.target)) {
          clickedInsideProfile = true;
        }
      });

      dropdowns.forEach(dropdown => {
        if (dropdown.contains(event.target)) {
          clickedInsideDropdown = true;
        }
      });

      if (!clickedInsideProduct && !clickedInsideDropdown) {
        this.showProductDropdown = false;
      }

      if (!clickedInsideProfile && !clickedInsideDropdown) {
        this.showProfileDropdown = false;
      }
    }
  }
}
</script>

<style scoped>
@font-face {
  font-family: 'BDavat';
  src: url('../assets/fonts/BDavat.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}

.havaleh-form {
  max-width: 1200px;
  margin: 20px auto;
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  direction: rtl;
  font-family: 'BDavat', Arial, sans-serif !important;
}

h2 {
  text-align: center;
  color: #333;
  margin-bottom: 20px;
}

.form-header {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.form-group {
  flex: 1;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.items-table {
  margin: 20px 0;
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

th,
td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: right;
}

th {
  background-color: #f5f5f5;
  font-weight: bold;
}

input[type="text"],
input[type="number"] {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.remove-btn {
  background-color: #ff4444;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
}

.add-btn {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 20px;
}

.form-footer {
  margin-top: 20px;
}

.total-weight {
  margin: 20px 0;
  font-size: 1.2em;
  font-weight: bold;
}

.generate-btn {
  background-color: #2196F3;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1.1em;
}

button:hover {
  opacity: 0.9;
}

textarea {
  width: 100%;
  min-height: 100px;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  resize: vertical;
}

#pdf-template {
  font-family: 'BDavat', Arial, sans-serif !important;
  direction: rtl;
  font-size: 12pt;
  background: white;
  width: 190mm;
  min-height: 277mm;
  margin: 0;
  padding: 10mm;
  box-sizing: border-box;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#pdf-template .copy {
  width: 100%;
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 2px dashed #000;
}

#pdf-template .copy:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

#pdf-template .header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 10px;
  width: 100%;
}

#pdf-template .logo-section {
  width: 50px;
  text-align: right;
}

#pdf-template .logo-section img {
  width: 40px;
  height: 40px;
  object-fit: contain;
  display: block;
  margin-bottom: 2px;
}

#pdf-template .logo-section div {
  font-size: 9pt;
  text-align: center;
}

#pdf-template .company-info {
  flex: 1;
  text-align: center;
  margin: 0 5px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

#pdf-template .company-name {
  font-size: 12pt;
  font-weight: bold;
  margin-bottom: 2px;
  text-align: center;
  width: 100%;
}

#pdf-template .document-title {
  font-size: 10pt;
  margin-bottom: 0;
  text-align: center;
  width: 100%;
}

#pdf-template .document-info {
  width: 100px;
  text-align: center;
  font-size: 8pt;
  line-height: 1.5;
  display: flex;
  flex-direction: column;
  align-items: center;
}

#pdf-template .document-info div {
  text-align: center;
  width: 100%;
}

#pdf-template table {
  width: 100%;
  border-collapse: collapse;
  margin: 10px 0;
  font-size: 9pt;
  border: 1px solid #000;
}

#pdf-template th {
  background: #e9ecef;
  font-weight: bold;
  padding: 3mm 2mm;
  border: 1px solid #000;
  text-align: center;
  vertical-align: middle;
}

#pdf-template td {
  border: 1px solid #000;
  padding: 2mm;
  text-align: center;
  font-size: 9pt;
  vertical-align: middle;
}

#pdf-template .notes {
  margin: 10px 0;
  padding: 5px;
  border: 1px solid #000;
  font-size: 9pt;
  width: 100%;
  text-align: center;
  line-height: 1.5;
}

#pdf-template .notes div {
  text-align: center;
  width: 100%;
}

#pdf-template .footer {
  display: flex;
  justify-content: space-between;
  gap: 5px;
  margin-top: 10px;
  width: 100%;
}

#pdf-template .signature-line {
  flex: 1;
  text-align: center;
  border-top: 1px solid #000;
  padding-top: 2px;
  font-size: 8pt;
  display: flex;
  justify-content: center;
  align-items: center;
}

#pdf-template .total-row td {
  font-weight: bold;
  background: #f5f5f5;
  text-align: center;
}

#pdf-template .confirmation-text {
  text-align: center;
  font-size: 10pt;
  margin-top: 10px;
  padding: 5px;
  width: 100%;
}

@media print {
  @page {
    size: A4 portrait;
    margin: 0;
  }

  #pdf-template {
    width: 210mm !important;
    height: 297mm !important;
    max-width: 210mm !important;
    max-height: 297mm !important;
    min-width: 210mm !important;
    min-height: 297mm !important;
    padding: 10mm !important;
  }
}

.plate-input {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  justify-content: center;
  align-items: center;
  background: #f8f9fa;
  padding: 15px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.plate-input input,
.plate-input select {
  width: 90px;
  height: 70px;
  text-align: center;
  font-size: 28pt;
  padding: 8px;
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  background-color: #ffffff;
  transition: all 0.3s ease;
  font-family: 'BDavat', Arial, sans-serif;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.plate-input input:focus,
.plate-input select:focus {
  border-color: #2196F3;
  box-shadow: 0 0 0 3px rgba(33, 150, 243, 0.1);
  outline: none;
}

.plate-input input:hover,
.plate-input select:hover {
  border-color: #2196F3;
  transform: translateY(-1px);
}

.plate-input select {
  width: 110px;
  height: 70px;
  cursor: pointer;
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%232196F3' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 12px center;
  background-size: 20px;
  padding-right: 35px;
  text-align: center;
  font-size: 28pt;
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  background-color: #ffffff;
  font-family: 'BDavat', Arial, sans-serif;
  transition: all 0.3s ease;
}

.plate-input select option {
  font-size: 24pt;
  text-align: center;
  padding: 15px;
  height: 70px;
  line-height: 70px;
  font-family: 'BDavat', Arial, sans-serif;
  background-color: #ffffff;
  color: #333;
  border-bottom: 1px solid #f0f0f0;
  transition: all 0.2s ease;
}

.plate-input select option:hover {
  background-color: #f5f5f5;
}

.plate-input select option:first-child {
  color: #999;
  font-style: italic;
  background-color: #f8f9fa;
}

/* استایل برای dropdown در مرورگرهای مختلف */
.plate-input select::-ms-expand {
  display: none;
}

.plate-input select::-webkit-scrollbar {
  width: 10px;
}

.plate-input select::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 5px;
  margin: 5px;
}

.plate-input select::-webkit-scrollbar-thumb {
  background: #2196F3;
  border-radius: 5px;
  border: 2px solid #f1f1f1;
}

.plate-input select::-webkit-scrollbar-thumb:hover {
  background: #1976D2;
}

/* اضافه کردن انیمیشن برای hover */
.plate-input input:hover,
.plate-input select:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* اضافه کردن استایل برای حالت focus */
.plate-input input:focus,
.plate-input select:focus {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(33, 150, 243, 0.15);
}

/* اضافه کردن استایل برای حالت active */
.plate-input input:active,
.plate-input select:active {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* اضافه کردن استایل برای حالت disabled */
.plate-input input:disabled,
.plate-input select:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
  opacity: 0.7;
}

/* اضافه کردن استایل برای حالت placeholder */
.plate-input input::placeholder {
  color: #999;
  font-size: 20pt;
}

/* اضافه کردن استایل برای حالت readonly */
.plate-input input[readonly] {
  background-color: #f8f9fa;
  cursor: default;
}

/* اضافه کردن استایل برای حالت invalid */
.plate-input input:invalid,
.plate-input select:invalid {
  border-color: #ff4444;
  box-shadow: 0 0 0 3px rgba(255, 68, 68, 0.1);
}

/* اضافه کردن استایل برای حالت valid */
.plate-input input:valid,
.plate-input select:valid {
  border-color: #4CAF50;
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 17pt;
}

.input-with-dropdown {
  position: relative;
  width: 100%;
}

.dropdown-list {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  max-height: 200px;
  overflow-y: auto;
  z-index: 1000;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-top: 4px;
}

.dropdown-item {
  padding: 8px 12px;
  cursor: pointer;
  transition: background-color 0.2s;
  text-align: right;
  border-bottom: 1px solid #eee;
}

.dropdown-item:hover {
  background-color: #f5f5f5;
}

.product-input,
.profile-input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.error-message {
  color: #ff4444;
  text-align: center;
  padding: 10px;
  font-weight: bold;
}

/* اضافه کردن استایل برای preview پلاک */
:deep(.plate-preview) {
  font-size: 36pt !important;
  margin-top: 15px;
  padding: 10px 20px;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
  min-width: 300px;
  border: 2px solid #e0e0e0;
}

:deep(.plate-preview .plate-number) {
  font-size: 36pt !important;
  font-weight: bold;
  color: #333;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
}

:deep(.plate-preview .plate-letter) {
  font-size: 36pt !important;
  color: #2196F3;
  margin: 0 5px;
  font-weight: bold;
}

:deep(.plate-preview .plate-year) {
  font-size: 36pt !important;
  color: #4CAF50;
  font-weight: bold;
}

/* Mobile Responsive Styles */
@media screen and (max-width: 768px) {
  .havaleh-form {
    margin: 10px;
    padding: 10px;
    width: auto;
    overflow-x: hidden;
  }

  .form-header {
    flex-direction: column;
    gap: 10px;
  }

  .form-group {
    width: 100%;
  }

  .form-group input {
    width: 100%;
    font-size: 16px; /* Prevent zoom on iOS */
  }

  .items-table {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }

  table {
    min-width: 800px; /* Ensure table doesn't break on mobile */
  }

  .plate-input {
    flex-wrap: wrap;
    gap: 8px;
    padding: 10px;
  }

  .plate-input input,
  .plate-input select {
    width: 70px;
    height: 50px;
    font-size: 20pt;
  }

  .form-footer {
    flex-direction: column;
  }

  .form-footer .form-group {
    width: 100%;
  }

  .total-weight {
    text-align: center;
    margin: 15px 0;
  }

  .generate-btn {
    width: 100%;
    margin: 10px 0;
  }

  /* PDF Template Mobile Styles */
  #pdf-template {
    width: 100%;
    padding: 5mm;
  }

  #pdf-template .header {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  #pdf-template .logo-section {
    width: 100%;
    text-align: center;
    margin-bottom: 10px;
  }

  #pdf-template .company-info {
    margin: 10px 0;
  }

  #pdf-template .document-info {
    width: 100%;
    margin-top: 10px;
  }

  #pdf-template table {
    font-size: 8pt;
  }

  #pdf-template th,
  #pdf-template td {
    padding: 2mm;
  }

  #pdf-template .footer {
    flex-direction: column;
    gap: 10px;
  }

  #pdf-template .signature-line {
    width: 100%;
    margin-bottom: 10px;
  }
}

/* iPhone Specific Styles */
@supports (-webkit-touch-callout: none) {
  .form-group input,
  .plate-input input,
  .plate-input select {
    font-size: 16px; /* Prevent zoom on iOS */
  }

  .items-table {
    -webkit-overflow-scrolling: touch;
  }

  .dropdown-list {
    max-height: 200px;
    -webkit-overflow-scrolling: touch;
  }
}
</style>