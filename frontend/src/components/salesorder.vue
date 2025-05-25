<template>
  <div class="sales-order-container">
    <!-- Form section (unchanged) -->
    <form @submit.prevent="submitForm">
      <div class="form-row">
        <label>شماره فاکتور:</label>
        <input v-model="form.serial" required />
        <label>تاریخ:</label>
        <input v-model="form.date" required readonly />
      </div>
      <div class="form-row">
        <label>نام خریدار:</label>
        <input v-model="form.buyer_name" required />
        <label>شماره اقتصادی خریدار:</label>
        <input v-model="form.buyer_economic_code" />
        <label>شماره ثبت خریدار:</label>
        <input v-model="form.buyer_reg" />
        <label>کد ملی خریدار:</label>
        <input v-model="form.buyer_national_id" />
        <label>کد پستی خریدار:</label>
        <input v-model="form.buyer_postcode" />
        <label>نشانی خریدار:</label>
        <input v-model="form.buyer_address" />
        <label>تلفن خریدار:</label>
        <input v-model="form.buyer_phone" />
      </div>
      <div class="form-row">
        <label>نام فروشنده:</label>
        <input v-model="form.seller_name" readonly />
        <label>شماره اقتصادی فروشنده:</label>
        <input v-model="form.seller_economic_code" readonly />
        <label>شماره ثبت فروشنده:</label>
        <input v-model="form.seller_reg" readonly />
        <label>کد پستی فروشنده:</label>
        <input v-model="form.seller_postcode" readonly />
        <label>شناسه ملی فروشنده:</label>
        <input v-model="form.seller_national_id" readonly />
        <label>نشانی فروشنده:</label>
        <input v-model="form.seller_address" readonly />
        <label>تلفن فروشنده:</label>
        <input v-model="form.seller_phone" readonly />
      </div>
      <table class="input-table">
        <thead>
          <tr>
            <th>کد کالا</th>
            <th>شرح کالا</th>
            <th>مقدار</th>
            <th>واحد</th>
            <th>مبلغ واحد (ریال)</th>
            <th>مبلغ کل (ریال)</th>
            <th>جمع مالیات و عوارض ۱۰٪</th>
            <th>جمع مبلغ کل و مالیات</th>
            <th>حذف</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, idx) in form.items" :key="idx">
            <td><input v-model="item.description" /></td>
            <td><input v-model="item.code" /></td>
            <td><input type="number" v-model.number="item.quantity" @input="updateTotal(item)" min="0" step="1" /></td>
            <td><input v-model="item.unit" /></td>
            <td><input type="number" v-model.number="item.price" @input="updateTotal(item)" min="0" step="1" /></td>
            <td>{{ formatNumber(item.total) }}</td>
            <td>{{ formatNumber(rowTax(item)) }}</td>
            <td>{{ formatNumber(rowWithTax(item)) }}</td>
            <td><button type="button" @click="removeItem(idx)">-</button></td>
          </tr>
        </tbody>
      </table>
      <div class="form-actions">
        <button type="button" class="btn-action" @click="addItem">افزودن ردیف</button>
        <button type="button" class="btn-action view-btn" @click="showLastSales">دیدن ۱۰ فروش آخر</button>
        <button type="submit" class="btn-action preview-btn">پیش نمایش</button>
      </div>
    </form>

    <!-- Last Sales Modal -->
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <div class="modal-header">
          <h2>۱۰ فروش آخر</h2>
          <button class="close-button" @click="closeModal">&times;</button>
        </div>
        <div class="modal-body">
          <table class="modal-table">
            <thead>
              <tr>
                <th>تاریخ</th>
                <th>شماره فاکتور</th>
                <th>نام خریدار</th>
                <th>شماره اقتصادی</th>
                <th>شماره ثبت</th>
                <th>کد ملی</th>
                <th>کد پستی</th>
                <th>نشانی</th>
                <th>تلفن</th>
                <th>تعداد اقلام</th>
                <th>مبلغ کل</th>
                <th>عملیات</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="sale in lastSales" :key="sale.id">
                <td>{{ sale.date }}</td>
                <td>{{ sale.serial }}</td>
                <td>{{ sale.buyer_name }}</td>
                <td>{{ sale.buyer_economic_code }}</td>
                <td>{{ sale.buyer_reg }}</td>
                <td>{{ sale.buyer_national_id }}</td>
                <td>{{ sale.buyer_postcode }}</td>
                <td>{{ sale.buyer_address }}</td>
                <td>{{ sale.buyer_phone }}</td>
                <td>{{ sale.items.length }}</td>
                <td>{{ formatNumber(sale.total_amount) }}</td>
                <td>
                  <button @click="selectSale(sale)" class="select-button">انتخاب</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Invoice Preview for PDF -->
    <div ref="pdfPreview" v-if="showData" class="pdf-preview">
      <div class="invoice-container">
        <!-- شماره و تاریخ بالا سمت چپ -->
        <div class="header-row">
          <div class="fact-info fact-info-box">
            شماره فاکتور: {{ form.serial || '-' }}<br>
            تاریخ: {{ form.date || '-' }}<br>
            ساعت: {{ form.time || '-' }}
          </div>
        </div>
        <div class="invoice-title">صورت حساب فروش کالا</div>

        <!-- جدول مشخصات فروشنده -->
        <table class="info-table">
          <tr>
            <th colspan="6" class="section-title">مشخصات فروشنده</th>
          </tr>
          <tr>
            <td>نام شرکت</td>
            <td>کد اقتصادی</td>
            <td>شماره ثبت</td>
            <td>شناسه ملی</td>
            <td>کد پستی</td>
            <td>تلفن</td>
          </tr>
          <tr>
            <td>{{ form.seller_name }}</td>
            <td>{{ form.seller_economic_code }}</td>
            <td>{{ form.seller_reg }}</td>
            <td>{{ form.seller_national_id }}</td>
            <td>{{ form.seller_postcode }}</td>
            <td>{{ form.seller_phone }}</td>
          </tr>
          <tr>
            <td colspan="6"><b>نشانی:</b> {{ form.seller_address }}</td>
          </tr>
        </table>

        <!-- جدول مشخصات خریدار -->
        <table class="info-table" style="margin-top: 18px;">
          <tr>
            <th colspan="7" class="section-title">مشخصات خریدار</th>
          </tr>
          <tr>
            <td>نام</td>
            <td>شماره اقتصادی</td>
            <td>شماره ثبت</td>
            <td>کد ملی</td>
            <td>کد پستی</td>
            <td>تلفن</td>
          </tr>
          <tr>
            <td>{{ form.buyer_name || '-' }}</td>
            <td>{{ form.buyer_economic_code || '-' }}</td>
            <td>{{ form.buyer_reg || '-' }}</td>
            <td>{{ form.buyer_national_id || '-' }}</td>
            <td>{{ form.buyer_postcode || '-' }}</td>
            <td>{{ form.buyer_phone || '-' }}</td>
          </tr>
          <tr>
            <td colspan="7"><b>نشانی:</b> {{ form.buyer_address || '-' }}</td>
          </tr>
        </table>

        <!-- جدول کالاها و جمع کل و مالیات و ... (بدون تغییر) -->
        <table class="details-table" style="margin-top: 18px;">
          <thead>
            <tr>
              <th>ردیف</th>
              <th>کد کالا</th>
              <th>شرح کالا</th>
              <th>مقدار</th>
              <th>واحد</th>
              <th>مبلغ واحد (ریال)</th>
              <th>مبلغ کل (ریال)</th>
              <th>جمع مالیات و عوارض ۱۰٪</th>
              <th>جمع مبلغ کل و مالیات</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, idx) in form.items" :key="idx">
              <td>{{ idx + 1 }}</td>
              <td>{{ item.code }}</td>
              <td>{{ item.description }}</td>
              <td>{{ item.quantity }}</td>
              <td>{{ item.unit }}</td>
              <td>{{ formatNumber(item.price) }}</td>
              <td>{{ formatNumber(item.total) }}</td>
              <td>{{ formatNumber(rowTax(item)) }}</td>
              <td>{{ formatNumber(rowWithTax(item)) }}</td>
            </tr>
          </tbody>
          <tfoot>
            <tr class="total-row">
              <td colspan="6" style="text-align: center;">جمع کل</td>
              <td>{{ formatNumber(totalAmount) }}</td>
              <td>{{ formatNumber(totalTax) }}</td>
              <td>{{ formatNumber(totalWithTax) }}</td>
            </tr>
          </tfoot>
        </table>

        <!-- بخش پایانی فاکتور -->
        <table class="footer-table standard-bordered-table">
          <tr>
            <!-- ستون سمت راست: مهر و امضاءها (در یک ردیف کنار هم) -->
            <td class="footer-signs">
              <div class="signs-row">
                <div class="sign-box">مهر و امضاء خریدار</div>
                <div class="sign-box">مهر و امضاء فروشنده</div>
              </div>
            </td>
            <!-- ستون سمت چپ: مبالغ -->
            <td class="footer-amounts">
              <div class="amount-in-number">
                مبلغ قابل پرداخت به عدد: {{ formatNumber(totalWithTax) }}
              </div>
              <div class="amount-separator"></div>
              <div class="amount-in-words">
                مبلغ قابل پرداخت به حروف: {{ totalWithTaxInWords }}
              </div>
            </td>
          </tr>
        </table>
      </div>
    </div>
    <button type="button" @click="printPreview" v-if="showData">دریافت PDF</button>
  </div>
</template>

<script>
import jalaali from 'jalaali-js';
import num2persian from "@/utils/num2persian";
import axios from 'axios';

// Configure axios
axios.defaults.baseURL = 'http://localhost:8000';

export default {
  name: 'SalesOrder',
  data() {
    return {
      form: {
        serial: '',
        date: '',
        time: '',
        buyer_name: '',
        buyer_economic_code: '',
        buyer_reg: '',
        buyer_postcode: '',
        buyer_phone: '',
        buyer_national_id: '',
        buyer_address: '',
        seller_name: 'شرکت همایون',
        seller_economic_code: '1234567890',
        seller_reg: '12345',
        seller_national_id: '1234567890',
        seller_postcode: '1234567890',
        seller_address: 'تهران',
        seller_phone: '02112345678',
        items: [
          { description: '', code: '', quantity: 1, unit: '', price: 0, total: 0 }
        ]
      },
      showData: false,
      showModal: false,
      lastSales: []
    }
  },
  computed: {
    totalAmount() {
      return this.form.items.reduce((sum, item) => sum + Number(item.total || 0), 0);
    },
    totalTax() {
      return this.form.items.reduce((sum, item) => sum + Math.round((item.total || 0) * 0.10), 0);
    },
    totalWithTax() {
      return this.totalAmount + this.totalTax;
    },
    totalWithTaxInWords() {
      return num2persian(this.totalWithTax) + " ریال";
    }
  },
  methods: {
    getToday() {
      const today = new Date();
      const y = today.getFullYear();
      const m = String(today.getMonth() + 1).padStart(2, '0');
      const d = String(today.getDate()).padStart(2, '0');
      return `${y}/${m}/${d}`;
    },
    getTodayJalali() {
      const today = new Date();
      const { jy, jm, jd } = jalaali.toJalaali(today);
      return `${jy}/${String(jm).padStart(2, '0')}/${String(jd).padStart(2, '0')}`;
    },
    getCurrentTime() {
      const now = new Date();
      now.setMinutes(now.getMinutes() + 60);
      const h = String(now.getHours()).padStart(2, '0');
      const m = String(now.getMinutes()).padStart(2, '0');
      return `${h}:${m}`;
    },
    updateTotal(item) {
      item.total = (parseFloat(item.quantity) || 0) * (parseFloat(item.price) || 0);
    },
    addItem() {
      this.form.items.push({ description: '', code: '', quantity: 1, unit: '', price: 0, total: 0 });
    },
    removeItem(idx) {
      this.form.items.splice(idx, 1);
    },
    submitForm() {
      this.form.date = this.getTodayJalali();
      this.form.time = this.getCurrentTime();
      this.showData = true;
    },
    formatNumber(val) {
      if (val == null || val === '') return '';
      return Number(val).toLocaleString('en-US', { minimumFractionDigits: 0 });
    },
    printPreview() {
      window.print();
    },
    rowTax(item) {
      return Math.round((item.total || 0) * 0.10);
    },
    rowWithTax(item) {
      return Number(item.total || 0) + this.rowTax(item);
    },
    async showLastSales() {
      try {
        const response = await axios.get('/invoice/api/get_last_10_sales/');
        console.log('API Response:', response.data);
        this.lastSales = response.data;
        this.showModal = true;
      } catch (error) {
        console.error('Error details:', error.response || error);
        alert('خطا در دریافت اطلاعات فروش‌های اخیر');
      }
    },
    selectSale(sale) {
      // Fill form with selected sale data
      this.form.serial = sale.serial;
      this.form.buyer_name = sale.buyer_name;
      this.form.buyer_economic_code = sale.buyer_economic_code;
      this.form.buyer_reg = sale.buyer_reg;
      this.form.buyer_national_id = sale.buyer_national_id;
      this.form.buyer_postcode = sale.buyer_postcode;
      this.form.buyer_address = sale.buyer_address;
      this.form.buyer_phone = sale.buyer_phone;

      // Fill items with all details
      this.form.items = sale.items.map(item => ({
        description: item.description,
        code: item.code || '',
        quantity: item.quantity,
        unit: item.unit,
        price: item.price,
        total: item.total
      }));

      this.closeModal();
    },
    closeModal() {
      this.showModal = false;
    }
  },
  created() {
    this.form.date = this.getTodayJalali();
    this.form.time = this.getCurrentTime();
  }
}
</script>

<style scoped>
@font-face {
  font-family: 'BDavat';
  src: url('@/assets/fonts/BDavat.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
}

.sales-order-container {
  max-width: 1200px;
  margin: 20px auto;
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  direction: rtl;
  font-family: 'BDavat', Arial, sans-serif;
}

.form-row {
  display: flex;
  gap: 15px;
  margin-bottom: 15px;
  flex-wrap: wrap;
}

.form-row label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #333;
}

.form-row input {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  width: 200px;
}

.input-table {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
  background: #fff;
}

.input-table th,
.input-table td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: center;
}

.input-table th {
  background-color: #f5f5f5;
  font-weight: bold;
}

.input-table input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.input-table input[type="number"] {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.input-table input[type="number"]::-webkit-outer-spin-button,
.input-table input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.preview-btn {
  background-color: #FF9800;
  color: white;
}

.pdf-preview {
  width: 1120px;
  max-width: 100vw;
  margin-left: auto;
  margin-right: auto;
  margin-top: 30px;
  background: #fff;
  padding: 12px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  font-size: 0.95em;
}

.invoice-container {
  width: 100%;
  margin: 30px auto;
  border: 2.5px solid #444;
  padding: 10px 8px 20px 8px;
  background: #fff;
  box-sizing: border-box;
  min-height: 900px;
  position: relative;
  font-size: 0.95em;
}

.header-row {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  margin-bottom: 10px;
}

.header-row .fact-info {
  font-size: 1em;
  margin-left: 30px;
  text-align: left;
}

.invoice-title {
  text-align: center;
  font-size: 1.6em;
  font-weight: bold;
  margin-top: 6px;
  margin-bottom: 10px;
  letter-spacing: 1px;
}

.party-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 18px;
}

.party-box {
  width: 49%;
  border: 1.5px solid #444;
  border-radius: 6px;
  padding: 10px 14px;
  background: #f7f7f7;
  font-size: 1em;
}

.party-title {
  font-weight: bold;
  margin-bottom: 6px;
  color: #222;
}

.party-box span {
  display: inline-block;
  min-width: 90px;
  font-weight: bold;
}

.details-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 0;
}

.details-table th,
.details-table td {
  border: 1.5px solid #444;
  padding: 5px 3px;
  text-align: center;
  font-size: 0.95em;
}

.details-table th {
  background: #e9ecef;
  font-weight: bold;
}

.details-table .total-row td {
  font-weight: bold;
  background: #f5f5f5;
  border-top: 2.5px solid #444;
  font-size: 1.1em;
}

.footer-section {
  margin-top: 30px;
  width: 100%;
}

.footer-section .amount-in-words {
  margin-bottom: 18px;
  font-size: 1em;
}

.footer-section .signatures {
  display: flex;
  justify-content: flex-end;
  gap: 60px;
  margin-top: 30px;
}

.footer-section .sign-box {
  border-top: 1.5px solid #444;
  width: 180px;
  text-align: center;
  padding-top: 8px;
  font-size: 1em;
}

/* Button Styles */
button {
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  border-radius: 4px;
  font-size: 1em;
  padding: 10px 20px;
  margin: 10px 0;
}

/* Add Row Button */
button[type="button"]:not(.preview-btn):not([v-if="showData"]) {
  background-color: #4CAF50;
  color: white;
}

button[type="button"]:not(.preview-btn):not([v-if="showData"]):hover {
  background-color: #45a049;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

/* Download PDF Button */
button[type="button"][v-if="showData"] {
  background-color: #2196F3;
  color: white;
  font-size: 1.1em;
  padding: 12px 24px;
  margin: 20px 0;
}

button[type="button"][v-if="showData"]:hover {
  background-color: #1976D2;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

/* Remove Item Button */
.input-table button {
  background-color: #ff4444;
  color: white;
  padding: 6px 12px;
  margin: 0;
  font-size: 0.9em;
}

.input-table button:hover {
  background-color: #cc0000;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

@media print {
  @page {
    size: A4 landscape;
    margin: 0;
  }

  body * {
    visibility: hidden;
  }

  .pdf-preview,
  .pdf-preview * {
    visibility: visible;
  }

  .pdf-preview {
    position: absolute;
    left: 0;
    top: 0;
    width: 297mm !important;
    height: 210mm !important;
    max-width: 297mm !important;
    max-height: 210mm !important;
    min-width: 297mm !important;
    min-height: 210mm !important;
    background: white !important;
    box-shadow: none !important;
    overflow: hidden !important;
    padding: 0 !important;
    margin: 0 !important;
    font-family: 'BDavat', Arial, sans-serif !important;
  }

  button,
  .form-actions,
  form {
    display: none !important;
  }

  .pdf-preview,
  .invoice-container,
  .details-table,
  .info-table,
  .footer-table {
    page-break-inside: avoid !important;
    break-inside: avoid !important;
    font-family: 'BDavat', Arial, sans-serif !important;
  }

  .pdf-preview,
  .invoice-container {
    font-size: 0.9em !important;
  }

  body,
  .pdf-preview,
  .invoice-container,
  .info-table,
  .details-table,
  .footer-table,
  .fact-info-box {
    font-family: 'BDavat', Arial, sans-serif !important;
  }

  .invoice-title {
    margin-top: 0 !important;
    margin-bottom: 2px !important;
  }

  .header-row {
    margin-top: 8px !important;
    margin-bottom: 2px !important;
  }

  .info-table {
    margin-top: 2px !important;
    margin-bottom: 2px !important;
  }

  .details-table {
    margin-top: 4px !important;
  }

  .invoice-container {
    padding-top: 4px !important;
    padding-bottom: 8px !important;
    margin-top: 0 !important;
  }

  .header-row,
  .invoice-title,
  .info-table,
  .details-table {
    margin-top: 0 !important;
    margin-bottom: 0 !important;
  }

  .invoice-container {
    padding-top: 0 !important;
    padding-bottom: 4px !important;
    margin-top: 0 !important;
  }

  .details-table th {
    background: #d1d1d1 !important;
  }

  .info-table .section-title {
    background: #d1d1d1 !important;
  }
}

.main-invoice-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  border: 2.5px solid #444;
  background: #fff;
  margin: 0 auto;
  font-size: 1em;
}

.section-title {
  font-weight: bold;
  font-size: 1.1em;
  margin-bottom: 8px;
  color: #222;
  text-align: right;
}

.info-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 0;
  border: 2.5px solid #444;
  background: #fff;
  margin-top: 18px;
}

.info-table th,
.info-table td {
  border: 1.5px solid #444;
  padding: 5px 3px;
  font-size: 0.95em;
  text-align: center;
  vertical-align: middle;
}

.info-table .section-title {
  background: #f2f2f2;
  font-weight: bold;
  text-align: center;
  font-size: 1.1em;
}

.fact-date-section {
  vertical-align: top;
  width: 220px;
  min-width: 180px;
}

.fact-box {
  border: 1.5px solid #444;
  border-radius: 8px;
  padding: 12px 18px;
  margin: 10px 0 0 0;
  background: #f7f7f7;
  font-size: 1.1em;
  text-align: right;
}

.seller-section,
.buyer-section {
  width: 50%;
  vertical-align: top;
  padding: 0 8px;
}

.details-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 16px;
}

.details-table th,
.details-table td {
  border: 1.5px solid #444;
  padding: 5px 3px;
  text-align: center;
}

.details-table th {
  background: #e9ecef;
  font-weight: bold;
}

.details-table .total-row td {
  font-weight: bold;
  background: #f5f5f5;
  border-top: 2.5px solid #444;
  font-size: 1.1em;
}

.footer-section {
  margin-top: 30px;
  width: 100%;
}

.footer-section .amount-in-words {
  margin-bottom: 18px;
  font-size: 1em;
}

.footer-section .signatures {
  display: flex;
  justify-content: flex-end;
  gap: 60px;
  margin-top: 30px;
}

.footer-section .sign-box {
  border-top: 1.5px solid #444;
  width: 180px;
  text-align: center;
  padding-top: 8px;
  font-size: 1em;
}

.signatures-row {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 18px;
  margin-top: 40px;
}

.signatures-row .sign-box {
  border-top: 1.5px solid #444;
  width: 220px;
  text-align: right;
  padding-top: 8px;
  font-size: 1em;
  margin-bottom: 10px;
}

.amount-in-number,
.amount-in-words {
  font-size: 1.1em;
  margin-top: 18px;
  text-align: right;
  font-weight: bold;
}

.footer-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  margin-top: 0;
  margin-bottom: 0;
}

.footer-table td {
  vertical-align: top;
  padding: 18px 12px 12px 12px;
}

.footer-signs {
  width: 40%;
  min-width: 220px;
}

.footer-amounts {
  width: 60%;
  text-align: left;
  vertical-align: top;
}

.footer-signs .sign-box {
  border-top: none;
  width: 160px;
  text-align: center;
  padding-top: 8px;
  font-size: 1em;
  margin-bottom: 0;
}

.footer-amounts .amount-in-number,
.footer-amounts .amount-in-words {
  font-size: 1.1em;
  margin-bottom: 18px;
  text-align: right;
  font-weight: bold;
}

.footer-table.standard-bordered-table {
  width: 100%;
  border-collapse: collapse;
  border: 2.5px solid #444;
  margin-top: 0;
  margin-bottom: 0;
  direction: rtl;
  background: #fff;
}

.footer-table.standard-bordered-table td {
  border: 1.5px solid #444;
  vertical-align: top;
  padding: 18px 12px 12px 12px;
  text-align: right;
  background: #fff;
}

.footer-signs .signs-row {
  display: flex;
  flex-direction: row;
  gap: 40px;
  justify-content: flex-start;
  align-items: center;
  margin-bottom: 0;
}

.footer-signs .sign-box {
  /* حذف خط بالای هر sign-box */
  border-top: none;
  width: 160px;
  text-align: center;
  padding-top: 8px;
  font-size: 1em;
  margin-bottom: 0;
}

.amount-separator {
  border-top: 1.5px solid #444;
  margin: 12px 0;
  width: 100%;
}

.fact-info-box {
  border: 2.5px solid #444;
  border-radius: 8px;
  padding: 12px 18px;
  background: #fff;
  font-size: 1.1em;
  text-align: right;
  direction: rtl;
  display: inline-block;
  min-width: 220px;
  margin-bottom: 10px;
}

.form-actions {
  display: flex;
  justify-content: center;
  gap: 24px;
  margin-top: 16px;
  margin-bottom: 8px;
}

.btn-action {
  min-width: 140px;
  min-height: 48px;
  padding: 12px 24px;
  font-size: 1.1em;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  display: inline-block;
  box-sizing: border-box;
}

.view-btn {
  background-color: #607D8B;
  color: white;
}

.view-btn:hover {
  background-color: #546E7A;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  width: 95%;
  max-width: 1400px;
  max-height: 80vh;
  overflow-y: auto;
  position: relative;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.modal-header h2 {
  margin: 0;
  color: #333;
  font-size: 1.5em;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5em;
  cursor: pointer;
  color: #666;
  padding: 5px;
}

.close-button:hover {
  color: #333;
}

.modal-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
  font-size: 0.9em;
}

.modal-table th,
.modal-table td {
  padding: 8px;
  text-align: right;
  border-bottom: 1px solid #eee;
  white-space: nowrap;
}

.modal-table th {
  background-color: #f8f9fa;
  font-weight: bold;
  color: #333;
  position: sticky;
  top: 0;
  z-index: 1;
}

.modal-table td {
  max-width: 150px;
  overflow: hidden;
  text-overflow: ellipsis;
}

.modal-table tr:hover {
  background-color: #f5f5f5;
}

.modal-table td:last-child {
  white-space: nowrap;
  min-width: 80px;
}

.select-button {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9em;
}

.select-button:hover {
  background-color: #45a049;
}

/* Mobile Responsive Styles */
@media screen and (max-width: 768px) {
  .sales-order-container {
    margin: 10px;
    padding: 10px;
    width: auto;
    overflow-x: hidden;
  }

  .form-row {
    flex-direction: column;
    gap: 10px;
  }

  .form-row input {
    width: 100%;
    font-size: 16px;
    /* Prevent zoom on iOS */
  }

  .input-table {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }

  .input-table table {
    min-width: 1000px;
    /* Ensure table doesn't break on mobile */
  }

  .form-actions {
    flex-direction: column;
    gap: 10px;
  }

  .btn-action {
    width: 100%;
    margin: 5px 0;
  }

  /* Modal Mobile Styles */
  .modal-content {
    width: 95%;
    margin: 10px;
    padding: 10px;
    max-height: 90vh;
  }

  .modal-table {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }

  .modal-table table {
    min-width: 1000px;
  }

  /* PDF Preview Mobile Styles */
  .pdf-preview {
    width: 100%;
    margin: 10px 0;
    padding: 5px;
  }

  .invoice-container {
    padding: 5px;
    margin: 10px 0;
  }

  .header-row {
    flex-direction: column;
    align-items: center;
  }

  .fact-info-box {
    width: 100%;
    margin: 5px 0;
  }

  .info-table,
  .details-table {
    font-size: 0.8em;
  }

  .footer-table.standard-bordered-table {
    font-size: 0.8em;
  }

  .footer-table td {
    padding: 10px 5px;
  }

  .footer-signs .signs-row {
    flex-direction: column;
    gap: 20px;
  }

  .footer-signs .sign-box {
    width: 100%;
  }
}

/* iPhone Specific Styles */
@supports (-webkit-touch-callout: none) {

  .form-row input,
  .input-table input {
    font-size: 16px;
    /* Prevent zoom on iOS */
  }

  .input-table,
  .modal-table {
    -webkit-overflow-scrolling: touch;
  }

  .modal-content {
    -webkit-overflow-scrolling: touch;
  }

  .pdf-preview {
    -webkit-overflow-scrolling: touch;
  }
}
</style>