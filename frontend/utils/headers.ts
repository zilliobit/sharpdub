export async function apiFetch<T>(url: string, options: any = {}) {
  url = "/endpoints" + url;
  const csrf = useCookie("csrf_token").value;

  return $fetch<T>(url, {
    credentials: "include",
    ...options,
    headers: {
      ...options.headers,
    },
  });
}
