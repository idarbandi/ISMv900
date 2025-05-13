<template>
  <div class="havaleh-form">
    <h2>حواله خروج از انبار</h2>
    <div class="loading-state" v-if="loading">
      <p>در حال بارگیری اطلاعات فاکتور...</p>
    </div>
    <div class="no-invoice" v-else-if="!hasInvoice">
      <p>فاکتوری با وضعیت تایید نشده وجود ندارد.</p>
    </div>
    <div v-else>
      <div class="form-header">
        <div class="form-group">
          <label>تاریخ ارسال:</label>
          <input type="text" v-model="formData.date" readonly />
        </div>
        <div class="form-group">
          <label>شماره سریال:</label>
          <input type="text" v-model="formData.serial" />
        </div>
        <div class="form-group">
          <label>شماره فاکتور:</label>
          <input type="text" v-model="latestInvoice.invoice_number" readonly />
        </div>
        <div class="form-group">
          <label>مشتری:</label>
          <input type="text" v-model="latestInvoice.customer_name" readonly />
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
                <input type="text" v-model="item.name" />
              </td>
              <td>
                <input type="text" v-model="item.gsm" />
              </td>
              <td>
                <input type="text" v-model="item.width" />
              </td>
              <td>
                <input type="text" v-model="item.buyer" />
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
          <label>ملاحظات:</label>
          <textarea v-model="formData.note"></textarea>
        </div>
        <div class="total-weight">
          <strong>جمع کل وزن:</strong> {{ calculateTotalWeight() }}
        </div>
        <div class="button-group">
          <button @click="generatePDF" class="generate-btn">تولید PDF حواله</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Havaleh',
  data() {
    return {
      loading: true,
      hasInvoice: false,
      latestInvoice: null,
      formData: {
        date: this.getCurrentDate(),
        serial: '',
        items: [],
        note: ''
      }
    }
  },
  created() {
    // Fetch the latest invoice when component is created
    this.fetchLatestInvoice();
  },
  methods: {
    async fetchLatestInvoice() {
      try {
        this.loading = true;
        // Use absolute URLs with window.location.origin
        const base = window.location.origin;
        const response = await fetch(`${base}/myapp/api/latest-invoice/`);
        
        if (!response.ok) {
          if (response.status === 404) {
            this.hasInvoice = false;
            this.loading = false;
            return;
          }
          throw new Error(`Error ${response.status}: ${await response.text()}`);
        }
        
        const data = await response.json();
        this.latestInvoice = data;
        this.hasInvoice = true;
        
        // Populate form data from invoice
        this.formData.serial = `HV-${data.id}`;
        
        // Create items from reels if available
        if (data.list_of_reels) {
          const reels = data.list_of_reels.split(',');
          
          reels.forEach(reel => {
            this.formData.items.push({
              name: `رول ${reel.trim()}`,
              gsm: '',
              width: data.width || '',
              buyer: data.customer_name || '',
              quantity: 1,
              weight: data.net_weight ? Math.round(data.net_weight / reels.length) : 0
            });
          });
        } else {
          // Default single item
          this.addItem();
          if (this.formData.items.length > 0) {
            this.formData.items[0].buyer = data.customer_name || '';
            this.formData.items[0].width = data.width || '';
            this.formData.items[0].weight = data.net_weight || 0;
          }
        }
      } catch (error) {
        console.error('Error fetching latest invoice:', error);
        this.hasInvoice = false;
      } finally {
        this.loading = false;
      }
    },
    getCurrentDate() {
      // Convert to Iranian date format
      const today = new Date();
      // Format: YYYY/MM/DD
      const year = today.getFullYear();
      const month = String(today.getMonth() + 1).padStart(2, '0');
      const day = String(today.getDate()).padStart(2, '0');
      return `${year}/${month}/${day}`;
    },
    addItem() {
      this.formData.items.push({
        name: '',
        gsm: '',
        width: '',
        buyer: this.latestInvoice?.customer_name || '',
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
    async generatePDF() {
      try {
        const requestData = {
          date: this.formData.date,
          serial: this.formData.serial,
          items: this.formData.items,
          note: this.formData.note,
          invoice_id: this.latestInvoice?.id
        };

        console.log('Form data being sent:', requestData);
        
        const base = window.location.origin;
        const response = await fetch(`${base}/myapp/api/havaleh-pdf/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.getCookie('csrftoken'),
          },
          body: JSON.stringify(requestData),
          credentials: 'include'
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || 'Error generating PDF');
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `havaleh_${this.formData.serial}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

      } catch (error) {
        console.error('خطا در تولید PDF:', error);
        alert('خطا در تولید PDF: ' + error.message);
      }
    },
    getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
  }
}
</script>

<style scoped>
.loading-state, .no-invoice {
  text-align: center;
  margin: 2rem 0;
  padding: 1rem;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.button-group {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.generate-btn {
  background-color: #2196F3;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.add-btn {
  background-color: #4CAF50;
  color: white;
  margin-top: 10px;
  padding: 5px 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.remove-btn {
  background-color: #f44336;
  color: white;
  padding: 5px 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

/* Form styling */
.form-header {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input, .form-group textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

/* Table styling */
.items-table {
  margin-bottom: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: right;
}

th {
  background-color: #f2f2f2;
  font-weight: bold;
}

.total-weight {
  margin-top: 15px;
  font-weight: bold;
}
</style>