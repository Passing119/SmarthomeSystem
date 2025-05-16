import { createRouter, createWebHistory } from 'vue-router'
import Home from './views/Home.vue'
import Aircon from './views/aircon.vue'
import Light from './views/light.vue'
import Door from './views/door.vue'
import Curtain from './views/curtain.vue'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/aircon',
        name: 'Aircon',
        component: Aircon
    },
    {
        path: '/light',
        name: 'Light',
        component: Light
    },
    {
        path: '/door',
        name: 'Door',
        component: Door
    },
    {
        path: '/curtain',
        name: 'Curtain',
        component: Curtain
    }
]

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
})

export default router  