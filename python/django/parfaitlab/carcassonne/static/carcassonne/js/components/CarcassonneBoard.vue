<template>
    <div class="carcassonne-board"
        :style="style"
    >
        <carcassonne-piece
            v-for="piece in pieces"
            :key="piece.key"
            :piece="piece"
         ></carcassonne-piece>
             <button @click="check">oiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiioioioi</button>
    </div>
</template>

<style>
.carcassonne-board {
}
</style>

<script>
import CarcassonnePiece from './CarcassonnePiece.vue'
export default {
    components: {
        'carcassonne-piece': CarcassonnePiece,
    },

    data () {
        return {
            pieces: [
                {
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
                },
                {
                    key: 1,
                    classes: {
                        'carcassonne-piece': false,
                        candidate: true,
                    },
                    x: 0,
                    y: 31,
                    draggable: true,
                    image: '/static/carcassonne/img/land.png',
                    terrain: {
                        up: 'road',
                        right: 'grass',
                        left: 'highlands',
                        down: 'city',
                    },
                    direction: 0,
                },
            ],
        }
    },
    
    computed: {
        style () {
            return {
                width: this.maxWidth + 'rem',
                height: this.maxHeight + 'rem',
            }
        },
        maxWidth () {
            return 5 * (Math.max(...this.pieces.map(piece => piece.x)) + 1)
        },
        maxHeight () {
            return 5 * (Math.max(...this.pieces.map(piece => piece.y)) + 1)
        },
    },

    methods: {
        check () {
            console.log(this)
        },
    },

}
</script>
