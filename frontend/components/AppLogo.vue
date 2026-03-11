<script setup lang="ts">
import { Languages } from "lucide-vue-next";
</script>
<template>
  <div class="flex gap-3 items-center">
    <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-primary to-accent flex items-center justify-center">
      <Languages class="w-5 h-5 text-primary-foreground" />
    </div>
    <div>
      <h1 class="text-xl font-bold">SharpDub</h1>
      <p class="text-xs text-muted-foreground">AI-Powered Translator</p>
    </div>
  </div>
</template>
