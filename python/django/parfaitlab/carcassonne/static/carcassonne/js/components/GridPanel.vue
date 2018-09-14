<template>
<grid-layout class="grid-layout"
            :layout="layout"
            :col-num="12"
            :row-height="80" 
            :is-draggable="true"
            :is-resizable="false"
            :is-mirrored="false"
            :vertical-compact="true"
            :margin="[0, 0]"
            :use-css-transforms="true"
    >

        <grid-item class="grid-panel" v-for="item in layout"
                   :x="item.x"
                   :y="item.y"
                   :w="item.w"
                   :h="item.h"
                   :i="item.i">
            {{item.i}}
        </grid-item>
    </grid-layout>
</template>

<script>
	import { GridLayout, GridItem } from 'vue-grid-layout';
	export default {
		components: {
		    GridLayout,
		    GridItem,
		},
		data: function() {
            return {
                layout: [
                    {"x":0,"y":0,"w":1,"h":1,"i":"0"},
                    {"x":2,"y":0,"w":1,"h":1,"i":"1"},
                    {"x":4,"y":0,"w":1,"h":1,"i":"2"},
                    {"x":6,"y":0,"w":1,"h":1,"i":"3"},
                    {"x":8,"y":0,"w":1,"h":1,"i":"4"},
                    {"x":10,"y":0,"w":1,"h":1,"i":"5"},
                    {"x":0,"y":5,"w":1,"h":1,"i":"6"},
                    {"x":2,"y":5,"w":1,"h":1,"i":"7"},
                    {"x":4,"y":5,"w":1,"h":1,"i":"8"},
                    {"x":6,"y":4,"w":1,"h":1,"i":"9"},
                    {"x":8,"y":4,"w":1,"h":1,"i":"10"},
                    {"x":10,"y":4,"w":1,"h":1,"i":"11"},
                    {"x":0,"y":10,"w":1,"h":1,"i":"12"},
                    {"x":2,"y":10,"w":1,"h":1,"i":"13"},
                    {"x":4,"y":8,"w":1,"h":1,"i":"14"},
                    {"x":6,"y":8,"w":1,"h":1,"i":"15"},
                    {"x":8,"y":10,"w":1,"h":1,"i":"16"},
                    {"x":10,"y":4,"w":1,"h":1,"i":"17"},
                    {"x":0,"y":9,"w":1,"h":1,"i":"18"},
                    {"x":2,"y":6,"w":1,"h":1,"i":"19"},
                ],
            }
		},
		methods: {
		},
	};
</script>

<style>
.grid-panel {
    height: 5rem !important;
    width: 5rem !important;
}
</style>
