<script setup lang="ts">
import * as z from "zod";
import type { FormSubmitEvent } from "@nuxt/ui";
/* import { getOrCreateDPoPKey, createDPoPProof } from "../utils/dpop";
const { keyPair, publicJwk } = await getOrCreateDPoPKey(); */
import { apiFetch } from "../utils/headers";

definePageMeta({
  layout: "auth",
});

useSeoMeta({
  title: "Login",
  description: "Login to your account to continue",
});

const toast = useToast();

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
      toast.add({ title: "Google", description: "Login with Google" });
    },
  },
];

const schema = z.object({
  email: z.email({
    error: (issue) => {
      return issue.input === "" || !issue.input ? "Please enter your valid email" : "Entered email is invalid";
  }}),
  password: z.string({
    error: "Password is required",
  }).min(8, "Must be at least 8 characters"),
});


type Schema = z.output<typeof schema>;

async function onSubmit(payload: FormSubmitEvent<Schema>) {
  const result = await apiFetch("/auth/login", {
    method: "POST",
    body: {
      email: payload.data.email,
      password: payload.data.password,
    },
  });

  console.log(result);

  /* const csrf = useCookie("csrf_token").value

await $fetch("/api/protected", {
  method: "POST",
  credentials: "include",
  headers: {
    "X-CSRF-Token": csrf!,
    DPoP: await createDPoPProof(
      "https://api.example.com/protected",
      "POST",
      keyPair,
      publicJwk
    ),
  },
}) */
  console.log("Submitted", payload);
}

/* const { data, error } = await useFetch("/endpoints/todos/", {
  server: false,
});
console.log(data.value); */
</script>

<template>
  <UAuthForm :fields="fields" :schema="schema" :providers="providers" title="Welcome back" icon="i-lucide-lock" @submit="onSubmit">
    <template #description> Don't have an account? <ULink to="/signup" class="text-primary font-medium">Sign up</ULink>. </template>

    <template #password-hint>
      <ULink to="/" class="text-primary font-medium" tabindex="-1">Forgot password?</ULink>
    </template>

    <template #footer> By signing in, you agree to our <ULink to="/" class="text-primary font-medium">Terms of Service</ULink>. </template>
  </UAuthForm>
</template>
