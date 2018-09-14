//var Vue = require('vue')
//var VueDragDrop = require('vue-drag-drop')
//Vue.use(VueDragDrop)
//import {Drag, Drop} from 'vue-drag-drop'
// import Container and Box components
//import { Container, Box } from '@dattn/dnd-grid'
// minimal css for the components to work properly
//import '@dattn/dnd-grid/dist/dnd-grid.css'
//Vue.component('board-piece', require('./components/BoardPiece.vue'))
//const aiai = require('./components/BoardPiece.vue');
//Vue.component('board-piece', require('./components/BoardPiece.vue'))
const DragImage = require('./components/DragImage.vue').default
//Vue.component('drag-image', require('./components/DragImage.vue'))
const DropArea = require('./components/DropArea.vue').default

new Vue({
  render(h) {
    return h(DragImage)
  }
}).$mount('#app')
//var vm = new Vue({
//    el: '#app',
//})