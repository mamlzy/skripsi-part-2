import type { Metadata } from "next"
import { Geist_Mono, Noto_Sans, Playfair_Display } from "next/font/google"

import "./globals.css"
import { ThemeProvider } from "@/components/theme-provider"
import { cn } from "@/lib/utils"

const playfairDisplayHeading = Playfair_Display({
  subsets: ["latin"],
  variable: "--font-heading",
})

const notoSans = Noto_Sans({ subsets: ["latin"], variable: "--font-sans" })

const fontMono = Geist_Mono({
  subsets: ["latin"],
  variable: "--font-mono",
})

export const metadata: Metadata = {
  title: "Klasifikasi Risiko Piutang Pelanggan",
  description:
    "Dashboard skripsi untuk klasifikasi risiko piutang pelanggan menggunakan Naive Bayes.",
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html
      lang="id"
      suppressHydrationWarning
      className={cn(
        "font-sans antialiased",
        fontMono.variable,
        notoSans.variable,
        playfairDisplayHeading.variable
      )}
    >
      <body>
        <ThemeProvider>{children}</ThemeProvider>
      </body>
    </html>
  )
}
