<script setup lang="ts">
import * as z from "zod";
import type { FormSubmitEvent } from "@nuxt/ui";
import { apiFetch } from "~/utils/headers";
import type { APIResponse } from "~/types";

definePageMeta({
  layout: "auth",
});

useSeoMeta({
  title: "Sign up",
  description: "Create an account to get started",
});

const toast = useToast();
const loading = ref(false);

const fields = [
  {
    name: "f_name",
    type: "text" as const,
    label: "First Name",
    placeholder: "",
    required: true,
  },
  {
    name: "l_name",
    type: "text" as const,
    label: "Last Name",
    placeholder: "",
    required: true,
  },
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
    required: true,
  },
];

const providers = [
  {
    label: "Google",
    icon: "i-custom-google",
    onClick: () => {
      toast.add({ title: "Google", description: "Login with Google" });
    },
  },
];

const schema = z.object({
  f_name: z
    .string({
      error: "First Name is required",
    })
    .min(1, "First Name is required"),
  l_name: z
    .string({
      error: "Last Name is required",
    })
    .min(1, "Last Name is required"),
  email: z.email({
    error: (issue) => {
      return issue.input === "" || !issue.input ? "Please enter your valid email" : "Entered email is invalid";
    },
  }),
  password: z
    .string({
      error: "Password is required",
    })
    .min(8, "Must be at least 8 characters"),
});

async function onSubmit(payload: FormSubmitEvent<any>) {
  loading.value = true;

  try {
    const data = await apiFetch<APIResponse>("/auth/signup", {
      method: "POST",
      body: {
        f_name: payload.data.f_name,
        l_name: payload.data.l_name,
        email: payload.data.email,
        password: payload.data.password,
      },
    });
    console.log(data);
    if (data.success) {
      navigateTo({
        path: "/signup/verifyotp",
        query: { email: payload.data.email }, // pass email
      });
    } else {
      toast.add({ title: "Error", description: data.message || "Something went wrong" });
    }
  } catch (err) {
    toast.add({ title: "Error", description: "Server error" });
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <UAuthForm
    id="signup-form"
    :fields="fields"
    :schema="schema"
    :providers="providers"
    title="Create an account"
    :submit="{ label: 'Create account', loading }"
    @submit="onSubmit"
  >
    <template #description> Already have an account? <ULink to="/login" class="text-primary font-medium">Login</ULink>. </template>

    <template #footer> By signing up, you agree to our <ULink to="/" class="text-primary font-medium">Terms of Service </ULink>. </template>
  </UAuthForm>
</template>

<style>
#signup-form {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}

#signup-form > div[data-slot="root"] {
  width: 100%;
}

#signup-form > div[data-slot="root"]:nth-child(1),
#signup-form > div[data-slot="root"]:nth-child(2) {
  width: 48%;
}
</style>
