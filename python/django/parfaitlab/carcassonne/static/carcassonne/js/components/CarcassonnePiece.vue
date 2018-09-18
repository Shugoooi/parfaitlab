<template>
<div 
     :class="classes"
     :style="style"
    >
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
    width: 4.9rem;
    height: 4.9rem;
    border: 0.1rem lightgrey dashed;
}
</style>


<script>
    // import CarcassonneBoard from '.'
    export default {
        components: {
            // CarcassonneBoard: CarcassonneBoard,
        },

        data: function() {
            return {
                classes: {
                    'carcassonne-piece': false,
                    candidate: true,
                },
                layout: {
                    x: 0,
                    y: 0,
                },
                draggable: true,
                image: './static/carcassonne/img/land.png',
                terrain: {
                    up: 'road',
                    right: 'grass',
                    left: 'highlands',
                    down: 'city',
                },
                direction: 0,
            }
        },

        computed: {
            style () {
                return {
                    
            },
        },

    }
</script>

