import Vue from 'vue'
import VueDragDrop from 'vue-drag-drop'

Vue.use(VueDragDrop)
import { Container, Box } from '@dattn/dnd-grid'
// minimal css for the components to work properly
//import '@dattn/dnd-grid/dist/dnd-grid.css'
Vue.component('board-piece', require('./components/BoardPiece.vue').default)
Vue.component('drag-image', require('./components/DragImage.vue').default)
Vue.component('drop-area', require('./components/DropArea.vue').default)
Vue.component('carcassonne-piece', require('./components/CarcassonnePiece.vue').default)
Vue.component('carcassonne-board', require('./components/CarcassonneBoard.vue').default)


//new Vue({
//  render(h) {
//    return h(DragImage)
//  }
//}).$mount('#app')
var vm = new Vue({
    el: '#app',
})
