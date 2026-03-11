<template>
  <div class="min-h-screen bg-background flex items-center justify-center p-4">
    <div class="fixed inset-0 pointer-events-none">
      <div class="absolute top-1/4 left-1/4 w-96 h-96 bg-primary/10 rounded-full blur-3xl" />
      <div class="absolute bottom-1/4 right-1/4 w-96 h-96 bg-accent/10 rounded-full blur-3xl" />
    </div>
    <UButton icon="i-lucide-chevron-left" to="/" size="xl" color="neutral" variant="subtle" class="absolute left-8 top-8 rounded-full z-10" />
    <main class="relative">
      <UPageCard variant="subtle" class="max-w-sm w-full bg-white">
        <slot />
      </UPageCard>
    </main>
    <UToaster />
  </div>
</template>
