<template>
    <div class="container-fluid">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        <h1>DEMO dnd-grid Vue.js Component</h1>

        <dnd-grid-container
            :layout.sync="layout"
            :cellSize="cellSize"
            :maxColumnCount="maxColumnCount"
            :maxRowCount="maxRowCount"
            :margin="margin"
            :bubbleUp="bubbleUp"
        >
        <button @click="addDndBox">add box</button>
            <dnd-grid-box
                v-for="number in layout"
                :boxId="number.id"
                :key="number.id"
                dragSelector="div"
            >
                <div class="card demo-box">
                    <div class="card-header">
                        Box {{ number.id }}
                    </div>
                <button @click="pinBox(number)">pin box</button>
                </div>
            </dnd-grid-box>
        </dnd-grid-container>
    </div>
</template>

<style>
    .demo-box {
        width: 100%;
        height: 100%;
    }
</style>

<script>
    import { Container, Box } from '@dattn/dnd-grid'
    export default {
        components: {
            DndGridContainer: Container,
            DndGridBox: Box
        },
        data () {
            return {
                cellSize: {
                    w: 100,
                    h: 100
                },
                maxColumnCount: 10,
                maxRowCount: Infinity,
                bubbleUp: false,
                margin: 0,
                boxCount: 5,
                layout: [
                    {
                        id: 'settings',
                        hidden: false,
                        pinned: false,
                        position: {
                            x: 0,
                            y: 0,
                            w: 1,
                            h: 1
                        }
                    },
                    {
                        id: 1,
                        hidden: false,
                        pinned: false,
                        position: {
                            x: 8,
                            y: 0,
                            w: 1,
                            h: 1
                        }
                    },
                    {
                        id: 2,
                        hidden: false,
                        pinned: false,
                        position: {
                            x: 2,
                            y: 0,
                            w: 1,
                            h: 1
                        }
                    },
                    {
                        id: 3,
                        hidden: false,
                        pinned: false,
                        position: {
                            x: -1,
                            y: 1,
                            w: 1,
                            h: 1
                        }
                    },
                    {
                        id: 4,
                        hidden: false,
                        pinned: false,
                        position: {
                            x: 1,
                            y: 1,
                            w: 1,
                            h: 1
                        }
                    }
                ]
            }
        },
        computed: {
            layoutWithoutSettings () {
                return this.layout.filter((box) => {
                    return box.id !== 'settings'
                })
            }
        },
        methods: {
            onLayoutUpdate (evt) {
                this.layout = evt.layout
            },
            addDndBox () {
                console.log('Start adding dnd box.')
                this.boxCount++
                this.layout.push({
                    id: 5,
                    position: {
                        x: 2,
                        y: 2,
                        w: 1,
                        h: 1
                    }
                })
            },
            pinBox (dndBox) {
                dndBox["pinned"] = !dndBox["pinned"]
            }
        }
    }
</script>
