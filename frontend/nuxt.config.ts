// https://nuxt.com/docs/api/configuration/nuxt-config
import tailwindcss from "@tailwindcss/vite";
export default defineNuxtConfig({
  compatibilityDate: "2025-07-15",
  devtools: { enabled: true },
  modules: ["@nuxt/icon", "@nuxt/content", "@nuxt/ui", "@nuxtjs/color-mode"],
  css: ["~/assets/css/main.css"],
  icon: {
    customCollections: [{
      prefix: 'custom',
      dir: './assets/icons'
    }]
  },
  vite: {
    plugins: [tailwindcss()],
    server: {
      proxy: {
        "/endpoints": {
          target: "http://127.0.0.1:8000",
          rewrite: (path) => path.replace(/^\/endpoints/, "/api"),
        },
      },
    },
  },
});
