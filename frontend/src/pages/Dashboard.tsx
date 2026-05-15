import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { PlusCircle, Loader2 } from 'lucide-react'
import { getProjects } from '@/services/api'
import { Button } from '@/components/ui/button'
import ProjectCard from '@/components/ProjectCard'
import HealthBar from '@/components/HealthBar'

interface Project {
  id: number
  name: string
  status: string
  client_idea: string
  created_at: string
}

export default function Dashboard() {
  const [projects, setProjects] = useState<Project[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchProjects = async () => {
      try {
        const { data } = await getProjects()
        setProjects(data)
      } catch (err) {
        setError('Failed to load projects')
      } finally {
        setLoading(false)
      }
    }

    fetchProjects()
  }, [])

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Dashboard</h2>
          <p className="text-muted-foreground">Manage your AI-generated product projects.</p>
        </div>
        <Link to="/new">
          <Button>
            <PlusCircle className="mr-2 h-4 w-4" />
            New Project
          </Button>
        </Link>
      </div>

      <HealthBar />

      {loading ? (
        <div className="flex items-center justify-center h-64">
          <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
        </div>
      ) : error ? (
        <div className="rounded-lg border border-destructive/50 p-4 text-destructive">{error}</div>
      ) : projects.length === 0 ? (
        <div className="flex flex-col items-center justify-center h-64 text-muted-foreground">
          <p className="mb-4">No projects yet. Create your first AI product.</p>
          <Link to="/new">
            <Button variant="outline">Create Project</Button>
          </Link>
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {projects.map((project) => (
            <ProjectCard key={project.id} project={project} />
          ))}
        </div>
      )}
    </div>
  )
}
