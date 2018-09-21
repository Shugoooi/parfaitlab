<template>
<div 
     :class="piece.classes"
     :style="style"
     :draggable="piece.draggable"
    >
    <img v-if="piece['classes']['carcassonne-piece']" class="land-img"
     :src="piece.image">
</div>
</template>


<style>
.carcassonne-piece {
    position: absolute;
    width: 5rem;
    height: 5rem;
}
.candidate {
    position: absolute;
    width: 4.8rem;
    height: 4.8rem;
    border: 0.1rem lightgrey dashed;
}
.land-img {
    width: 100%;
    height: 100%;
}
</style>


<script>
    // import CarcassonneBoard from './'
    export default {
        components: {
           // CarcassonneBoard: CarcassonneBoard,
        },

        props: {
            piece: {
                type: Object,
                default: function () {
                    return {
                        key: 0,
                        classes: {
                            'carcassonne-piece': false,
                            candidate: true,
                        },
                        x: 0,
                        y: 0,
                        draggable: true,
                        image: '/static/carcassonne/img/land.png',
                        terrain: {
                            up: 'road',
                            right: 'grass',
                            left: 'highlands',
                            down: 'city',
                        },
                        direction: 0,
                    }
                },
            },
        },

        computed: {
            style () {
                return {
                    top: 5 * this.piece.y　+ 'rem',
                    left: 5 * this.piece.x + 'rem',
                    transform: 'rotate(' + this.piece.direction + 'deg)',
                } 
            },
        },

    }
</script>

