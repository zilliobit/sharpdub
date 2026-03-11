<script setup lang="ts">
import { apiFetch } from "~/utils/headers";

definePageMeta({
  middleware: "auth",
});

useSeoMeta({
  title: "Dashboard",
  description: "Your personal dashboard",
});

interface User {
  id: string;
  f_name: string;
  l_name: string;
  email: string;
  roles: string[];
}

const user = ref<User | null>(null);
const toast = useToast();

const { data, error } = await useAsyncData("me", () =>
  apiFetch<{ user: User }>("/auth/me")
);

if (error.value || !data.value?.user) {
  toast.add({ title: "Session expired", description: "Please log in again.", color: "error" });
  await navigateTo("/login");
} else {
  user.value = data.value.user;
}

const logoutLoading = ref(false);

async function logout() {
  logoutLoading.value = true;
  try {
    await apiFetch("/auth/logout", { method: "POST" });
  } finally {
    logoutLoading.value = false;
    await navigateTo("/login");
  }
}

const stats = [
  { label: "Projects", value: "12", icon: "i-lucide-folder", color: "text-blue-500" },
  { label: "Tasks", value: "48", icon: "i-lucide-check-square", color: "text-green-500" },
  { label: "Messages", value: "7", icon: "i-lucide-mail", color: "text-purple-500" },
  { label: "Notifications", value: "3", icon: "i-lucide-bell", color: "text-orange-500" },
];

const recentActivity = [
  { title: "Signed up", description: "Account created successfully", time: "Just now", icon: "i-lucide-user-check" },
  { title: "Email verified", description: "OTP verification completed", time: "Just now", icon: "i-lucide-mail-check" },
  { title: "Profile setup", description: "Basic profile information saved", time: "Just now", icon: "i-lucide-settings" },
];
</script>

<template>
  <div class="min-h-screen bg-background">
    <!-- Top Nav -->
    <header class="border-b border-default bg-background/80 backdrop-blur sticky top-0 z-10">
      <UContainer class="flex items-center justify-between h-16">
        <div class="flex items-center gap-3">
          <AppLogo class="h-6 w-auto" />
          <USeparator orientation="vertical" class="h-5" />
          <span class="text-sm text-muted font-medium">Dashboard</span>
        </div>
        <div class="flex items-center gap-3">
          <UColorModeButton />
          <UButton
            v-if="user"
            color="neutral"
            variant="ghost"
            :loading="logoutLoading"
            icon="i-lucide-log-out"
            label="Sign out"
            size="sm"
            @click="logout"
          />
        </div>
      </UContainer>
    </header>

    <UContainer class="py-8 space-y-8">
      <!-- Welcome Banner -->
      <UPageCard v-if="user" variant="subtle">
        <div class="flex items-center gap-4">
          <UAvatar :alt="`${user.f_name} ${user.l_name}`" size="lg" />
          <div>
            <h1 class="text-2xl font-bold">Welcome back, {{ user.f_name }}! 👋</h1>
            <p class="text-muted text-sm mt-0.5">
              {{ user.email }}
              <UBadge
                v-for="role in user.roles"
                :key="role"
                :label="role"
                size="xs"
                color="primary"
                variant="subtle"
                class="ml-2 capitalize"
              />
            </p>
          </div>
        </div>
      </UPageCard>

      <!-- Stats Grid -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <UPageCard
          v-for="stat in stats"
          :key="stat.label"
          variant="subtle"
          class="text-center"
        >
          <UIcon :name="stat.icon" class="text-3xl mb-2" :class="stat.color" />
          <div class="text-2xl font-bold">{{ stat.value }}</div>
          <div class="text-muted text-sm">{{ stat.label }}</div>
        </UPageCard>
      </div>

      <!-- Content Row -->
      <div class="grid md:grid-cols-2 gap-6">
        <!-- Recent Activity -->
        <UPageCard variant="subtle">
          <template #header>
            <div class="flex items-center gap-2 font-semibold">
              <UIcon name="i-lucide-activity" />
              Recent Activity
            </div>
          </template>
          <ul class="space-y-4">
            <li v-for="item in recentActivity" :key="item.title" class="flex items-start gap-3">
              <div class="mt-0.5 p-1.5 rounded-lg bg-primary/10">
                <UIcon :name="item.icon" class="text-primary text-sm" />
              </div>
              <div class="flex-1 min-w-0">
                <p class="text-sm font-medium">{{ item.title }}</p>
                <p class="text-xs text-muted">{{ item.description }}</p>
              </div>
              <span class="text-xs text-muted whitespace-nowrap">{{ item.time }}</span>
            </li>
          </ul>
        </UPageCard>

        <!-- Account Security -->
        <UPageCard variant="subtle">
          <template #header>
            <div class="flex items-center gap-2 font-semibold">
              <UIcon name="i-lucide-shield-check" />
              Account Security
            </div>
          </template>
          <ul class="space-y-3 text-sm">
            <li class="flex justify-between items-center py-2 border-b border-default">
              <span class="text-muted">Email</span>
              <span class="font-medium">{{ user?.email }}</span>
            </li>
            <li class="flex justify-between items-center py-2 border-b border-default">
              <span class="text-muted">Password</span>
              <UBadge label="Set" color="success" variant="subtle" size="xs" />
            </li>
            <li class="flex justify-between items-center py-2 border-b border-default">
              <span class="text-muted">2FA</span>
              <UBadge label="Not enabled" color="warning" variant="subtle" size="xs" />
            </li>
            <li class="flex justify-between items-center py-2">
              <span class="text-muted">Session</span>
              <UBadge label="Active" color="success" variant="subtle" size="xs" />
            </li>
          </ul>
          <template #footer>
            <UButton
              label="Enable 2FA"
              icon="i-lucide-shield"
              color="neutral"
              variant="outline"
              size="sm"
              block
            />
          </template>
        </UPageCard>
      </div>
    </UContainer>
  </div>
</template>
