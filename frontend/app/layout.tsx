import type { Metadata } from "next"
import { Providers } from "./providers"
import { ThemeProvider } from "./theme-provider"
import "./globals.css"

export const metadata: Metadata = {
  title: "PDF Research Assistant - AI-Powered Document Analysis",
  description: "Upload PDFs and interact with them using advanced AI. Get instant answers with source citations powered by RAG technology.",
  keywords: ["PDF", "AI", "Chat", "Document Analysis", "RAG", "LLM"],
  authors: [{ name: "Somil Shankar Gupta" }],
  creator: "Somil Shankar Gupta",
  openGraph: {
    type: "website",
    locale: "en_US",
    url: "https://pdf-research-assistant.vercel.app",
    title: "PDF Research Assistant",
    description: "AI-Powered PDF Document Analysis with Conversational Interface",
    siteName: "PDF Research Assistant",
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="bg-background text-foreground">
        <ThemeProvider>
          <Providers>{children}</Providers>
        </ThemeProvider>
      </body>
    </html>
  )
}
