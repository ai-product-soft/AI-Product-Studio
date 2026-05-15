import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { ArrowLeft, Loader2 } from 'lucide-react'
import { createProject } from '@/services/api'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

export default function NewProject() {
  const navigate = useNavigate()
  const [name, setName] = useState('')
  const [idea, setIdea] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!name.trim() || !idea.trim()) return

    setLoading(true)
    try {
      const { data } = await createProject({ name, client_idea: idea })
      navigate(`/project/${data.id}`)
    } catch (err) {
      alert('Failed to create project')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <Button variant="ghost" onClick={() => navigate('/')} className="pl-0">
        <ArrowLeft className="mr-2 h-4 w-4" />
        Back
      </Button>

      <Card>
        <CardHeader>
          <CardTitle>Create New Project</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="text-sm font-medium mb-1.5 block">Project Name</label>
              <Input
                placeholder="e.g., AI Resume Builder"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </div>
            <div>
              <label className="text-sm font-medium mb-1.5 block">Client Idea / Requirements</label>
              <Textarea
                placeholder="Describe the product idea, target audience, and key features..."
                value={idea}
                onChange={(e) => setIdea(e.target.value)}
                rows={6}
                required
              />
            </div>
            <Button type="submit" disabled={loading} className="w-full">
              {loading ? <Loader2 className="h-4 w-4 animate-spin mr-2" /> : null}
              Create Project
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
