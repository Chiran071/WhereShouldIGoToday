import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Where To Go Today?',
  description: 'Discover the perfect place to visit in Nepal based on your mood, budget, and time',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  )
}
