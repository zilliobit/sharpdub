<script setup lang="ts">
const { isLoading } = useLoadingIndicator();

const appear = ref(false);
const appeared = ref(false);

onMounted(() => {
  setTimeout(() => {
    appear.value = true;
    setTimeout(() => {
      appeared.value = true;
    }, 1000);
  }, 0);
});
</script>

<template>
  <div class="absolute w-full -top-px transition-all text-primary shrink-0 min-h-[550px] z-[-1]">
    <div class="absolute inset-0 pointer-events-none">
      <div class="absolute top-1/4 left-1/4 w-96 h-96 bg-primary/10 rounded-full blur-3xl" />
      <div class="absolute bottom-1/4 right-1/4 w-96 h-96 bg-accent/10 rounded-full blur-3xl" />
    </div>
  </div>
</template>
