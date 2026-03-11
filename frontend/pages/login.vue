<script setup lang="ts">
import * as z from "zod";
import type { FormSubmitEvent } from "@nuxt/ui";
import { apiFetch } from "../utils/headers";

definePageMeta({
  layout: "auth",
});

useSeoMeta({
  title: "Login",
  description: "Login to your account to continue",
});

const toast = useToast();
const loading = ref(false);

const fields = [
  {
    name: "email",
    type: "text" as const,
    label: "Email",
    placeholder: "",
    required: true,
  },
  {
    name: "password",
    label: "Password",
    type: "password" as const,
    placeholder: "",
  },
  {
    name: "remember",
    label: "Remember me",
    type: "checkbox" as const,
  },
];

const providers = [
  {
    label: "Google",
    icon: "i-custom-google",
    onClick: () => {
      window.location.href = `${useRuntimeConfig().public.apiBase}/auth/google/login`;
    },
  },
];

const schema = z.object({
  email: z.email({
    error: (issue) => {
      return issue.input === "" || !issue.input
        ? "Please enter your valid email"
        : "Entered email is invalid";
    },
  }),
  password: z
    .string({ error: "Password is required" })
    .min(8, "Must be at least 8 characters"),
});

type Schema = z.output<typeof schema>;

async function onSubmit(payload: FormSubmitEvent<Schema>) {
  loading.value = true;

  try {
    const data = await apiFetch<{ success: boolean; message?: string }>("/auth/login", {
      method: "POST",
      body: {
        email: payload.data.email,
        password: payload.data.password,
      },
    });

    if (data?.success) {
      toast.add({ title: "Welcome back!", description: "Logged in successfully." });
      await navigateTo("/dashboard");
    } else {
      toast.add({
        title: "Login failed",
        description: data?.message || "Invalid credentials. Please try again.",
        color: "error",
      });
    }
  } catch (err: any) {
    const status = err?.response?.status;
    const detail = err?.response?._data?.detail;

    if (status === 401) {
      toast.add({
        title: "Invalid credentials",
        description: "Incorrect email or password.",
        color: "error",
      });
    } else if (status === 422) {
      toast.add({
        title: "Invalid request",
        description: "Please check your email and password.",
        color: "error",
      });
    } else if (status === 429) {
      toast.add({
        title: "Too many attempts",
        description: "Please wait a moment before trying again.",
        color: "error",
      });
    } else {
      toast.add({
        title: "Something went wrong",
        description: detail || "Unable to connect. Please try again.",
        color: "error",
      });
    }
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <UAuthForm
    :fields="fields"
    :schema="schema"
    :providers="providers"
    :submit="{ label: 'Sign in', loading }"
    title="Welcome back"
    icon="i-lucide-lock"
    @submit="onSubmit"
  >
    <template #description>
      Don't have an account?
      <ULink to="/signup" class="text-primary font-medium">Sign up</ULink>.
    </template>

    <template #password-hint>
      <ULink to="/forgot-password" class="text-primary font-medium" tabindex="-1">
        Forgot password?
      </ULink>
    </template>

    <template #footer>
      By signing in, you agree to our
      <ULink to="/" class="text-primary font-medium">Terms of Service</ULink>.
    </template>
  </UAuthForm>
</template>
