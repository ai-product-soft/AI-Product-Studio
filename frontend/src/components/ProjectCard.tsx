import { Link } from 'react-router-dom'
import { ArrowRight, Clock } from 'lucide-react'
import { Badge } from '@/components/ui/badge'

interface ProjectCardProps {
  project: {
    id: number
    name: string
    status: string
    client_idea: string
    created_at: string
  }
}

const statusColors: Record<string, string> = {
  idea: 'bg-slate-100 text-slate-800',
  researching: 'bg-blue-100 text-blue-800',
  research_complete: 'bg-blue-100 text-blue-800',
  planning: 'bg-purple-100 text-purple-800',
  plan_complete: 'bg-purple-100 text-purple-800',
  generating: 'bg-amber-100 text-amber-800',
  generation_review: 'bg-amber-100 text-amber-800',
  promoting: 'bg-pink-100 text-pink-800',
  sales_ready: 'bg-pink-100 text-pink-800',
  completed: 'bg-green-100 text-green-800',
  failed: 'bg-red-100 text-red-800',
}

export default function ProjectCard({ project }: ProjectCardProps) {
  return (
    <Link
      to={`/project/${project.id}`}
      className="block group rounded-lg border bg-card p-5 hover:shadow-md transition-shadow"
    >
      <div className="flex items-start justify-between mb-3">
        <h3 className="font-semibold text-lg group-hover:text-primary transition-colors">{project.name}</h3>
        <Badge variant="secondary" className={statusColors[project.status] || ''}>
          {project.status.replace(/_/g, ' ')}
        </Badge>
      </div>
      <p className="text-sm text-muted-foreground line-clamp-2 mb-4">{project.client_idea}</p>
      <div className="flex items-center justify-between text-xs text-muted-foreground">
        <div className="flex items-center gap-1">
          <Clock className="h-3 w-3" />
          {new Date(project.created_at).toLocaleDateString()}
        </div>
        <div className="flex items-center gap-1 text-primary opacity-0 group-hover:opacity-100 transition-opacity">
          View <ArrowRight className="h-3 w-3" />
        </div>
      </div>
    </Link>
  )
}
