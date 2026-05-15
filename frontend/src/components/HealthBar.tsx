import { useEffect, useState } from 'react'
import { CheckCircle, XCircle, Loader2 } from 'lucide-react'
import { healthCheck } from '@/services/api'

interface HealthStatus {
  status: string
  checks: Array<{ status: string; service: string; detail?: string }>
}

export default function HealthBar() {
  const [health, setHealth] = useState<HealthStatus | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const check = async () => {
      try {
        const { data } = await healthCheck()
        setHealth(data)
      } catch (err) {
        setHealth({
          status: 'unhealthy',
          checks: [
            { status: 'error', service: 'api', detail: 'Connection failed' },
          ],
        })
      } finally {
        setLoading(false)
      }
    }

    check()
    const interval = setInterval(check, 30000)
    return () => clearInterval(interval)
  }, [])

  if (loading) {
    return (
      <div className="flex items-center gap-2 text-sm text-muted-foreground">
        <Loader2 className="h-4 w-4 animate-spin" />
        Checking services...
      </div>
    )
  }

  const allHealthy = health?.status === 'healthy'

  return (
    <div className="flex items-center gap-4 text-sm">
      <div className={`flex items-center gap-1.5 font-medium ${allHealthy ? 'text-green-600' : 'text-red-600'}`}>
        {allHealthy ? <CheckCircle className="h-4 w-4" /> : <XCircle className="h-4 w-4" />}
        {allHealthy ? 'All Systems Operational' : 'System Issues Detected'}
      </div>
      <div className="flex gap-3">
        {health?.checks.map((check) => (
          <div
            key={check.service}
            className={`flex items-center gap-1 text-xs ${
              check.status === 'ok' ? 'text-green-600' : 'text-red-600'
            }`}
            title={check.detail || ''}
          >
            <span className={`h-2 w-2 rounded-full ${check.status === 'ok' ? 'bg-green-500' : 'bg-red-500'}`} />
            {check.service}
          </div>
        ))}
      </div>
    </div>
  )
}
