// middleware/auth.ts
// Protects any page that uses definePageMeta({ middleware: 'auth' })
// Checks for the __Host-csrf_token cookie (readable by JS, set on login/signup)
// If missing → redirects to /login with ?redirect= so user lands back after login

export default defineNuxtRouteMiddleware((to) => {
  const csrfToken = useCookie("__Host-csrf_token");

  if (!csrfToken.value) {
    return navigateTo(`/login?redirect=${encodeURIComponent(to.fullPath)}`);
  }
});
