<template>
  <div class="sales-order-container">
    <div v-if="loading" class="loading">
      در حال بارگذاری...
    </div>
    
    <div v-else-if="error" class="error">
      {{ error }}
    </div>
    
    <div v-if="!loading && !confirmed && error" class="refresh-container">
      <button @click="fetchLatestSale" class="refresh-btn">
        بارگذاری مجدد
      </button>
    </div>
    
    <div v-else-if="!saleData" class="no-data">
      فاکتور جدیدی برای تأیید وجود ندارد.
    </div>
    
    <div v-else>
      <!-- Invoice Preview -->
      <div ref="pdfPreview" class="pdf-preview">
        <div class="invoice-main">
          <div class="invoice-title">صورت حساب فروش کالا</div>
          <table class="invoice-details-table">
            <tr>
              <td class="detail-title">مشخصات فروشنده</td>
              <td>نام فروشنده: {{ form.seller_name }}</td>
              <td>شماره اقتصادی: {{ form.seller_economic_code }}</td>
              <td>شماره ثبت: {{ form.seller_reg }}</td>
              <td>کد پستی: {{ form.seller_postcode }}</td>
              <td>تلفن: {{ form.seller_phone }}</td>
            </tr>
            <tr>
              <td class="detail-title">مشخصات خریدار</td>
              <td>نام خریدار: {{ form.buyer_name }}</td>
              <td>شماره اقتصادی: {{ form.buyer_economic_code }}</td>
              <td>شماره ثبت: {{ form.buyer_reg }}</td>
              <td>کد پستی: {{ form.buyer_postcode }}</td>
              <td>تلفن: {{ form.buyer_phone }}</td>
            </tr>
            <tr>
              <td class="detail-title">شماره فاکتور</td>
              <td colspan="2">{{ form.serial || saleData.id }}</td>
              <td class="detail-title">تاریخ</td>
              <td colspan="2">{{ form.date }}</td>
            </tr>
          </table>
          <table class="invoice-table">
            <thead>
              <tr>
                <th>شرح کالا</th>
                <th>کد کالا</th>
                <th>تعداد</th>
                <th>واحد</th>
                <th>مبلغ واحد</th>
                <th>مبلغ کل</th>
                <th>ملاحظات</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in form.items" :key="item.code + item.description">
                <td>{{ item.description }}</td>
                <td>{{ item.code }}</td>
                <td>{{ item.quantity }}</td>
                <td>{{ item.unit }}</td>
                <td>{{ formatNumber(item.price) }}</td>
                <td>{{ formatNumber(item.total) }}</td>
                <td>{{ item.comment }}</td>
              </tr>
              <tr>
                <td colspan="5" class="total-label">جمع کل</td>
                <td colspan="2" class="total-value">{{ formatNumber(totalAmount) }}</td>
              </tr>
            </tbody>
          </table>
          <div class="footer-row">
            <div>مبلغ قابل پرداخت به حروف و عدد: {{ formatNumber(totalAmount) }}</div>
            <div>
              <span>امضا خریدار:</span> ....................................
              <span style="margin-right:40px;">امضا فروشنده:</span> ....................................
            </div>
          </div>
        </div>
      </div>
      
      <div class="button-container">
        <!-- Only show confirm button if invoice_status is 'NA' -->
        <button 
          v-if="!confirmed" 
          type="button" 
          @click="confirmInvoice" 
          class="confirm-btn"
          :disabled="confirming"
        >
          {{ confirming ? 'در حال تایید...' : 'تایید فاکتور' }}
        </button>
        
        <!-- Only show download PDF button after confirmation -->
        <button 
          v-if="confirmed" 
          type="button" 
          @click="downloadPDF" 
          class="download-btn"
        >
          دریافت PDF
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import html2pdf from "html2pdf.js";
import axios from 'axios';

export default {
  name: 'SalesOrder',
  data() {
    return {
      loading: true,
      error: null,
      saleData: null,
      confirming: false,
      confirmed: false,
      form: {
        serial: '',
        date: '',
        buyer_name: '',
        buyer_economic_code: '',
        buyer_reg: '',
        buyer_postcode: '',
        buyer_phone: '',
        seller_name: 'شرکت تولیدی کاغذ و مقوای همایون',
        seller_economic_code: '',
        seller_reg: '',
        seller_postcode: '',
        seller_phone: '',
        items: []
      }
    }
  },
  computed: {
    totalAmount() {
      return this.form.items.reduce((sum, item) => sum + Number(item.total || 0), 0);
    },
    saleId() {
      return this.saleData ? this.saleData.id : null;
    }
  },
  mounted() {
    this.fetchLatestSale();
  },
  methods: {
    async fetchLatestSale() {
      try {
        this.loading = true;
        this.error = null;
        
        console.log("Fetching latest pending sale from API...");
        
        // First try the simple endpoint to check if basic API works
        try {
          const testResponse = await axios.get('/api/test-endpoint/');
          console.log("Test API response:", testResponse.data);
        } catch (testErr) {
          console.error("Test API failed:", testErr);
        }
        
        // Get the latest sale with invoice_status = 'NA'
        const response = await axios.get('/api/latest-pending-sale/');
        console.log("Received API response:", response);
        
        if (response.data && response.data.id) {
          this.saleData = response.data;
          this.populateFormFromSale(response.data);
          this.confirmed = this.saleData.invoice_status === 'Sent';
        } else {
          this.error = 'فاکتور جدیدی برای تایید وجود ندارد.';
        }
      } catch (err) {
        console.error('Error fetching sale data:', err);
        this.error = err.response?.data?.message || err.response?.data?.error || 'خطا در بارگیری اطلاعات فاکتور';
        
        // Try the simple version as a fallback
        try {
          console.log("Trying simple API as fallback...");
          const simpleResponse = await axios.get('/api/simple-latest-pending-sale/');
          if (simpleResponse.data && simpleResponse.data.id) {
            this.saleData = simpleResponse.data;
            // Create a minimal form with just the available data
            this.form.serial = `S-${simpleResponse.data.id}`;
            this.form.date = String(simpleResponse.data.date).split('T')[0] || '';
            this.form.buyer_name = 'مشتری';
            this.form.items = [{
              description: 'محصول',
              code: '',
              quantity: 1,
              unit: 'عدد',
              price: 0,
              total: 0,
              comment: ''
            }];
            this.confirmed = this.saleData.invoice_status === 'Sent';
            this.error = 'اطلاعات ناقص است، تنها برخی از اطلاعات نمایش داده می‌شود.';
          } else {
            this.error = 'فاکتور جدیدی برای تایید وجود ندارد.';
          }
        } catch (simpleErr) {
          console.error('Fallback API also failed:', simpleErr);
          // Keep the original error
        }
      } finally {
        this.loading = false;
      }
    },
    
    populateFormFromSale(sale) {
      // Safer date conversion with fallback
      let formattedDate;
      try {
        const saleDate = sale.date ? new Date(sale.date) : new Date();
        formattedDate = saleDate.toLocaleDateString('fa-IR');
      } catch (e) {
        formattedDate = String(sale.date).split('T')[0] || '';
      }
      
      // Populate form safely with fallbacks
      this.form.serial = sale.invoice_number || `S-${sale.id}`;
      this.form.date = formattedDate;
      this.form.buyer_name = sale.customer_name || '';
      
      // Safely access customer data with optional chaining
      if (sale.customer) {
        this.form.buyer_economic_code = sale.customer.economic_code || '';
        this.form.buyer_reg = '';  // Not included in the model
        this.form.buyer_postcode = sale.customer.postcode || '';
        this.form.buyer_phone = sale.customer.phone || '';
      }
      
      // Create items array safely
      if (sale.shipment) {
        this.form.items = [{
          description: sale.shipment.material_name || 'محصول',
          code: sale.shipment.purchase_id || '',
          quantity: sale.shipment.quantity || 1,
          unit: sale.shipment.unit || 'عدد',
          price: sale.price_per_kg || 0,
          total: sale.total_price || 0,
          comment: ''
        }];
      } else {
        this.form.items = [{
          description: 'محصول',
          code: '',
          quantity: 1,
          unit: 'عدد',
          price: sale.price_per_kg || 0,
          total: sale.total_price || 0,
          comment: ''
        }];
      }
    },
    
    formatNumber(val) {
      if (val == null || val === '') return '';
      return Number(val).toLocaleString('fa-IR', { minimumFractionDigits: 0 });
    },
    
    async confirmInvoice() {
      if (!this.saleId) {
        this.error = 'خطا: شناسه فاکتور یافت نشد.';
        return;
      }
      
      try {
        this.confirming = true;
        this.error = null; // Clear any previous errors
        
        console.log(`Confirming invoice with ID: ${this.saleId}`);
        
        const response = await axios.post(`/api/confirm-sales-invoice/${this.saleId}/`);
        console.log("Confirmation response:", response);
        
        if (response.data && response.data.status === 'success') {
          console.log("Invoice confirmed successfully");
          this.confirmed = true;
          this.saleData.invoice_status = 'Sent';
        } else {
          console.error("Unexpected response format:", response.data);
          this.error = response.data?.message || 'خطا در تایید فاکتور: پاسخ نامعتبر';
        }
      } catch (err) {
        console.error('Error confirming invoice:', err);
        let errorMessage = 'خطا در تایید فاکتور';
        
        if (err.response) {
          console.error("Error response data:", err.response.data);
          errorMessage = err.response.data?.message || err.response.data?.error || `خطا با کد ${err.response.status}`;
        }
        
        this.error = errorMessage;
      } finally {
        this.confirming = false;
      }
    },
    
    async downloadPDF() {
      try {
        await this.$nextTick();
        const options = {
          margin: 0.2,
          filename: `sales_order_${this.form.serial}.pdf`,
          html2canvas: { scale: 2 },
          jsPDF: { orientation: "landscape", unit: "mm", format: "a4" }
        };
        
        await html2pdf().from(this.$refs.pdfPreview).set(options).save();
      } catch (err) {
        console.error('Error generating PDF:', err);
        alert('خطا در ساخت فایل PDF. لطفا مجدد تلاش کنید.');
      }
    }
  }
}
</script>

<style scoped>
.sales-order-container {
  max-width: 1100px;
  margin: 0 auto;
  direction: rtl;
  font-family: Tahoma, Arial, sans-serif;
  background: #fafbfc;
  padding: 20px;
}
.loading, .error, .no-data {
  text-align: center;
  padding: 50px;
  font-size: 1.2em;
  color: #555;
}
.error {
  color: #e53935;
}
.refresh-container {
  text-align: center;
  margin: 20px 0;
}
.refresh-btn {
  padding: 8px 16px;
  background-color: #757575;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1em;
}
.refresh-btn:hover {
  background-color: #616161;
}
.pdf-preview {
  background: #fff;
  padding: 24px;
  border-radius: 8px;
  box-shadow: 0 2px 8px #0001;
}
.invoice-main {
  width: 100%;
  margin: 0 auto;
  border: 2px solid #444;
  background: white;
  padding: 0;
}
.invoice-title {
  text-align: center;
  font-size: 1.6em;
  font-weight: bold;
  margin: 30px 0 18px 0;
  letter-spacing: 1px;
}
.invoice-details-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 16px;
  font-size: 1em;
}
.invoice-details-table td {
  border: 1px solid #888;
  padding: 6px 10px;
  text-align: right;
  background: #f6f6f6;
}
.invoice-details-table .detail-title {
  background: #e7e7e7;
  font-weight: bold;
  text-align: center;
}
.invoice-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 1em;
  margin-bottom: 16px;
}
.invoice-table th, .invoice-table td {
  border: 1.5px solid #444;
  padding: 6px 3px;
  text-align: center;
}
.invoice-table th {
  background: #ececec;
  font-weight: bold;
}
.total-label {
  background: #e7e7e7;
  font-weight: bold;
}
.total-value {
  background: #ededed;
  font-weight: bold;
  font-size: 1.1em;
}
.footer-row {
  padding: 12px 10px;
  font-size: 1em;
  text-align: right;
  line-height: 2;
}
.button-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  gap: 20px;
}
.confirm-btn, .download-btn {
  padding: 10px 24px;
  font-size: 1.1em;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}
.confirm-btn {
  background-color: #4caf50;
  color: white;
  border: none;
}
.confirm-btn:hover {
  background-color: #388e3c;
}
.confirm-btn:disabled {
  background-color: #a5d6a7;
  cursor: not-allowed;
}
.download-btn {
  background-color: #2196f3;
  color: white;
  border: none;
}
.download-btn:hover {
  background-color: #1976d2;
}
@media print {
  .sales-order-container {
    background: white !important;
    padding: 0;
  }
  .button-container, .loading, .error, .no-data, .refresh-container {
    display: none;
  }
  .invoice-main {
    page-break-after: always;
    border: none;
  }
}
</style>