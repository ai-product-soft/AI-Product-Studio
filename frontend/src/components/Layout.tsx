import { Link } from 'react-router-dom'
import { Zap } from 'lucide-react'

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-background">
      <header className="border-b">
        <div className="container mx-auto px-4 h-14 flex items-center">
          <Link to="/" className="flex items-center gap-2 font-bold text-lg">
            <Zap className="h-5 w-5 text-primary" />
            AI Product Studio
          </Link>
          <span className="ml-2 text-xs text-muted-foreground">v3.0</span>
        </div>
      </header>
      <main className="container mx-auto px-4 py-6">
        {children}
      </main>
    </div>
  )
}
