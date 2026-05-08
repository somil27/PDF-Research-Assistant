"use client"

import { ReactNode } from "react"
import { QueryClient, QueryClientProvider } from "react-query"
import { Toaster } from "react-hot-toast"

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes
      retry: 1,
      refetchOnWindowFocus: false,
    },
    mutations: {
      retry: 1,
    },
  },
})

export function Providers({ children }: { children: ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <Toaster
        position="top-right"
        reverseOrder={false}
        gutter={8}
        toastOptions={{
          duration: 4000,
          style: {
            background: "hsl(var(--card))",
            color: "hsl(var(--card-foreground))",
            border: "1px solid hsl(var(--border))",
            borderRadius: "calc(var(--radius) - 2px)",
          },
          success: {
            style: {
              borderLeft: "3px solid hsl(34, 97%, 52%)",
            },
          },
          error: {
            style: {
              borderLeft: "3px solid hsl(var(--destructive))",
            },
          },
        }}
      />
    </QueryClientProvider>
  )
}
