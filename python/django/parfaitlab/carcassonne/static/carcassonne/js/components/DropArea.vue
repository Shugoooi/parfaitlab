<template>
    <div>
        <drop class="drop" @drop="handleDrop">
            <div class="drop-area"></div>
        </drop>
    </div>
</template>

<script>
    import Drop from 'vue-drag-drop';
    export default {
        name: 'DropArea',
        components: Drop,
        methods: {
            handleDrop(data) {
                alert('Dropped: ${JSON.stringify(data)}');
            },
        },
    };
</script>

<style>
.drop {
    height: 4.8rem;
    width: 4.8rem;
}
.drop-area {
    height: 100%;
    width: 100%;
    border: 0.1rem dashed lightgrey;
}
</style>                         
