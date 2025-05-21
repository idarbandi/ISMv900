import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import addTruck from "@/components/addTruck.vue";
import addSupplier from "@/components/addSupplier.vue";
import addCustomer from "@/components/addCustomer.vue";
import addRawMaterial from "@/components/addRawMaterial.vue";
import addNewReel from "@/components/addNewReel.vue";
import forkliftPanel from "@/components/forkliftPanel.vue";
import createShipment from "@/components/createShipment.vue";
import sales from "@/components/weightStation/sales.vue";
import purchase from "@/components/weightStation/purchase.vue";
import weight1 from "@/components/weightStation/weight1.vue";
import weight2 from "@/components/weightStation/weight2.vue";
import weightStationPanel from "@/components/weightStation/weightStationPanel.vue";
import addNewAnbar from "@/components/admin/addNewAnbar.vue";
import addNewUnit from "@/components/admin/addNewUnit.vue";
import addNewMatrialType from "@/components/admin/addNewMatrialType.vue";
import consumptionProfile from "@/components/admin/consumptionProfile.vue";
import Cancel from '../components/admin/cancel.vue'
import reportPage from "@/components/admin/reportPage.vue";
import AllPages from "@/components/admin/AllPages.vue";
import Products from "@/components/admin/Products.vue";
import AdminLogin from '../components/admin/AdminLogin.vue'
import ReportLogin from '../components/admin/ReportLogin.vue'
import Havaleh from '@/components/Havaleh.vue'
import salesorder from '@/components/salesorder.vue';
import FilterPage from '@/components/FilterPage.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/myapp/addTruck/',
    name: 'addTruck',
    component: addTruck
  },
  {
    path: '/myapp/addSupplier/',
    name: 'addSupplier',
    component: addSupplier
  },
  {
    path: '/myapp/addCustomer/',
    name: 'addCustomer',
    component: addCustomer
  },
  {
    path: '/myapp/addRawMaterial/',
    name: 'addRawMaterial',
    component: addRawMaterial
  },
  {
    path: '/myapp/addNewReel/',
    name: 'addNewReel',
    component: addNewReel
  },
  {
    path: '/myapp/forkliftPanel/',
    name: 'forkliftPanel',
    component: forkliftPanel
  },
  {
    path: '/myapp/addShipment/',
    name: 'addShipment',
    component: createShipment
  },
  {
    path: '/myapp/createSalesOrder/',
    name: 'createSalesOrder',
    component: sales
  },
  {
    path: '/myapp/createPurchaseOrder/',
    name: 'createPurchaseOrder',
    component: purchase
  },
  {
    path: '/myapp/updateWeight1/',
    name: 'updateWeight1',
    component: weight1
  },
  {
    path: '/myapp/updateWeight2/',
    name: 'updateWeight2',
    component: weight2
  },
  {
    path: '/myapp/weightStationPanel/',
    name: 'weightStationPanel',
    component: weightStationPanel
  },
  {
    path: '/myapp/addNewAnbar/',
    name: 'addNewAnbar',
    component: addNewAnbar
  },
  {
    path: '/myapp/addUnit/',
    name: 'addNewUnit',
    component: addNewUnit
  },
  {
    path: '/myapp/addMaterialType/',
    name: 'addNewMatrialType',
    component: addNewMatrialType
  },
  {
    path: '/myapp/addConsumptionProfile/',
    name: 'addConsumptionProfile',
    component: consumptionProfile
  },
  {
    path: '/myapp/cancel/',
    name: 'Cancel',
    component: AdminLogin,
    meta: { requiresAuth: true }
  },
  {
    path: '/myapp/admin/cancel/',
    name: 'CancelAction',
    component: Cancel,
    meta: { requiresAuth: true }
  },
  {
    path: '/myapp/admin/login/',
    name: 'AdminLogin',
    component: AdminLogin
  },
  {
    path: '/myapp/report/',
    name: 'Report',
    component: ReportLogin,
    meta: { requiresAuth: true }
  },
  {
    path: '/myapp/admin/report/',
    name: 'ReportAction',
    component: reportPage,
    meta: { requiresAuth: true }
  },
  {
    path: '/myapp/',
    name: 'AllPages',
    component: AllPages
  },
  {
    path: '/myapp/ProductsPage/',
    name: 'Products',
    component: Products
  },
  {
    path: '/myapp/invoice/',
    component: () => import('@/components/invoice.vue')
  },
  {
    path: '/myapp/invoice/sales_order/',
    component: () => import('@/components/salesorder.vue')
  },
  {
    path: '/myapp/invoice/havaleh',
    component: () => import('@/components/Havaleh.vue'),
  },
  {
    path: '/myapp/filter/',
    name: 'Filter',
    component: FilterPage
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// بررسی احراز هویت قبل از هر مسیریابی
router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    const token = localStorage.getItem('token')
    const isSuperuser = localStorage.getItem('is_superuser') === 'true'

    if (!token || !isSuperuser) {
      next({
        path: '/myapp/admin/login/',
        query: { redirect: to.fullPath }
      })
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router
