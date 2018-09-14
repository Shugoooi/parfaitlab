<template>
	<div>
    <drag class="drag"
		:transfer-data="{ example: 'drag-image' }">
		<img src="/static/carcassonne/img/land.png" class="drag-img">
	</drag>
	</div>
</template>

<script>
	import Drag from 'vue-drag-drop';
	export default {
		name: 'DragImage',
		components: Drag,
	};
</script>

<style>
.drag {
	height: 5rem;
	width: 5rem;
}
.drag-img {
	height: 100%;
	width: 100%;
}
</style>
