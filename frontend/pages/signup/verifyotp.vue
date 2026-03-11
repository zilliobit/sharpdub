<script setup lang="ts">
import * as z from "zod";
import type { FormSubmitEvent } from "@nuxt/ui";
import { apiFetch } from "~/utils/headers";
import type { APIResponse } from "~/types";


definePageMeta({
  layout: "auth"
});

const route = useRoute();
const toast = useToast();
const loading = ref(false);

const email = route.query.email as string;

if (!email) {
  navigateTo('/signup');
}

const fields = [
  {
    name: 'otp',
    type: 'otp',
    label: '',
    length: 6,
    placeholder: '',
    class: 'justify-center',
    inputmode: 'numeric',
    pattern: '[0-9]*',
  }
];

// ---------------- TIMER ----------------
const OTP_EXPIRY = 60;
const timer = ref(OTP_EXPIRY);
let interval: ReturnType<typeof setInterval>;

const startTimer = () => {
  timer.value = OTP_EXPIRY;
  clearInterval(interval);

  interval = setInterval(() => {
    if (timer.value > 0) timer.value--;
    else clearInterval(interval);
  }, 1000);
};

onMounted(startTimer);
onBeforeUnmount(() => clearInterval(interval));

const schema = z.object({
  otp: z.preprocess(
    (val) => {
      if (!val) return "";
      return Array.isArray(val) ? val.join('') : val;
    },
    z.string().length(6, "OTP must be 6 digits")
  ),
});

async function verifyOtp(payload: FormSubmitEvent<any>) {
  
  if (payload.data.otp.length !== 6) return;

  loading.value = true;

  try {
    const data = await apiFetch<APIResponse>("/auth/signup/verify", {
      method: "POST",
      body: {
        email,
        otp: payload.data.otp,
      },
    });

    if (data.success) {
      toast.add({ title: "Verified", description: "OTP verified successfully 🎉" });
      navigateTo("/login");
    }
    // else {
    //   toast.add({
    //     title: "Invalid OTP",
    //     description: "Please try again"
    //   });
    //   payload.data.otp = "";
    // }
  } catch (err: any) {
    toast.add({ title: "Error", description: err.response?._data?.detail || "Something went wrong" });
  } finally {
    payload.data.otp = "";
    loading.value = false;
  }

}

// ---------------- RESEND ----------------
const canResend = computed(() => timer.value === 0);

async function resendOtp() {
  await apiFetch("/auth/resend-otp", {
    method: "POST",
    body: { email },
  });

  toast.add({ title: "OTP Sent", description: "New OTP sent to your email" });
  startTimer();
}
</script>

<template>

  <UAuthForm :fields="fields" :schema="schema" title="Verify OTP" :submit="{ label: 'Verify', loading }"
    class="text-center" @submit="verifyOtp">
    <template #description> Please enter the 6-digit code sent to <span class="text-primary">{{ email }}</span>
    </template>
    <template #footer>
      <div class="flex justify-between">
        <div v-if="!canResend" class="text-sm text-gray-500">
          Resend OTP in <span class="text-primary">{{ timer }}s</span>
        </div>
        <ULink v-else @click="resendOtp" class="text-primary font-medium">
          Resend OTP
        </ULink>
        <ULink to="/signup" class="text-primary font-medium">
          Cancel
        </ULink>

      </div>
    </template>

  </UAuthForm>
</template>
